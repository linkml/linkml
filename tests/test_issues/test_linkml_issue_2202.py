import os
import tempfile
from importlib import util
import io

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import RDFLibDumper
from linkml_runtime.loaders import YAMLLoader
from owlready2 import get_ontology

from linkml.generators import OwlSchemaGenerator, PythonGenerator
from linkml.validator import ValidationReport, Validator

import rdflib

# THIS IS EXPERIMENTATION FOR CHECKING
#   SOME OF NMDC'S VALIDATION EXCEPTIONS

super_household_schema = """
name: super_household_schema
id: http://example.com/super_household_schema

prefixes:
  linkml: https://w3id.org/linkml/
  superhouse: http://example.com/super_household_schema/
  
default_prefix: superhouse
default_range: string

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

super_household_database = """
people:
  - id: superhouse:1
    name: Superman
    has_pet: superhouse:2
  - id: superhouse:3
    name: Batman
pets:
  - id: superhouse:2
    name: Krypto the dog
"""

super_household_view = SchemaView(super_household_schema)

validator_for_household = Validator(super_household_view.schema)


def test_view_created():
    assert type(super_household_view).__name__ == "SchemaView"


def test_minimal_validation():
    report_from_minimal_validation: ValidationReport = validator_for_household.validate(
        super_household_database, "Database"
    )

    assert len(report_from_minimal_validation.results) == 0


def test_minimal_instantiation():
    gen = PythonGenerator(schema=super_household_schema)
    generated_python = gen.serialize()

    # Create a new module
    module_name = "super_household_module"
    spec = util.spec_from_loader(module_name, loader=None)
    super_household_module = util.module_from_spec(spec)

    # Execute the code in the newly created module's namespace
    exec(generated_python, super_household_module.__dict__)  # todo: doesn't linkml have a compile python method?

    Database = getattr(super_household_module, "Database")

    my_loader = YAMLLoader()
    minimal_database = my_loader.load(
        source=super_household_database, target_class=Database, schema_view=super_household_view
    )

    assert minimal_database.people[0].id == "superhouse:1"


def test_convert_data_to_rdf():
    gen = PythonGenerator(schema=super_household_schema)
    generated_python = gen.serialize()

    # Create a new module
    module_name = "super_household_module"
    spec = util.spec_from_loader(module_name, loader=None)
    super_household_module = util.module_from_spec(spec)

    # Execute the code in the newly created module's namespace
    exec(generated_python, super_household_module.__dict__)  # todo: doesn't linkml have a compile python method?

    Database = getattr(super_household_module, "Database")

    my_loader = YAMLLoader()
    minimal_database = my_loader.load(
        source=super_household_database, target_class=Database, schema_view=super_household_view
    )

    my_dumper = RDFLibDumper()
    dumped_rdf = my_dumper.dumps(element=minimal_database, schemaview=super_household_view)
    print("\n")
    print(dumped_rdf)

    # todo assertion # how to test the rdf within python ?


def test_convert_schema_to_owl():
    my_generator = OwlSchemaGenerator(schema=super_household_schema)
    owl_ttl_string = my_generator.serialize()
    print("\n")
    print(len(owl_ttl_string))


# todo useful tests:
#  - person claims to have pet but pet is not defined
#  - person claims to have pet but it is of the wrong type
#  - pet is defined but uses the wrong id pattern (pattern is defined only for pet id)

def test_web():
    print("\n")
    print("hello web")
    onto = get_ontology("https://raw.githubusercontent.com/owlcs/pizza-ontology/master/pizza.owl").load()
    print(list(onto.classes()))


def test_pizza_file():
    print("\n")
    print("hello pizza file")
    # file:///home/mark/Downloads/pizza.owl
    onto = get_ontology("file:///home/mark/Downloads/pizza.owl").load()
    print(list(onto.classes()))


def test_linkml_file():
    my_generator = OwlSchemaGenerator(schema=super_household_schema)
    owl_ttl_string = my_generator.serialize()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttl", mode="w") as tmp:
        tmp.write(owl_ttl_string)

    g = rdflib.Graph()

    # Parse the Turtle file
    g.parse(tmp.name, format='ttl')

    # Serialize the graph to RDF/XML
    rdf_xml_data = g.serialize(format='xml')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".owl", mode="w") as tmp:
        tmp.write(rdf_xml_data)

    onto = get_ontology(tmp.name).load()
    print(list(onto.classes()))
