from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from linkml.generators.owlgen import OwlSchemaGenerator

"""
Tests: https://github.com/linkml/linkml/issues/387

Ensure attributes have correct names in OWL
"""


def test_name_mangling(input_path, snapshot):
    infile = input_path("linkml_issue_387.yaml")

    gen = OwlSchemaGenerator(
        infile,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
    )
    output = gen.serialize(mergeimports=False)
    assert output == snapshot("linkml_issue_387.owl")

    g = Graph()
    g.parse(data=output, format="turtle")

    def uri(s) -> URIRef:
        return URIRef(f"https://w3id.org/linkml/examples/test/{s}")

    C1 = uri("C1")
    a = uri("a")
    assert (C1, RDFS.label, Literal("C1")) in g
    assert (C1, RDF.type, OWL.Class) in g
    assert (a, RDFS.label, Literal("a")) in g
    assert (a, RDF.type, OWL.DatatypeProperty) in g
    assert len(list(g.objects(a, RDF.type))) == 1
    assert len(list(g.objects(C1, RDF.type))) == 1
    sv = gen.schemaview
    my_str = sv.get_type("my_str")
    assert my_str.uri == "xsd:string"
    # assert my_str.definition_uri == "https://w3id.org/linkml/examples/test/MyStr"
