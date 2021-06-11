import os
import unittest

import yaml
from jsonasobj2 import as_json

from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml.utils.rawloader import load_raw_schema
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, as_yaml
from tests.test_utils.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class YamlUtilTestCase(TestEnvironmentTestCase):
    env = env

    def fix_schema_metadata(self, schema: SchemaDefinition) -> SchemaDefinition:
        self.assertIsNotNone(schema.generation_date)
        schema.source_file = os.path.basename(schema.source_file)
        schema.generation_date = "2018-12-31 17:23"
        self.assertIsNotNone(schema.metamodel_version)
        schema.metamodel_version = "0.5.0"
        self.assertIsNotNone(schema.source_file_size)
        schema.source_file_size = 259
        self.assertIsNotNone(schema.source_file_date)
        schema.source_file_date = "2018-12-31 17:23"
        return schema

    def test_dupcheck_loader(self):
        """ Make sure the duplicate checker finds duplicates """
        with open(env.input_path('yaml1.yaml')) as f:
            y1 = yaml.safe_load(f)
            self.assertEqual(17, y1['f1'])
        with open(env.input_path('yaml1.yaml')) as f:
            with self.assertRaises(ValueError):
                yaml.load(f, DupCheckYamlLoader)
        with open(env.input_path('yaml2.yaml')) as f:
            with self.assertRaises(ValueError):
                yaml.load(f, DupCheckYamlLoader)
        with open(env.input_path('schema1.yaml')) as f:
            s1 = yaml.load(f, DupCheckYamlLoader)
            self.assertEqual('schema1', s1['name'])

    def test_as_json(self):
        schema = self.fix_schema_metadata(load_raw_schema(env.input_path('schema6.yaml')))
        env.eval_single_file(env.expected_path('schema6.json'), as_json(schema), filtr=lambda s: s)

    @unittest.skip("MULTI-Schema test -- re-enable if necessary")
    def test_as_yaml(self):
        """ Test the YAML output representation """
        schema = self.fix_schema_metadata(load_raw_schema(env.input_path('schema4.yaml')))
        env.eval_single_file(env.expected_path('schema4.yaml'), as_yaml(schema), filtr=lambda s: s)

if __name__ == '__main__':
    unittest.main()
