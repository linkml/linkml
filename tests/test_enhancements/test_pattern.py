import unittest
from io import StringIO

import yaml

from linkml.generators.pythongen import PythonGenerator
from linkml.utils.schemaloader import SchemaLoader
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python, compile_python
from tests.utils.test_environment import TestEnvironmentTestCase

d1_test = """
device: /dev/tty.Bluetooth-Incoming-Port
label: AbCd0123-1111-FF10-AAF1-A1B2C3D4A1B2C3D4A1B2C3D4
"""


class PatternTestCase(TestEnvironmentTestCase):
    env = env
    testdir = 'issue_pattern'

    def test_pattern_1(self):
        """ Test the pattern ehnancement  """
        file = "pattern_1"
        env.generate_single_file(f'{self.testdir}/{file}.py',
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(f'{self.testdir}/{file}.py')),
                                 value_is_returned=True)
        module = compile_python(env.expected_path(self.testdir, f"{file}.py"))
        d1 = yaml.load(StringIO(d1_test), yaml.loader.SafeLoader)
        dev1 = module.DiskDevice(**d1)
        print("HERE")


if __name__ == '__main__':
    unittest.main()
