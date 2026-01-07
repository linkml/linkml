import pytest
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import SKOS

from linkml.generators.rdfgen import JSONLDGenerator, RDFGenerator

BIOLINK = Namespace("https://w3id.org/biolink/vocab/")

# as reported in https://github.com/linkml/linkml/issues/163,
# rdfgenerator can create unparsable files if ttl is used.
# TODO: make this test work when format = 'ttl'
RDF_FORMAT = "ttl"


# Tests: https://github.com/linkml/linkml/issues/163


@pytest.mark.network
def test_roundtrip(input_path, tmp_path):
    name = "linkml_issue_163"
    inpath = input_path(f"{name}.yaml")
    outpath = str(tmp_path / f"{name}-gen.{RDF_FORMAT}")
    gen = RDFGenerator(inpath, format=RDF_FORMAT)
    gen.serialize(output=outpath)
    g = Graph()
    g.parse(outpath, format=RDF_FORMAT)


@pytest.mark.skip("skipping until https://github.com/linkml/linkml/issues/163 is fixed")
def test_namespace(input_path):
    name = "linkml_issue_163"
    inpath = input_path(f"{name}.yaml")

    gen = JSONLDGenerator(inpath, metadata=True, importmap={})
    jsonld_str = gen.serialize()

    nsl = gen.namespaces
    # namespaces directly declared
    assert nsl["RO"] == "http://purl.obolibrary.org/obo/RO_"
    assert nsl["biolink"] == "https://w3id.org/biolink/vocab/"
    assert nsl["linkml"] == "https://w3id.org/linkml/"
    assert nsl["SIO"] == "http://semanticscience.org/resource/SIO_"
    assert nsl["prov"] == "http://www.w3.org/ns/prov#"

    # from OBO context
    assert nsl["SO"] == "http://purl.obolibrary.org/obo/SO_"

    # from semweb
    assert nsl["rdf"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    assert nsl["owl"] == "http://www.w3.org/2002/07/owl#"

    graph = Graph()
    graph.parse(
        data=jsonld_str,
        format="json-ld",
        base=str(gen.namespaces._base),
        prefix=True,
    )


@pytest.mark.skip("skipping until https://github.com/linkml/linkml/issues/163 is fixed")
def test_issue_mappings_namespace(input_path, snapshot):
    """Make sure that types are generated as part of the output"""
    name = "linkml_issue_163"
    path = f"{name}.{RDF_FORMAT}"
    output = RDFGenerator(input_path(f"{name}.yaml"), format=RDF_FORMAT).serialize()
    assert output == snapshot(path)

    g = Graph()
    g.parse(data=output, format=RDF_FORMAT)

    HAS_EVIDENCE = BIOLINK.has_evidence
    SNV = BIOLINK.Snv
    NAME = BIOLINK.name
    assert (
        HAS_EVIDENCE,
        SKOS.exactMatch,
        URIRef("http://purl.obolibrary.org/obo/RO_0002558"),
    ) in g
    assert (
        SNV,
        SKOS.exactMatch,
        URIRef("http://example.org/UNKNOWN/UNKNOWN_PREFIX/1234567"),
    ) in g
    assert (SNV, SKOS.exactMatch, URIRef("http://purl.obolibrary.org/obo/SO_0001483")) in g
    assert (NAME, SKOS.narrowMatch, URIRef("http://purl.org/dc/terms/title")) in g
