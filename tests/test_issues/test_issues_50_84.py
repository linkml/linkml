import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue5084TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_84(self):
        env.generate_single_file('issue_50.py',
                                 lambda: PythonGenerator(env.input_path('issue_50.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_50.py')),
                                 value_is_returned=True)

    def test_issue_50(self):
        env.generate_single_file('issue_84.py',
                                 lambda: PythonGenerator(env.input_path('issue_84.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_84.py')),
                                 value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
