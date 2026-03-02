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


@pytest.fixture(scope="module", autouse=True)
def manage_click_monkeypatch():
    """
    Manage the Click monkeypatch for linkml_runtime tests.

    The test_environment.py module monkeypatches click.core.Context.exit at import time.
    This fixture ensures that:
    1. The monkeypatch is active during linkml_runtime module tests
    2. The original behavior is restored after each module's tests complete
    """
    # Import to trigger the monkeypatch (if not already done)
    try:
        from tests.linkml_runtime.support import test_environment  # noqa: F401
    except ImportError:
        pass

    yield  # Let module tests run with the monkeypatch active

    # After this module's tests are done, restore the original Click exit
    try:
        from tests.linkml_runtime.support.test_environment import _original_click_exit
        import click

        click.core.Context.exit = _original_click_exit
    except (ImportError, AttributeError):
        # If the monkeypatch wasn't applied or original wasn't saved, skip restoration
        pass
