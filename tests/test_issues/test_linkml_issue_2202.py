from importlib import util

from linkml_runtime import SchemaView
from linkml_runtime.loaders import YAMLLoader

from linkml.generators import PythonGenerator
from linkml.validator import ValidationReport, Validator

# THIS IS EXPERIMENTATION FOR CHECKINS
# # SOME OF NMDC'S VALIDATION EXCEPTIONS
# ASSUMPTIONS ABOUT

minimal_household_schema = """
name: minimal_household_schema
id: http://example.com/minimal_household_schema

prefixes:
  linkml: https://w3id.org/linkml/
    
imports:
  - linkml:types

classes:
  NamedThing:
    slots:
      - id
  Person:
    is_a: NamedThing
    slots:
      - name
  
slots:
  id:
    identifier: true
    range: curie
  name:
    range: string
    required: true
  has_roommate: {}
  has_pet:
  
"""
# todo boilerplate in fixture (could return schemabuidler)
#  each method can use fixture and modify with schemabuilder

minimal_household_data = """
id: http://example.com/minimal_household_schema/1
"""

minimal_view = SchemaView(minimal_household_schema)

validator_for_minimal = Validator(minimal_view.schema)


def test_minimal_view():
    assert minimal_view is not None


def test_minimal_validation():
    report_from_minimal_validation: ValidationReport = validator_for_minimal.validate(
        minimal_household_data, "NamedThing"
    )

    assert len(report_from_minimal_validation.results) == 0


def test_convert_to_rdf():
    gen = PythonGenerator(schema=minimal_household_schema)
    generated_python = gen.serialize()

    # Create a new module
    module_name = "minimal_household_module"
    spec = util.spec_from_loader(module_name, loader=None)
    minimal_household_module = util.module_from_spec(spec)

    # Execute the code in the newly created module's namespace
    exec(generated_python, minimal_household_module.__dict__)  # todo: doesn't linkml have a compile python method?

    # Now you can access the class NamedThing from dynamic_module
    NamedThing = getattr(minimal_household_module, "NamedThing")

    my_loader = YAMLLoader()
    minimal_instance = my_loader.load(source=minimal_household_data, target_class=NamedThing, schema_view=minimal_view)

    assert minimal_instance.id == "http://example.com/minimal_household_schema/1"
