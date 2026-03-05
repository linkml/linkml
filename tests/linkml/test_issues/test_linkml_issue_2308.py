from rdflib import OWL, RDF, Graph
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

# Schema with multiple examples, description, object, class-level examples,
# and an example that violates its own pattern
schema_yaml_extended = """
id: https://examples.org/extended-schema
prefixes:
  linkml: https://w3id.org/linkml/
  myschema: https://examples.org/extended-schema
imports:
  - linkml:types
default_prefix: myschema
default_range: string

classes:
  SampleClass:
    description: A class with examples
    examples:
      - value: "class-level example"
    slots:
      - multi_example_slot
      - slot_with_description
      - slot_with_object
      - slot_with_pattern

slots:
  multi_example_slot:
    range: string
    examples:
      - value: "first"
      - value: "second"
      - value: "third"

  slot_with_description:
    range: string
    examples:
      - value: "the_value"
        description: "this description is currently ignored by owlgen"

  slot_with_object:
    range: string
    examples:
      - object:
          key1: "val1"
          key2: 42

  slot_with_pattern:
    range: string
    pattern: "^[0-9]+$"
    examples:
      - value: "not_a_number"
        description: "this example violates the pattern — owlgen emits it anyway"
"""


def _owl_graph(schema: str) -> Graph:
    """Generate OWL and parse into an rdflib Graph."""
    gen = OwlSchemaGenerator(schema)
    g = Graph()
    g.parse(data=gen.serialize(), format="turtle")
    return g


def _owl_example_values(schema: str) -> dict[str, list[str]]:
    """Return {subject_uri_str: [example_value_str]} from OWL output."""
    g = _owl_graph(schema)
    result = {}
    for subj, _, obj in g.triples((None, SKOS.example, None)):
        result.setdefault(str(subj), []).append(str(obj))
    return result


def _examples_for(examples: dict[str, list[str]], name_fragment: str) -> list[str]:
    """Find example values for a subject whose URI ends with the given fragment."""
    for uri, vals in examples.items():
        if uri.endswith(name_fragment):
            return vals
    return []


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


def test_multiple_examples_all_emitted():
    """All examples on a slot should produce separate skos:example triples."""
    examples = _owl_example_values(schema_yaml_extended)
    vals = _examples_for(examples, "multi_example_slot")
    assert sorted(vals) == ["first", "second", "third"]


def test_class_level_examples():
    """Examples on classes (not just slots) should also be emitted."""
    examples = _owl_example_values(schema_yaml_extended)
    vals = _examples_for(examples, "SampleClass")
    assert "class-level example" in vals


def test_example_description_not_emitted():
    """The description field on Example is currently ignored — only .value is emitted.

    This test documents the gap. If someone adds description support later,
    this test should be updated to verify the new behavior.
    """
    gen = OwlSchemaGenerator(schema_yaml_extended)
    output = gen.serialize()
    # The description text should NOT appear anywhere in the OWL output
    assert "this description is currently ignored" not in output


def test_example_object_emitted_as_string_repr():
    """Example.object is json.dumps'd with default=str, producing a str() repr.

    For linkml_runtime JsonObj values, this produces something like
    '"JsonObj(key1=\'val1\', key2=42)"' — not valid JSON and not what
    OWL consumers would expect. This test documents the current behavior.
    It may be better to skip .object examples entirely (see PR discussion).
    """
    examples = _owl_example_values(schema_yaml_extended)
    obj_examples = _examples_for(examples, "slot_with_object")
    assert len(obj_examples) == 1
    # The value contains the object's content but in str() repr form
    assert "key1" in obj_examples[0]
    assert "val1" in obj_examples[0]


def test_examples_are_annotations_not_abox():
    """skos:example triples are annotation properties, not OWL individuals.

    This addresses the concern that examples in OWL could create ABox
    individuals that cause satisfiability problems or unintended imports
    when combined with other ontologies.
    """
    g = _owl_graph(schema_yaml_extended)

    # Collect all subjects of skos:example triples
    example_subjects = {subj for subj, _, _ in g.triples((None, SKOS.example, None))}

    for subj in example_subjects:
        # Each subject should be an OWL Class or Property, never an Individual
        types = {obj for _, _, obj in g.triples((subj, RDF.type, None))}
        assert OWL.NamedIndividual not in types, (
            f"{subj} has skos:example and is an OWL NamedIndividual — "
            "examples should be annotations on classes/properties, not on individuals"
        )


def test_invalid_example_still_emitted():
    """Examples that violate their slot's pattern are emitted without validation.

    owlgen does not check examples against slot constraints. This test
    documents that behavior. Upstream linkml#2564 tracks the missing
    validation step.
    """
    examples = _owl_example_values(schema_yaml_extended)
    vals = _examples_for(examples, "slot_with_pattern")
    # "not_a_number" doesn't match pattern "^[0-9]+$" but is emitted anyway
    assert "not_a_number" in vals
