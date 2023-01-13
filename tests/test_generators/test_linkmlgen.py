import os
import tempfile
import unittest

import yaml
from linkml_runtime import SchemaView

from linkml.generators.linkmlgen import LinkmlGenerator
from linkml.generators.sssomgen import SSSOMGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
PATTERN_SCHEMA = env.input_path("pattern-example.yaml")
CORE = env.input_path("core.yaml")

class LinkMLGenTestCase(unittest.TestCase):

    def setUp(self):
        self.schemaview = SchemaView(SCHEMA)

    def test_generate(self):
        sv = self.schemaview
        self.assertIn("activity", sv.all_classes(imports=True))
        self.assertNotIn("activity", sv.all_classes(imports=False))
        self.assertListEqual(["is_living"], list(sv.get_class("Person").attributes.keys()))

        gen = LinkmlGenerator(SCHEMA, format='yaml', mergeimports=False)
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
        # self.assertNotIn("attributes", yobj["classes"]["Person"])
        # test with material-attributes option
        gen2 = LinkmlGenerator(SCHEMA, format='yaml', mergeimports=False)
        gen2.materialize_attributes = True
        out2 = gen2.serialize()
        yobj2 = yaml.safe_load(out2)
        self.assertEqual(len(yobj2["classes"]), len(sv.all_classes(imports=False)))
        self.assertIn("attributes", yobj2["classes"]["Person"])
        self.assertNotIn("activity", yobj2["classes"])
        self.assertNotIn("agent", yobj2["classes"])

        # turn on mergeimports option
        gen3 = LinkmlGenerator(SCHEMA, format="yaml", mergeimports=True)
        out3 = gen3.serialize()
        yobj3 = yaml.safe_load(out3)
        self.assertEqual(len(yobj3["classes"]), len(sv.all_classes(imports=True)))
        self.assertIn("activity", yobj3["classes"])
        self.assertIn("agent", yobj3["classes"])

        # test that structured patterns are being expanded
        # and populated into the pattern property on a class
        pattern_gen = LinkmlGenerator(
            PATTERN_SCHEMA,
            materialize_patterns=True,
            format="yaml",
        )

        _, filename = tempfile.mkstemp()
        yaml_filename = filename + ".yaml"
                
        pattern_gen.serialize(output=yaml_filename)
        # log yaml_filename so developers can look at its contents
        self.assertEqual(
            pattern_gen.schemaview.get_slot("id").pattern,
            "^P\d{7}"
        )
        self.assertEqual(
            pattern_gen.schemaview.get_slot("height").pattern,
            "\\d+[\\.\\d+] (centimeter|meter|inch)",
        )
        self.assertEqual(
            pattern_gen.schemaview.get_slot("weight").pattern,
            "\\d+[\\.\\d+] (kg|g|lbs|stone)",
        )
        

if __name__ == "__main__":
    unittest.main()
