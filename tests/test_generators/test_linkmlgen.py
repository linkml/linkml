import os
import unittest

import yaml
from linkml_runtime import SchemaView

from linkml.generators.linkmlgen import LinkmlGenerator
from linkml.generators.sssomgen import SSSOMGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
CORE = env.input_path("core.yaml")

class LinkMLGenTestCase(unittest.TestCase):

    def setUp(self):
        self.schemaview = SchemaView(SCHEMA)

    def test_generate(self):
        sv = self.schemaview
        self.assertIn("activity", sv.all_classes(imports=True))
        self.assertNotIn("activity", sv.all_classes(imports=False))
        self.assertEqual([], list(sv.get_class("Person").attributes.keys()))

        gen = LinkmlGenerator(SCHEMA, format='yaml')
        out = gen.serialize()
        # TODO: restore this when imports works for string inputs
        #schema2 = YAMLGenerator(out).schema
        #sv2 = SchemaView(schema2)
        #self.assertEqual(len(sv2.all_classes(imports=False)), len(sv.all_classes(imports=False)))
        #self.assertIn("activity", sv2.all_classes(imports=True))
        #self.assertNotIn("activity", sv2.all_classes(imports=False))
        #self.assertEqual([], list(sv2.get_class("Person").attributes.keys()))

        yobj = yaml.safe_load(out)
        self.assertEqual(len(yobj["classes"]), len(sv.all_classes(imports=False)))
        self.assertNotIn("attributes", yobj["classes"]["Person"])
        # test with material-attributes option
        gen2 = LinkmlGenerator(SCHEMA, format='yaml')
        gen2.materialize_attributes = True
        out2 = gen2.serialize()
        yobj2 = yaml.safe_load(out2)
        self.assertEqual(len(yobj2["classes"]), len(sv.all_classes(imports=False)))
        self.assertIn("attributes", yobj2["classes"]["Person"])

if __name__ == "__main__":
    unittest.main()
