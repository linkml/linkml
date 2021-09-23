import unittest

from linkml_runtime.loaders import json_loader, yaml_loader
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator
from tests.test_validation.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
DATA = env.input_path('kitchen_sink_inst_01.yaml')




class JsonSchemaValidatorTestCase(unittest.TestCase):

    def test_jsonschema_validation(self):
        """ Validate data against a LinkML module using a json-schema validator  """
        print(f'TEST: Loading {SCHEMA}')
        mod = PythonGenerator(SCHEMA).compile_module()
        obj = yaml_loader.load(source=DATA,  target_class=mod.Dataset)
        #schema = SchemaView(SCHEMA).schema
        v = JsonSchemaDataValidator(schema=SCHEMA)
        print(f'Validating: {obj}')
        results = v.validate_object(obj)
        print(results)

if __name__ == '__main__':
    unittest.main()
