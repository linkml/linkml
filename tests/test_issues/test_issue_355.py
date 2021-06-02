import os
import unittest

from jsonasobj2 import as_json

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.yamlutils import YAMLRoot, as_yaml
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python, compile_python
from tests.utils.test_environment import TestEnvironmentTestCase


class ContainedObjectTestCase(TestEnvironmentTestCase):
    env = env

    def test_contained_constructor(self):
        test_name = 'issue_355'
        """ Make sure that types are generated as part of the output """
        env.generate_single_file(f'{test_name}.py',
                                 lambda: PythonGenerator(env.input_path(f'{test_name}.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path(f'{test_name}.py')),
                                 value_is_returned=True)
        module = compile_python(env.expected_path(f'{test_name}.py'))
        c = module.Container(module.Containee('11111', "Glaubner's disease"))
        self.assertEqual('''entry:
  '11111':
    id: '11111'
    value: Glaubner's disease''', as_yaml(c).strip())

        c = module.Container({'22222': dict(id='22222', value='Phrenooscopy')})
        self.assertEqual('''entry:
  '22222':
    id: '22222'
    value: Phrenooscopy''', as_yaml(c).strip())
        alt_object = YAMLRoot()
        alt_object.id = '33333'
        alt_object.value = 'test'
        c = module.Container(alt_object)
        self.assertEqual('''entry:
  '33333':
    id: '33333'
    value: test''', as_yaml(c).strip())
        c = module.Container([dict(id='44444', value="Gracken's curse")])
        self.assertEqual('''entry:
  '44444':
    id: '44444'
    value: Gracken's curse''', as_yaml(c).strip())



if __name__ == '__main__':
    unittest.main()
