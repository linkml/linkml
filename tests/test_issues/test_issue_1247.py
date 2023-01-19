import pprint
import unittest

import yaml
from linkml_runtime import SchemaView

from linkml.generators.linkmlgen import LinkmlGenerator

SCHEMA = """
id: https://example.cam/StructPateExp
name: StructPatExp

settings:
  breed_frag: "^breed:"
  flavor_frag: "^flavor:"

classes:
  Person:
    slots:
      - id
      - name
  Pet:
    slots:
      - breed
      
  IceCream:
    slots:
      - flavor
      
slots:
    id:
      pattern: "^person:"
    name: {}
    breed:
      structured_pattern: 
        syntax:
          "{breed_frag}"
    flavor:
      pattern: "^flav:"
      structured_pattern: 
        syntax:
          "{flavor_frag}"
"""

DATA = """
- id: "person:1"
  name: "John"
"""


class StructPatExpTestCase(unittest.TestCase):

    def setUp(self):
        self.schemaview = SchemaView(SCHEMA)

    def test_access_view(self):
        name = self.schemaview.schema.name
        self.assertEqual(name, "StructPatExp")

    def test_generation(self):
        gen = LinkmlGenerator(SCHEMA, format='yaml', materialize_patterns=True)
        serialized_yaml = gen.serialize()
        dict_from_gen = yaml.safe_load(serialized_yaml)

        self.assertEqual(dict_from_gen['slots']['breed']['pattern'], "^breed:")

    def test_asserted_pattern(self):
        gen = LinkmlGenerator(SCHEMA, format='yaml', materialize_patterns=False)
        serialized_yaml = gen.serialize()
        dict_from_gen = yaml.safe_load(serialized_yaml)

        self.assertEqual(dict_from_gen['slots']['flavor']['pattern'], "^flav:")

    def test_struct_overrides_pat(self):
        gen = LinkmlGenerator(SCHEMA, format='yaml', materialize_patterns=True)
        serialized_yaml = gen.serialize()
        dict_from_gen = yaml.safe_load(serialized_yaml)

        # pprint.pprint(dict_from_gen)

        self.assertEqual(dict_from_gen['slots']['flavor']['pattern'], "^flavor:")
