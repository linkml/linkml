from rdflib import Graph

from linkml.generators import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator

schema_yaml = """
id: https://examples.org/my-schema
prefixes:
  linkml: https://w3id.org/linkml/
  myschema: https://examples.org/my-schema
imports:
  - linkml:types
default_prefix: myschema
default_range: string

classes:
  MyClass:
    slots:
      - my_slot

slots:
  my_slot:
    range: string
    examples:
      value: "xyz"
"""


def test_retention_of_examples_in_owl():
    """See https://github.com/linkml/linkml/issues/2006"""
    gen = OwlSchemaGenerator(schema_yaml)
    output = gen.serialize()
    # print(output)
    print("\n")

    # Create a graph
    g = Graph()

    # Parse the multi-line Turtle string
    g.parse(data=output, format="turtle")

    # Find any triples where the predicate contains the string "example"
    example_statements = [(subject, predicate, obj) for subject, predicate, obj in g if "example" in predicate]

    # Assert that there is at least one example statement
    assert len(example_statements) > 0, "No statements with 'example' in the predicate were found."


def test_retention_of_examples_in_rdf():
    """See https://github.com/linkml/linkml/issues/2006"""
    gen = RDFGenerator(schema_yaml)
    output = gen.serialize()
    # print(output)
    print("\n")

    # Create a graph
    g = Graph()

    # Parse the multi-line Turtle string
    g.parse(data=output, format="turtle")

    # Find any triples where the predicate contains the string "example"
    example_statements = [(subject, predicate, obj) for subject, predicate, obj in g if "example" in predicate]
    # pprint.pprint(example_statements)

    # Assert that there is at least one example statement
    assert len(example_statements) > 0, "No statements with 'example' in the predicate were found."
