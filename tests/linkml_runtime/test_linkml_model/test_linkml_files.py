import pytest
import requests
from pathlib import Path
from itertools import product
from urllib.parse import urlparse
from importlib.util import find_spec

HAVE_REQUESTS_CACHE = bool(find_spec("requests_cache"))

from linkml_runtime.linkml_model.linkml_files import (
    Source,
    Format,
    _Path,
    URL_FOR,
    LOCAL_PATH_FOR,
    LOCAL_BASE,
    GITHUB_IO_PATH_FOR,
    GITHUB_PATH_FOR,
    META_ONLY,
    ReleaseTag
)

EXPECTED_FORMATS = [
    (source, fmt) for source, fmt in product(Source, Format)
    if (fmt not in META_ONLY or source == Source.META)
]

W3ID_EXTENSIONS = (
    'html',
    'yaml',
    'graphql',
    'context.json',
    'context.jsonld',
    'schema.json',
    'json',
    'ttl',
    'owl',
    'shex',
    'shexc',
    'shexj'
)
W3ID_FORMATS = [
    (source, fmt) for source, fmt in EXPECTED_FORMATS
    if _Path.get(fmt.name).extension in W3ID_EXTENSIONS
]
"""The formats that have rewrite rules at https://github.com/perma-id/w3id.org/blob/master/linkml/.htaccess"""

@pytest.mark.parametrize(
    'source,fmt',
    EXPECTED_FORMATS
)
def test_local_paths(source, fmt):
    a_path = Path(LOCAL_PATH_FOR(source, fmt))
    assert a_path.exists()
    assert a_path.is_absolute()

@pytest.mark.parametrize(
    'fmt',
    Format.__iter__()
)
def test_format_paths(fmt):
    """Every format should have an entry in _Path"""
    assert fmt.name in _Path.items()

def test_no_unmapped_dirs():
    """
    There should be no additional directories that don't have a mapping for Format.
    """
    EXCLUDES = ('__pycache__',)

    expected = {LOCAL_BASE / _Path.get(fmt.name).path for fmt in Format}
    expected.add(LOCAL_BASE / 'model')

    actual = {a_dir for a_dir in LOCAL_BASE.iterdir() if a_dir.is_dir() and a_dir.name not in EXCLUDES}
    # Special case the root directory
    actual.add(LOCAL_BASE)
    # Special case YAML which is in a subdirectory - we've checked for existence above
    actual.add(LOCAL_BASE / _Path.get('YAML').path)
    assert expected == actual


# --------------------------------------------------
# URLs
# --------------------------------------------------

@pytest.mark.skip("github paths largely unused and expensive to test due to ratelimiting")
@pytest.mark.parametrize(
    'release_type',
    ReleaseTag.__iter__()
)
@pytest.mark.parametrize(
    'source,fmt',
    EXPECTED_FORMATS
)
def test_github_path_exists(source,fmt, release_type):
    url = GITHUB_PATH_FOR(source, fmt, release_type)
    res = requests.get(url)
    assert res.status_code != 404, url


@pytest.mark.parametrize(
    'release_type',
    ReleaseTag.__iter__()
)
@pytest.mark.parametrize(
    'source,fmt',
    EXPECTED_FORMATS
)
def test_github_path_format(source,fmt, release_type):
    if release_type == ReleaseTag.CURRENT:
        pytest.skip("Need to cache network requests for this")

    url = GITHUB_PATH_FOR(source, fmt, release_type)
    # ensure it parses
    assert urlparse(url)
    # for windows...
    assert '\\' not in url

@pytest.mark.skip("github paths largely unused")
@pytest.mark.parametrize(
    'source,fmt',
    EXPECTED_FORMATS
)
def test_github_io_path(source,fmt):
    url = GITHUB_IO_PATH_FOR(source, fmt)
    res = requests.get(url)
    assert res.status_code != 404, url


@pytest.mark.skipif(not HAVE_REQUESTS_CACHE,reason= 'Need to cache this')
@pytest.mark.parametrize(
    'source,fmt',
    W3ID_FORMATS
)
def test_url_for_format(source,fmt):
    url = URL_FOR(source, fmt)
    res = requests.get(url)
    assert res.status_code != 404, url

def test_fixed_meta_url():
    """
    One fixed canary value - the METAMODEL_URI as used in linkml main shouldn't change
    """
    assert URL_FOR(Source.META, Format.YAML) == 'https://w3id.org/linkml/meta.yaml'
    assert URL_FOR(Source.META, Format.JSONLD) == 'https://w3id.org/linkml/meta.context.jsonld'







