#!/usr/bin/env python3
"""Link checker with caching and per-domain rate limiting.

This script checks URLs in documentation files, using a cache to avoid
re-checking recently verified links. It implements per-domain rate limiting
to avoid triggering anti-bot measures on external sites.
"""

import argparse
import csv
import random
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import requests

# URL pattern to match in docs
URL_PATTERN = re.compile(r'https?://[^\s<>")\]`\'\,]+')

# Domains to skip (localhost, example domains, etc.)
SKIP_DOMAINS = {
    "localhost",
    "127.0.0.1",
    "example.com",
    "example.org",
    "example.net",
}


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    match = re.match(r"https?://([^/]+)", url)
    return match.group(1) if match else ""


def clean_url(url: str) -> str:
    """Clean trailing punctuation from URL."""
    return url.rstrip(".,;:!?)")


def extract_urls_from_file(filepath: Path) -> set[str]:
    """Extract all URLs from a file."""
    urls = set()
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        for match in URL_PATTERN.findall(content):
            url = clean_url(match)
            domain = extract_domain(url)
            # Skip certain domains
            if domain and not any(skip in domain for skip in SKIP_DOMAINS):
                urls.add(url)
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
    return urls


def extract_all_urls(docs_dir: Path) -> set[str]:
    """Extract all URLs from docs directory."""
    urls = set()
    for pattern in ["**/*.md", "**/*.rst"]:
        for filepath in docs_dir.glob(pattern):
            urls.update(extract_urls_from_file(filepath))
    return urls


def load_cache(cache_file: Path) -> dict[str, dict]:
    """Load cache from CSV file."""
    cache = {}
    if cache_file.exists():
        try:
            with open(cache_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cache[row["url"]] = {
                        "domain": row["domain"],
                        "status": row["status"],
                        "checked_at": row["checked_at"],
                    }
        except Exception as e:
            print(f"Warning: Could not load cache: {e}", file=sys.stderr)
    return cache


def save_cache(cache: dict[str, dict], cache_file: Path) -> None:
    """Save cache to CSV file."""
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "domain", "status", "checked_at"])
        writer.writeheader()
        for url, data in sorted(cache.items()):
            writer.writerow({"url": url, **data})


def needs_check(url: str, cache: dict[str, dict], ttl_days: int, jitter_days: int) -> bool:
    """Determine if a URL needs to be checked."""
    if url not in cache:
        return True

    entry = cache[url]

    # Always re-check broken links
    if entry["status"] != "200":
        return True

    # Check if expired (with jitter)
    try:
        checked_at = datetime.fromisoformat(entry["checked_at"])
        jitter = random.randint(0, jitter_days)
        expiry = checked_at + timedelta(days=ttl_days + jitter)
        return datetime.now() > expiry
    except (ValueError, KeyError):
        return True


def check_url(url: str, timeout: int = 10) -> tuple[str, str]:
    """
    Check a URL and return (status, error_message).

    Returns:
        Tuple of (status_code_or_error, error_message_or_empty)
    """
    try:
        response = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "LinkML-Doc-Checker/1.0"},
        )
        # Some servers don't support HEAD, try GET
        if response.status_code == 405:
            response = requests.get(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers={"User-Agent": "LinkML-Doc-Checker/1.0"},
                stream=True,  # Don't download body
            )
        return str(response.status_code), ""
    except requests.exceptions.Timeout:
        return "timeout", "Request timed out"
    except requests.exceptions.SSLError as e:
        return "ssl_error", str(e)
    except requests.exceptions.ConnectionError as e:
        return "connection_error", str(e)
    except requests.exceptions.RequestException as e:
        return "error", str(e)


def main():
    parser = argparse.ArgumentParser(description="Check links in documentation with caching and rate limiting.")
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path("docs"),
        help="Documentation directory to scan (default: docs)",
    )
    parser.add_argument(
        "--cache-file",
        type=Path,
        default=Path(".github/link-cache.csv"),
        help="Cache file path (default: .github/link-cache.csv)",
    )
    parser.add_argument(
        "--ttl-days",
        type=int,
        default=30,
        help="Days before re-checking a valid link (default: 30)",
    )
    parser.add_argument(
        "--jitter-days",
        type=int,
        default=7,
        help="Random jitter days added to TTL (default: 7)",
    )
    parser.add_argument(
        "--links-per-domain",
        type=int,
        default=10,
        help="Max links to check per domain per run (default: 10)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be checked without checking",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    # Extract all URLs from docs
    print(f"Scanning {args.docs_dir} for URLs...")
    all_urls = extract_all_urls(args.docs_dir)
    print(f"Found {len(all_urls)} unique URLs")

    # Load cache
    cache = load_cache(args.cache_file)
    print(f"Loaded {len(cache)} cached entries")

    # Determine which URLs need checking
    urls_to_check = [url for url in all_urls if needs_check(url, cache, args.ttl_days, args.jitter_days)]
    print(f"URLs needing check: {len(urls_to_check)}")

    # Group by domain and apply per-domain limit
    by_domain: dict[str, list[str]] = defaultdict(list)
    for url in urls_to_check:
        domain = extract_domain(url)
        by_domain[domain].append(url)

    # Select URLs to check (respecting per-domain limit)
    urls_this_run = []
    for domain, urls in sorted(by_domain.items()):
        selected = urls[: args.links_per_domain]
        urls_this_run.extend(selected)
        if args.verbose and len(urls) > args.links_per_domain:
            print(f"  {domain}: checking {len(selected)}/{len(urls)} (limited by --links-per-domain)")

    print(f"Checking {len(urls_this_run)} URLs this run")

    if args.dry_run:
        print("\nDry run - would check:")
        for url in sorted(urls_this_run):
            print(f"  {url}")
        return 0

    # Check URLs
    broken_links = []
    now = datetime.now().isoformat()

    for i, url in enumerate(urls_this_run, 1):
        status, error = check_url(url, timeout=args.timeout)
        domain = extract_domain(url)

        # Update cache
        cache[url] = {
            "domain": domain,
            "status": status,
            "checked_at": now,
        }

        # Track broken links
        is_ok = status in ("200", "201", "202", "203", "204", "301", "302", "303", "307", "308")
        if not is_ok:
            broken_links.append((url, status, error))
            print(f"[{i}/{len(urls_this_run)}] BROKEN: {url} ({status})")
        elif args.verbose:
            print(f"[{i}/{len(urls_this_run)}] OK: {url}")

    # Also collect any previously cached broken links still in docs
    cached_broken = []
    for url in all_urls:
        if url in cache and url not in urls_this_run:
            entry = cache[url]
            if entry["status"] not in ("200", "201", "202", "203", "204", "301", "302", "303", "307", "308"):
                cached_broken.append((url, entry["status"], ""))

    # Save updated cache
    # Also prune URLs no longer in docs
    pruned_cache = {url: data for url, data in cache.items() if url in all_urls}
    save_cache(pruned_cache, args.cache_file)
    print(f"Cache saved ({len(pruned_cache)} entries)")

    # Report results
    all_broken = broken_links + cached_broken
    if all_broken:
        print(f"\n{'=' * 60}")
        print(f"BROKEN LINKS ({len(all_broken)}):")
        print(f"{'=' * 60}")
        for url, status, error in sorted(all_broken):
            msg = f"  [{status}] {url}"
            if error:
                msg += f" - {error}"
            print(msg)
        return 1

    print("\nAll checked links are OK!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
