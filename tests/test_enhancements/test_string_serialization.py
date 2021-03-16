import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_enhancements.environment import env
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class StringSerializationTestCase(TestEnvironmentTestCase):
    env = env
    testdir = 'string_serialization'

    def test_simple_example(self):
        """ Test evidence enumeration  """
        file = "simple_example"
        env.generate_single_file(f'{self.testdir}/{file}.py',
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(f'{self.testdir}/{file}.py')),
                                 value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
