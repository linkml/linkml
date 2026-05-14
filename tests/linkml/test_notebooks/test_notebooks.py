import os
import sys

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

from tests.environment import env

# Tests moved to root: tests/linkml/test_notebooks, notebooks at root
NBBASEDIR = os.path.join(env.cwd, "..", "notebooks")


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
    """Verify the notebook executes end-to-end without raising in any cell."""
    with open(os.path.join(NBBASEDIR, nbname), encoding="utf-8") as nbf:
        nb = nbformat.read(nbf, as_version=4)
    ep.preprocess(nb, dict(metadata=dict(path=NBBASEDIR)))
