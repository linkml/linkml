import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class SlotSubclassTestCase(TestEnvironmentTestCase):
    env = env

    @unittest.expectedFailure
    def test_slot_subclass(self):
        """ Test slot domain as superclass of parent """
        env.generate_single_file('issue_56_good.py',
                                 lambda: PythonGenerator(env.input_path('issue_56_good.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_56_good.py')),
                                 value_is_returned=True)

        with self.assertRaises(Exception) as e:
            env.generate_single_file('issue_56_bad.py',
                                     lambda: PythonGenerator(env.input_path('issue_56_bad.yaml')).serialize(),
                                     comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_56.py')),
                                     value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
