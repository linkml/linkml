"""Every generator and the RDF dumper give a URI-like value the same RDF term kind.

The rule is ``linkml_runtime.utils.rdf_terms.type_term``: ``uri``, ``uriorcurie``,
the types derived from them and the node types (``objectidentifier``,
``nodeidentifier``, ``rdfs:Resource``, ``shex:bnode``) are IRIs or blank nodes; a type
derived from ``string`` with ``uri: xsd:anyURI`` keeps URI references as ``xsd:anyURI``
literals; ``curie`` stays an ``xsd:string`` literal.
"""

import json
import warnings

import pyoxigraph
import pytest
import yaml
from click.testing import CliRunner
from pyshacl import validate
from rdflib import OWL, RDF, SH, XSD, BNode, Graph, Literal, URIRef

from linkml.converter.cli import cli as convert_cli
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.yarrrmlgen import YarrrmlGenerator
from linkml.validator import validate as linkml_validate
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.rdf_canonicalize import RDFCanonicalizationWarning
from linkml_runtime.utils.rdf_terms import value_term

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


@pytest.mark.parametrize("type_name", ["uri", "uriorcurie", "objectidentifier", "nodeidentifier", "ImageLink"])
@pytest.mark.parametrize(
    "value",
    [
        "https://example.org/x\n",
        "https://example.org/x\ny",
        "https://example.org/a b",
        "https://example.org/<x>",
        "https://example.org/\x85",
        "https://example.org/\u202e",
    ],
)
def test_iri_types_refuse_what_an_iri_cannot_hold(type_name, value):
    """Turtle 1.1 excludes line breaks, spaces and angle brackets from an IRI, and RFC 3987 the rest."""
    with pytest.raises(ValueError, match="cannot hold"):
        value_term(SchemaView(SCHEMA), type_name, value)


def test_iri_types_admit_a_non_ascii_iri():
    """An RDF IRI may hold a non-ASCII character, although the ``uri`` type's validation rejects one."""
    iri = "https://example.org/é"
    assert value_term(SchemaView(SCHEMA), "uri", iri) == URIRef(iri)


def test_dumper_refuses_a_line_break_from_a_pydantic_model():
    """A Pydantic model holds a link as a plain string, so the dumper checks it."""
    document = compile_python(PydanticGenerator(SCHEMA).serialize()).Document(
        id="ex:doc", homepage="https://example.org/x\ny"
    )
    with pytest.raises(ValueError, match="cannot hold"):
        rdflib_dumper.dumps(document, schemaview=SchemaView(SCHEMA))


@pytest.mark.parametrize("type_name", ["nodeidentifier", "ResourceRef", "BlankOnly"])
@pytest.mark.parametrize("label", ["n1", "a.b", "a-b", "é"])
def test_blank_node_types_admit_a_valid_label(type_name, label):
    """A label holds word characters, with dots and hyphens inside it."""
    assert value_term(SchemaView(SCHEMA), type_name, f"_:{label}") == BNode(label)


@pytest.mark.parametrize("type_name", ["nodeidentifier", "ResourceRef", "BlankOnly"])
@pytest.mark.parametrize("label", ["", "a b", "a\n", "a.", ".a", "-a", "a;b"])
def test_blank_node_types_refuse_an_invalid_label(type_name, label):
    """A label outside the Turtle grammar is refused."""
    with pytest.raises(ValueError, match="invalid blank node label"):
        value_term(SchemaView(SCHEMA), type_name, f"_:{label}")


def test_dumper_refuses_a_blank_node_label_that_would_add_triples():
    """rdflib writes a label as it finds it, so this one would add a triple about another subject."""
    label = '_:x .\n<https://victim.example/a> <https://evil.example/p> "o" .\n_:y <https://evil.example/q> _:z'
    document = compile_python(PydanticGenerator(SCHEMA).serialize()).Document(id="ex:doc", any_node=label)
    with pytest.raises(ValueError, match="invalid blank node label"):
        rdflib_dumper.dumps(document, schemaview=SchemaView(SCHEMA))


@pytest.mark.parametrize("generator", [PydanticGenerator, PythonGenerator])
@pytest.mark.parametrize("identifier", ["https://example.org/x\n", "https://example.org/x\ny"])
def test_dumper_refuses_a_line_break_in_an_identifier(generator, identifier):
    """A class's identifier takes its own route to an IRI, and the dumper checks that route too."""
    document = compile_python(generator(SCHEMA).serialize()).Document(id=identifier)
    with pytest.raises(ValueError, match="cannot hold"):
        rdflib_dumper.dumps(document, schemaview=SchemaView(SCHEMA))


def test_validator_refuses_a_final_newline_in_a_uri():
    """The checks behind ``format: uri`` end in ``$``, which also matches before a final newline."""
    value = "https://alice.example.org/\n"
    results = linkml_validate({"id": "ex:doc", "homepage": value}, SCHEMA, "Document").results
    assert [result.message for result in results] == [f"{value!r} is not a 'uri' in /homepage"]


ROUTES = """
id: https://example.org/routes
name: routes
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/routes/
default_prefix: ex
default_range: string
imports:
  - linkml:types
types:
  Anon:
    typeof: string
    uri: shex:bnode
classes:
  Citation:
    attributes:
      id:
        identifier: true
  Encoded:
    attributes:
      id:
        identifier: true
        annotations:
          percent_encoded: true
  Paper:
    tree_root: true
    attributes:
      id:
        identifier: true
      author:
        range: Anon
      homepage:
        range: uri
      mirrors:
        range: uri
        multivalued: true
      ordered_mirrors:
        range: uri
        multivalued: true
        list_elements_ordered: true
      cites:
        range: Citation
      all_cites:
        range: Citation
        multivalued: true
      created:
        range: datetime
      opens:
        range: time
"""

# rdflib writes this label as it finds it, so it would close the statement and start another.
INJECTING_LABEL = '_:x .\n<https://victim.example/a> <https://evil.example/p> "o" .\n_:y <https://evil.example/q> _:z'


@pytest.fixture(scope="module")
def pydantic_routes():
    return compile_python(PydanticGenerator(ROUTES).serialize())


@pytest.fixture(scope="module")
def dataclass_routes():
    return compile_python(PythonGenerator(ROUTES).serialize())


@pytest.mark.parametrize(
    "slot,value",
    [
        ("mirrors", ["https://example.org/a", "https://example.org/x\n"]),
        ("ordered_mirrors", ["https://example.org/x\ny"]),
    ],
)
def test_dumper_checks_every_value_of_a_multivalued_slot(pydantic_routes, slot, value):
    """An ordered slot takes its own route to an ``rdf:List``, and the check covers that route too."""
    paper = pydantic_routes.Paper(id="ex:p", **{slot: value})
    with pytest.raises(ValueError, match="cannot hold"):
        rdflib_dumper.as_rdf_graph(paper, schemaview=SchemaView(ROUTES))


@pytest.mark.parametrize("slot,value", [("cites", "ex:a\nb"), ("all_cites", ["ex:a\nb"])])
def test_dumper_checks_a_reference_to_another_class(dataclass_routes, slot, value):
    """A reference to a class with an identifier becomes an IRI by the identifier's route."""
    paper = dataclass_routes.Paper(id="ex:p", **{slot: value})
    with pytest.raises(ValueError, match="^Identifier 'ex:a.nb' holds"):
        rdflib_dumper.as_rdf_graph(paper, schemaview=SchemaView(ROUTES))


def test_dumper_percent_encodes_a_percent_encoded_identifier(pydantic_routes):
    """A line break in such an identifier is data to encode, so the dumper does not refuse it."""
    graph = rdflib_dumper.as_rdf_graph(pydantic_routes.Encoded(id="a b\nc"), schemaview=SchemaView(ROUTES))
    assert set(graph.subjects()) == {URIRef("a%20b%0Ac")}


@pytest.mark.parametrize(
    "slot,value",
    [
        ("homepage", "https://example.org/é"),
        ("author", "_:a·b"),
        ("author", "_:é"),
        ("author", "_:a.b-c_1"),
    ],
)
def test_dumper_writes_what_it_admits(pydantic_routes, slot, value):
    """pyoxigraph serializes the graph and is strict, so a value it refused would raise the warning here."""
    paper = pydantic_routes.Paper(id="ex:p", **{slot: value})
    with warnings.catch_warnings():
        warnings.simplefilter("error", RDFCanonicalizationWarning)
        turtle = rdflib_dumper.dumps(paper, schemaview=SchemaView(ROUTES))
    assert len(Graph().parse(data=turtle, format="turtle")) == 2
    assert len(list(pyoxigraph.parse(turtle.encode(), format=pyoxigraph.RdfFormat.TURTLE))) == 2


def test_dumper_writes_an_iri_only_rfc_3987_refuses(pydantic_routes):
    """Turtle's IRIREF admits ``[`` outside a host, so the dumper still writes it, through rdflib, with a warning."""
    paper = pydantic_routes.Paper(id="ex:p", homepage="https://example.org/a[1]")
    with pytest.warns(RDFCanonicalizationWarning):
        turtle = rdflib_dumper.dumps(paper, schemaview=SchemaView(ROUTES))
    assert (None, None, URIRef("https://example.org/a[1]")) in Graph().parse(data=turtle, format="turtle")


def test_dump_leaves_an_existing_file_when_the_dumper_refuses(pydantic_routes, tmp_path):
    """The dumper refuses before anything is written, so the earlier output survives."""
    output = tmp_path / "out.ttl"
    output.write_text("earlier output")
    paper = pydantic_routes.Paper(id="ex:p", author=INJECTING_LABEL)
    with pytest.raises(ValueError, match="invalid blank node label"):
        rdflib_dumper.dump(paper, to_file=str(output), schemaview=SchemaView(ROUTES))
    assert output.read_text() == "earlier output"


def test_linkml_convert_refuses_the_injecting_label(tmp_path):
    """The value passes validation, since its type derives from string, and stops at the dumper."""
    schema, data, output = (tmp_path / name for name in ("schema.yaml", "data.yaml", "out.ttl"))
    schema.write_text(ROUTES)
    data.write_text(yaml.safe_dump({"id": "ex:p", "author": INJECTING_LABEL}))
    output.write_text("earlier output")
    args = ["-s", str(schema), "-C", "Paper", "-t", "ttl", "-o", str(output), str(data)]
    result = CliRunner().invoke(convert_cli, args)
    assert isinstance(result.exception, ValueError)
    assert "invalid blank node label" in str(result.exception)
    assert output.read_text() == "earlier output"


@pytest.mark.parametrize(
    "slot,value,format_name,location",
    [
        ("homepage", "https://example.org/x\n", "uri", "/homepage"),
        ("mirrors", ["https://example.org/x\n"], "uri", "/mirrors/0"),
        ("created", "2020-01-01T00:00:00Z\n", "date-time", "/created"),
        ("opens", "00:00:00Z\n", "time", "/opens"),
    ],
)
def test_validator_refuses_a_final_newline_in_each_format(slot, value, format_name, location):
    """Each of these formats has its own library check, and each of those ends in ``$``."""
    results = linkml_validate({"id": "ex:p", slot: value}, ROUTES, "Paper").results
    bad = value[0] if isinstance(value, list) else value
    assert [result.message for result in results] == [f"{bad!r} is not a {format_name!r} in {location}"]
    good = [item.rstrip() for item in value] if isinstance(value, list) else value.rstrip()
    assert not linkml_validate({"id": "ex:p", slot: good}, ROUTES, "Paper").results


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
