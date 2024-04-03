from pathlib import Path
import pytest
import requests_cache

@pytest.fixture(scope="session", autouse=True)
def patch_requests_cache(pytestconfig):
    """
    Cache network requests - for each unique network request, store it in
    an sqlite cache. only do unique requests once per session.
    """
    cache_file = Path(__file__).parent / "output" / "requests-cache.sqlite"
    cache_file.parent.mkdir(exist_ok=True)
    requests_cache.install_cache(
        str(cache_file),
        backend="sqlite",
        urls_expire_after={"localhost": requests_cache.DO_NOT_CACHE},
    )
    requests_cache.clear()
    yield
    # If we want to delete cache, this is how we might do it!
    # if not pytestconfig.getoption("--with-output"):
    #    cache_file.unlink(missing_ok=True)