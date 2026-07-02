import subprocess
import tempfile
from importlib.util import find_spec
from itertools import product
from pathlib import Path
from urllib.parse import urlparse

import pytest
import requests

HAVE_REQUESTS_CACHE = bool(find_spec("requests_cache"))

from linkml_runtime.linkml_model.linkml_files import (
    GITHUB_IO_PATH_FOR,
    GITHUB_PATH_FOR,
    LOCAL_BASE,
    LOCAL_PATH_FOR,
    META_ONLY,
    URL_FOR,
    Format,
    ReleaseTag,
    Source,
    _Path,
)

_LOCAL_BASE = Path(LOCAL_BASE) if not isinstance(LOCAL_BASE, Path) else LOCAL_BASE

EXPECTED_FORMATS = [
    (source, fmt) for source, fmt in product(Source, Format) if (fmt not in META_ONLY or source == Source.META)
]

W3ID_EXTENSIONS = (
    "html",
    "yaml",
    "graphql",
    "context.json",
    "context.jsonld",
    "schema.json",
    "json",
    "ttl",
    "owl",
    "shex",
    "shexc",
    "shexj",
)
W3ID_FORMATS = [(source, fmt) for source, fmt in EXPECTED_FORMATS if _Path.get(fmt.name).extension in W3ID_EXTENSIONS]
"""The formats that have rewrite rules at https://github.com/perma-id/w3id.org/blob/master/linkml/.htaccess"""


@pytest.mark.parametrize("source,fmt", EXPECTED_FORMATS)
def test_local_paths(source, fmt):
    a_path = Path(LOCAL_PATH_FOR(source, fmt))
    assert a_path.exists()
    assert a_path.is_absolute()


@pytest.mark.parametrize("fmt", Format.__iter__())
def test_format_paths(fmt):
    """Every format should have an entry in _Path"""
    assert fmt.name in _Path.items()


def test_no_unmapped_dirs():
    """
    There should be no additional directories that don't have a mapping for Format.
    """
    EXCLUDES = ("__pycache__",)

    expected = {_LOCAL_BASE / _Path.get(fmt.name).path for fmt in Format}
    expected.add(_LOCAL_BASE / "model")

    actual = {a_dir for a_dir in _LOCAL_BASE.iterdir() if a_dir.is_dir() and a_dir.name not in EXCLUDES}
    # Special case the root directory
    actual.add(_LOCAL_BASE)
    # Special case YAML which is in a subdirectory - we've checked for existence above
    actual.add(_LOCAL_BASE / _Path.get("YAML").path)
    assert expected == actual


# --------------------------------------------------
# URLs
# --------------------------------------------------


@pytest.mark.skip("github paths largely unused and expensive to test due to ratelimiting")
@pytest.mark.parametrize("release_type", ReleaseTag.__iter__())
@pytest.mark.parametrize("source,fmt", EXPECTED_FORMATS)
def test_github_path_exists(source, fmt, release_type):
    url = GITHUB_PATH_FOR(source, fmt, release_type)
    res = requests.get(url)
    assert res.status_code != 404, url


@pytest.mark.parametrize("release_type", ReleaseTag.__iter__())
@pytest.mark.parametrize("source,fmt", EXPECTED_FORMATS)
def test_github_path_format(source, fmt, release_type):
    if release_type == ReleaseTag.CURRENT:
        pytest.skip("Need to cache network requests for this")

    url = GITHUB_PATH_FOR(source, fmt, release_type)
    # ensure it parses
    assert urlparse(url)
    # for windows...
    assert "\\" not in url


@pytest.mark.skip("github paths largely unused")
@pytest.mark.parametrize("source,fmt", EXPECTED_FORMATS)
def test_github_io_path(source, fmt):
    url = GITHUB_IO_PATH_FOR(source, fmt)
    res = requests.get(url)
    assert res.status_code != 404, url


@pytest.mark.skipif(not HAVE_REQUESTS_CACHE, reason="Need to cache this")
@pytest.mark.parametrize("source,fmt", W3ID_FORMATS)
def test_url_for_format(source, fmt):
    url = URL_FOR(source, fmt)
    res = requests.get(url)
    assert res.status_code != 404, url


def test_fixed_meta_url():
    """
    One fixed canary value - the METAMODEL_URI as used in linkml main shouldn't change
    """
    assert URL_FOR(Source.META, Format.YAML) == "https://w3id.org/linkml/meta.yaml"
    assert URL_FOR(Source.META, Format.JSONLD) == "https://w3id.org/linkml/meta.context.jsonld"


VENDORED_RUNTIME_FILES = [(source, fmt) for source in Source for fmt in (Format.YAML, Format.JSONLD)]
"""Source files resolved locally at runtime by generators (YAML for schema imports,
JSONLD for context resolution). Drift here means generators silently use stale definitions."""

UPSTREAM_SHA_FILE = _LOCAL_BASE / "UPSTREAM_SHA"
"""File written by ``make update_model`` that records the upstream linkml-model commit SHA
that was vendored. The test uses this SHA to fetch the exact same revision from GitHub."""

LINKML_MODEL_GITHUB_RAW_BASE = "https://raw.githubusercontent.com/linkml/linkml-model/"
"""Base URL for raw content on the linkml-model GitHub repository."""

LINKML_MODEL_REPO = "https://github.com/linkml/linkml-model.git"
"""URL of the upstream linkml-model Git repository."""

LINKML_MODEL_MAIN_BASE = f"{LINKML_MODEL_GITHUB_RAW_BASE}main/linkml_model/"
"""Base URL for the source-of-truth copies on linkml-model's main branch."""


def _get_upstream_sha() -> str:
    """Read the upstream commit SHA recorded by ``make update_model``.

    Returns the 40-character hex SHA written to ``UPSTREAM_SHA`` at vendoring time.
    """
    assert UPSTREAM_SHA_FILE.exists(), (
        f"{UPSTREAM_SHA_FILE} not found. Run 'make update_model' in packages/linkml_runtime/ to regenerate it."
    )
    assert len(open(UPSTREAM_SHA_FILE).read()) > 0, (
        f"{UPSTREAM_SHA_FILE} is empty. Run 'make update_model' in packages/linkml_runtime/ to regenerate it."
    )
    return UPSTREAM_SHA_FILE.read_text().strip()


def _git_show_file(sha: str, repo_path: str) -> str:
    """Return the content of a file at a specific commit in the upstream repository.

    Uses the git protocol (``git fetch`` + ``git show``) to retrieve the file
    without touching the GitHub REST API, avoiding IP-based rate limiting.

    ``repo_path`` is the path inside the repository (e.g.
    ``"linkml_model/model/schema/meta.yaml"``).
    """
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "init", "--bare", "-q", tmp], check=True)
        subprocess.run(
            ["git", "-C", tmp, "fetch", "--depth=1", LINKML_MODEL_REPO, sha],
            check=True,
            capture_output=True,
        )
        result = subprocess.run(
            ["git", "-C", tmp, "show", f"FETCH_HEAD:{repo_path}"],
            check=True,
            capture_output=True,
            text=True,
        )
    return result.stdout


def _linkml_model_main_url(source: Source, fmt: Format) -> str:
    """Build the raw.githubusercontent URL for the source/format pair on linkml-model main."""
    rel = Path(LOCAL_PATH_FOR(source, fmt)).relative_to(_LOCAL_BASE).as_posix()
    return f"{LINKML_MODEL_MAIN_BASE}{rel}"


@pytest.mark.network
@pytest.mark.parametrize("source,fmt", VENDORED_RUNTIME_FILES)
def test_vendored_files_match_upstream(source, fmt):
    """Detect drift between vendored files and the upstream commit they were vendored from.

    Generators resolve these files locally instead of fetching from the network.
    The expected upstream revision is read from ``UPSTREAM_SHA``, which is written
    by ``make update_model`` at vendoring time and committed alongside the files.
    If the vendored files were modified without re-running ``make update_model``,
    this test will catch it.

    File content is fetched via the git protocol (not the GitHub REST API) to
    avoid IP-based rate limiting.
    """
    sha = _get_upstream_sha()
    local_path = Path(LOCAL_PATH_FOR(source, fmt))
    repo_path = f"linkml_model/{Path(LOCAL_PATH_FOR(source, fmt)).relative_to(_LOCAL_BASE).as_posix()}"

    local_content = local_path.read_text()
    upstream_content = _git_show_file(sha, repo_path)

    assert local_content == upstream_content, (
        f"Vendored {local_path.name} differs from upstream {LINKML_MODEL_REPO} "
        f"at {repo_path} (SHA {sha[:12]}). "
        "Run 'make update_model' in packages/linkml_runtime/ to re-vendor the files."
    )


@pytest.mark.network
@pytest.mark.upstream_main
@pytest.mark.parametrize("source,fmt", VENDORED_RUNTIME_FILES)
def test_vendored_files_match_upstream_main(source, fmt):
    """Detect drift between vendored files and the linkml-model main branch.

    This is a soft-fail early-warning test. It catches cases where upstream main
    has moved ahead of the vendored files before a new release is cut. Failures
    here are informational — they do not block a PR — but signal that a vendored
    update may be needed soon.

    For the hard check against the vendored commit, see
    ``test_vendored_files_match_upstream``.
    """
    local_path = Path(LOCAL_PATH_FOR(source, fmt))
    url = _linkml_model_main_url(source, fmt)

    local_content = local_path.read_text()
    response = requests.get(url, timeout=10)
    assert response.ok, f"Failed to fetch {url}: {response.status_code}"

    assert local_content == response.text, (
        f"Vendored {local_path.name} differs from upstream main {url}. "
        "This is an early warning: upstream main has diverged from the vendored files. "
        "No action is required until a new linkml-model release is cut."
    )
