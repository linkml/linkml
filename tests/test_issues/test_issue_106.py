import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue106TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_106(self):
        env.generate_single_file('issue_106.py',
                                 lambda: PythonGenerator(env.input_path('issue_106.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_106.py')),
                                 value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
