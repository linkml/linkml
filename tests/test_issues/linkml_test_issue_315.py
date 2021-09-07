import os
import unittest

from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.yamlgen import YAMLGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.loaders import yaml_loader
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

# Tests: https://github.com/linkml/linkml/issues/314
class Issue314TestCase(TestEnvironmentTestCase):
    env = env

    def test_keyval(self):
        name = 'linkml_issue_315'
        inpath = env.input_path(f'{name}.yaml')
        gen = PythonGenerator(inpath, mergeimports=True)
        pstr = str(gen.serialize())
        mod = compile_python(pstr)
        d1 = mod.Container(word_mappings={'hand': 'manus'})
        print(d1)
        assert d1.word_mappings['hand'] == mod.WordMapping(src='hand', tgt='manus')
        obj = yaml_loader.load(env.input_path(f'{name}_data.yaml'), target_class=mod.Container)
        print(obj)
        assert obj.word_mappings['foot'] == mod.WordMapping(src='foot', tgt='pes')





if __name__ == '__main__':
    unittest.main()
