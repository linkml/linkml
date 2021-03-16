import os
import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue260TestCase(TestEnvironmentTestCase):
    env = env

    def test_local_imports(self):
        """ Check the local import behavior """
        test_dir = 'issue_260'

        # Useful to have an __init__.py available
        init_path = env.actual_path(test_dir, '__init__.py')
        if not os.path.exists(init_path):
            with open(init_path, 'w'):
                pass

        fp = f'{test_dir}/issue_260a.py'
        env.generate_single_file(fp, lambda: PythonGenerator(env.input_path(test_dir, 'issue_260a.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda expected, actual: compare_python(expected, actual, env.expected_path(fp)), value_is_returned=True)
        fp = f'{test_dir}/issue_260b.py'
        env.generate_single_file(fp, lambda: PythonGenerator(env.input_path(test_dir, 'issue_260b.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda expected, actual: compare_python(expected, actual, env.expected_path(fp)), value_is_returned=True)
        fp = f'{test_dir}/issue_260c.py'
        env.generate_single_file(fp, lambda: PythonGenerator(env.input_path(test_dir, 'issue_260c.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda expected, actual: compare_python(expected, actual, env.expected_path(fp)), value_is_returned=True)
        fp = f'{test_dir}/issue_260.py'
        env.generate_single_file(fp, lambda: PythonGenerator(env.input_path(test_dir, 'issue_260.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda expected, actual: compare_python(expected, actual, env.expected_path(fp)), value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
