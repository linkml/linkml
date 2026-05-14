import os
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


@pytest.fixture
def ep():
    return ExecutePreprocessor(timeout=600)


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="charset failure on windows in github actions. See https://github.com/linkml/linkml/issues/314",
)
@pytest.mark.parametrize(
    "nbname",
    [filename for filename in os.listdir(NBBASEDIR) if not filename.startswith(".") and filename.endswith(".ipynb")],
)
def test_redo_notebook(nbname: str, ep: ExecutePreprocessor) -> None:
    """Verify the notebook executes end-to-end without raising or surfacing errors in output."""
    with open(os.path.join(NBBASEDIR, nbname), encoding="utf-8") as nbf:
        nb = nbformat.read(nbf, as_version=4)
    ep.preprocess(nb, dict(metadata=dict(path=NBBASEDIR)))

    findings = _collect_output_errors(nb)
    if findings:
        pytest.fail(f"{nbname} executed but cell output contains failure markers:\n  " + "\n  ".join(findings))
