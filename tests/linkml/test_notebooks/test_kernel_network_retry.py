"""Verify the transient-network retry reaches the notebook kernel process.

Notebooks run in a separate kernel started by ``ExecutePreprocessor``, so the
``retry_transient_network`` fixture in ``tests/conftest.py`` does not apply to
them -- a dropped connection inside a notebook cell fails the test outright.
``tests/_kernel_startup/sitecustomize.py`` closes that gap.

Without this test the mechanism is theory: nothing else would notice if the
``PYTHONPATH`` injection stopped taking effect.
"""

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

PROBE = """
import urllib.request

import requests

print("urlopen:", urllib.request.urlopen.__name__)
print("retries:", requests.Session().get_adapter("https://example.invalid").max_retries.total)
"""


@pytest.fixture
def probe_outputs(pytestconfig, tmp_path):
    """Run ``PROBE`` in a real kernel and return its stdout lines."""
    if pytestconfig.getoption("--without-cache"):
        pytest.skip("kernel_network_retry is disabled by --without-cache")

    nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(PROBE)])
    ExecutePreprocessor(timeout=120).preprocess(nb, {"metadata": {"path": str(tmp_path)}})

    streams = [out for cell in nb.cells for out in cell.outputs if out.output_type == "stream"]
    return "".join(out.text for out in streams).splitlines()


def test_kernel_urlopen_is_wrapped(probe_outputs):
    """``urlopen`` inside the kernel retries transient failures."""
    assert "urlopen: wrapped" in probe_outputs, (
        f"sitecustomize did not install in the kernel; got {probe_outputs}. "
        "Notebook cells fetching over urllib will fail on any transient error."
    )


def test_kernel_requests_sessions_get_a_retrying_adapter(probe_outputs):
    """Sessions built inside the kernel carry the retrying adapter.

    ``context_issue.ipynb`` fetches with ``requests``, so this is the path that
    actually flakes in CI.
    """
    from tests.network_retry import NETWORK_RETRY_ATTEMPTS

    # Retry.total counts retries, so a total of N-1 means N attempts.
    assert f"retries: {NETWORK_RETRY_ATTEMPTS - 1}" in probe_outputs, (
        f"kernel requests Sessions have no retrying adapter; got {probe_outputs}"
    )
