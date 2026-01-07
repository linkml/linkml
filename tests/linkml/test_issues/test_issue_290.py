from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF

from linkml.generators.owlgen import OwlSchemaGenerator


def test_issue_owl(input_path, snapshot):
    """Make sure property characteristics are included"""
    output = OwlSchemaGenerator(input_path("issue_290.yaml")).serialize()
    assert output == snapshot("issue_290.owl")

    g = Graph()
    g.parse(data=output, format="turtle")
    s = URIRef("http://example.org/s")
    t = URIRef("http://example.org/t")
    assert (s, RDF.type, OWL.SymmetricProperty) in g
    assert (s, OWL.inverseOf, t) in g
