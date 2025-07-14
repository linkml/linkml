import rdflib

from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import rdflib_loader, yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_issues.environment import env
from tests.test_issues.models.linkml_issue_576 import Dataset


def test_issue_576() -> None:
    """Test loading schemas with no namespace.

    https://github.com/linkml/linkml/issues/576
    """
    view = SchemaView(env.input_path("linkml_issue_576.yaml"))
    inst = yaml_loader.load(env.input_path("linkml_issue_576_data.yaml"), target_class=Dataset)
    s = rdflib_dumper.dumps(inst, view, "turtle", prefix_map={"@base": "http://example.org/default/"})
    assert "@base <http://example.org/default/> ." in s

    g = rdflib.Graph().parse(data=s, format="turtle")
    for t in g.triples((None, None, None)):
        print(t)
    cases = [
        (
            None,
            rdflib.term.URIRef("https://w3id.org/linkml/personinfo/source"),
            rdflib.term.Literal("ex:source", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#anyURI")),
        ),
        (
            None,
            rdflib.term.URIRef("https://w3id.org/linkml/personinfo/pets"),
            rdflib.term.URIRef("https://example.org/PetA"),
        ),
        (
            rdflib.term.URIRef("http://example.org/default/org%201"),
            rdflib.term.URIRef("http://schema.org/name"),
            rdflib.term.Literal("Acme Inc. (US)"),
        ),
        (
            rdflib.term.URIRef("https://example.org/P1"),
            rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            rdflib.term.URIRef("http://schema.org/Person"),
        ),
        (
            rdflib.term.URIRef("https://example.org/P1"),
            rdflib.term.URIRef("http://schema.org/name"),
            rdflib.term.Literal("John Doe"),
        ),
    ]
    for case in cases:
        s, p, o = case
        if s is None:
            assert o in g.objects(s, p)
        else:
            assert case in g

    inst2 = rdflib_loader.load(g, target_class=Dataset, schemaview=view)
    assert len(inst.persons) == len(inst2.persons)
    assert len(inst.organizations) == len(inst2.organizations)
    assert len(inst.pets) == len(inst2.pets)
