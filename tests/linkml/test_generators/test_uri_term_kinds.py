"""Every generator and the RDF dumper give a URI-like value the same RDF term kind.

The rule is ``linkml_runtime.utils.rdf_terms.type_term``: ``uri``, ``uriorcurie``,
the types derived from them and the node types (``objectidentifier``,
``nodeidentifier``, ``rdfs:Resource``, ``shex:bnode``) are IRIs or blank nodes; a type
derived from ``string`` with ``uri: xsd:anyURI`` keeps URI references as ``xsd:anyURI``
literals; ``curie`` stays an ``xsd:string`` literal.
"""

import json

import pytest
import yaml
from pyshacl import validate
from rdflib import OWL, RDF, SH, XSD, BNode, Graph, Literal, URIRef

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.yarrrmlgen import YarrrmlGenerator
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.compile_python import compile_python

EX = "https://example.org/terms/"

SCHEMA = """
id: https://example.org/terms
name: terms
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/terms/
default_prefix: ex
default_range: string
imports:
  - linkml:types
types:
  ImageLink:
    typeof: uri
  FilePath:
    typeof: string
    uri: xsd:anyURI
  ResourceRef:
    typeof: uriorcurie
    uri: rdfs:Resource
  BlankOnly:
    typeof: string
    uri: shex:bnode
classes:
  Container:
    tree_root: true
    attributes:
      documents:
        range: Document
        multivalued: true
        inlined_as_list: true
  Document:
    class_uri: ex:Document
    attributes:
      id:
        identifier: true
      homepage:
        range: uri
      related:
        range: uriorcurie
      image:
        range: ImageLink
      file_path:
        range: FilePath
      node:
        range: objectidentifier
      any_node:
        range: nodeidentifier
      code:
        range: curie
      cross_ref:
        range: ResourceRef
      anon:
        range: BlankOnly
      title:
        range: string
"""

# slot -> (type, kind of its values): "iri", "nonliteral" (IRI or blank node), "bnode", or a literal datatype
SLOTS = {
    "homepage": ("Uri", "iri"),
    "related": ("Uriorcurie", "iri"),
    "image": ("ImageLink", "iri"),
    "file_path": ("FilePath", XSD.anyURI),
    "node": ("Objectidentifier", "iri"),
    "any_node": ("Nodeidentifier", "nonliteral"),
    "code": ("Curie", XSD.string),
    "cross_ref": ("ResourceRef", "nonliteral"),
    "anon": ("BlankOnly", "bnode"),
    "title": ("String", XSD.string),
}
# SHACL node kinds (§4.1.3) of the node term kinds
SH_NODE_KINDS = {"iri": SH.IRI, "nonliteral": SH.BlankNodeOrIRI, "bnode": SH.BlankNode}

DATA = {
    "id": "ex:d1",
    "homepage": "https://example.org/terms/home",
    "related": "ex:other",
    "image": "https://example.org/terms/me.jpg",
    "file_path": "./docs/cv.pdf",
    "node": "ex:target",
    "any_node": "ex:target",
    "code": "ex:code",
    "cross_ref": "ex:ref",
    "anon": "_:n1",
    "title": "Alice",
}

EXPECTED_TERMS = {
    "homepage": URIRef(EX + "home"),
    "related": URIRef(EX + "other"),
    "image": URIRef(EX + "me.jpg"),
    "file_path": Literal("./docs/cv.pdf", datatype=XSD.anyURI),
    "node": URIRef(EX + "target"),
    "any_node": URIRef(EX + "target"),
    "code": Literal("ex:code"),
    "cross_ref": URIRef(EX + "ref"),
    "anon": BNode("n1"),
    "title": Literal("Alice"),
}


@pytest.fixture(scope="module")
def shapes() -> Graph:
    return Graph().parse(data=ShaclGenerator(SCHEMA).serialize(), format="turtle")


@pytest.fixture(scope="module")
def module():
    return compile_python(PythonGenerator(SCHEMA).serialize())


def _dumped(module, document: dict) -> Graph:
    """The RDF of *document* written by the runtime RDF dumper."""
    container = module.Container(documents=[module.Document(**document)])
    return rdflib_dumper.as_rdf_graph(container, SchemaView(SCHEMA))


def _via_context(document: dict) -> Graph:
    """The RDF of *document* read through the generated JSON-LD context."""
    context = json.loads(ContextGenerator(SCHEMA).serialize())["@context"]
    doc = {"@context": context, "documents": [{"@type": "Document", **document}]}
    return Graph().parse(data=json.dumps(doc), format="json-ld", base="https://reader.example/downloads/doc.json")


@pytest.mark.parametrize("slot", SLOTS)
def test_json_ld_context(slot):
    coercion = json.loads(ContextGenerator(SCHEMA).serialize())["@context"][slot].get("@type")
    kind = SLOTS[slot][1]
    expected = {"iri": "@id", "nonliteral": "@id", "bnode": "@id", XSD.anyURI: "xsd:anyURI", XSD.string: None}[kind]
    assert coercion == expected


@pytest.mark.parametrize("slot", SLOTS)
def test_shacl(slot, shapes):
    prop = next(shapes.subjects(SH.path, URIRef(EX + slot)))
    node_kind, datatype = shapes.value(prop, SH.nodeKind), shapes.value(prop, SH.datatype)
    kind = SLOTS[slot][1]
    if kind in SH_NODE_KINDS:
        assert (node_kind, datatype) == (SH_NODE_KINDS[kind], None)
    else:
        assert (node_kind, datatype) == (SH.Literal, kind)


def _owl_property(slot: str, **kwargs) -> tuple[set, set]:
    """The OWL property types of *slot* and the fillers of its universal restrictions."""
    graph = OwlSchemaGenerator(SCHEMA, metaclasses=False, **kwargs).as_graph()
    prop = URIRef(EX + slot)
    fillers = {f for r in graph.subjects(OWL.onProperty, prop) for f in graph.objects(r, OWL.allValuesFrom)}
    return set(graph.objects(prop, RDF.type)), fillers


@pytest.mark.parametrize("slot", SLOTS)
def test_owl(slot):
    """Node-valued slots are object properties ranging over owl:Thing (OWL 2 §5.3, §5.8.1)."""
    types, fillers = _owl_property(slot, type_objects=False)
    kind = SLOTS[slot][1]
    if kind in SH_NODE_KINDS:
        assert (types, fillers) == ({OWL.ObjectProperty}, {OWL.Thing})
    else:
        assert (types, fillers) == ({OWL.DatatypeProperty}, {kind})


@pytest.mark.parametrize("slot", SLOTS)
def test_owl_type_objects_mode_is_unchanged(slot):
    """With ``type_objects``, every typed value is an individual of the type's class, whatever its term kind."""
    types, fillers = _owl_property(slot, type_objects=True)
    assert types == {OWL.ObjectProperty}
    assert [str(f).rsplit("/", 1)[-1] for f in fillers] == [SLOTS[slot][0]]


@pytest.mark.parametrize("slot", SLOTS)
def test_shex(slot):
    shapes = json.loads(ShExGenerator(SCHEMA, format="json").serialize())["shapes"]
    type_name, kind = SLOTS[slot]
    shape = next(s for s in shapes if s["id"].rsplit("/", 1)[-1] == type_name)
    if kind in SH_NODE_KINDS:
        assert shape.get("nodeKind") == kind
    else:
        assert shape.get("datatype") == str(kind)


@pytest.mark.parametrize("slot", SLOTS)
def test_yarrrml(slot):
    mapping = yaml.safe_load(YarrrmlGenerator(SCHEMA).serialize())["mappings"]["Document"]["po"]
    obj = next(po["o"] for po in mapping if po["p"] == f"ex:{slot}")
    kind = SLOTS[slot][1]
    if kind in SH_NODE_KINDS:
        assert obj["type"] == {"iri": "iri", "nonliteral": "iri", "bnode": "blank"}[kind]
    else:
        assert obj["datatype"] == {XSD.anyURI: "xsd:anyURI", XSD.string: "xsd:string"}[kind]


@pytest.mark.parametrize("path", ["dumper", "context"])
def test_both_data_paths_give_the_same_terms_and_conform(module, shapes, path):
    """The dumper and the generated context write the same terms, and the generated shapes accept them.

    The relative file path stays text on both paths; it is not resolved against the reader's location.
    """
    graph = _dumped(module, DATA) if path == "dumper" else _via_context(DATA)
    subject = URIRef(EX + "d1")
    assert {slot: graph.value(subject, URIRef(EX + slot)) for slot in SLOTS} == EXPECTED_TERMS
    conforms, _, report = validate(graph, shacl_graph=shapes)
    assert conforms, report


@pytest.mark.parametrize(
    "slot,wrong",
    [
        ("homepage", Literal(EX + "home", datatype=XSD.anyURI)),
        ("image", Literal("ex:me.jpg")),
        ("file_path", URIRef("https://example.org/cv.pdf")),
        ("node", BNode("b1")),
        ("any_node", Literal("ex:target", datatype=URIRef("http://www.w3.org/ns/shex#nonLiteral"))),
        ("code", URIRef(EX + "code")),
        ("cross_ref", Literal("ex:ref", datatype=URIRef("http://www.w3.org/2000/01/rdf-schema#Resource"))),
        ("anon", URIRef(EX + "n1")),
    ],
)
def test_shapes_reject_the_wrong_term_kind(module, shapes, slot, wrong):
    graph = _dumped(module, DATA)
    subject = URIRef(EX + "d1")
    graph.set((subject, URIRef(EX + slot), wrong))
    conforms, _, report = validate(graph, shacl_graph=shapes)
    assert not conforms, f"{slot}={wrong!r} accepted"


@pytest.mark.parametrize("cast_literals", [True, False])
def test_dumped_terms_load_back(module, cast_literals):
    """The loader accepts the dumper's terms, also in strict mode; ``uri`` values stay complete, CURIEs stay CURIEs."""
    graph = _dumped(module, DATA)
    [container] = rdflib_loader.from_rdf_graph(
        graph, schemaview=SchemaView(SCHEMA), target_class=module.Container, cast_literals=cast_literals
    )
    loaded = {slot: getattr(container.documents[0], slot) for slot in SLOTS}
    assert loaded == {slot: DATA[slot] for slot in SLOTS}


def test_loader_keeps_blank_node_labels(module):
    """A blank node in an IRI-or-blank-node slot loads as its ``_:`` label instead of an inlined object."""
    graph = Graph()
    container, document = BNode(), URIRef(EX + "d1")
    graph.add((container, RDF.type, URIRef(EX + "Container")))
    graph.add((container, URIRef(EX + "documents"), document))
    graph.add((document, RDF.type, URIRef(EX + "Document")))
    graph.add((document, URIRef(EX + "cross_ref"), BNode("n1")))
    [container] = rdflib_loader.from_rdf_graph(graph, schemaview=SchemaView(SCHEMA), target_class=module.Container)
    assert container.documents[0].cross_ref == "_:n1"


@pytest.mark.parametrize("slot", ["homepage", "image"])
def test_dumper_rejects_relative_links(module, slot):
    """A relative reference is not an RDF IRI (RDF 1.1 Concepts §3.2); text needs a string-derived type."""
    with pytest.raises(ValueError, match="relative reference"):
        _dumped(module, {**DATA, slot: "../img/cover.png"})


def test_blank_node_values_through_the_context(shapes):
    """``_:`` labels in an IRI-or-blank-node slot become blank nodes and conform."""
    graph = _via_context({**DATA, "any_node": "_:n1", "cross_ref": "_:n2"})
    subject = URIRef(EX + "d1")
    assert isinstance(graph.value(subject, URIRef(EX + "any_node")), BNode)
    assert isinstance(graph.value(subject, URIRef(EX + "cross_ref")), BNode)
    conforms, _, report = validate(graph, shacl_graph=shapes)
    assert conforms, report


SUBPROPERTY_SCHEMA = """
id: https://example.org/sub
name: sub
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/sub/
default_prefix: ex
imports:
  - linkml:types
slots:
  related_to: {range: curie}
  part_of: {is_a: related_to}
classes:
  Edge:
    class_uri: ex:Edge
    attributes:
      predicate:
        range: curie
        subproperty_of: related_to
"""


def test_subproperty_values_take_the_slot_term_kind():
    """``sh:in`` members are compared exactly (SHACL §4.8.3), so a ``curie`` slot lists CURIE literals."""
    shapes = Graph().parse(data=ShaclGenerator(SUBPROPERTY_SCHEMA).serialize(), format="turtle")
    edge = '@prefix ex: <https://example.org/sub/> . ex:e1 a ex:Edge ; ex:predicate "{}" .'
    assert validate(Graph().parse(data=edge.format("ex:part_of"), format="turtle"), shacl_graph=shapes)[0]
    assert not validate(Graph().parse(data=edge.format("ex:unrelated"), format="turtle"), shacl_graph=shapes)[0]
