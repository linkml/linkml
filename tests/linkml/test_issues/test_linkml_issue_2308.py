from rdflib import Graph
from rdflib.namespace import SKOS

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
      - value: "xyz"
"""


def test_retention_of_examples_in_owl():
    """See https://github.com/linkml/linkml/issues/2308"""
    gen = OwlSchemaGenerator(schema_yaml)
    output = gen.serialize()

    g = Graph()
    g.parse(data=output, format="turtle")

    # Find triples with skos:example predicate
    example_statements = list(g.triples((None, SKOS.example, None)))

    assert len(example_statements) > 0, "No skos:example statements were found."
    # Verify the example value is present
    example_values = [str(obj) for _, _, obj in example_statements]
    assert "xyz" in example_values, f"Expected 'xyz' in examples, got {example_values}"


def test_retention_of_examples_in_rdf():
    """See https://github.com/linkml/linkml/issues/2308"""
    gen = RDFGenerator(schema_yaml)
    output = gen.serialize()

    g = Graph()
    g.parse(data=output, format="turtle")

    # Find triples with skos:example predicate
    example_statements = list(g.triples((None, SKOS.example, None)))

    assert len(example_statements) > 0, "No skos:example statements were found."
    # Verify the example value is present
    example_values = [str(obj) for _, _, obj in example_statements]
    assert "xyz" in example_values, f"Expected 'xyz' in examples, got {example_values}"
