import json
import unittest

import jsonasobj
import jsonschema
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

data_str = """
contains:
 - label: n1
   type:
     label: foo type
     system: bar system
 - label: n2
   type:
     label: foo type
     system: bar system
"""



class IssueJSONSchemaInlinedAsDictCase(TestEnvironmentTestCase):
    env = env

    def test_inlined(self):
        """ Ensure that inlined lists without identifiers work """
        gen = PythonGenerator(env.input_path('linkml_issue_463.yaml'))
        pystr = gen.serialize()
        #print(pystr)
        with open(env.expected_path('linkml_issue_463.py'), 'w') as stream:
            stream.write(pystr)
        module = compile_python(pystr)
        # test: construction via objects using append
        type_obj = module.TypeObj(label='foo type', system='bar system')
        contained = module.Contained(label='n1', type=type_obj)
        container = module.Container(contains=[])
        container.contains.append(contained)
        # TODO: this currently yields "TypeError: unhashable type: 'TypeObj'"
        obj = yaml_loader.loads(data_str, target_class=module.Container)


if __name__ == '__main__':
    unittest.main()
