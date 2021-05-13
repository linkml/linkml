import os
import unittest

from jsonasobj2 import as_json

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue121TestCase(TestEnvironmentTestCase):
    env = env

    def header(self, txt: str) -> str:
        return '\n' + ("=" * 20) + f" {txt} " + ("=" * 20)

    def test_issue_121(self):
        """ Make sure that types are generated as part of the output """
        env.generate_single_file('issue_121.py',
                                 lambda: PythonGenerator(env.input_path('issue_121.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_121.py')),
                                 value_is_returned=True)
        with open(env.expected_path('issue_121.py')) as f:
            python= f.read()

        has_includes = False
        for line in python.split("\n"):
            if line.startswith("from linkml_runtime.linkml_model.types "):
                assert line == "from linkml_runtime.linkml_model.types import String"
                has_includes = True
        assert has_includes
        module = compile_python(env.expected_path('issue_121.py'))

        example = module.Biosample(depth="test")
        assert hasattr(example, "depth")
        assert example.depth == "test"

        example2 = module.ImportedClass()

        def output_generator(dirname) -> None:
            with open(os.path.join(dirname, 'issue_121_1.json'), 'w') as f:
                f.write(as_json(example))
            with open(os.path.join(dirname, 'issue_121_2.json'), 'w') as f:
                f.write(as_json(example2))

        env.generate_directory('issue_121', lambda dirname: output_generator(dirname))


if __name__ == '__main__':
    unittest.main()
