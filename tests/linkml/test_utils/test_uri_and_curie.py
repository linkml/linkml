import json
from pathlib import PurePath

import pytest
from jsonasobj2 import as_json, loads
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph
from linkml_runtime.utils.yamlutils import as_rdf
from tests.linkml.utils.compare_jsonld_context import CompareJsonldContext


@pytest.mark.jsonldgen
@pytest.mark.jsonldcontextgen
@pytest.mark.pythongen
def test_uri_and_curie(input_path, snapshot, snapshot_path):
    """Compile a model of URI's and Curies and then test the various types"""
    model_name = "uriandcurie"
    model_path = input_path(f"{model_name}.yaml")

    pythongen_output = PythonGenerator(model_path).serialize()
    assert pythongen_output == snapshot(f"{model_name}.py")

    # Check that the interpretations are correct
    contextgen_output = ContextGenerator(model_path).serialize()
    CompareJsonldContext.compare_with_snapshot(contextgen_output, snapshot_path(f"{model_name}.jsonld"))

    jsonldgen_output = JSONLDGenerator(model_path).serialize(context_kwargs={"model": True})
    assert jsonldgen_output == snapshot(f"{model_name}.json")

    module = compile_python(pythongen_output)

    curie_obj = module.C1(
        "ex:obj1",
        hasCurie="ex:curie",
        hasURI="http://example.org/test/uri",
        hasNcName="A123",
        id2="ex:id2",
    )
    instance_jsonld = loads('{ "ex": "http://example.org/test/inst#" }')

    g = as_rdf(
        curie_obj,
        [
            PurePath(input_path(f"{model_name}.jsonld")).as_uri(),
            instance_jsonld,
        ],
    )
    assert canonicalize_rdf_graph(g, output_format="turtle") == snapshot(f"{model_name}.ttl")


def test_issue_80_objectidentifier_roundtrip(input_path):
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

    rdf_output = canonicalize_rdf_graph(
        as_rdf(example, contexts=json.dumps({"@context": generated_context})), output_format="turtle"
    )
    graph = Graph()
    graph.parse(data=rdf_output, format="turtle")

    person = URIRef("http://example.org/person/17")
    assert (person, RDF.type, URIRef("http://example.org/PERSON")) in graph
    assert (person, URIRef("https://w3id.org/biolink/vocab/name"), Literal("Fred Jones")) in graph
    assert (person, URIRef("https://w3id.org/biolink/vocab/age"), Literal(43)) in graph
