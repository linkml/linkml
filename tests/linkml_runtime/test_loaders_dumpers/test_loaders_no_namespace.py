import os

import pytest
import rdflib

from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import rdflib_loader, yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_loaders_dumpers import INPUT_DIR
from tests.test_loaders_dumpers.models.issue_576 import Dataset


@pytest.fixture(scope="module")
def view() -> SchemaView:
    """Create a SchemaView using issue_576.yaml."""
    return SchemaView(os.path.join(INPUT_DIR, "issue_576.yaml"))


@pytest.fixture(scope="module")
def inst() -> Dataset:
    """Create a Dataset object with the data from issue_576_data.yaml."""
    return yaml_loader.load(os.path.join(INPUT_DIR, "issue_576_data.yaml"), target_class=Dataset)


@pytest.fixture(scope="module")
def graph(inst: Dataset, view: SchemaView) -> rdflib.Graph:
    """Create an rdflib Graph object using the issue_576_data.yaml."""
    # dump the Dataset object in turtle format
    s = rdflib_dumper.dumps(inst, view, "turtle", prefix_map={"@base": "http://example.org/default/"})
    assert "@base <http://example.org/default/> ." in s
    # load the turtle into an rdflib Graph
    return rdflib.Graph().parse(data=s, format="turtle")


@pytest.mark.parametrize(
    ("subject", "predicate", "object"),
    [
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
    ],
)
def test_schema_load_no_namespace(graph: rdflib.Graph, subject, predicate, object) -> None:
    """Test loading schema and dataset with no namespace using rdflib.

    https://github.com/linkml/linkml/issues/576
    """
    if subject is None:
        assert object in graph.objects(subject, predicate)
    else:
        assert (subject, predicate, object) in graph


def test_schema_load_no_ns_compare(view: SchemaView, inst: Dataset, graph: rdflib.Graph) -> None:
    """Load a dataset object from the RDF graph and ensure it is the same as the yaml dataset."""
    inst2: Dataset = rdflib_loader.load(graph, target_class=Dataset, schemaview=view)

    assert inst.persons == inst2.persons
    assert inst.organizations == inst2.organizations
    assert inst.pets == inst2.pets
