import json

import pytest
import yaml
from rdflib import Graph, URIRef

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator

pytestmark = [pytest.mark.owlgen, pytest.mark.jsonschemagen, pytest.mark.network]


def test_attribute_slot_uri_conflicts_stay_disambiguated(input_path):
    """Ambiguous attribute URIs should keep minimal shared metadata."""
    schema = input_path("linkml_issue_388.yaml")

    generated_yaml = yaml.safe_load(YAMLGenerator(schema).serialize())
    assert set(generated_yaml["slots"]) == {"c1__a", "c2__a", "c3__a"}
    assert generated_yaml["slots"]["c3__a"]["slot_uri"] == "other:a"

    generated_schema = json.loads(JsonSchemaGenerator(schema).serialize())
    assert generated_schema["$defs"]["C1"]["properties"]["a"]["type"] == ["string", "null"]
    assert generated_schema["$defs"]["C2"]["properties"]["a"]["type"] == ["integer", "null"]
    assert generated_schema["$defs"]["C3"]["properties"]["a"]["anyOf"][0]["$ref"] == "#/$defs/C1"

    generated_rdf = RDFGenerator(schema).serialize(context=[METAMODEL_CONTEXT_URI])
    rdf_graph = Graph()
    rdf_graph.parse(data=generated_rdf, format="turtle")
    for slot in ("c1__a", "c2__a", "c3__a"):
        assert len(list(rdf_graph.triples((URIRef(f"https://example.org/this/{slot}"), None, None)))) > 0

    generated_owl = OwlSchemaGenerator(
        schema,
        metaclasses=False,
        skip_vacuous_min_zero_cardinality_axioms=False,
        skip_vacuous_local_range_axioms=False,
        consolidate_cardinality_axioms=False,
    ).serialize(context=[METAMODEL_CONTEXT_URI])

    owl_graph = Graph()
    owl_graph.parse(data=generated_owl, format="turtle")
    this_a = URIRef("https://example.org/this/a")
    assert len(list(owl_graph.triples((this_a, None, None)))) == 1
