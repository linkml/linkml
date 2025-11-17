import pytest
from linkml_runtime.linkml_model import String
from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator

TESTFILE = "linkml_issue_384"

"""
Tests: https://github.com/linkml/linkml/issues/384
"""


def _test_other(name: str, input_path, snapshot) -> None:
    infile = input_path(f"{name}.yaml")

    output = YAMLGenerator(infile).serialize()
    assert output == snapshot(f"{name}.yaml")

    output = ContextGenerator(infile).serialize()
    assert output == snapshot(f"{name}.context.jsonld")

    output = RDFGenerator(infile).serialize(context=[METAMODEL_CONTEXT_URI])
    assert output == snapshot(f"{name}.ttl")

    output = PythonGenerator(infile).serialize()
    assert output == snapshot(f"{name}.py")


def _test_owl(name: str, input_path, snapshot, metaclasses=False, type_objects=False) -> Graph:
    infile = input_path(f"{name}.yaml")
    outpath = f"{name}-{metaclasses}-{type_objects}.owl"

    output = OwlSchemaGenerator(
        infile,
        mergeimports=False,
        add_ols_annotations=True,
        metaclasses=metaclasses,
        type_objects=type_objects,
    ).serialize(mergeimports=False)
    assert output == snapshot(outpath)

    g = Graph()
    g.parse(data=output, format="turtle")
    return g


def _contains_restriction(g: Graph, c: URIRef, prop: URIRef, pred: URIRef, filler: URIRef) -> bool:
    for r in g.objects(c, RDFS.subClassOf):
        if prop in g.objects(r, OWL.onProperty):
            if filler in g.objects(r, pred):
                return True
    return False


@pytest.mark.owlgen
def test_issue_owl_properties(input_path, snapshot):
    def uri(s) -> URIRef:
        return URIRef(f"https://w3id.org/linkml/examples/personinfo/{s}")

    for conf in [
        dict(metaclasses=False, type_objects=False),
        dict(metaclasses=True, type_objects=True),
    ]:
        g = _test_owl(TESTFILE, input_path, snapshot, **conf)
        Thing = uri("Thing")
        Person = uri("Person")
        Organization = uri("Organization")
        parent = uri("parent")
        age = uri("age")
        aliases = uri("aliases")
        classes = [Thing, Person, Organization]
        props = [parent, age]
        # if type_objects=True then the range of slots that are types will be mapped to Object
        # representations of literals
        if conf["type_objects"]:
            string_rep = URIRef(String.type_model_uri)
        else:
            string_rep = XSD.string
        for c in classes:
            assert (c, RDF.type, OWL.Class) in g
        for p in props:
            assert (p, RDF.type, OWL.ObjectProperty) in g
        assert _contains_restriction(g, Person, parent, OWL.allValuesFrom, Person)
        assert _contains_restriction(g, Organization, parent, OWL.allValuesFrom, Organization)
        assert _contains_restriction(g, Person, aliases, OWL.allValuesFrom, string_rep), (
            f"expected {string_rep} for {conf}"
        )
        # TODO: also validate cardinality restrictions
        # assert self._contains_restriction(g, Thing, full_name, OWL.allValuesFrom, string_rep)

    # self.assertIn((A, RDF.type, OWL.Class), g)
    # NAME = URIRef('http://example.org/name')
    # self.assertIn((NAME, RDF.type, OWL.ObjectProperty), g)


@pytest.mark.rdfgen
@pytest.mark.jsonldcontextgen
@pytest.mark.yamlgen
@pytest.mark.pythongen
@pytest.mark.network
def test_other_formats(input_path, snapshot):
    _test_other(TESTFILE, input_path, snapshot)
