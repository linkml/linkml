import rdflib

from linkml.generators.shaclgen import ShaclGenerator

EXPECTED = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
        rdflib.term.URIRef("http://www.w3.org/ns/shacl#NodeShape"),
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.URIRef("http://www.w3.org/ns/shacl#closed"),
        rdflib.term.Literal(
            "true", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#boolean")
        ),
    ),
]


def test_shacl(kitchen_sink_path):
    """tests shacl generation"""
    shaclstr = ShaclGenerator(kitchen_sink_path, mergeimports=True).serialize()
    g = rdflib.Graph()
    g.parse(data=shaclstr)
    triples = list(g.triples((None, None, None)))
    for et in EXPECTED:
        assert et in triples
    # TODO: test shacl validation; pyshacl requires rdflib6
