import pytest
from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator


def test_issue_owl_namespace(input_path, snapshot):
    """Make sure that types are generated as part of the output"""
    output = OwlSchemaGenerator(input_path("issue_163.yaml")).serialize()
    expected = snapshot("issue_163.owl")
    assert output == expected

    g = Graph().parse(expected.path, format="turtle")
    A = URIRef("http://example.org/A")
    assert (A, RDF.type, OWL.Class) in g
    NAME = URIRef("http://example.org/name")
    assert (NAME, RDF.type, OWL.ObjectProperty) in g


def test_issue_no_default(input_path, snapshot):
    """Make sure that types are generated as part of the output"""
    output = OwlSchemaGenerator(input_path("issue_163b.yaml")).serialize()
    expected = snapshot("issue_163b.owl")
    assert output == expected

    g = Graph().parse(expected.path, format="turtle")
    A = URIRef("http://example.org/sample/example1/A")
    assert (A, RDF.type, OWL.Class) in g
    NAME = URIRef("http://example.org/sample/example1/name")
    assert (NAME, RDF.type, OWL.ObjectProperty) in g


def test_aliases(input_path, snapshot):
    """Make sure aliases work"""
    output = OwlSchemaGenerator(input_path("issue_163c.yaml")).serialize()
    assert output == snapshot("issue_163c.owl")


@pytest.mark.network
def test_issue_genrdf_exact_mappings(input_path, snapshot):
    """Make sure that exact_mappings curies are correctly converted in rdfgen"""
    output = RDFGenerator(input_path("issue_163d.yaml")).serialize()
    expected = snapshot("issue_163d.ttl")
    assert output == expected
