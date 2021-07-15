import logging
import unittest
from typing import Union, List

from linkml.generators.pythongen import PythonGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.test_enhancements.environment import env
from tests.utils.filters import yaml_filter
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.test_environment import TestEnvironmentTestCase


class EnumerationTestCase(TestEnvironmentTestCase):
    env = env
    testdir = 'enumeration'

    def _check_error(self, file: str, error: str) -> None:
        with self.assertRaises(ValueError, msg=error) as e:
            YAMLGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                          mergeimports=False, log_level=logging.INFO).serialize(validateonly=True)
        # print(str(e.exception))
        self.assertIn(error, str(e.exception), error)

    def _check_warns(self, file: str, msgs: Union[str, List[str]]) -> None:
        with self.redirect_logstream() as logger:
            YAMLGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                          mergeimports=False, log_level=logging.INFO, logger=logger).serialize(validateonly=True)
        for msg in msgs if isinstance(msgs, list) else [msgs]:
            self.assertIn(msg, logger.result, msg)


    def test_evidence(self):
        """ Test evidence enumeration  """
        file = "evidence"
        env.generate_single_file(f'{self.testdir}/{file}.py',
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(f'{self.testdir}/{file}.py')),
                                 value_is_returned=True)

    def test_enum_constraints(self):
        """ Test the various enum constraints """
        self._check_error("enum_name_error", '":" not allowed in identifier')

        self._check_error("enum_class_name_error", "Overlapping enum and class names: test1, test2")

        self._check_error("enum_type_name_error", "Overlapping type and enum names: test2")

        self._check_warns("enum_name_overlaps", ['Overlapping subset and slot names: a random name',
                                                 'Overlapping enum and slot names: a random name, a slot',
                                                 'Overlapping subset and enum names: a random name, a subset'])

    def test_enum_errors(self):
        """ Test the other invariants """
        self._check_error("enum_error_1", 'Enum: "error1" needs a code set to have a version')

        self._check_error("enum_error_2", 'Enum: "error2" cannot have both version and tag')

        self._check_error("enum_error_3", 'Enum: "error3" needs a code set to have a tag')

        self._check_error("enum_error_4", 'Enum: "error4" needs a code set to have a formula')

        self._check_error("enum_error_5", 'Enum: "error5" can have a formula or permissible values but not both')

        self._check_error("enum_error_6a", 'Slot: "classError1__slot_1" enumerations cannot be inlined')

        self._check_error("enum_error_6b", 'Slot: "classError1__slot_1" enumerations cannot be inlined')

        self._check_error("enum_error_7", 'Unknown PvFormulaOptions enumeration code: LABEL')

    @unittest.skipIf(True, "Enable this when we get the emitter updated to include the location of the error")
    def test_enum_valueerror(self):
        """ Make sure that the link to the error is included in the output """
        self._check_error("enum_error_7", 'alternatives.yaml", line ')

    def test_enum_alternatives(self):
        """ test various variants on enum constraints """
        file = "alternatives"
        env.generate_single_file(env.expected_path(self.testdir, f'{file}.yaml'),
                                 lambda: YAMLGenerator(env.input_path(self.testdir, f'{file}.yaml')).serialize(),
                                 filtr=yaml_filter, value_is_returned=True)

        python_name = f'{self.testdir}/{file}.py'
        YAMLGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                      mergeimports=False, log_level=logging.INFO).serialize()
        env.generate_single_file(python_name,
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(python_name)),
                                 value_is_returned=True)

        module = compile_python(env.expected_path(python_name))

    def test_notebook_model_1(self):
        file = 'notebook_model_1'
        python_name = f'{self.testdir}/{file}.py'
        env.generate_single_file(python_name,
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False,
                                                         gen_classvars=False, gen_slots=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(python_name)),
                                 value_is_returned=True)

        module = compile_python(env.expected_path(python_name))
        c1 = module.PositionalRecord('my location', 'a')
        self.assertEqual("PositionalRecord(id='my location', position=(text='a', description='top'))", str(c1))
        self.assertEqual("a", str(c1.position))
        self.assertEqual("(text='a', description='top')", repr(c1.position))
        try:
            c2 = module.PositionalRecord('your location', 'z')
        except ValueError as e:
            self.assertEqual("Unknown OpenEnum enumeration code: z", str(e))
        x = module.PositionalRecord("117493", "c")
        self.assertEqual('c', str(x.position))
        self.assertEqual("PositionalRecord(id='117493', position=(text='c', description='bottom'))", repr(x))
        self.assertEqual("(text='c', description='bottom')", repr(x.position))

    def test_notebook_model_2(self):
        file = 'notebook_model_2'
        python_name = f'{self.testdir}/{file}.py'
        env.generate_single_file(python_name,
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False,
                                                         gen_classvars=False, gen_slots=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(python_name)),
                                 value_is_returned=True)

        module = compile_python(env.expected_path(python_name))
        t = module.Sample("Something", [module.UnusualEnumPatterns.M, module.UnusualEnumPatterns['% ! -- whoo']])
        print(str(t))

    def test_notebook_model_3(self):
        file = 'notebook_model_3'
        python_name = f'{self.testdir}/{file}.py'
        env.generate_single_file(python_name,
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False,
                                                         gen_classvars=False, gen_slots=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(python_name)),
                                 value_is_returned=True)

        module = compile_python(env.expected_path(python_name))
        colorrec = module.FavoriteColor("Harold", module.Colors['2'])
        print(colorrec)
        print(str(colorrec.position))
        print(colorrec.position.meaning)
        cr2 = module.FavoriteColor("Donald", module.Colors['4'])
        print(cr2.position.meaning)

    def test_notebook_model_4(self):
        file = 'notebook_model_4'
        python_name = f'{self.testdir}/{file}.py'
        env.generate_single_file(python_name,
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False,
                                                         gen_classvars=False, gen_slots=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(python_name)),
                                 value_is_returned=True)

        module = compile_python(env.expected_path(python_name))
        colorrec = module.FavoriteColor("Harold", module.Colors['2'])
        print(colorrec)
        print(str(colorrec.position))
        print(colorrec.position.meaning)
        cr2 = module.FavoriteColor("Donald", module.Colors['4'])
        print(cr2.position.meaning)


if __name__ == '__main__':
    unittest.main()
