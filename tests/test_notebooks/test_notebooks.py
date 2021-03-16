import os
import unittest
from io import StringIO

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

from tests.environment import env
from tests.test_notebooks.environment import nbenv
from tests.utils.filters import nb_filter
from tests.utils.test_environment import TestEnvironmentTestCase

FORCE_REWRITE = True


def force_rewrite_comparator(expected: str, actual: str) -> str:
    msg = nbenv.string_comparator(expected, actual)
    if not msg and FORCE_REWRITE:
        msg = "Forced rewrite"
    return msg

@unittest.skipIf(True, "Skipped until we figure out why this fails in github actions")
class NotebookTestCase(TestEnvironmentTestCase):
    ep = ExecutePreprocessor(timeout=600)
    nbbasedir = os.path.join(env.cwd, '..', 'notebooks')
    env = nbenv

    def _test_notebook(self, nbname: str):
        # The information on how to do this comes from: http://tritemio.github.io/smbits/2016/01/02/execute-notebooks/
        with open(os.path.join(NotebookTestCase.nbbasedir, nbname)) as nbf:
            nb = nbformat.read(nbf, as_version=4)
        NotebookTestCase.ep.preprocess(nb, dict(metadata=dict(path=NotebookTestCase.nbbasedir)))

        outf = StringIO()
        nbformat.write(nb, outf)
        if self.env.eval_single_file(os.path.join(NotebookTestCase.nbbasedir, nbname), outf.getvalue(), nb_filter,
                                     force_rewrite_comparator) and self.env.fail_on_error:
            with open(nbenv.temp_file_path(nbname), 'w') as actualf:
                actualf.write(outf.getvalue())

    def test_redo_notebooks(self):
        for filename in os.listdir(NotebookTestCase.nbbasedir):
            if not filename.startswith('.') and filename.endswith('.ipynb'):
                print(f"Generating: {filename}")
                self._test_notebook(filename)


if __name__ == '__main__':
    unittest.main()
