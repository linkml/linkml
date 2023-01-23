import unittest

from jsonschema.exceptions import ValidationError
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
    slots:
      - id
      - children_count
      - daughters_count
      
  Biosample:
    rules:
      - description: Samples in tubes can't have a plate position. 
            But plate_position currently does have to be asserted as an empty string. 
            Can't be null, None, un-asserted,etc.
            Had wanted to use value_present, but that may not be implemented in the linkml-runtime yet.
        preconditions:
          slot_conditions:
            container_type:
              equals_string: "TUBE"
        postconditions:
          slot_conditions:
            plate_position:
                none_of:
                  pattern: ".+"
      - description: Samples in plates must have a plate position that matches the regex
        preconditions:
          slot_conditions:
            container_type:
              equals_string: "PLATE"
        postconditions:
          slot_conditions:
            plate_position:
              pattern: ^(?!A1|A12|H1|H12)(([A-H][1-9])|([A-H]1[0-2]))$

    slots:
      - id
      - container_type
      - plate_position

slots:
    id: {}
    children_count:
      range: integer
    daughters_count:
      range: integer
    container_type:
      range: ContainerTypeEnum
      required: true
    plate_position:
      range: string
            
enums:
  ContainerTypeEnum:
    permissible_values:
      TUBE: {}
      PLATE: {}
"""

PERSON_VALID = """
id: "person:1"
children_count: 4
daughters_count: 3
"""

PERSON_INVALID = """
id: "person:1"
daughters_count: 4
children_count: 1
"""

TUBE_VALID = """
id: biosample1
container_type: TUBE
plate_position: ""
"""

TUBE_INVALID = """
id: biosample1
container_type: TUBE
plate_position: C3
"""

PLATE_VALID = """
id: biosample1
container_type: PLATE
plate_position: C3
"""

PLATE_INVALID = """
id: biosample1
container_type: PLATE
plate_position: ""
"""


class MinRulesTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.pygen = PythonGenerator(SCHEMA)
        self.mod = self.pygen.compile_module()

    def get_dynclass_validator_object(self, dynamic_class_name, source):
        dynamic_class = getattr(self.mod, dynamic_class_name)
        obj = yaml_loader.load(source=source, target_class=dynamic_class)
        validator = JsonSchemaDataValidator(schema=SCHEMA)
        return dynamic_class, validator, obj

    def run_valid_test(self, class_name, source):
        dynamic_class, validator, obj = self.get_dynclass_validator_object(dynamic_class_name=class_name, source=source)
        validator.validate_object(obj)

    def run_invalid_test(self, class_name, source):
        dynamic_class, validator, obj = self.get_dynclass_validator_object(dynamic_class_name=class_name, source=source)
        with self.assertRaises(ValidationError) as context:
            validator.validate_object(obj)

    def test_instantiate_valid_person(self):
        self.run_valid_test(class_name="Person", source=PERSON_VALID)

    def test_invalid_person_exception_expected(self):
        dynamic_class, validator, obj = self.get_dynclass_validator_object(dynamic_class_name="Person", source=
        PERSON_INVALID)
        print(yaml_dumper.dumps(obj))

        # with self.assertRaises(Exception) as context:
        #     validator.validate_object(person_obj)

    def test_tube_valid(self):
        self.run_valid_test(class_name="Biosample", source=TUBE_VALID)

    def test_tube_invalid(self):
        self.run_invalid_test(class_name="Biosample", source=TUBE_INVALID)

    def test_plate_valid(self):
        self.run_valid_test(class_name="Biosample", source=PLATE_VALID)

    def test_plate_invalid(self):
        self.run_invalid_test(class_name="Biosample", source=PLATE_INVALID)
