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


def test_generation_date_opt_out():
    """``include_generation_date=False`` suppresses the generation_date timestamp triple.

    Regression test for https://github.com/linkml/linkml/issues/3516 (bullet 2): the
    load-time ``generation_date`` stamp is serialized as a data triple in RDF output,
    which defeats byte-stable/reproducible generation. The default still emits it; the
    flag drops it and makes repeated runs identical.
    """
    generation_date = URIRef("https://w3id.org/linkml/generation_date")

    default_graph = Graph()
    default_graph.parse(data=RDFGenerator(schema, mergeimports=False).serialize(), format="turtle")
    assert list(default_graph.triples((None, generation_date, None))), "generation_date should be present by default"

    suppressed = RDFGenerator(schema, mergeimports=False, include_generation_date=False).serialize()
    suppressed_graph = Graph()
    suppressed_graph.parse(data=suppressed, format="turtle")
    assert not list(suppressed_graph.triples((None, generation_date, None))), "generation_date should be suppressed"

    # With the timestamp gone, output is byte-stable across runs.
    rerun = RDFGenerator(schema, mergeimports=False, include_generation_date=False).serialize()
    assert suppressed == rerun


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
