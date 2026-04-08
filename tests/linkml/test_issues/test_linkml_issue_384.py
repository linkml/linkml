import pytest
from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml_runtime.linkml_model import String

TESTFILE = "linkml_issue_384"

"""
Tests: https://github.com/linkml/linkml/issues/384
"""


def _other_outputs(name: str, input_path) -> dict[str, str]:
    infile = input_path(f"{name}.yaml")
    outputs: dict[str, str] = {}

    output = YAMLGenerator(infile).serialize()
    outputs[f"{name}.yaml"] = output

    output = ContextGenerator(infile).serialize()
    outputs[f"{name}.context.jsonld"] = output

    output = RDFGenerator(infile).serialize(context=[METAMODEL_CONTEXT_URI])
    outputs[f"{name}.ttl"] = output

    output = PythonGenerator(infile).serialize()
    outputs[f"{name}.py"] = output

    return outputs


def _test_owl(name: str, input_path, metaclasses=False, type_objects=False) -> tuple[Graph, str, str]:
    infile = input_path(f"{name}.yaml")
    outpath = f"{name}-{metaclasses}-{type_objects}.owl"

    output = OwlSchemaGenerator(
        infile,
        mergeimports=False,
        add_ols_annotations=True,
        metaclasses=metaclasses,
        type_objects=type_objects,
    ).serialize(mergeimports=False)

    g = Graph()
    g.parse(data=output, format="turtle")
    return g, outpath, output


def _contains_restriction(g: Graph, c: URIRef, prop: URIRef, pred: URIRef, filler: URIRef) -> bool:
    for r in g.objects(c, RDFS.subClassOf):
        if prop in g.objects(r, OWL.onProperty):
            if filler in g.objects(r, pred):
                return True
    return False


@pytest.mark.owlgen
def test_issue_owl_properties(input_path, snapshot, bundled_snapshot_text):
    def uri(s) -> URIRef:
        return URIRef(f"https://w3id.org/linkml/examples/personinfo/{s}")

    outputs: dict[str, str] = {}
    for conf in [
        dict(metaclasses=False, type_objects=False),
        dict(metaclasses=True, type_objects=True),
    ]:
        g, outpath, output = _test_owl(TESTFILE, input_path, **conf)
        outputs[outpath] = output
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

    assert bundled_snapshot_text(outputs) == snapshot(f"{TESTFILE}.owl.txt")

    # self.assertIn((A, RDF.type, OWL.Class), g)
    # NAME = URIRef('http://example.org/name')
    # self.assertIn((NAME, RDF.type, OWL.ObjectProperty), g)


@pytest.mark.rdfgen
@pytest.mark.jsonldcontextgen
@pytest.mark.yamlgen
@pytest.mark.pythongen
@pytest.mark.network
def test_other_formats(input_path, snapshot, bundled_snapshot_text):
    assert bundled_snapshot_text(_other_outputs(TESTFILE, input_path)) == snapshot(f"{TESTFILE}.other.txt")
