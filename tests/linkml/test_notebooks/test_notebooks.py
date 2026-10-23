import os
import re
import sys

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

from tests.environment import env

# Tests moved to root: tests/linkml/test_notebooks, notebooks at root
NBBASEDIR = os.path.join(env.cwd, "..", "notebooks")

# Substrings that indicate a real failure leaked into cell output
# without raising (e.g., shell-magic install errors, post-execution tracebacks).
# Kept narrow on purpose: must appear at line start so they match tool error
# prefixes (setuptools, pip, uv) rather than incidental occurrences in strings.
_ERROR_LINE_PREFIXES = ("error: ", "ERROR: ")
_ERROR_SUBSTRINGS = (
    "Traceback (most recent call last):",
    "No module named",
)


def _collect_output_errors(nb: nbformat.NotebookNode) -> list[str]:
    """Scan executed notebook for failure indicators that didn't raise.

    Returns a list of human-readable findings; empty list means clean.
    """
    findings: list[str] = []
    for idx, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") != "stream":
                continue
            text = "".join(output.get("text", []))
            for marker in _ERROR_SUBSTRINGS:
                if marker in text:
                    findings.append(f"cell {idx} ({output.get('name')}): contains {marker!r}")
                    break
            for line in text.splitlines():
                if line.startswith(_ERROR_LINE_PREFIXES):
                    findings.append(f"cell {idx} ({output.get('name')}): {line[:160]}")
                    break
    return findings


# Package-install lines in any of the forms the notebooks use:
# `%pip install`, `!pip install`, `%uv pip install`, `!uv pip install`.
_INSTALL_LINE = re.compile(r"^\s*[%!](uv\s+)?pip\s+install\b")


def _strip_install_lines(nb: nbformat.NotebookNode) -> None:
    """Remove package-install lines so the notebook runs against the locked environment.

    The packages those lines install must be provided by the ``notebooks``
    dependency group instead; a missing one surfaces as an import failure.

    >>> cell = nbformat.v4.new_code_cell("%pip install -q yamlmagic\\n%load_ext yamlmagic")
    >>> nb = nbformat.v4.new_notebook(cells=[cell])
    >>> _strip_install_lines(nb)
    >>> nb.cells[0].source
    '%load_ext yamlmagic'
    """
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = "\n".join(line for line in cell.source.splitlines() if not _INSTALL_LINE.match(line))


@pytest.fixture
def ep():
    return ExecutePreprocessor(timeout=600)


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="charset failure on windows in github actions. See https://github.com/linkml/linkml/issues/314",
)
# network: the kernel process fetches remote schemas/contexts; the conftest
# fixture injects the offline guard into it via sitecustomize
@pytest.mark.network
@pytest.mark.parametrize(
    "nbname",
    [filename for filename in os.listdir(NBBASEDIR) if not filename.startswith(".") and filename.endswith(".ipynb")],
)
# locked: install lines removed, so the notebook runs offline against this
# checkout's linkml and the lockfile. as-shipped: run verbatim, as a user
# would, installing from PyPI; live-only, in the weekly upstream workflow.
@pytest.mark.parametrize(
    "as_shipped",
    [pytest.param(False, id="locked"), pytest.param(True, id="as-shipped", marks=pytest.mark.upstream)],
)
def test_redo_notebook(nbname: str, as_shipped: bool, ep: ExecutePreprocessor) -> None:
    """Verify the notebook executes end-to-end without raising or surfacing errors in output."""
    with open(os.path.join(NBBASEDIR, nbname), encoding="utf-8") as nbf:
        nb = nbformat.read(nbf, as_version=4)
    if not as_shipped:
        _strip_install_lines(nb)
    ep.preprocess(nb, dict(metadata=dict(path=NBBASEDIR)))

    findings = _collect_output_errors(nb)
    if findings:
        pytest.fail(f"{nbname} executed but cell output contains failure markers:\n  " + "\n  ".join(findings))
