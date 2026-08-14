"""Tests for the transient-network retry installed by ``tests/conftest.py``.

Several dependencies fetch over ``urllib`` rather than ``requests`` --
``hbreader`` when reading schemas, and ``rdflib.parser`` -- so they bypass
``requests_cache`` and a momentary upstream failure fails an unrelated test.
The session fixture retries those.

These pin the behaviour that matters most: that non-transient errors are *not*
retried. Retrying a 404 would mean a genuinely broken upstream is tolerated
silently, which is the opposite of what these network tests are for.
"""

import http.client
import urllib.error

import pytest

from tests.conftest import NETWORK_RETRY_ATTEMPTS, _is_transient, with_urlopen_retry


@pytest.fixture(autouse=True)
def _no_backoff_sleep(monkeypatch):
    """Keep the retry tests fast; the backoff itself is not under test."""
    monkeypatch.setattr("tests.conftest.time.sleep", lambda _seconds: None)


@pytest.mark.parametrize(
    "exc,expected",
    [
        (urllib.error.HTTPError("u", 503, "Service Unavailable", {}, None), True),
        (urllib.error.HTTPError("u", 502, "Bad Gateway", {}, None), True),
        (urllib.error.HTTPError("u", 429, "Too Many Requests", {}, None), True),
        (urllib.error.URLError("connection reset"), True),
        (http.client.RemoteDisconnected("closed without response"), True),
        (ConnectionError("reset by peer"), True),
        (TimeoutError("timed out"), True),
        # Real failures, which must keep failing.
        (urllib.error.HTTPError("u", 404, "Not Found", {}, None), False),
        (urllib.error.HTTPError("u", 401, "Unauthorized", {}, None), False),
        (ValueError("unknown url type"), False),
    ],
)
def test_transient_classification(exc, expected):
    """Only server-side and connection-level failures count as transient."""
    assert _is_transient(exc) is expected


def _failing(exc, succeed_on=None):
    """Build a urlopen-like callable that raises ``exc`` until ``succeed_on``."""
    calls = {"n": 0}

    def inner(*args, **kwargs):
        calls["n"] += 1
        if succeed_on is not None and calls["n"] >= succeed_on:
            return "payload"
        raise exc

    return inner, calls


def test_transient_failure_is_retried_then_succeeds():
    """A 503 that clears on a later attempt returns normally."""
    inner, calls = _failing(
        urllib.error.HTTPError("u", 503, "Service Unavailable", {}, None),
        succeed_on=NETWORK_RETRY_ATTEMPTS,
    )
    assert with_urlopen_retry(inner)("https://example.invalid") == "payload"
    assert calls["n"] == NETWORK_RETRY_ATTEMPTS


def test_persistent_transient_failure_still_raises():
    """Retries are bounded, so a sustained outage fails instead of hanging."""
    inner, calls = _failing(urllib.error.HTTPError("u", 503, "Service Unavailable", {}, None))
    with pytest.raises(urllib.error.HTTPError):
        with_urlopen_retry(inner)("https://example.invalid")
    assert calls["n"] == NETWORK_RETRY_ATTEMPTS


def test_non_transient_failure_is_not_retried():
    """A 404 fails on the first attempt -- broken upstreams stay visible."""
    inner, calls = _failing(urllib.error.HTTPError("u", 404, "Not Found", {}, None))
    with pytest.raises(urllib.error.HTTPError):
        with_urlopen_retry(inner)("https://example.invalid")
    assert calls["n"] == 1


def test_retry_is_actually_installed_during_a_session():
    """The autouse fixture has patched urlopen; without this the rest is theory."""
    import urllib.request

    assert urllib.request.urlopen.__name__ == "wrapped", (
        "urllib.request.urlopen is not wrapped -- the retry_transient_network fixture "
        "did not install, so transient failures will surface as test failures."
    )


def test_requests_sessions_get_a_retrying_adapter():
    """New requests Sessions carry retries and remain cached."""
    import requests

    session = requests.Session()
    assert session.get_adapter("https://example.invalid").max_retries.total == NETWORK_RETRY_ATTEMPTS
    assert hasattr(session, "cache"), "requests_cache should still be installed"


def test_success_is_not_retried():
    """The happy path calls through exactly once."""
    inner, calls = _failing(AssertionError("unreachable"), succeed_on=1)
    assert with_urlopen_retry(inner)("https://example.invalid") == "payload"
    assert calls["n"] == 1
