"""Tests for the network rules enforced by :mod:`tests.offline_network`.

Three behaviours matter, and each is pinned through the autouse fixture itself
rather than by installing the guard by hand -- an assertion that the patch *is
installed* can pass while the mechanism is inert, so these drive real callers:

- unmarked tests cannot reach the network at any layer, even for mapped URLs;
- ``network``-marked tests are served from local files, faithfully to what the
  live servers would do (a URL that 404s live must not succeed here);
- unmapped access fails loudly instead of quietly going out.
"""

import socket
import urllib.error
import urllib.request
from pathlib import Path

import hbreader
import pytest
import requests

from linkml_runtime.linkml_model.linkml_files import URL_FOR, Format, Source
from linkml_runtime.utils.schemaview import SchemaView
from tests.linkml_runtime.test_linkml_model.test_linkml_files import W3ID_FORMATS
from tests.offline_network import (
    GITHUB_RAW_MAIN,
    KNOWN_MISSING_URLS,
    REPO_ROOT,
    UnexpectedNetworkAccess,
    resolve,
)

CREATURE_SCHEMA_RELPATH = "tests/linkml_runtime/test_utils/input/mcc/creature_schema.yaml"
META_YAML_URL = URL_FOR(Source.META, Format.YAML)

# ---------------------------------------------------------------------------
# resolve(): the URL -> local file mapping, faithful to the w3id rewrite rules
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("source,fmt", W3ID_FORMATS)
def test_every_published_purl_resolves_to_a_vendored_file(source, fmt):
    """Each URL the w3id rewrite rules serve is backed by a vendored file.

    This is the per-PR, offline half of ``test_url_for_format``: a change to
    ``URL_FOR`` or ``_Path`` that would break the published PURLs breaks this
    immediately, without asking w3id. The weekly ``upstream`` run checks the
    live half.
    """
    url = URL_FOR(source, fmt)
    local = resolve(url)
    assert local is not None, f"{url} is not served from a local file"
    assert local.is_file()


@pytest.mark.parametrize("name", ["units", "datasets", "validation"])
def test_sources_without_a_source_member_are_still_served(name):
    """w3id rewrites by filename pattern, not by the ``Source`` enum.

    units/datasets/validation ship vendored files but have no ``Source``
    member; the live rules serve them, so the stub must too.
    """
    assert resolve(f"https://w3id.org/linkml/{name}.context.jsonld") is not None
    assert resolve(f"https://w3id.org/linkml/{name}.yaml") is not None


@pytest.mark.parametrize(
    "url",
    [
        # No w3id rewrite rule serves these extensions; live they 404 (or fall
        # through to a redirect that 404s). Serving them here would let a test
        # pass against a URL that does not exist.
        "https://w3id.org/linkml/meta.sql",
        "https://w3id.org/linkml/meta.proto",
        "https://w3id.org/linkml/meta.py",
        "https://w3id.org/linkml/meta.xlsx",
        "https://w3id.org/linkml/__init__.py",
        "https://example.invalid/nope.yaml",
    ],
)
def test_urls_that_404_live_do_not_resolve(url):
    assert resolve(url) is None


def test_http_scheme_variant_is_served():
    """Some schemas still carry http:// PURLs; w3id serves both."""
    assert resolve("http://w3id.org/linkml/meta.yaml") == resolve(META_YAML_URL)


def test_github_raw_urls_resolve_to_the_working_tree():
    """A repo file fetched over https resolves to this checkout, not main."""
    local = resolve(f"{GITHUB_RAW_MAIN}{CREATURE_SCHEMA_RELPATH}")
    assert local == (REPO_ROOT / CREATURE_SCHEMA_RELPATH).resolve()


def test_github_raw_url_cannot_escape_the_repo():
    """A traversal in the URL path does not reach outside the checkout."""
    assert resolve(f"{GITHUB_RAW_MAIN}../../../etc/passwd") is None


# ---------------------------------------------------------------------------
# Unmarked tests: no network, at any layer, even for mapped URLs
# ---------------------------------------------------------------------------


def test_unmarked_urllib_access_is_blocked_even_for_mapped_urls():
    with pytest.raises(UnexpectedNetworkAccess, match="not marked 'network'"):
        urllib.request.urlopen(META_YAML_URL)  # noqa: S310


def test_unmarked_requests_access_is_blocked_even_for_mapped_urls():
    with pytest.raises(UnexpectedNetworkAccess, match="not marked 'network'"):
        requests.get(META_YAML_URL, timeout=5)


def test_unmarked_raw_socket_access_is_blocked():
    """The socket backstop catches libraries that use neither urllib nor requests."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)
    try:
        # 192.0.2.1 is TEST-NET-1 (RFC 5737): guaranteed unroutable, so if the
        # backstop were missing this would time out rather than fetch anything.
        with pytest.raises(UnexpectedNetworkAccess, match="socket connect"):
            sock.connect(("192.0.2.1", 80))
    finally:
        sock.close()


def test_file_urls_pass_through_the_block(tmp_path: Path):
    """``file://`` never touches the network, so even unmarked tests may use it."""
    target = tmp_path / "local.yaml"
    # write_bytes, not write_text: text mode would translate the newline to CRLF
    # on Windows, which hbreader then hands back untranslated.
    target.write_bytes(b"name: local\n")
    assert hbreader.hbread(target.as_uri()) == "name: local\n"


# ---------------------------------------------------------------------------
# network-marked tests: served from local files (or live under --with-network)
# ---------------------------------------------------------------------------


def _expected_bytes(path: Path) -> str:
    # Compared as raw bytes: the stub serves the file without translating
    # newlines, and ``.gitattributes`` sets ``text=auto``, so the working tree
    # copy has CRLF on Windows. ``read_text`` would normalise it and never match.
    return path.read_bytes().decode("utf-8")


@pytest.mark.network
def test_urlopen_is_served_from_disk(pytestconfig):
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; stub not installed")
    with urllib.request.urlopen(META_YAML_URL) as response:  # noqa: S310
        assert response.status == 200
        body = response.read().decode("utf-8")
    assert body == _expected_bytes(resolve(META_YAML_URL))


@pytest.mark.network
def test_hbreader_is_served_from_disk(pytestconfig):
    """A real caller that bound ``urlopen`` at import time still resolves.

    ``hbreader`` does ``from urllib.request import urlopen``, so a patch of the
    module attribute would never reach it; this pins that the guard sits at a
    seam every caller funnels through.
    """
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; stub not installed")
    url = f"{GITHUB_RAW_MAIN}{CREATURE_SCHEMA_RELPATH}"
    assert hbreader.hbread(url) == _expected_bytes(REPO_ROOT / CREATURE_SCHEMA_RELPATH)


@pytest.mark.network
def test_requests_is_served_from_disk(pytestconfig):
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; stub not installed")
    response = requests.get(META_YAML_URL, timeout=5)
    assert response.status_code == 200
    assert response.text == _expected_bytes(resolve(META_YAML_URL))


@pytest.mark.network
def test_schemaview_loads_a_remote_url_offline(pytestconfig):
    """The end-to-end path the flaky tests take, with no network available."""
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; stub not installed")
    view = SchemaView(f"{GITHUB_RAW_MAIN}{CREATURE_SCHEMA_RELPATH}")
    assert view.schema.name == "creature_schema"
    assert "Creature" in view.all_classes()


@pytest.mark.network
def test_unmapped_urllib_url_raises(pytestconfig):
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; stub not installed")
    with pytest.raises(UnexpectedNetworkAccess, match="No local file backs"):
        urllib.request.urlopen("https://example.invalid/schema.yaml")  # noqa: S310


@pytest.mark.network
def test_unmapped_requests_url_raises(pytestconfig):
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; stub not installed")
    with pytest.raises(UnexpectedNetworkAccess, match="No local file backs"):
        requests.get("https://example.invalid/schema.yaml", timeout=5)


@pytest.mark.network
def test_known_missing_url_still_404s(pytestconfig):
    """The unresolvable generated @context keeps 404ing, as it does upstream."""
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; stub not installed")
    url = next(iter(KNOWN_MISSING_URLS))
    with pytest.raises(urllib.error.HTTPError) as excinfo:
        urllib.request.urlopen(url)  # noqa: S310
    assert excinfo.value.code == 404


@pytest.mark.network
def test_with_network_flag_hands_back_the_live_opener(pytestconfig):
    """Under ``--with-network``, network-marked tests get the real seams.

    Asserts on the patch state rather than making a request, so this stays
    offline-safe in both modes.
    """
    if pytestconfig.getoption("--with-network"):
        assert urllib.request.OpenerDirector.open.__name__ != "open_offline"
        assert requests.adapters.HTTPAdapter.send.__name__ != "send_offline"
    else:
        assert urllib.request.OpenerDirector.open.__name__ == "open_offline"
        assert requests.adapters.HTTPAdapter.send.__name__ == "send_offline"
