"""Annotation values declared through a metamodel extension take the RDF term of their declared range.

The rule is ``linkml.generators.common.annotations``: a slot of a metaclass that a
schema element ``instantiates`` gives the annotation value the term a slot value of
that range gets (``linkml_runtime.utils.rdf_terms``). gen-owl and gen-shacl share it,
and gen-owl applies the same rule to native metadata such as ``see_also``.
"""

import warnings
from pathlib import Path

import pytest
import yaml
from pyshacl import validate
from rdflib import DCTERMS, RDF, RDFS, SH, XSD, BNode, Graph, Literal, URIRef

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime.utils.rdf_canonicalize import RDFCanonicalizationWarning

EX = "https://example.org/"
EXAMPLE = Path(__file__).resolve().parents[3] / "docs/examples/owl-dcmi-agent-annotations.yaml"

SCHEMA = """
id: https://example.org/model
name: model
prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/
imports: [linkml:types]
default_prefix: ex
default_range: string
types:
  FilePath:
    typeof: string
    uri: xsd:anyURI
enums:
  Status:
    permissible_values: {draft: {}, final: {}}
classes:
  Metadata:
    attributes:
      reviewer: {range: nodeidentifier}
      homepage: {range: uri}
      file_path: {range: FilePath}
      code: {range: curie}
      status: {range: Status}
      review: {range: string}
      note: {}
  Profile:
    is_a: Metadata
    class_uri: ex:Profile
  Thing:
    instantiates: [ex:Profile]
    annotations:
      reviewer: ex:alice
      homepage: https://alice.example.org/
      file_path: ./docs/cv.pdf
      code: ex:c1
      status: draft
      review: well defined
      note: free text
"""

# tag -> the term its declared range gives the value (with default_language "en")
EXPECTED = {
    "reviewer": URIRef(EX + "alice"),
    "homepage": URIRef("https://alice.example.org/"),
    "file_path": Literal("./docs/cv.pdf", datatype=XSD.anyURI),
    "code": Literal("ex:c1"),
    "status": Literal("draft"),
    "review": Literal("well defined", lang="en"),
    "note": Literal("free text", lang="en"),
}


def _graph(source: str | Path, generator: str, **kwargs) -> Graph:
    """The generated OWL ontology or SHACL shapes, parsed back from Turtle."""
    if generator == "owl":
        text = OwlSchemaGenerator(source, type_objects=False, metaclasses=False, default_language="en", **kwargs)
    else:
        text = ShaclGenerator(source, include_annotations=True, default_language="en", **kwargs)
    return Graph().parse(data=text.serialize(), format="turtle")


@pytest.mark.parametrize("generator", ["owl", "shacl"])
@pytest.mark.parametrize("tag", EXPECTED)
def test_declared_range_gives_the_term(generator, tag):
    """Nodes, typed literals, strings and enum values follow the metaclass slot's range.

    The metaclass needs no ``implements`` role for this, as in the annotations guide.
    """
    graph = _graph(SCHEMA, generator)
    assert set(graph.objects(URIRef(EX + "Thing"), URIRef(EX + tag))) == {EXPECTED[tag]}


@pytest.mark.parametrize("generator", ["owl", "shacl"])
@pytest.mark.parametrize("form", ["name", "curie", "iri"])
def test_tag_as_slot_name_curie_or_iri(generator, form):
    schema = yaml.safe_load(SCHEMA)
    prefix = {"name": "", "curie": "ex:", "iri": EX}[form]
    schema["classes"]["Thing"]["annotations"] = {prefix + "reviewer": "ex:alice"}
    graph = _graph(yaml.safe_dump(schema), generator)
    assert set(graph.objects(URIRef(EX + "Thing"), URIRef(EX + "reviewer"))) == {URIRef(EX + "alice")}


@pytest.mark.parametrize(
    "generator,owner",
    [
        ("owl", "class"),
        ("owl", "slot"),
        ("owl", "enum"),
        ("owl", "permissible_value"),
        ("shacl", "slot"),
        ("shacl", "type"),
    ],
)
def test_annotated_elements(generator, owner):
    """Every element that carries annotations in the output uses the same rule."""
    schema = yaml.safe_load(SCHEMA)
    metadata = {"instantiates": ["ex:Profile"], "annotations": {"reviewer": "ex:alice"}}
    schema["classes"]["Thing"].pop("annotations")
    if owner == "class":
        schema["classes"]["Thing"].update(metadata)
    elif owner == "slot":
        schema["classes"]["Thing"]["attributes"] = {"value": {"range": "string", **metadata}}
    elif owner == "enum":
        schema["enums"]["Status"].update(metadata)
    elif owner == "permissible_value":
        schema["enums"]["Status"]["permissible_values"]["draft"] = {"meaning": "ex:Draft", **metadata}
    else:
        schema["types"]["FilePath"].update(metadata)
        schema["classes"]["Thing"]["attributes"] = {"value": {"range": "FilePath"}}
    graph = _graph(yaml.safe_dump(schema), generator)
    assert URIRef(EX + "alice") in graph.objects(None, URIRef(EX + "reviewer"))


@pytest.mark.parametrize("generator", ["owl", "shacl"])
def test_imported_metaclass(tmp_path, generator):
    """A metaclass from an imported schema is found by its class URI, with its inherited slots."""
    profile = yaml.safe_load(SCHEMA)
    del profile["classes"]["Thing"]
    (tmp_path / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    consumer = yaml.safe_load(SCHEMA)
    consumer.update({"id": EX + "consumer", "imports": ["profile"], "classes": {"Thing": consumer["classes"]["Thing"]}})
    del consumer["types"], consumer["enums"]
    source = tmp_path / "consumer.yaml"
    source.write_text(yaml.safe_dump(consumer), encoding="utf-8")
    assert URIRef(EX + "alice") in _graph(source, generator).objects(None, URIRef(EX + "reviewer"))


@pytest.mark.parametrize("generator", ["owl", "shacl"])
def test_blank_node_label_for_a_node_type(generator):
    schema = yaml.safe_load(SCHEMA)
    schema["classes"]["Thing"]["annotations"]["reviewer"] = "_:anonymous"
    graph = _graph(yaml.safe_dump(schema), generator)
    assert isinstance(next(graph.objects(URIRef(EX + "Thing"), URIRef(EX + "reviewer"))), BNode)


@pytest.mark.parametrize(
    "generator,tag,expected", [("owl", "other", Literal("ex:x", lang="en")), ("shacl", "ex:other", URIRef(EX + "x"))]
)
def test_undeclared_tag_keeps_the_generator_behaviour(generator, tag, expected):
    """Without a declaration, gen-owl writes text and gen-shacl guesses an IRI from the colon, as before."""
    schema = yaml.safe_load(SCHEMA)
    schema["classes"]["Thing"]["annotations"][tag] = "ex:x"
    graph = _graph(yaml.safe_dump(schema), generator)
    assert set(graph.objects(URIRef(EX + "Thing"), URIRef(EX + "other"))) == {expected}


@pytest.mark.parametrize("generator,owner", [("owl", "class"), ("shacl", "class"), ("owl", "permissible_value")])
def test_conflicting_declarations_fail(generator, owner):
    schema = yaml.safe_load(SCHEMA)
    schema["classes"]["Other"] = {"attributes": {"reviewer": {"range": "string"}}}
    metadata = {"instantiates": ["ex:Profile", "ex:Other"], "annotations": {"reviewer": "ex:alice"}}
    if owner == "class":
        schema["classes"]["Thing"].update(metadata)
    else:
        schema["enums"]["Status"]["permissible_values"]["draft"] = {"meaning": "ex:Draft", **metadata}
    with pytest.raises(ValueError, match="ex:Other.*different terms"):
        _graph(yaml.safe_dump(schema), generator)


@pytest.mark.parametrize("generator", ["owl", "shacl"])
@pytest.mark.parametrize("value,message", [("./home.html", "relative reference"), ("_:b1", "blank node")])
def test_value_of_the_wrong_kind_fails(generator, value, message):
    """A ``uri`` value must be an absolute IRI (RDF 1.1 Concepts §3.2), not text or a blank node."""
    schema = yaml.safe_load(SCHEMA)
    schema["classes"]["Thing"]["annotations"]["homepage"] = value
    with pytest.raises(ValueError, match=message):
        _graph(yaml.safe_dump(schema), generator)


def test_native_metadata_follows_the_metamodel_range():
    """``see_also`` and ``source`` are ``uriorcurie`` (IRIs); ``license`` is a string; ``created_on`` a datetime."""
    schema = yaml.safe_load(SCHEMA)
    schema.update(
        {
            "see_also": ["ex:docs"],
            "source": "https://example.org/source",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "created_on": "2026-10-21T10:00:00",
        }
    )
    graph = _graph(yaml.safe_dump(schema), "owl")
    ontology = URIRef(EX + "model")
    assert set(graph.objects(ontology, RDFS.seeAlso)) == {URIRef(EX + "docs")}
    assert set(graph.objects(ontology, DCTERMS.source)) == {URIRef("https://example.org/source")}
    assert set(graph.objects(ontology, DCTERMS.license)) == {Literal(schema["license"], lang="en")}
    assert set(graph.objects(ontology, URIRef("http://purl.org/pav/createdOn"))) == {
        Literal("2026-10-21T10:00:00", datatype=XSD.dateTime)
    }


def test_native_link_uses_the_schema_prefixes_without_a_types_import():
    """A schema that imports nothing still expands its own CURIEs; the term kind comes from the metamodel."""
    schema = {
        "id": EX + "bare",
        "name": "bare",
        "prefixes": {"ex": EX, "linkml": "https://w3id.org/linkml/"},
        "default_prefix": "ex",
        "classes": {"Thing": {"see_also": ["ex:docs", "skos:Concept"]}},
    }
    graph = _graph(yaml.safe_dump(schema), "owl")
    assert set(graph.objects(URIRef(EX + "Thing"), RDFS.seeAlso)) == {
        URIRef(EX + "docs"),
        URIRef("http://www.w3.org/2004/02/skos/core#Concept"),
    }


def test_native_link_that_is_not_a_link_is_kept_as_a_literal(caplog):
    """A bare element name in ``see_also`` cannot be resolved; it is kept as text, so the output stays standard RDF."""
    schema = yaml.safe_load(SCHEMA)
    schema["classes"]["Thing"]["see_also"] = ["implements"]
    with warnings.catch_warnings():
        warnings.simplefilter("error", RDFCanonicalizationWarning)
        output = OwlSchemaGenerator(yaml.safe_dump(schema), type_objects=False, metaclasses=False).serialize()
    graph = Graph().parse(data=output, format="turtle")
    assert set(graph.objects(URIRef(EX + "Thing"), RDFS.seeAlso)) == {Literal("implements")}
    assert "see_also of https://example.org/Thing: 'implements' is neither an IRI nor a CURIE" in caplog.text


def test_documented_dcmi_example():
    """The example in the OWL documentation names its creator by IRI and holds its rights as text."""
    graph = _graph(EXAMPLE, "owl")
    ontology = URIRef(EX + "model")
    assert set(graph.objects(ontology, DCTERMS.creator)) == {URIRef("https://orcid.org/0000-0002-1825-0097")}
    assert set(graph.objects(ontology, DCTERMS.rights)) == {Literal("Copyright 2026 The Example Team", lang="en")}


def test_shacl_annotations_do_not_constrain_data():
    """An annotation on a node shape is metadata; instances need no such property."""
    shapes = _graph(SCHEMA, "shacl")
    shape = next(shapes.subjects(SH.targetClass, URIRef(EX + "Thing")))
    assert (shape, URIRef(EX + "reviewer"), URIRef(EX + "alice")) in shapes
    data = Graph()
    data.add((URIRef(EX + "instance"), RDF.type, URIRef(EX + "Thing")))
    conforms, _, report = validate(data, shacl_graph=shapes)
    assert conforms, report
