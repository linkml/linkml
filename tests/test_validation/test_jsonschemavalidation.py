import unittest

from linkml_runtime.loaders import yaml_loader

from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator
from tests.test_validation.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
INSTANCE_DATA_1 = env.input_path("kitchen_sink_inst_01.yaml")
INSTANCE_DATA_2 = env.input_path("kitchen_sink_inst_02.yaml")


class JsonSchemaValidatorTestCase(unittest.TestCase):
    def test_jsonschema_validation(self):
        """Validate data against a LinkML module using a json-schema validator"""
        mod = PythonGenerator(SCHEMA).compile_module()
        obj1 = yaml_loader.load(source=INSTANCE_DATA_1, target_class=mod.Dataset)
        v = JsonSchemaDataValidator(schema=SCHEMA)
        # check that jsonschema_objs dict cache is empty before validate_object()
        # first call
        self.assertIsNone(v.jsonschema_objs)
        v.validate_object(obj1, target_class=mod.Dataset)

        obj2 = yaml_loader.load(source=INSTANCE_DATA_2, target_class=mod.Dataset)
        v.validate_object(obj2, target_class=mod.Dataset)

        # check that the cache store is a dict
        self.assertEqual(type(v.jsonschema_objs), dict)
        # check that the cache store is not empty
        self.assertGreater(len(v.jsonschema_objs.keys()), 0)
        for f, j in v.jsonschema_objs.items():
            # check that cache store keys are of type frozendict()
            self.assertEqual(type(f), frozenset)
            # check that cache store values are dicts
            self.assertEqual(type(j), dict)
            self.assertGreater(len(j.keys()), 0)


if __name__ == "__main__":
    unittest.main()
