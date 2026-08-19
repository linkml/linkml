"""Retry transient network failures raised through ``urllib`` and ``requests``.

``requests_cache`` only patches ``requests``. Several dependencies --
``hbreader`` when reading schemas, and ``rdflib.parser`` -- fetch via
``urllib.request.urlopen`` instead, so they bypass the cache entirely and a
momentary 503 or dropped connection fails an unrelated test.

Retrying rather than caching is deliberate: a cache would also hide genuine
upstream breakage, which these tests exist to notice.

This module is kept free of pytest and of anything in ``tests/__init__.py`` so
that :mod:`sitecustomize` in ``tests/_kernel_startup`` can load it by path into
a notebook kernel, where importing the ``tests`` package -- and through it all
of ``linkml`` -- during interpreter startup would be both slow and fragile.
"""

import http.client
import time
import urllib.error
import urllib.request
from collections.abc import Callable

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

NETWORK_RETRY_ATTEMPTS = 3
NETWORK_RETRY_BACKOFF_SECONDS = 2

TRANSIENT_HTTP_STATUS = frozenset({429, 500, 502, 503, 504})
"""Server-side statuses that mean "try again", not "this resource is wrong"."""


def _is_transient(exc: BaseException) -> bool:
    """Return True if ``exc`` looks like a transient network failure.

    Deliberately narrow. A 404 or a bad URL is a real failure and must keep
    failing; only server-side and connection-level errors are retried, so a
    genuinely broken upstream still surfaces rather than being papered over.
    """
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in TRANSIENT_HTTP_STATUS
    return isinstance(exc, urllib.error.URLError | http.client.HTTPException | ConnectionError | TimeoutError)


def with_urlopen_retry(inner: Callable) -> Callable:
    """Wrap a ``urlopen``-like callable so transient failures are retried.

    Non-transient failures propagate on the first attempt, so a genuinely
    broken upstream still fails rather than being retried into silence.
    """

    def wrapped(*args, **kwargs):
        for attempt in range(1, NETWORK_RETRY_ATTEMPTS + 1):
            try:
                return inner(*args, **kwargs)
            except Exception as exc:
                if attempt == NETWORK_RETRY_ATTEMPTS or not _is_transient(exc):
                    raise
                time.sleep(NETWORK_RETRY_BACKOFF_SECONDS * attempt)

    return wrapped


def install() -> Callable[[], None]:
    """Patch ``urlopen`` and ``requests`` sessions to retry transient failures.

    Returns a callable that restores both to their original state.
    """
    original_urlopen = urllib.request.urlopen

    # requests-based fetches (prefixcommons resolving default_curi_maps, for one)
    # go through requests_cache, but it is cleared at session start, so the first
    # fetch of each URL in a run is still live. Mount a retrying adapter on every
    # new Session; this composes with requests_cache, which subclasses Session.
    original_session_init = requests.sessions.Session.__init__

    def session_init_with_retry(self, *args, **kwargs) -> None:
        original_session_init(self, *args, **kwargs)
        adapter = HTTPAdapter(
            max_retries=Retry(
                # Retry.total counts retries, not attempts, so subtract one to
                # make both paths try the same number of times.
                total=NETWORK_RETRY_ATTEMPTS - 1,
                backoff_factor=NETWORK_RETRY_BACKOFF_SECONDS,
                status_forcelist=sorted(TRANSIENT_HTTP_STATUS),
                allowed_methods=None,
            )
        )
        self.mount("http://", adapter)
        self.mount("https://", adapter)

    urllib.request.urlopen = with_urlopen_retry(original_urlopen)
    requests.sessions.Session.__init__ = session_init_with_retry

    def uninstall() -> None:
        urllib.request.urlopen = original_urlopen
        requests.sessions.Session.__init__ = original_session_init

    return uninstall
