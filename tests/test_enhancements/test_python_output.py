import unittest
from typing import Type, List, Tuple

from linkml.generators.pythongen import PythonGenerator
from tests.test_enhancements.environment import env
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.test_environment import TestEnvironmentTestCase


class NonStr:
    def __init__(self, v) -> None:
        self.v = v

    def __str__(self) -> str:
        return self.v


python_types_entries = {
    "Strings": [
        [('s1', 's2', 's3', 's4'), {},
         "Strings(mand_string='s1', mand_multi_string=['s2'], opt_string='s3', opt_multi_string=['s4'])", None],
        [('s1', ['s21', 's22'], 's3', ['s41', 's42']), {},
         "Strings(mand_string='s1', mand_multi_string=['s21', 's22'], opt_string='s3', opt_multi_string=['s41', 's42'])", None],
        [('s1', ['s21', 's22'], None, None), {},
         "Strings(mand_string='s1', mand_multi_string=['s21', 's22'], opt_string=None, opt_multi_string=[])", None],
        [(NonStr('s1'), NonStr('s2'), NonStr('s3'), NonStr('s4')), {},
         "Strings(mand_string='s1', mand_multi_string=['s2'], opt_string='s3', opt_multi_string=['s4'])", None],
        [(NonStr('s1'), [NonStr('s21'), NonStr('s22')], NonStr('s3'), [NonStr('s41'), 's42']), {},
         "Strings(mand_string='s1', mand_multi_string=['s21', 's22'], opt_string='s3', opt_multi_string=['s41', 's42'])", None],
        [(), {}, "mand_string must be supplied", ValueError],
        [('s1',), {}, "mand_multi_string must be supplied", ValueError],
        [('s1',[]), {}, "mand_multi_string must be supplied", ValueError]
    ],
    "Booleans": [
        [('True', "false", 1, [1, 0, True, False]), {},
         "Booleans(mand_boolean=True, mand_multi_boolean=[False], opt_boolean=True, opt_multi_boolean=[True, False, True, False])", None]
    ],
    "Integers": [
        [('17', -2, 12+3, [42, "17"]), {},
         "Integers(mand_integer=17, mand_multi_integer=[-2], opt_integer=15, opt_multi_integer=[42, 17])", None],
        [('17e', 1, 2, 3), {},
         "invalid literal for int() with base 10: '17e'", ValueError]
    ]
}

class PythonOutputTestCase(TestEnvironmentTestCase):
    env = env

    def check_expecteds(self, constructor: Type, check_entries: str) -> None:
        checks = python_types_entries[check_entries]
        for args, argv, expected, err in checks:
            if not err:
                inst = constructor(*args, **argv)
                self.assertEqual(expected, str(inst))
            else:
                with self.assertRaises(err) as e:
                    constructor(*args, **argv)
                self.assertEqual(expected, str(e.exception))

    def test_python_types(self):
        """ description """
        test_dir = 'python_generation'
        test_name = 'python_types'
        python_name = f'{test_dir}/{test_name}.py'

        env.generate_single_file(python_name,
                                 lambda: PythonGenerator(env.input_path(test_dir, f'{test_name}.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda expected, actual: compare_python(expected, actual, env.expected_path(python_name)), value_is_returned=True)

        module = compile_python(env.expected_path(python_name))
        from tests.test_enhancements.output.python_generation.python_types import Strings
        self.check_expecteds(Strings, "Strings")
        self.check_expecteds(module.Strings, "Strings")
        self.check_expecteds(module.Booleans, "Booleans")
        self.check_expecteds(module.Integers, "Integers")


    def test_python_complex_ranges(self):
        """ description """
        test_dir = 'python_generation'
        test_name = 'python_complex_ranges'

        env.generate_single_file(f'{test_dir}/{test_name}.py',
                                 lambda: PythonGenerator(env.input_path(test_dir, f'{test_name}.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(f'{test_dir}/{test_name}.py')),
                                 value_is_returned=True)

    def test_python_lists_and_keys(self):
        """ description """
        test_dir = 'python_generation'
        test_name = 'python_lists_and_keys'
        test_path = f'{test_dir}/{test_name}.py'

        env.generate_single_file(test_path,
                                 lambda: PythonGenerator(env.input_path(test_dir, f'{test_name}.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda expected, actual: compare_python(expected, actual, env.expected_path(test_path)), value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
