"""Tests for the weekly upstream-failure quarantine (tests/upstream_failures.py)."""

import json
from pathlib import Path

import pytest

from tests.upstream_failures import FAILURES_FILE, dump, failed_tests, load, merge_outcomes, update

pytest_plugins = ["pytester"]

ENTRY = {"test": "tests/t.py::test_a", "first_seen": "2026-01-01", "run": "https://run/0", "error": "boom"}


def test_tracked_file_is_valid():
    """The committed file loads; a malformed edit fails every session's collection too."""
    load(FAILURES_FILE)


@pytest.mark.parametrize(
    "failures,message",
    [
        ([{**ENTRY, "reason": "outage"}], "unknown keys"),
        ([{k: v for k, v in ENTRY.items() if k != "error"}], "missing"),
        ([{**ENTRY, "accepted": ""}], "without a reason"),
        ([ENTRY, ENTRY], "duplicate"),
    ],
)
def test_load_rejects_malformed_entries(tmp_path: Path, failures: list[dict], message: str):
    """A malformed entry is an error, never silently ignored."""
    path = tmp_path / "f.yaml"
    dump(failures, path)
    with pytest.raises(ValueError, match=message):
        load(path)


def test_dump_round_trips(tmp_path: Path):
    """What the workflow writes, load accepts unchanged."""
    path = tmp_path / "f.yaml"
    entries = [{**ENTRY, "accepted": "w3id outage, see upstream issue"}]
    dump(entries, path)
    assert load(path) == entries


@pytest.mark.parametrize(
    "entries,outcome,expected",
    [
        # new persistent failure is recorded
        ([], {"outcome": "failed", "error": "boom"}, [{**ENTRY, "run": "https://run/1", "first_seen": "2026-02-02"}]),
        # a still-failing unaccepted entry keeps its original first_seen and run
        ([ENTRY], {"outcome": "failed", "error": "boom2"}, [ENTRY]),
        # unaccepted entry that passes again is dropped
        ([ENTRY], {"outcome": "passed"}, []),
        # accepted entry that still fails (xfailed) is kept
        ([{**ENTRY, "accepted": "r"}], {"outcome": "xfailed"}, [{**ENTRY, "accepted": "r"}]),
        # accepted entry whose strict xfail XPASSed: upstream recovered, dropped
        ([{**ENTRY, "accepted": "r"}], {"outcome": "xpassed", "error": "x"}, []),
    ],
)
def test_update(entries: list[dict], outcome: dict, expected: list[dict]):
    """Each weekly outcome moves an entry the right way."""
    assert update(entries, {ENTRY["test"]: outcome}, "https://run/1", "2026-02-02") == expected


def test_update_leaves_entries_for_tests_that_did_not_run():
    """An entry is only changed by an outcome for its own test."""
    assert update([ENTRY], {"tests/t.py::test_other": {"outcome": "passed"}}, "r", "d") == [ENTRY]


def test_retry_overrides_first_pass(tmp_path: Path):
    """A failure that passes on the delayed re-run was transient and is not recorded."""
    first = tmp_path / "first.json"
    retry = tmp_path / "retry.json"
    first.write_text(
        json.dumps({"t::a": {"outcome": "failed", "error": "e"}, "t::b": {"outcome": "failed", "error": "e"}})
    )
    retry.write_text(json.dumps({"t::a": {"outcome": "passed"}, "t::b": {"outcome": "failed", "error": "e2"}}))
    assert failed_tests([first]) == ["t::a", "t::b"]
    merged = merge_outcomes([first], retry)
    assert [entry["test"] for entry in update([], merged, "r", "d")] == ["t::b"]


def test_recorder_and_quarantine_in_a_real_session(pytester: pytest.Pytester):
    """End to end: accepted entries xfail strictly only when live, and outcomes are recorded faithfully."""
    failures = pytester.path / "failures.yaml"
    pytester.makeconftest(
        f"""
        from pathlib import Path
        from tests.upstream_failures import OutcomeRecorder, quarantine

        def pytest_addoption(parser):
            parser.addoption("--with-network", action="store_true")
            parser.addoption("--upstream-outcomes", type=Path)

        def pytest_configure(config):
            config.addinivalue_line("markers", "network: n")
            config.pluginmanager.register(OutcomeRecorder(config.getoption("--upstream-outcomes")), "rec")

        def pytest_collection_modifyitems(items):
            quarantine(items, Path({str(failures)!r}))
        """
    )
    pytester.makepyfile(
        test_live="""
        import pytest

        @pytest.mark.network
        def test_still_broken():
            assert False

        @pytest.mark.network
        def test_recovered():
            pass

        @pytest.mark.network
        def test_new_failure():
            assert False, "upstream moved"

        @pytest.mark.network
        def test_skips_itself():
            pytest.skip("not applicable here")
        """
    )
    accepted = {"first_seen": "d", "run": "r", "error": "e", "accepted": "outage"}
    dump(
        [
            {"test": "test_live.py::test_still_broken", **accepted},
            {"test": "test_live.py::test_recovered", **accepted},
        ],
        failures,
    )

    offline = pytester.path / "offline.json"
    pytester.runpytest("--upstream-outcomes", str(offline))
    # Offline (stubs), nothing is quarantined, so the recovered test simply passes.
    assert json.loads(offline.read_text())["test_live.py::test_recovered"]["outcome"] == "passed"

    live = pytester.path / "live.json"
    pytester.runpytest("--with-network", "--upstream-outcomes", str(live))
    outcomes = {test: result["outcome"] for test, result in json.loads(live.read_text()).items()}
    assert outcomes == {
        "test_live.py::test_still_broken": "xfailed",
        "test_live.py::test_recovered": "xpassed",
        "test_live.py::test_new_failure": "failed",
    }
    assert "upstream moved" in json.loads(live.read_text())["test_live.py::test_new_failure"]["error"]
