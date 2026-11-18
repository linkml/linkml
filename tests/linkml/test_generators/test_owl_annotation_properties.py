"""gen-owl gives annotation properties their OWL role and no logical axioms.

A slot that implements ``owl:AnnotationProperty``, or whose property IRI is one of
the built-in annotation properties of OWL 2 (Structural Specification §5.5), is
declared as such and produces no class restriction (annotation properties have no
logical meaning, §10.1). Its domain, range and super-properties are emitted as the
annotation axioms of §10.2; logical uses are errors.
"""

from pathlib import Path

import pytest
import yaml
from rdflib import DCTERMS, OWL, RDF, RDFS, XSD, Graph, URIRef

from linkml.generators.owlgen import OwlSchemaGenerator

EX = "https://example.org/m/"
EXAMPLE = Path(__file__).resolve().parents[3] / "docs/examples/owl-dcmi-agent-annotations.yaml"

SCHEMA = """
id: https://example.org/m
name: m
prefixes:
  ex: https://example.org/m/
  linkml: https://w3id.org/linkml/
  owl: http://www.w3.org/2002/07/owl#
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  dcterms: http://purl.org/dc/terms/
imports: [linkml:types]
default_prefix: ex
default_range: string
slots:
  comment:
    slot_uri: rdfs:comment
    # an annotation property with native URIs too, so that note may refine it
    implements: [owl:AnnotationProperty]
  note:
    slot_uri: dcterms:description
    range: string
    implements: [owl:AnnotationProperty]
    is_a: comment
    domain: Thing
  ref:
    range: nodeidentifier
    implements: [owl:AnnotationProperty]
classes:
  Thing:
    slots: [comment, note, ref]
    attributes:
      name:
        slot_uri: rdfs:label
      plain:
        range: string
"""


def _graph(source: str | Path, **kwargs) -> Graph:
    """The generated ontology, parsed back from Turtle."""
    generator = OwlSchemaGenerator(source, type_objects=False, metaclasses=False, **kwargs)
    return Graph().parse(data=generator.serialize(), format="turtle")


def _restrictions(graph: Graph, prop: URIRef) -> int:
    return len(list(graph.subjects(OWL.onProperty, prop)))


@pytest.mark.parametrize("prop", ["note", "ref"])
def test_declared_annotation_property_has_no_restrictions(prop):
    """``implements: [owl:AnnotationProperty]`` gives the declaration and suppresses the restrictions."""
    graph = _graph(SCHEMA)
    assert set(graph.objects(URIRef(EX + prop), RDF.type)) == {OWL.AnnotationProperty}
    assert _restrictions(graph, URIRef(EX + prop)) == 0
    assert set(graph.objects(URIRef(EX + "plain"), RDF.type)) == {OWL.DatatypeProperty}
    assert _restrictions(graph, URIRef(EX + "plain")) > 0


@pytest.mark.parametrize(
    "native,expected",
    [
        pytest.param(True, {URIRef(EX + "name"): OWL.DatatypeProperty}, id="native"),
        pytest.param(False, {RDFS.label: None, RDFS.comment: None}, id="mapped"),
    ],
)
def test_builtin_annotation_property_iri(native, expected):
    """A slot emitted with a built-in annotation property IRI gets no declaration and no restriction.

    With native URIs the local property is an ordinary data property, as before.
    """
    graph = _graph(SCHEMA, use_native_uris=native)
    for prop, role in expected.items():
        assert set(graph.objects(prop, RDF.type)) == ({role} if role else set())
        assert (_restrictions(graph, prop) > 0) is (role is not None)
        if role is None:
            assert not set(graph.objects(prop, RDFS.range)) | set(graph.objects(prop, RDFS.domain))


def test_annotation_property_axioms():
    """Domain, a datatype range and super-properties are kept; a node type gives no range (OWL 2 §10.2)."""
    graph = _graph(SCHEMA, use_native_uris=False)
    note = URIRef("http://purl.org/dc/terms/description")
    assert set(graph.objects(note, RDFS.domain)) == {URIRef(EX + "Thing")}
    assert set(graph.objects(note, RDFS.range)) == {XSD.string}
    assert set(graph.objects(note, RDFS.subPropertyOf)) == {RDFS.comment}
    assert set(graph.objects(URIRef(EX + "ref"), RDFS.range)) == set()


def test_declared_annotation_predicate_is_declared():
    """A metaclass slot with the annotation role declares the predicate its annotations use."""
    graph = _graph(EXAMPLE)
    ontology = URIRef("https://example.org/model")
    assert set(graph.objects(ontology, DCTERMS.creator)) == {URIRef("https://orcid.org/0000-0002-1825-0097")}
    for predicate in (DCTERMS.creator, DCTERMS.rights):
        assert (predicate, RDF.type, OWL.AnnotationProperty) in graph
        assert _restrictions(graph, predicate) == 0
    assert not any(obj in {OWL.AnnotationProperty} for obj in graph.objects(None, OWL.onProperty))


def test_contradictory_roles_fail():
    schema = yaml.safe_load(SCHEMA)
    schema["slots"]["note"]["implements"] = ["owl:AnnotationProperty", "owl:DatatypeProperty"]
    with pytest.raises(ValueError, match="more than one OWL property role"):
        _graph(yaml.safe_dump(schema))


@pytest.mark.parametrize(
    "change,message",
    [
        pytest.param({"slots": {"note": {"symmetric": True}}}, "cannot declare symmetric", id="characteristic"),
        pytest.param({"slots": {"note": {"inverse": "comment"}}}, "cannot declare inverse", id="inverse"),
        pytest.param(
            {"classes": {"Thing": {"unique_keys": {"k": {"unique_key_slots": ["note"]}}}}}, "unique key", id="key"
        ),
        pytest.param(
            {"slots": {"ref": {"designates_type": True, "range": "string"}}}, "type designator", id="designator"
        ),
        pytest.param(
            {
                "classes": {
                    "Thing": {"rules": [{"preconditions": {"slot_conditions": {"note": {"equals_string": "x"}}}}]}
                }
            },
            "condition of a class expression",
            id="rule",
        ),
    ],
)
def test_logical_use_of_annotation_property_fails(change, message):
    """An annotation property cannot carry object property axioms or appear in a class expression."""
    schema = yaml.safe_load(SCHEMA)
    for section, elements in change.items():
        for name, fields in elements.items():
            schema[section][name].update(fields)
    with pytest.raises(ValueError, match=message):
        _graph(yaml.safe_dump(schema))


@pytest.mark.parametrize(
    "child,parent,message",
    [
        pytest.param(
            {"implements": ["owl:AnnotationProperty"]},
            {},
            "is an annotation property but its super-property 'base' is not one",
            id="annotation-under-data",
        ),
        pytest.param(
            {},
            {"implements": ["owl:AnnotationProperty"]},
            "is not an annotation property but its super-property 'base' is one",
            id="data-under-annotation",
        ),
    ],
)
@pytest.mark.parametrize("link", ["is_a", "mixins"])
def test_super_property_with_another_role_fails(child, parent, message, link):
    """A sub-property axiom relates properties of one role (OWL 2 §9.3.1, §10.2.1)."""
    schema = yaml.safe_load(SCHEMA)
    schema["slots"]["base"] = {"range": "string", **parent}
    schema["slots"]["derived"] = {"range": "string", **child, link: "base" if link == "is_a" else ["base"]}
    schema["classes"]["Thing"]["slots"].append("derived")
    with pytest.raises(ValueError, match=message):
        _graph(yaml.safe_dump(schema))


@pytest.mark.parametrize(
    "native,sub,sup",
    [
        pytest.param(True, URIRef(EX + "note"), URIRef(EX + "comment"), id="native"),
        pytest.param(False, URIRef("http://purl.org/dc/terms/description"), RDFS.comment, id="mapped"),
    ],
)
def test_super_property_with_the_same_role_is_emitted(native, sub, sup):
    """An annotation property under an annotation property keeps its super-property,
    as ``note`` under ``comment``, which is ``rdfs:comment`` with mapped URIs."""
    graph = _graph(SCHEMA, use_native_uris=native)
    assert (sub, RDFS.subPropertyOf, sup) in graph
    assert (sub, RDF.type, OWL.AnnotationProperty) in graph


@pytest.mark.parametrize("native", [True, False])
def test_every_predicate_without_a_role_is_an_annotation_property(native):
    """OWL 2 DL requires each property IRI to be declared (§5.8.1): the predicates gen-owl writes
    for metadata are annotation properties, logical properties keep their role, and the reserved
    vocabulary (§2.4) gets no declaration."""
    schema = yaml.safe_load(SCHEMA)
    schema["title"] = "A schema"
    schema["classes"]["Thing"]["description"] = "A thing."
    schema["classes"]["Thing"]["exact_mappings"] = ["dcterms:Agent"]
    graph = _graph(yaml.safe_dump(schema), use_native_uris=native)
    skos = "http://www.w3.org/2004/02/skos/core#"
    for metadata in (
        DCTERMS.title,
        URIRef(skos + "definition"),
        URIRef(skos + "inScheme"),
        URIRef(skos + "exactMatch"),
    ):
        assert (metadata, RDF.type, OWL.AnnotationProperty) in graph, metadata
    restricted = set(graph.objects(None, OWL.onProperty))
    assert restricted, "the schema has class restrictions"
    for prop in restricted:
        assert (prop, RDF.type, OWL.AnnotationProperty) not in graph
    roles = (OWL.AnnotationProperty, OWL.ObjectProperty, OWL.DatatypeProperty)
    for predicate in set(graph.predicates()):
        if str(predicate).startswith((str(RDF), str(RDFS), str(XSD), str(OWL))):
            assert not any((predicate, RDF.type, role) in graph for role in roles), predicate
        else:
            assert any((predicate, RDF.type, role) in graph for role in roles), predicate
