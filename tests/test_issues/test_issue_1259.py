import unittest

from jsonschema.exceptions import ValidationError
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
    container_type:
      range: ContainerTypeEnum
      required: true
    plate_position:
      range: string
    plate_height_mm:
      range: float
            
enums:
  ContainerTypeEnum:
    permissible_values:
      TUBE: {}
      PLATE: {}
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

    def run_felxible_test(self, class_name, source, expected_pass=True):
        dynamic_class, validator, obj = self.get_dynclass_validator_object(dynamic_class_name=class_name, source=source)

        if expected_pass:
            validator.validate_object(obj)
        else:
            with self.assertRaises(ValidationError) as context:
                validator.validate_object(obj)

    def test_tube_valid(self):
        self.run_felxible_test(class_name="Biosample", source=TUBE_VALID, expected_pass=True)

    def test_tube_invalid(self):
        self.run_felxible_test(class_name="Biosample", source=TUBE_INVALID, expected_pass=False)

    def test_plate_valid(self):
        self.run_felxible_test(class_name="Biosample", source=PLATE_VALID, expected_pass=True)

    def test_plate_invalid(self):
        self.run_felxible_test(class_name="Biosample", source=PLATE_INVALID, expected_pass=False)
