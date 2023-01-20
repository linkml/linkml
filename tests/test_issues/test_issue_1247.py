import unittest

import yaml
from jsonschema.exceptions import ValidationError
from linkml_runtime import SchemaView
from linkml_runtime.loaders import yaml_loader

from linkml.generators.linkmlgen import LinkmlGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator

SCHEMA = """
id: https://example.cam/StructPateExp
name: StructPatExp

prefixes:
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

settings:
  flavor_frag: "^flavor:"
  ssn_frag: "^ssn:"

classes:
  Animal:
    slots:
      - id
      - name
      
  Person:
    is_a: Animal
    slot_usage:
      id:
        structured_pattern:
          syntax: "{ssn_frag}"
      
  IceCream:
    slots:
      - flavor
      
slots:
    id:
      pattern: "^person:"
    name: {}
    flavor:
      pattern: "^flav:"
      structured_pattern: 
        syntax:
          "{flavor_frag}"
"""

DATA_INVALID = """
id: "person:1"
name: "John"
"""

DATA_VALID = """
id: "ssn:1"
name: "John"
"""


class StructPatExpTestCase(unittest.TestCase):

    def test_asserted_pattern(self):
        # with materialize_patterns=False, we should get the ASSERTED pattern
        # on ['slots']['flavor']['pattern'] of "^flav:"
        gen = LinkmlGenerator(SCHEMA, format='yaml', materialize_patterns=False)
        serialized_yaml = gen.serialize()
        dict_from_gen = yaml.safe_load(serialized_yaml)

        self.assertEqual(dict_from_gen['slots']['flavor']['pattern'], "^flav:")

    def test_struct_overrides_pat(self):
        # with materialize_patterns=True, we should override the ASSERTED pattern
        # and get the MATERIALIZED pattern
        # on ['slots']['flavor']['pattern'] of "^flavor:"
        gen = LinkmlGenerator(SCHEMA, format='yaml', materialize_patterns=True)
        serialized_yaml = gen.serialize()
        dict_from_gen = yaml.safe_load(serialized_yaml)

        self.assertEqual(dict_from_gen['slots']['flavor']['pattern'], "^flavor:")

    def test_pat_from_usage(self):
        # does the structured pattern get materialized when it comes via slot_usage?
        gen = LinkmlGenerator(SCHEMA, format='yaml', materialize_patterns=True)
        serialized_yaml = gen.serialize()

        # abruptly switch from examining a dict to recreating a SchemaView
        # from the generated YAML

        sv_from_materialized = SchemaView(serialized_yaml)

        self.assertEqual(sv_from_materialized.induced_class('Person').attributes['id'].pattern, "^ssn:")

    def test_valid_person_data(self):
        # actually validate some data against the schema

        gen = LinkmlGenerator(SCHEMA, format='yaml', materialize_patterns=True)
        serialized_yaml = gen.serialize()

        v = JsonSchemaDataValidator(serialized_yaml)

        mod = PythonGenerator(SCHEMA).compile_module()

        person_obj = yaml_loader.load(source=DATA_VALID, target_class=mod.Person)
        v.validate_object(person_obj)

        self.assertTrue(True)

    def test_invalid_person_data(self):
        gen = LinkmlGenerator(SCHEMA, format='yaml', materialize_patterns=True)
        serialized_yaml = gen.serialize()

        v = JsonSchemaDataValidator(serialized_yaml)

        mod = PythonGenerator(SCHEMA).compile_module()

        person_obj = yaml_loader.load(source=DATA_INVALID, target_class=mod.Person)

        with self.assertRaises(ValidationError):
            v.validate_object(person_obj)
