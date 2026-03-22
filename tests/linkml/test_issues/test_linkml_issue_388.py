import pytest
from rdflib import Graph, URIRef

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator


@pytest.mark.owlgen
@pytest.mark.jsonschemagen
@pytest.mark.network
def test_attribute_behavior(input_path, snapshot, bundled_snapshot_text):
    """
    Tests: https://github.com/linkml/linkml/issues/388

    Note: this test is currently for exploration, it does not yet do tests beyond ensuring conversion
    generates no errors
    """

    name = "linkml_issue_388"
    schema = input_path(f"{name}.yaml")
    outputs: dict[str, str] = {}

    output = YAMLGenerator(schema).serialize()
    outputs[f"{name}.yaml"] = output

    output = JsonSchemaGenerator(schema).serialize()
    outputs[f"{name}.schema.json"] = output

    output = RDFGenerator(schema).serialize(context=[METAMODEL_CONTEXT_URI])
    outputs[f"{name}.ttl"] = output

    output = OwlSchemaGenerator(schema, metaclasses=False).serialize(context=[METAMODEL_CONTEXT_URI])
    outputs[f"{name}.owl"] = output

    assert bundled_snapshot_text(outputs) == snapshot(f"{name}.txt")

    g = Graph()
    g.parse(data=output, format="turtle")
    this_a = URIRef("https://example.org/this/a")
    URIRef("https://example.org/other/a")
    # slot_uri refers to two attributes, ambiguous, so minimal metadata;
    assert len(list(g.triples((this_a, None, None)))) == 1
    # assert len(list(g.triples((other_a, None, None)))) > 1
