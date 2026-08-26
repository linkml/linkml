"""Serve the test suite's outbound fetches from files already in the repo.

Most network traffic in the suite is incidental. ``rdflib`` resolves ``@context``
URLs while parsing generated JSON-LD, and a handful of ``SchemaView`` tests load
schemas over ``https`` to exercise URL-based import resolution. None of those
tests are *about* the network -- every URL they fetch has a counterpart on disk,
either vendored in ``linkml_runtime`` or sitting in ``tests/``.

Fetching them live made offline jobs fail on upstream hiccups. The ``Slow Tests``
job is the clearest case: it never passes ``--with-network``, yet it made 34
outbound requests, and that is where every reported flake landed.

So the mapped URLs are served from disk and anything unmapped raises. Tests that
genuinely need the network -- checking that a published PURL resolves, or that
vendored files still match upstream -- opt in with ``@pytest.mark.network`` and
are handed the real ``urlopen``.

Serving from disk also closes a blind spot. The GitHub URLs point at
``refs/heads/main``, so a branch that edited ``creature_schema.yaml`` was tested
against *main's* copy of it. They now resolve to the working tree.
"""

import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from email.message import Message
from email.utils import formatdate
from functools import cache
from io import BytesIO
from pathlib import Path

from linkml_runtime.linkml_model.linkml_files import LINKML_URL_BASE, LOCAL_PATH_FOR, Format, Source

REPO_ROOT = Path(__file__).resolve().parents[1]

GITHUB_RAW_MAIN = "https://raw.githubusercontent.com/linkml/linkml/refs/heads/main/"
"""Tests fetch repo files from here; they resolve to the working tree instead."""

ALLOWED_SCHEMES = frozenset({"file", "data"})
ALLOWED_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})

CONTENT_TYPE_BY_SUFFIX = {
    ".jsonld": "application/ld+json",
    ".json": "application/json",
    ".yaml": "text/yaml",
    ".ttl": "text/turtle",
    ".shex": "text/shex",
    ".shexj": "application/json",
}
DEFAULT_CONTENT_TYPE = "text/plain"

KNOWN_MISSING_URLS = frozenset(
    {
        # Generated JSON-LD carries a bare relative "core.context.jsonld" in its
        # @context, resolved against @base https://w3id.org/linkml/tests/kitchen_sink/.
        # Nothing is published there, so this 404s upstream too and rdflib moves on.
        # Served as a 404 to keep behaviour identical; the generator emitting an
        # unresolvable context reference is a separate bug.
        "https://w3id.org/linkml/tests/kitchen_sink/core.context.jsonld",
    }
)


@cache
def _model_url_map() -> dict[str, Path]:
    """Map every published linkml-model URL to its vendored file.

    Published URLs are flat -- ``https://w3id.org/linkml/<filename>`` -- while the
    vendored files sit in per-format directories. Rather than hand-list them, learn
    each format's directory and extension from ``LOCAL_PATH_FOR`` and glob, so new
    files are picked up without touching this module.

    Globbing rather than iterating ``Source`` also catches the sources that ship
    vendored files but have no ``Source`` member -- units, datasets and validation
    -- which the enum product alone misses.
    """
    mapping: dict[str, Path] = {}
    for fmt in Format:
        probe = Path(LOCAL_PATH_FOR(Source.META, fmt))
        extension = probe.name[len(f"{Source.META.value}.") :]
        # A couple of formats share an extension (SQLDDL/SQLSCHEMA), so the flat
        # URL space genuinely collides upstream. setdefault keeps this deterministic.
        for path in sorted(probe.parent.glob(f"*.{extension}")):
            mapping.setdefault(f"{LINKML_URL_BASE}{path.name}", path)
    return mapping


def resolve(url: str) -> Path | None:
    """Return the local file backing ``url``, or None if it is not mapped."""
    mapped = _model_url_map().get(url)
    if mapped is not None:
        return mapped

    if url.startswith(GITHUB_RAW_MAIN):
        candidate = (REPO_ROOT / url[len(GITHUB_RAW_MAIN) :]).resolve()
        # Keep a mangled URL from reaching outside the repo.
        if candidate.is_relative_to(REPO_ROOT) and candidate.is_file():
            return candidate
    return None


def _is_exempt(url: str) -> bool:
    """Return True for URLs that never touch the network in the first place."""
    parsed = urllib.parse.urlsplit(url)
    return parsed.scheme in ALLOWED_SCHEMES or parsed.hostname in ALLOWED_HOSTS


def _content_type_for(path: Path) -> str:
    """Return the Content-Type to serve ``path`` as."""
    for suffix, content_type in CONTENT_TYPE_BY_SUFFIX.items():
        if path.name.endswith(suffix):
            return content_type
    return DEFAULT_CONTENT_TYPE


class _ResponseBody(BytesIO):
    """A response body that looks enough like a socket to satisfy consumers.

    ``hbreader`` reads ``response.fp.mode`` to pick a text wrapper, which a real
    socket-backed response has and a bare ``BytesIO`` does not.
    """

    mode = "rb"


def _response_for(path: Path, url: str) -> urllib.response.addinfourl:
    """Build a urlopen-shaped response serving ``path``.

    A synthetic response rather than a ``file://`` redirect: rdflib picks its
    JSON-LD parser off the Content-Type, which the file handler does not set.
    """
    body = path.read_bytes()
    modified = formatdate(path.stat().st_mtime, usegmt=True)
    headers = Message()
    headers["Content-Type"] = _content_type_for(path)
    headers["Content-Length"] = str(len(body))
    # hbreader records these on the schema it loads.
    headers["Last-Modified"] = modified
    headers["Date"] = modified
    return urllib.response.addinfourl(_ResponseBody(body), headers, url, 200)


class UnexpectedNetworkAccess(RuntimeError):
    """Raised when a test reaches for a URL that is not served from disk."""


def _unexpected(url: str) -> UnexpectedNetworkAccess:
    return UnexpectedNetworkAccess(
        f"Test tried to fetch {url!r}, which is not served from a local file.\n"
        f"Either add a mapping in {Path(__file__).name} (preferred, if the file is in the repo), "
        f"or mark the test @pytest.mark.network to opt into real network access."
    )


def install() -> Callable[[], None]:
    """Serve mapped URLs from disk and block everything else.

    Patches ``OpenerDirector.open`` rather than ``urllib.request.urlopen``:
    ``hbreader`` and ``rdflib`` do ``from urllib.request import urlopen`` at
    import time, so they hold a reference the module attribute never reaches.
    Every caller funnels through the opener regardless of how it imported.
    """
    original_open = urllib.request.OpenerDirector.open

    def open_offline(self, fullurl, *args, **kwargs):
        url = fullurl.full_url if isinstance(fullurl, urllib.request.Request) else fullurl
        if _is_exempt(url):
            return original_open(self, fullurl, *args, **kwargs)
        if url in KNOWN_MISSING_URLS:
            raise urllib.error.HTTPError(url, 404, "Not Found", Message(), None)
        local = resolve(url)
        if local is None:
            raise _unexpected(url)
        return _response_for(local, url)

    urllib.request.OpenerDirector.open = open_offline

    def uninstall() -> None:
        urllib.request.OpenerDirector.open = original_open

    return uninstall
