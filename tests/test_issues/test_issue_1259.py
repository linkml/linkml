import unittest

from jsonschema.exceptions import ValidationError
from linkml_runtime.loaders import yaml_loader

from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator

SCHEMA = """
name: well_plate
id: http://example.com/well_plate

prefixes:
  well_plate: http://example.com/well_plate/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

classes:
  Biosample:
    rules:
      - description: Samples in plates must have a plate position that matches the regex
        preconditions:
          slot_conditions:
            dna_cont_type:
              equals_string: plate
        postconditions:
          slot_conditions:
            dna_cont_well:
              pattern: ^(?!A1|A12|H1|H12)(([A-H][1-9])|([A-H]1[0-2]))$
      - description: Samples in tubes can't have a plate position.
          But plate_position currently does have to be asserted as an empty string.
          Can't be null, None, un-asserted,etc.
          Had wanted to use value_present, but that may not be implemented in the linkml-runtime yet.
        preconditions:
          slot_conditions:
            dna_cont_type:
              equals_string: tube
        postconditions:
          slot_conditions:
            dna_cont_well:
              none_of:
                pattern: ".+"
    slots:
      - id
      - name
      - dna_cont_type
      - dna_cont_well
  Database:
    slots:
      - biosample_set

slots:
  id: { }
  name: { }
  dna_cont_type:
    examples:
      - value: plate
    range: dna_cont_type_enum
    required: true
  dna_cont_well:
    examples:
      - value: B2
#    pattern: ^(?!A1|A12|H1|H12)(([A-H][1-9])|([A-H]1[0-2]))$
  biosample_set:
    range: Biosample
    multivalued: true
    inlined_as_list: true

enums:
  dna_cont_type_enum:
    permissible_values:
      plate:
        text: plate
      tube:
        text: tube
"""

TUBE_VALID = """
id: biosample1
dna_cont_type: tube
dna_cont_well: ""
"""

TUBE_INVALID = """
id: biosample1
dna_cont_type: tube
dna_cont_well: C3
"""

PLATE_VALID = """
id: biosample1
dna_cont_type: plate
dna_cont_well: C3
"""

PLATE_INVALID = """
id: biosample1
dna_cont_type: plate
dna_cont_well: ""
"""

DATABASED_PLATE_INVALID = """
- id: biosample1
  dna_cont_type: plate
  dna_cont_well: ""
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

    def test_databased_plate_invalid(self):
        self.run_felxible_test(class_name="Biosample", source=DATABASED_PLATE_INVALID, expected_pass=False)
