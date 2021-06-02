import os
import unittest

from jsonasobj2 import as_json

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue113TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_113(self):
        """ Make sure that types are generated as part of the output """
        env.generate_single_file('issue_113.py',
                                 lambda: PythonGenerator(env.input_path('issue_113.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, 'issue_113.py'),
                                 value_is_returned=True)
        module = compile_python(env.expected_path('issue_113.py'))
        example = module.TestClass(test_attribute_2="foo")
        assert hasattr(example, "test_attribute_2")
        assert hasattr(example, "test_attribute_1")
        example.wiible = "foo"
        example.test_attribute_1 = "foo"
        example.test_attribute_2 = "foo"

        env.generate_single_file('issue_113.json',
                                 lambda: PythonGenerator(env.input_path('issue_113.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, 'issue_113.py'),
                                 value_is_returned=True)

        def output_generator(dirname) -> None:
            with open(os.path.join(dirname, 'issue_113.json'), 'w') as f:
                f.write(as_json(example))

        env.generate_directory('issue_113', lambda dirname: output_generator(dirname))


if __name__ == '__main__':
    unittest.main()
