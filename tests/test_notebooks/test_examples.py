import importlib
import os
import re
import unittest
from contextlib import redirect_stdout
from io import StringIO

from tests.test_notebooks import output_directory


class NotebookTests(unittest.TestCase):
    def eval_test(self, target: str, import_module: str) -> None:
        output = StringIO()
        output_file = os.path.join(output_directory, target)
        with redirect_stdout(output):
            importlib.import_module(import_module)
        with open(output_file, 'w') as f:
            f.write(re.sub(r'Generation date: .*?(["\n])', r'Generation date:\1', output.getvalue()))
        print(f"Output written to {output_file}")

    def test_examples(self):
        self.eval_test('examples.txt', "tests.test_notebooks.input.examples")

    def test_inheritence(self):
        self.eval_test('inheritence.txt', "tests.test_notebooks.input.inheritence")

    @unittest.skipIf(True, "Re-enable this once online biolink model is fixed")
    def test_distributed_models(self):
        self.eval_test('distributedmodels.txt', "tests.test_notebooks.input.distributedmodels")


if __name__ == '__main__':
    unittest.main()
