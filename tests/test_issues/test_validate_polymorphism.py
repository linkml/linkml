import  unittest

from linkml.generators.pythongen import PythonGenerator

from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase
from linkml_runtime.utils.compile_python import compile_python
from linkml.validators import JsonSchemaDataValidator
from linkml_runtime.utils.schemaview import SchemaDefinition, SchemaView
from .test_pydantic_polymorphism import data_str, schema_str
import json

class PydanticPolymorphismTestCase(TestEnvironmentTestCase):
    env = env

    def test_pythongenerator_loads_poly(self):
        gen = PythonGenerator(schema_str)
        output = gen.serialize()
        mod = compile_python(output, "testschema")
        json_data = json.loads(data_str)
        cont = mod.Container(**json_data)
        self.assertEquals(len([x for x in cont.things if type(x) == mod.Person]),1)
        self.assertEquals(len([x for x in cont.things if type(x) == mod.Organisation]),1)
        
    def test_jsonschema_validates_poly(self):
        sv = SchemaView(schema_str)
        j = JsonSchemaDataValidator(sv.schema)
        json_data = json.loads(data_str)
        errs = j.validate_dict(json_data)
        self.assertIsNone(errs)


