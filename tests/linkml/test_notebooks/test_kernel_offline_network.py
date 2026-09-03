"""Verify the offline network guard is active inside notebook kernel processes.

The kernel is a separate process, so the conftest fixture's patches cannot be
inspected from here -- these tests execute code *in* a real kernel, exactly as
the notebook tests do, and assert on what that code observes. Asserting from
the outside that ``PYTHONPATH`` was set would pass even if ``sitecustomize``
silently failed to install.
"""

import nbformat
import pytest
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

from tests.offline_network import GITHUB_RAW_MAIN

CREATURE_SCHEMA_RELPATH = "tests/linkml_runtime/test_utils/input/mcc/creature_schema.yaml"


def _run_cell(source: str) -> None:
    """Execute ``source`` in a fresh kernel, raising on any cell error."""
    nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(source)])
    ExecutePreprocessor(timeout=120).preprocess(nb, {"metadata": {"path": "."}})


@pytest.mark.network
def test_kernel_serves_mapped_urls_from_disk(pytestconfig):
    """A urllib fetch inside the kernel is served from the working tree."""
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; kernel guard not installed")
    _run_cell(
        f"""
import urllib.request
assert urllib.request.OpenerDirector.open.__name__ == "open_offline", (
    "the offline guard did not install in the kernel"
)
with urllib.request.urlopen({GITHUB_RAW_MAIN + CREATURE_SCHEMA_RELPATH!r}) as response:
    body = response.read().decode("utf-8")
assert "creature_schema" in body
"""
    )


@pytest.mark.network
def test_kernel_blocks_unmapped_urls(pytestconfig):
    """An unmapped fetch inside the kernel raises instead of going out."""
    if pytestconfig.getoption("--with-network"):
        pytest.skip("live network requested; kernel guard not installed")
    with pytest.raises(CellExecutionError, match="UnexpectedNetworkAccess"):
        _run_cell(
            """
import urllib.request
urllib.request.urlopen("https://example.invalid/schema.yaml")
"""
        )
