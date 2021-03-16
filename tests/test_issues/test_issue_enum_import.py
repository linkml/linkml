import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class EnumImportTestCase(TestEnvironmentTestCase):
    env = env
    directory = 'issue_enum_import'

    def test_enum_import(self):
        """ Enum reference isn't getting merged on module import  """
        # env.generate_single_file('file1.py',
        #                          lambda: PythonGenerator(env.input_path(self.directory, 'file1.yaml'),
        #                                                  mergeimports=True).serialize(),
        #                          comparator=lambda exp, act: compare_python(exp, act, env.expected_path(self.directory, 'file1.py')),
        #                          value_is_returned=True)
        env.generate_single_file('file2.py',
                                 lambda: PythonGenerator(env.input_path(self.directory, 'file2.yaml'),
                                                         mergeimports=True).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, env.expected_path(self.directory, 'file2.py')),
                                 value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
