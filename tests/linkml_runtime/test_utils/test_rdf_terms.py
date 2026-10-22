"""Tests for the RDF term kind of values of LinkML types (``linkml_runtime.utils.rdf_terms``)."""

import pytest
from rdflib import XSD, BNode, Literal, URIRef

from linkml_runtime.utils.rdf_terms import TermKind, TypeTerm, link_root, type_term, value_term
from linkml_runtime.utils.schemaview import SchemaView

ANYURI = str(XSD.anyURI)

SCHEMA = """
id: https://example.org/terms
name: terms
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/terms/
default_prefix: ex
imports:
  - linkml:types
types:
  ImageLink:
    typeof: uri
  FilePath:
    typeof: string
    uri: xsd:anyURI
  RootAnyUri:
    uri: xsd:anyURI
    base: str
  ResourceRef:
    typeof: uriorcurie
    uri: rdfs:Resource
  TextLink:
    typeof: uri
    uri: xsd:string
  FullIriLink:
    typeof: uri
    uri: http://www.w3.org/2001/XMLSchema#anyURI
  FullIriText:
    typeof: string
    uri: http://www.w3.org/2001/XMLSchema#anyURI
  BlankOnly:
    typeof: string
    uri: shex:bnode
"""


@pytest.fixture(scope="module")
def sv() -> SchemaView:
    return SchemaView(SCHEMA)


@pytest.mark.parametrize(
    "type_name,expected",
    [
        ("uri", TypeTerm(TermKind.IRI)),
        ("uriorcurie", TypeTerm(TermKind.IRI)),
        ("ImageLink", TypeTerm(TermKind.IRI)),
        ("FullIriLink", TypeTerm(TermKind.IRI)),
        ("objectidentifier", TypeTerm(TermKind.IRI)),
        ("nodeidentifier", TypeTerm(TermKind.BLANK_NODE_OR_IRI)),
        ("ResourceRef", TypeTerm(TermKind.BLANK_NODE_OR_IRI)),
        ("BlankOnly", TypeTerm(TermKind.BLANK_NODE)),
        ("FilePath", TypeTerm(TermKind.LITERAL, ANYURI)),
        ("FullIriText", TypeTerm(TermKind.LITERAL, ANYURI)),
        ("RootAnyUri", TypeTerm(TermKind.LITERAL, ANYURI)),
        ("TextLink", TypeTerm(TermKind.LITERAL, str(XSD.string))),
        ("curie", TypeTerm(TermKind.LITERAL, str(XSD.string))),
        ("string", TypeTerm(TermKind.LITERAL, str(XSD.string))),
        ("integer", TypeTerm(TermKind.LITERAL, str(XSD.integer))),
    ],
)
def test_type_term(sv, type_name, expected):
    """Links and node types are nodes; every other type, including text anyURI types, is a literal.

    An explicit datatype on a type derived from ``uri`` wins (``TextLink``), and the
    spelling of the datatype IRI (CURIE or full IRI) does not matter.
    """
    assert type_term(sv, type_name) == expected


def test_vocabulary_prefix_need_not_be_declared(sv):
    """``ResourceRef`` uses ``rdfs:`` without declaring it; the vocabulary prefix is recognised."""
    assert "rdfs" not in sv.namespaces()
    assert type_term(sv, "ResourceRef").kind is TermKind.BLANK_NODE_OR_IRI


def test_undeclared_prefix_fails_fast():
    """A datatype with a prefix that is neither declared nor a vocabulary prefix is an error."""
    sv = SchemaView(SCHEMA + "  Odd:\n    typeof: string\n    uri: foo:bar\n")
    with pytest.raises(ValueError, match="does not declare prefix 'foo'"):
        type_term(sv, "Odd")


@pytest.mark.parametrize(
    "prefix,uri,expected",
    [
        ("ex: https://example.org/c/", "ex:a:b", "https://example.org/c/a:b"),
        ("urn: 'urn:'", "urn:example:dt", "urn:example:dt"),
    ],
)
def test_declared_prefix_expands_a_local_part_with_a_colon(prefix, uri, expected):
    """A declared prefix expands whatever the local part, so a ``urn:`` datatype works once ``urn`` is declared."""
    sv = SchemaView(
        f"id: https://example.org/c\nname: c\nprefixes:\n  {prefix}\ntypes:\n  Odd:\n    base: str\n    uri: {uri}\n"
    )
    assert type_term(sv, "Odd") == TypeTerm(TermKind.LITERAL, expected)


@pytest.mark.parametrize(
    "type_name,expected",
    [
        ("uri", "uri"),
        ("ImageLink", "uri"),
        ("TextLink", "uri"),
        ("FullIriLink", "uri"),
        ("uriorcurie", "uriorcurie"),
        ("ResourceRef", "uriorcurie"),
        ("RootAnyUri", None),
        ("FilePath", None),
        ("objectidentifier", None),
        ("curie", None),
        ("string", None),
    ],
)
def test_link_root(sv, type_name, expected):
    """``uri`` values are complete URIs and ``uriorcurie`` values may be CURIEs; the root is found through ``typeof``."""
    assert link_root(sv, type_name) == expected


OWN_TYPES = """
id: https://example.org/own
name: own
prefixes:
  ex: https://example.org/own/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
types:
  string:
    uri: xsd:string
    base: str
  uri:
    typeof: string
    uri: xsd:anyURI
  uriorcurie:
    uri: xsd:anyURI
    base: URIorCURIE
"""


@pytest.mark.parametrize("type_name,kind", [("uri", TermKind.LITERAL), ("uriorcurie", TermKind.IRI)])
def test_link_types_are_identified_by_their_definition(type_name, kind):
    """A user type that is merely called ``uri`` is text; a verbatim copy of ``uriorcurie`` is a link."""
    assert type_term(SchemaView(OWN_TYPES), type_name).kind is kind


def test_merged_schema_keeps_link_types():
    """Merging imports rewrites ``from_schema``; the link types are still recognised."""
    sv = SchemaView(SCHEMA)
    sv.merge_imports()
    assert type_term(sv, "uri").kind is TermKind.IRI
    assert type_term(sv, "ImageLink").kind is TermKind.IRI


@pytest.mark.parametrize(
    "type_name,value,expected",
    [
        ("uri", "https://example.org/x", URIRef("https://example.org/x")),
        ("uriorcurie", "ex:x", URIRef("https://example.org/terms/x")),
        ("objectidentifier", "ex:x", URIRef("https://example.org/terms/x")),
        ("nodeidentifier", "_:b1", BNode("b1")),
        ("ResourceRef", "_:b1", BNode("b1")),
        ("FilePath", "./docs/cv.pdf", Literal("./docs/cv.pdf", datatype=XSD.anyURI)),
        ("FilePath", "ex:x", Literal("ex:x", datatype=XSD.anyURI)),
        ("curie", "ex:x", Literal("ex:x")),
        ("string", "text", Literal("text")),
        ("boolean", True, Literal(True)),
    ],
)
def test_value_term(sv, type_name, value, expected):
    """IRIs are expanded, text stays as written, and literals keep their native value."""
    term = value_term(sv, type_name, value)
    assert term == expected
    assert type(term) is type(expected)


def test_boolean_literal_has_canonical_lexical_form(sv):
    assert value_term(sv, "boolean", True).n3() == '"true"^^<http://www.w3.org/2001/XMLSchema#boolean>'


@pytest.mark.parametrize(
    "type_name,value,message",
    [
        ("uri", "./docs/cv.pdf", "relative reference"),
        ("ImageLink", "../img/a.png", "relative reference"),
        ("uriorcurie", "_:b1", "is a blank node"),
        ("BlankOnly", "https://example.org/x", "blank node label"),
    ],
)
def test_value_term_rejects_values_of_the_wrong_kind(sv, type_name, value, message):
    """A relative reference cannot be an RDF IRI (RDF 1.1 Concepts §3.2), nor a blank node an IRI."""
    with pytest.raises(ValueError, match=message):
        value_term(sv, type_name, value)
