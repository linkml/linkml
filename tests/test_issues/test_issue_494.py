import unittest

from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from linkml.utils.datautils import infer_root_class

from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator
from tests.test_issues.environment import env

SCHEMA = env.input_path('issue_494/slot_usage_example.yaml')
DATA = env.input_path('issue_494/data.yaml')


class JsonSchemaValidatorLocalImport(unittest.TestCase):
    def test_jsonschema_validation(self):
        """Test case that runs the JSON Schema Validator for a schema
           that has a local import and doesn't explicitly specify the
           target class"""        
        sv = SchemaView(schema=SCHEMA)

        # infer target_class rather than explicit specification
        inferred_target_class = infer_root_class(sv)

        # load data.yaml that is to be validated
        obj = yaml_loader.load(source=DATA, target_class=inferred_target_class)

        # create validator object with JSON Schema running behind it
        v = JsonSchemaDataValidator(schema=SCHEMA)
        
        print(f'Validating: {obj}')
        results = v.validate_object(obj)
        print(results)

if __name__ == '__main__':
    unittest.main()
