#!/usr/bin/env python3
"""Run ``uv audit``, ignoring advisories younger than a grace period.

A freshly published advisory is Dependabot's to fix: it raises an alert and
opens a security PR. Failing every dependency-changing PR in the meantime just
races Dependabot. So advisories published within the last ``GRACE_DAYS`` are
ignored here; one that is still unfixed after that means Dependabot did not
come through (no alert, or a bump it could not resolve), and the audit fails.

Advisories a PR *introduces* are caught separately, regardless of age, by the
dependency review step. Releases run plain ``uv audit`` with no grace.

Fail-safe by construction: an advisory is only ignored when its publish date
was looked up successfully and is recent. If ``uv audit``'s output cannot be
parsed, or OSV cannot be reached, nothing is ignored and the audit fails as it
would without this script.

Usage:
    uv_audit_with_grace.py <grace_days>
"""

from __future__ import annotations

import datetime
import json
import re
import subprocess
import sys
import urllib.request

OSV_VULN_URL = "https://api.osv.dev/v1/vulns/{}"
TIMEOUT_SECONDS = 30

ADVISORY_LINE = re.compile(r"^- (\S+): ", re.MULTILINE)
"""Matches the ``- <ID>: <title>`` lines ``uv audit`` prints for each advisory."""


def run_audit(ignore: list[str]) -> subprocess.CompletedProcess[str]:
    """Run ``uv audit``, ignoring the given advisory IDs, and echo its output.

    Args:
        ignore: Advisory IDs to pass as ``--ignore``.

    Returns:
        The completed process, with combined output captured.
    """
    args = ["uv", "audit"]
    for advisory in ignore:
        args += ["--ignore", advisory]
    result = subprocess.run(args, capture_output=True, text=True)
    print(result.stdout + result.stderr, end="")
    return result


def lookup(advisory: str) -> dict | None:
    """Fetch ``advisory``'s OSV record.

    Args:
        advisory: An OSV, GHSA or PYSEC identifier.

    Returns:
        The record, or ``None`` if it could not be fetched.
    """
    try:
        with urllib.request.urlopen(OSV_VULN_URL.format(advisory), timeout=TIMEOUT_SECONDS) as response:
            return json.load(response)
    except (OSError, ValueError) as error:
        print(f"Could not look up {advisory} on OSV ({error}); not ignoring it.")
        return None


def grace_clock(advisory: str) -> datetime.datetime | None:
    """Return when the grace period for ``advisory`` started.

    Dependabot works from GitHub's advisory database, so it cannot act until a
    GHSA record exists -- which can be well after the PYSEC record for the same
    vulnerability. The clock therefore starts at the earliest GHSA publication
    among the advisory and its aliases, falling back to the advisory's own date.
    ``uv audit --ignore`` also suppresses aliases, so every ID of one
    vulnerability resolves to the same clock and is ignored (or not) together.

    Args:
        advisory: An OSV, GHSA or PYSEC identifier.

    Returns:
        The start of the grace period, or ``None`` if any lookup failed.
    """
    record = lookup(advisory)
    if record is None:
        return None
    ghsa_ids = sorted(i for i in {advisory, *record.get("aliases", [])} if i.startswith("GHSA-"))
    records = [record if i == advisory else lookup(i) for i in ghsa_ids] or [record]
    if any(r is None or "published" not in r for r in records):
        return None
    return min(datetime.datetime.fromisoformat(r["published"].replace("Z", "+00:00")) for r in records)


def main(grace_days: int) -> int:
    """Audit, then re-audit ignoring advisories younger than ``grace_days``.

    Args:
        grace_days: How many days an advisory is left to Dependabot.

    Returns:
        The exit code of the final ``uv audit`` run.
    """
    first = run_audit([])
    if first.returncode == 0:
        return 0

    now = datetime.datetime.now(datetime.UTC)
    recent = []
    for advisory in sorted(set(ADVISORY_LINE.findall(first.stdout + first.stderr))):
        when = grace_clock(advisory)
        if when is not None and now - when < datetime.timedelta(days=grace_days):
            print(f"Ignoring {advisory}: on GitHub since {when:%Y-%m-%d}, within the {grace_days}-day grace period.")
            recent.append(advisory)

    if not recent:
        return first.returncode
    print(f"\nRe-running uv audit without {len(recent)} recent advisories:")
    return run_audit(recent).returncode


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1])))
