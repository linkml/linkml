import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator

SCHEMA = """
id: https://example.cam/MinRules
name: MinRules

prefixes:
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

classes:
  Animal:
    slots:
      - id
      - name

  Person:
    rules:
      - description: can't have any daughters if you don't have any children
        preconditions:
          slot_conditions:
            daughters_count:
              minimum_value: 2
        postconditions:
          slot_conditions:
            children_count:
              minimum_value: 2
    is_a: Animal
    slots:
      - children_count
      - daughters_count

slots:
    id: {}
    name: {}
    children_count:
      range: integer
    daughters_count:
        range: integer
"""

DATA_INVALID = """
id: "person:1"
name: "John"
daughters_count: 4
children_count: 1
"""

DATA_VALID = """
id: "ssn:1"
name: "John"
children_count: 4
daughters_count: 3
"""


class MinRulesTestCase(unittest.TestCase):

    def test_instantiate_valid(self):
        pygen = PythonGenerator(SCHEMA)
        mod = pygen.compile_module()
        dynamic_class = getattr(mod, "Person")
        person_instance = yaml_loader.load(source=DATA_VALID, target_class=dynamic_class)
        # print(yaml_dumper.dumps(person_instance))
        assert self.assertIsNotNone(person_instance)

    def test_instantiate_invalid(self):
        pygen = PythonGenerator(SCHEMA)
        mod = pygen.compile_module()
        dynamic_class = getattr(mod, "Person")

        validator = JsonSchemaDataValidator(schema=SCHEMA)
        obj = yaml_loader.load(source=DATA_INVALID, target_class=dynamic_class)

        with self.assertRaises(Exception) as context:
            validator.validate_object(obj)
