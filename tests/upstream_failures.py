"""Track live upstream failures in a file, so the weekly job can raise them as PRs.

Per-PR CI runs offline (see :mod:`tests.offline_network`), so the only place the
real outside world is checked is the weekly ``metamodel-compat`` workflow. A
failure there used to turn the run red and nothing else -- easy to never see.
Instead, a failure that survives a delayed re-run is recorded in
``tests/upstream_failures.yaml`` and proposed as a PR. That PR's CI re-runs the
listed tests live, so it arrives red, documenting the real failure. Resolve it
in the PR by either:

- **fixing it** -- update the stub, rewrite rule, or code -- and deleting the
  entry, or
- **accepting it** -- adding ``accepted: <reason>`` to the entry. Accepted
  entries become strict xfails whenever the test runs live, so when upstream
  recovers the test XPASSes and the weekly job proposes removing the entry.

The weekly job also drops unaccepted entries whose tests pass again.
"""

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

FAILURES_FILE = Path(__file__).parent / "upstream_failures.yaml"
"""Tracked record of persistent live failures; relative path is ``tests/upstream_failures.yaml``."""

REQUIRED_KEYS = frozenset({"test", "first_seen", "run", "error"})
OPTIONAL_KEYS = frozenset({"accepted"})

HEADER = """\
# Live upstream/network test failures that persisted across a delayed re-run in the
# weekly metamodel-compat workflow. Maintained by that workflow; see
# tests/upstream_failures.py for how to resolve an entry (fix it and delete the
# entry, or add `accepted: <reason>` to quarantine it as a strict xfail).
"""

ERROR_EXCERPT_LINES = 15

XPASS_STRICT = "[XPASS(strict)]"


def load(path: Path = FAILURES_FILE) -> list[dict]:
    """Load and validate the failures file.

    Unknown keys are rejected rather than ignored, so a wrong key like ``reason``
    cannot silently leave a failure unquarantined.

    >>> import tempfile
    >>> p = Path(tempfile.mkdtemp()) / "f.yaml"
    >>> _ = p.write_text("failures: []\\n")
    >>> load(p)
    []
    """
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict) or set(data) != {"failures"} or not isinstance(data["failures"], list):
        raise ValueError(f"{path}: expected a mapping with a single `failures` list")
    for entry in data["failures"]:
        keys = set(entry)
        if not REQUIRED_KEYS <= keys:
            raise ValueError(f"{path}: entry {entry!r} is missing {sorted(REQUIRED_KEYS - keys)}")
        if keys - REQUIRED_KEYS - OPTIONAL_KEYS:
            raise ValueError(
                f"{path}: entry {entry['test']!r} has unknown keys {sorted(keys - REQUIRED_KEYS - OPTIONAL_KEYS)}"
            )
        if "accepted" in entry and not (isinstance(entry["accepted"], str) and entry["accepted"].strip()):
            raise ValueError(f"{path}: entry {entry['test']!r} has `accepted` without a reason")
    tests = [entry["test"] for entry in data["failures"]]
    if len(tests) != len(set(tests)):
        raise ValueError(f"{path}: duplicate test entries")
    return data["failures"]


def dump(entries: list[dict], path: Path = FAILURES_FILE) -> None:
    """Write entries back, sorted by test id so diffs stay minimal."""
    body = yaml.safe_dump({"failures": sorted(entries, key=lambda e: e["test"])}, sort_keys=False, width=120)
    path.write_text(HEADER + body)


def runs_live(item: pytest.Item) -> bool:
    """Whether ``item`` will hit the real network in this session."""
    if item.get_closest_marker("upstream"):
        return True
    return bool(item.get_closest_marker("network")) and item.config.getoption("--with-network")


def quarantine(items: list[pytest.Item], path: Path = FAILURES_FILE) -> None:
    """Mark accepted entries as strict xfails, but only where the test runs live.

    Offline, the test runs against stubs and passes, so an xfail there would
    itself fail.
    """
    accepted = {entry["test"]: entry["accepted"] for entry in load(path) if "accepted" in entry}
    for item in items:
        if item.nodeid in accepted and runs_live(item):
            item.add_marker(
                pytest.mark.xfail(strict=True, reason=f"Upstream failure accepted: {accepted[item.nodeid]}")
            )


class OutcomeRecorder:
    """Pytest plugin recording one outcome per test id: passed, failed, xfailed or xpassed."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.outcomes: dict[str, dict] = {}

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        """Keep the worst outcome across setup, call and teardown."""
        if report.failed:
            outcome = "xpassed" if report.longreprtext.startswith(XPASS_STRICT) else "failed"
            excerpt = "\n".join(report.longreprtext.splitlines()[-ERROR_EXCERPT_LINES:])
            self.outcomes[report.nodeid] = {"outcome": outcome, "error": excerpt}
        elif report.when == "call" and report.nodeid not in self.outcomes:
            if hasattr(report, "wasxfail"):
                self.outcomes[report.nodeid] = {"outcome": "xfailed"}
            elif report.passed:
                self.outcomes[report.nodeid] = {"outcome": "passed"}

    def pytest_sessionfinish(self) -> None:
        """Write the collected outcomes as JSON."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.outcomes, indent=2))


def merge_outcomes(outcome_files: list[Path], retry_file: Path | None) -> dict[str, dict]:
    """Combine first-pass outcomes, letting the delayed re-run override them.

    A test that failed first and passed on re-run was a transient blip.
    """
    outcomes: dict[str, dict] = {}
    for path in outcome_files:
        outcomes.update(json.loads(path.read_text()))
    if retry_file is not None:
        outcomes.update(json.loads(retry_file.read_text()))
    return outcomes


def update(entries: list[dict], outcomes: dict[str, dict], run_url: str, today: str) -> list[dict]:
    """Apply a weekly run's outcomes to the recorded entries.

    - new persistent failures are added;
    - unaccepted entries whose test passed are dropped (recovered before anyone acted);
    - accepted entries whose strict xfail XPASSed are dropped (upstream recovered).

    Entries for tests that did not run are left alone.

    >>> old = [{"test": "t::a", "first_seen": "2026-01-01", "run": "r0", "error": "e"}]
    >>> outcomes = {"t::a": {"outcome": "passed"}, "t::b": {"outcome": "failed", "error": "boom"}}
    >>> new = update(old, outcomes, "r1", "2026-02-02")
    >>> [(e["test"], e["first_seen"]) for e in new]
    [('t::b', '2026-02-02')]
    """
    by_test = {entry["test"]: entry for entry in entries}
    for test, result in outcomes.items():
        entry = by_test.get(test)
        if result["outcome"] == "failed" and entry is None:
            by_test[test] = {"test": test, "first_seen": today, "run": run_url, "error": result["error"]}
        elif result["outcome"] == "passed" and entry is not None and "accepted" not in entry:
            del by_test[test]
        elif result["outcome"] == "xpassed" and entry is not None:
            del by_test[test]
    return list(by_test.values())


def failed_tests(outcome_files: list[Path]) -> list[str]:
    """Test ids that failed (or XPASSed) in a first pass and deserve a re-run."""
    outcomes = merge_outcomes(outcome_files, None)
    return sorted(test for test, result in outcomes.items() if result["outcome"] in {"failed", "xpassed"})


def listed_at(ref: str) -> list[str]:
    """Test ids listed in the failures file at a git ref (empty if absent there)."""
    relative = FAILURES_FILE.relative_to(Path(__file__).parents[1]).as_posix()
    shown = subprocess.run(["git", "show", f"{ref}:{relative}"], capture_output=True, text=True)
    if shown.returncode != 0:
        return []
    return [entry["test"] for entry in yaml.safe_load(shown.stdout)["failures"]]


def main(argv: list[str] | None = None) -> None:
    """CLI used by the workflows; see the subcommand help."""
    parser = argparse.ArgumentParser(prog="python -m tests.upstream_failures")
    sub = parser.add_subparsers(dest="command", required=True)

    listed = sub.add_parser("listed", help="print test ids listed now, plus those listed at --base")
    listed.add_argument("--base", help="git ref whose entries to include, so deleted entries are re-checked")

    failed = sub.add_parser("failed", help="print test ids that failed in the given outcome files")
    failed.add_argument("outcomes", nargs="+", type=Path)

    upd = sub.add_parser("update", help="apply outcomes to the failures file")
    upd.add_argument("outcomes", nargs="+", type=Path)
    upd.add_argument("--retry", type=Path, help="outcomes of the delayed re-run, overriding the first pass")
    upd.add_argument("--run-url", required=True)

    args = parser.parse_args(argv)
    if args.command == "listed":
        current = [entry["test"] for entry in load()]
        base = listed_at(args.base) if args.base else []
        sys.stdout.writelines(f"{test}\n" for test in sorted(set(current) | set(base)))
    elif args.command == "failed":
        sys.stdout.writelines(f"{test}\n" for test in failed_tests(args.outcomes))
    else:
        outcomes = merge_outcomes(args.outcomes, args.retry)
        dump(update(load(), outcomes, args.run_url, datetime.date.today().isoformat()))


if __name__ == "__main__":
    sys.exit(main())
