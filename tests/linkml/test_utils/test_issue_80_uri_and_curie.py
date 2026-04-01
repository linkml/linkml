import json

import pytest
from jsonasobj2 import as_json
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.yamlutils import as_rdf

pytestmark = [pytest.mark.jsonldcontextgen, pytest.mark.pythongen]


def test_objectidentifier_roundtrip(input_path):
    """Objectidentifier classes should round-trip cleanly through Python, context, and RDF."""
    schema = input_path("issue_80.yaml")

    generated_python = PythonGenerator(schema).serialize()
    assert "class Person" in generated_python

    module = compile_python(generated_python)
    example = module.Person("http://example.org/person/17", "Fred Jones", 43)
    assert json.loads(as_json(example)) == {
        "id": "http://example.org/person/17",
        "name": "Fred Jones",
        "age": 43,
    }

    generated_context = json.loads(ContextGenerator(schema).serialize())["@context"]
    assert generated_context["Person"]["@id"] == "ex:PERSON"
    assert generated_context["age"]["@type"] == "xsd:integer"

    rdf_output = as_rdf(example, contexts=json.dumps({"@context": generated_context})).serialize(format="turtle")
    graph = Graph()
    graph.parse(data=rdf_output, format="turtle")

    person = URIRef("http://example.org/person/17")
    assert (person, RDF.type, URIRef("http://example.org/PERSON")) in graph
    assert (person, URIRef("https://w3id.org/biolink/vocab/name"), Literal("Fred Jones")) in graph
    assert (person, URIRef("https://w3id.org/biolink/vocab/age"), Literal(43)) in graph
