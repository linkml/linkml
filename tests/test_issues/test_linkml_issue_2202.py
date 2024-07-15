from importlib import util

from linkml_runtime import SchemaView
from linkml_runtime.loaders import YAMLLoader

from linkml.generators import PythonGenerator
from linkml.validator import ValidationReport, Validator

# THIS IS EXPERIMENTATION FOR CHECKING
# # SOME OF NMDC'S VALIDATION EXCEPTIONS

minimal_household_schema = """
name: minimal_household_schema
id: http://example.com/minimal_household_schema

prefixes:
  linkml: https://w3id.org/linkml/
  minhouse: http://example.com/minimal_household_schema/
    
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
      - has_relative
      - has_pet
  Pet:
    is_a: NamedThing
    slots:
      - name
  Database:
    slots:
      - people
      - pets
  
slots:
  id:
    identifier: true
    range: curie
  name:
    range: string
    required: true
  has_relative:
    range: Person
  has_pet:
    range: Pet
  people:
    range: Person
    multivalued: true
    inlined_as_list: true
  pets:
    range: Pet
    multivalued: true
    inlined_as_list: true    
  
"""
# todo boilerplate in fixture (could return schemabuidler)
#  each method can use fixture and modify with schemabuilder

minimal_household_database = """
people:
  - id: minhouse:1
    name: Superman
    has_pet: minhouse:2
  - id: minhouse:3
    name: Batman  
pets:
  - id: minhouse:2
    name: Krypto    
"""

minimal_view = SchemaView(minimal_household_schema)

validator_for_minimal = Validator(minimal_view.schema)


def test_view_created():
    assert type(minimal_view).__name__ == "SchemaView"


def test_minimal_validation():
    report_from_minimal_validation: ValidationReport = validator_for_minimal.validate(
        minimal_household_database, "Database"
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

    Database = getattr(minimal_household_module, "Database")

    my_loader = YAMLLoader()
    minimal_database = my_loader.load(source=minimal_household_database, target_class=Database, schema_view=minimal_view)

    assert minimal_database.people[0].id == "minhouse:1"
