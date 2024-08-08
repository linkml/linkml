import pytest
from rdflib import Graph, URIRef

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator


@pytest.mark.owlgen
@pytest.mark.jsonschemagen
def test_attribute_behavior(input_path, snapshot, snapshot_path):
    """
    Tests: https://github.com/linkml/linkml/issues/388

    Note: this test is currently for exploration, it does not yet do tests beyond ensuring conversion
    generates no errors
    """

    name = "linkml_issue_388"
    schema = input_path(f"{name}.yaml")

    output = YAMLGenerator(schema).serialize()
    assert output == snapshot(f"{name}.yaml")

    output = JsonSchemaGenerator(schema).serialize()
    assert output == snapshot(f"{name}.schema.json")

    output = RDFGenerator(schema).serialize(context=[METAMODEL_CONTEXT_URI])
    assert output == snapshot(f"{name}.ttl")

    output = OwlSchemaGenerator(schema, metaclasses=False).serialize(context=[METAMODEL_CONTEXT_URI])
    assert output == snapshot(f"{name}.owl")

    g = Graph()
    g.parse(snapshot_path(f"{name}.owl"), format="turtle")
    this_a = URIRef("https://example.org/this/a")
    URIRef("https://example.org/other/a")
    # slot_uri refers to two attributes, ambiguous, so minimal metadata;
    assert len(list(g.triples((this_a, None, None)))) == 1
    # assert len(list(g.triples((other_a, None, None)))) > 1
