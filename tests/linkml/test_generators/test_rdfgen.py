import pytest
import rdflib
from rdflib import Graph, URIRef

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.rdfgen import RDFGenerator

pytestmark = pytest.mark.xdist_group("rdfgen")

schema = """
id: http://example.org/interval

default_curi_maps:
  - semweb_context

prefixes:
  ex: http://example.org/
  schema: http://schema.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex

classes:

  c:
    annotations:
      - tag: my_tag1
        value: my_value1
      - tag: my_tag2
        value: my_value2
"""

JSONLD = """
{
  "slots": [
    {
      "name": "type",
      "slot_uri": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    }
  ],
  "@context": [
  {
      "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "@vocab": "https://w3id.org/linkml/",
      "slot_uri": {
         "@type": "@id"
      }
    }
  ]
}"""


def test_annotation_extensions():
    """Test that annotation extensions are properly serialized"""
    s = RDFGenerator(schema, mergeimports=False).serialize()
    rdf_graph = Graph()
    rdf_graph.parse(data=s, format="turtle")

    # Query for annotations in the ClassDefinition
    query = """
        SELECT ?example ?tag
        WHERE {
            ex:C linkml:annotations ?annotation .
            ?annotation skos:example ?example .
            ?annotation linkml:tag ?tag .
        }
        """

    results = list(rdf_graph.query(query))

    # Check if there are exactly two annotations
    assert len(results) == 2

    # Check each annotation for the required properties
    for example, tag in results:
        assert isinstance(example, rdflib.Literal)
        assert isinstance(tag, rdflib.URIRef | rdflib.Literal)


@pytest.mark.network
def test_issue_388_attribute_slot_uri_conflicts_stay_disambiguated_in_rdf(input_path):
    generated_rdf = RDFGenerator(input_path("linkml_issue_388.yaml")).serialize(context=[METAMODEL_CONTEXT_URI])
    rdf_graph = Graph()
    rdf_graph.parse(data=generated_rdf, format="turtle")

    for slot in ("c1__a", "c2__a", "c3__a"):
        assert len(list(rdf_graph.triples((URIRef(f"https://example.org/this/{slot}"), None, None)))) > 0


@pytest.mark.skip("TODO")
def test_rdfgen(kitchen_sink_path):
    """rdf"""
    s = RDFGenerator(kitchen_sink_path, mergeimports=False).serialize()
    g = Graph()
    g.parse(data=s, format="turtle")


@pytest.mark.skip("TODO")
def test_rdf_type_in_jsonld(self):
    graph = Graph()
    graph.parse(data=JSONLD, format="json-ld", prefix=True)
    ttl_str = graph.serialize(format="turtle")
    graph.parse(data=ttl_str, format="turtle")


def test_stable_blank_node_labels(input_path):
    """--stable-blank-node-labels relabels blank nodes by content hash, isomorphic to the default.

    The schema-as-RDF contains recursive (cyclic) blank-node structure, so a residue of
    ordinal ``c14n`` labels legitimately remains -- #3704 keeps those for cyclic closures
    (correctness over locality). The assertion is therefore that content-hash labels are
    introduced and the ordinal count strictly drops, not that every ``c14n`` is gone.
    """
    schema = input_path("personinfo.yaml")
    default = RDFGenerator(schema).serialize()
    hashed = RDFGenerator(schema, stable_blank_node_labels=True).serialize()
    assert "_:c14n" in default and "_:b" not in default, "default should use only ordinal c14n labels"
    assert "_:b" in hashed, "opt-in output should introduce content-hash blank-node labels"
    assert hashed.count("_:c14n") < default.count("_:c14n"), "opt-in should relabel blank nodes by hash"
    g_default = Graph().parse(data=default, format="turtle")
    g_hashed = Graph().parse(data=hashed, format="turtle")
    assert rdflib.compare.isomorphic(g_default, g_hashed), "opt-in relabeling changed the graph"
