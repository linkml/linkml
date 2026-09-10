"""Keep the test suite off the network: block by default, serve stubs on opt-in.

The rules a test author needs:

- **Unmarked tests must not touch the network at all.** Any outbound request --
  ``urllib``, ``requests``, or a raw socket -- raises ``UnexpectedNetworkAccess``.
- **``@pytest.mark.network``** declares that a test's code path performs outbound
  requests. Those requests are served from files already in the repo (stubs);
  a URL with no local counterpart raises. Passing ``--with-network`` switches
  these tests to the live network instead.
- **``@pytest.mark.upstream``** is for tests whose *assertion* is about the
  outside world -- a published PURL resolves, vendored files match upstream.
  Stubbing them would be vacuous, so they always run live, and only under
  ``--with-upstream`` (the weekly ``metamodel-compat`` workflow).

Two stub sources:

- ``https://w3id.org/linkml/...`` is served per the actual w3id rewrite rules
  (see ``W3ID_REWRITES``) from the vendored linkml-model files, so a URL that
  would 404 live also fails here rather than being quietly served.
- ``https://raw.githubusercontent.com/linkml/linkml/refs/heads/main/...`` is
  served from the working tree. This also closes a blind spot: a branch that
  edited ``creature_schema.yaml`` used to be tested against *main's* copy.

Patching happens at the seams every caller funnels through, not at names
callers may have imported already: ``OpenerDirector.open`` for ``urllib``
(``hbreader`` and ``rdflib`` bind ``urlopen`` at import time, so rebinding the
module attribute never reaches them), ``HTTPAdapter.send`` for ``requests``,
and ``socket.socket.connect`` as a backstop for anything else.

This module is deliberately importable without the ``tests`` package and keeps
``linkml_runtime`` imports inside functions: ``tests/_kernel_startup/sitecustomize.py``
loads it by path into notebook kernel processes at interpreter startup, where
importing all of linkml would be slow and fragile.
"""

import socket
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from email.message import Message
from email.utils import formatdate
from functools import cache
from io import BytesIO
from pathlib import Path

import requests
import requests.adapters

REPO_ROOT = Path(__file__).resolve().parents[1]

GITHUB_RAW_MAIN = "https://raw.githubusercontent.com/linkml/linkml/refs/heads/main/"
"""Tests fetch repo files from here; they resolve to the working tree instead."""

STUB_DIR = REPO_ROOT / "tests" / "offline_stubs"
"""Vendored copies of stable third-party files, laid out as ``<host>/<path>``.

For URLs that belong to neither linkml-model nor this repo (e.g. the W3C ShEx
context). To serve a new URL, drop the file at the matching path -- no code
change needed.
"""

ALIASED_URLS = {
    # URLs whose backing file already lives in the repo under another name, so
    # duplicating it into offline_stubs/ would just create a second copy to
    # keep in sync. The DistributedModels notebook and its test import the
    # published biolink model; the snapshot the biolink test suite maintains
    # serves it -- and its (deliberate) staleness is fine for stubs, since the
    # weekly live run exercises the real URL.
    "https://w3id.org/biolink/biolink-model.yaml": "tests/linkml/test_biolink_model/input/biolink-model.yaml",
}

W3ID_BASES = ("https://w3id.org/linkml/", "http://w3id.org/linkml/")
"""Canonical PURL base and the http:// variant some schemas still carry."""

W3ID_REWRITES = (
    # (URL suffix, vendored subdirectory, local filename suffix) -- mirrors
    # https://github.com/perma-id/w3id.org/blob/master/linkml/.htaccess so a URL
    # that would 404 live is NOT served here. Longest suffixes first so e.g.
    # ``.context.jsonld`` wins over a hypothetical ``.jsonld`` rule.
    (".context.jsonld", "jsonld", ".context.jsonld"),
    (".context.json", "jsonld", ".context.jsonld"),
    (".schema.json", "jsonschema", ".schema.json"),
    (".graphql", "graphql", ".graphql"),
    (".yaml", "model/schema", ".yaml"),
    (".owl", "owl", ".owl.ttl"),
    (".ttl", "rdf", ".ttl"),
    (".shexj", "shex", ".shexj"),
    (".shexc", "shex", ".shex"),
    (".shex", "shex", ".shex"),
)

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
        # unresolvable context reference is tracked separately.
        "https://w3id.org/linkml/tests/kitchen_sink/core.context.jsonld",
    }
)


class UnexpectedNetworkAccess(RuntimeError):
    """Raised when a test reaches for the network in a way its marker does not allow."""

    def __init__(self, target: str, hint: str) -> None:
        super().__init__(f"Test attempted network access: {target}\n{hint}")


BLOCKED_HINT = (
    "This test is not marked 'network', so it must not touch the network at all.\n"
    "If its code path legitimately performs outbound requests, mark it "
    "@pytest.mark.network -- requests are then served from local files by default."
)
UNMAPPED_HINT = (
    "No local file backs this URL. Either add a mapping in tests/offline_network.py "
    "(preferred, if the content lives in this repo or the vendored model), or -- if "
    "the test's purpose is to check the real outside world -- mark it "
    "@pytest.mark.upstream so it runs live in the weekly workflow instead of per-PR CI."
)


@cache
def _w3id_local_base() -> Path:
    """Directory holding the vendored linkml-model files.

    Imported lazily: this module is loaded into notebook kernels at interpreter
    startup, where a module-level ``linkml_runtime`` import would drag all of
    linkml into every kernel (and any Python subprocess a notebook spawns).
    """
    from linkml_runtime.linkml_model.linkml_files import LOCAL_BASE

    return Path(LOCAL_BASE)


def _resolve_w3id(name: str) -> Path | None:
    """Resolve a w3id.org/linkml/ filename per the published rewrite rules."""
    for url_suffix, subdir, local_suffix in W3ID_REWRITES:
        if not name.endswith(url_suffix):
            continue
        if url_suffix == ".ttl" and ".owl." in name:
            # htaccess excludes .owl. names from the .ttl rule.
            continue
        stem = name[: -len(url_suffix)]
        candidate = _w3id_local_base() / subdir / f"{stem}{local_suffix}"
        if candidate.is_file():
            return candidate
    return None


def resolve(url: str) -> Path | None:
    """Return the local file backing ``url``, or None if it is not mapped."""
    if url in ALIASED_URLS:
        return REPO_ROOT / ALIASED_URLS[url]

    for base in W3ID_BASES:
        if url.startswith(base):
            return _resolve_w3id(url[len(base) :])

    if url.startswith(GITHUB_RAW_MAIN):
        candidate = (REPO_ROOT / url[len(GITHUB_RAW_MAIN) :]).resolve()
        # Keep a mangled URL from reaching outside the repo.
        if candidate.is_relative_to(REPO_ROOT) and candidate.is_file():
            return candidate
        return None

    parsed = urllib.parse.urlsplit(url)
    if parsed.hostname:
        stub = (STUB_DIR / parsed.hostname / parsed.path.lstrip("/")).resolve()
        if stub.is_relative_to(STUB_DIR) and stub.is_file():
            return stub
    return None


def _is_exempt(url: str) -> bool:
    """Return True for URLs that never touch the external network."""
    parsed = urllib.parse.urlsplit(url)
    return parsed.scheme in ALLOWED_SCHEMES or parsed.hostname in ALLOWED_HOSTS


def _is_local_address(host: str) -> bool:
    return host in ALLOWED_HOSTS or host.startswith("127.")


def _content_type_for(path: Path) -> str:
    return CONTENT_TYPE_BY_SUFFIX.get(path.suffix, DEFAULT_CONTENT_TYPE)


class _ResponseBody(BytesIO):
    """A response body that looks enough like a socket to satisfy consumers.

    ``hbreader`` reads ``response.fp.mode`` to pick a text wrapper, which a real
    socket-backed response has and a bare ``BytesIO`` does not.
    """

    mode = "rb"


def _urllib_response(path: Path, url: str) -> urllib.response.addinfourl:
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


def _requests_response(
    request: requests.PreparedRequest, status: int, body: bytes, path: Path | None
) -> requests.Response:
    """Build a requests-shaped response serving ``body``.

    ``raw`` is a real ``urllib3.HTTPResponse``: ``requests_cache`` serialises
    responses through their raw object, so a bare file-like stand-in breaks it.
    """
    import urllib3

    headers = {"Content-Length": str(len(body))}
    if path is not None:
        headers["Content-Type"] = _content_type_for(path)
    raw = urllib3.HTTPResponse(
        body=BytesIO(body),
        status=status,
        reason="OK" if status == 200 else "Not Found",
        headers=headers,
        preload_content=False,
        request_url=request.url,
    )
    response = requests.Response()
    response.status_code = status
    response.reason = raw.reason
    response._content = body
    response.raw = raw
    response.url = request.url
    response.request = request
    response.headers.update(headers)
    return response


def install(mode: str) -> Callable[[], None]:
    """Patch the network seams; return a callable restoring the originals.

    ``mode`` is ``"block"`` (any external access raises -- unmarked tests) or
    ``"stub"`` (mapped URLs served from disk, anything else raises -- tests
    marked ``network``).
    """
    if mode not in ("block", "stub"):
        raise ValueError(f"unknown offline-network mode: {mode!r}")

    original_open = urllib.request.OpenerDirector.open
    original_send = requests.adapters.HTTPAdapter.send
    original_connect = socket.socket.connect

    def _disposition(url: str) -> Path | None:
        """Return the file to serve, or raise. ``None`` means serve a 404."""
        if mode == "block":
            raise UnexpectedNetworkAccess(url, BLOCKED_HINT)
        if url in KNOWN_MISSING_URLS:
            return None
        local = resolve(url)
        if local is None:
            raise UnexpectedNetworkAccess(url, UNMAPPED_HINT)
        return local

    def open_offline(self, fullurl, *args, **kwargs):
        url = fullurl.full_url if isinstance(fullurl, urllib.request.Request) else fullurl
        if _is_exempt(url):
            return original_open(self, fullurl, *args, **kwargs)
        local = _disposition(url)
        if local is None:
            raise urllib.error.HTTPError(url, 404, "Not Found", Message(), None)
        return _urllib_response(local, url)

    def send_offline(self, request, *args, **kwargs):
        if _is_exempt(request.url):
            return original_send(self, request, *args, **kwargs)
        local = _disposition(request.url)
        if local is None:
            return _requests_response(request, 404, b"", None)
        return _requests_response(request, 200, local.read_bytes(), local)

    def connect_offline(self, address):
        # Backstop for libraries that use neither urllib nor requests. The
        # stub seams answer before a socket is ever opened, so anything
        # arriving here with a non-local address is an unhandled escape.
        if self.family in (socket.AF_INET, socket.AF_INET6):
            host = str(address[0]) if isinstance(address, tuple) else str(address)
            if not _is_local_address(host):
                raise UnexpectedNetworkAccess(f"socket connect to {address!r}", BLOCKED_HINT)
        return original_connect(self, address)

    urllib.request.OpenerDirector.open = open_offline
    requests.adapters.HTTPAdapter.send = send_offline
    socket.socket.connect = connect_offline

    def uninstall() -> None:
        urllib.request.OpenerDirector.open = original_open
        requests.adapters.HTTPAdapter.send = original_send
        socket.socket.connect = original_connect

    return uninstall
