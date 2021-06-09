import unittest

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.yamlutils import from_yaml
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_enhancements.environment import env


class TemplateTestCase(TestEnvironmentTestCase):
    env = env
    testdir = 'string_template'

    @unittest.skip("Need update to linkml-model and supporting software first")
    def test_template_basics(self):
        """ Test the basics of a string template  """
        file = "templated_classes"
        env.generate_single_file(f'{self.testdir}/{file}.py',
                                 lambda: PythonGenerator(env.input_path(self.testdir, f'{file}.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(
                                     f'{self.testdir}/{file}.py')),
                                 value_is_returned=True)
        module = compile_python(env.expected_path(self.testdir, f"{file}.py"))
        inst = module.FirstClass("Sam Sneed", 42, "Male")
        self.assertEqual('Sam Sneed - a 42 year old Male', str(inst))
        inst2 = module.FirstClass.parse("Jillian Johnson - a 93 year old female")
        self.assertEqual("FirstClass(name='Jillian Johnson', age=93, gender='female')", repr(inst2))
        self.assertEqual('Jillian Johnson - a 93 year old female', str(inst2))
        with open(env.input_path(self.testdir, 'jones.yaml')) as yf:
            inst3 = from_yaml(yf, module.FirstClass)
        self.assertEqual('Freddy Buster Jones - a 11 year old Undetermined', str(inst3))


if __name__ == '__main__':
    unittest.main()
