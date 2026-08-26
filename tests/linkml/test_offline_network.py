"""Tests for the offline network guard in :mod:`tests.offline_network`.

The guard serves mapped URLs from files in the repo and blocks everything else,
so that jobs which never pass ``--with-network`` cannot fail on an upstream
hiccup. These pin the two things that make it trustworthy: that a *real* caller
resolves through it, and that an unmapped URL fails loudly rather than silently
reaching the network.
"""

import urllib.error
import urllib.request
from pathlib import Path

import hbreader
import pytest

from linkml_runtime.linkml_model.linkml_files import LINKML_URL_BASE
from linkml_runtime.utils.schemaview import SchemaView
from tests.offline_network import (
    GITHUB_RAW_MAIN,
    KNOWN_MISSING_URLS,
    REPO_ROOT,
    UnexpectedNetworkAccess,
    resolve,
)

CREATURE_SCHEMA_RELPATH = "tests/linkml_runtime/test_utils/input/mcc/creature_schema.yaml"


def test_model_urls_resolve_to_vendored_files():
    """Published linkml-model URLs are served from the vendored copies."""
    local = resolve(f"{LINKML_URL_BASE}meta.yaml")
    assert local is not None
    assert local.is_file()
    assert local.name == "meta.yaml"


def test_model_url_map_covers_sources_without_a_source_member():
    """units/datasets/validation ship vendored files but have no ``Source`` member."""
    for name in ("units", "datasets", "validation"):
        url = f"{LINKML_URL_BASE}{name}.context.jsonld"
        assert resolve(url) is not None, f"{url} should be served from disk"


def test_github_raw_urls_resolve_to_the_working_tree():
    """A repo file fetched over https resolves to this checkout, not main."""
    local = resolve(f"{GITHUB_RAW_MAIN}{CREATURE_SCHEMA_RELPATH}")
    assert local == (REPO_ROOT / CREATURE_SCHEMA_RELPATH).resolve()


def test_unmapped_url_does_not_resolve():
    """Anything without a local counterpart is not served."""
    assert resolve("https://example.invalid/nope.yaml") is None


def test_github_raw_url_cannot_escape_the_repo():
    """A traversal in the URL path does not reach outside the checkout."""
    assert resolve(f"{GITHUB_RAW_MAIN}../../../etc/passwd") is None


@pytest.mark.parametrize(
    "url",
    [
        "https://example.invalid/schema.yaml",
        "https://raw.githubusercontent.com/linkml/linkml/refs/heads/main/does/not/exist.yaml",
    ],
)
def test_unmapped_url_raises_through_a_real_fetch(url):
    """Unmapped access fails loudly instead of quietly hitting the network."""
    with pytest.raises(UnexpectedNetworkAccess, match="not served from a local file"):
        urllib.request.urlopen(url)  # noqa: S310


def test_known_missing_url_still_404s():
    """The unresolvable generated @context keeps 404ing, as it does upstream."""
    url = next(iter(KNOWN_MISSING_URLS))
    with pytest.raises(urllib.error.HTTPError) as excinfo:
        urllib.request.urlopen(url)  # noqa: S310
    assert excinfo.value.code == 404


def test_hbreader_resolves_through_the_guard():
    """A real caller is served from disk.

    ``hbreader`` does ``from urllib.request import urlopen`` at import time, so a
    patch of the module attribute would never reach it. This is the assertion that
    the guard is genuinely installed -- checking that an attribute was reassigned
    would pass even if no consumer resolved through it.
    """
    content = hbreader.hbread(f"{GITHUB_RAW_MAIN}{CREATURE_SCHEMA_RELPATH}")
    assert content == (REPO_ROOT / CREATURE_SCHEMA_RELPATH).read_text()


def test_schemaview_loads_a_remote_url_offline():
    """The end-to-end path the flaky tests take, with no network available."""
    view = SchemaView(f"{GITHUB_RAW_MAIN}{CREATURE_SCHEMA_RELPATH}")
    assert view.schema.name == "creature_schema"
    assert "Creature" in view.all_classes()


def test_file_urls_are_not_blocked(tmp_path: Path):
    """``file://`` never touches the network, so it passes straight through."""
    target = tmp_path / "local.yaml"
    target.write_text("name: local\n")
    assert hbreader.hbread(target.as_uri()) == "name: local\n"


@pytest.mark.network
def test_network_marked_tests_get_the_real_opener():
    """Opting in with the marker hands back real network access.

    Asserts the guard is absent rather than making a request, so this stays
    offline-safe even though it only runs under ``--with-network``.
    """
    assert urllib.request.OpenerDirector.open.__name__ != "open_offline"
