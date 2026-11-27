"""Tests for the RDF term kind of values of LinkML types (``linkml_runtime.utils.rdf_terms``)."""

from collections.abc import Callable

import pyoxigraph
import pytest
from rdflib import XSD, BNode, Literal, URIRef

from linkml_runtime.utils.rdf_terms import TermKind, TypeTerm, checked_iri, link_root, type_term, value_term
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


def _accepted(check: Callable[[str], object], value: str) -> bool:
    """Whether *check* accepts *value*. Each check here refuses with a ``ValueError``."""
    try:
        check(value)
    except ValueError:
        return False
    return True


def test_checked_iri_agrees_with_rfc_3987_on_every_code_point():
    """pyoxigraph's IRI parser follows RFC 3987, and the query is the part of an IRI that allows the most.

    The check refuses only what no part allows, so it leaves ``%``, ``[`` and ``]``. It does
    refuse the bidirectional formatting characters, which RFC 3987 excludes in its prose (section
    4.1) and not in its grammar.
    """
    differences = {
        code_point
        for code_point in range(0x110000)
        if _accepted(lambda iri: checked_iri(iri, "Value"), iri := f"https://example.org/?{chr(code_point)}")
        != _accepted(pyoxigraph.NamedNode, iri)
    }
    assert differences == {ord("%"), ord("["), ord("]"), 0x200E, 0x200F, *range(0x202A, 0x202F)}


def test_checked_iri_leaves_what_some_part_of_an_iri_allows():
    """A private-use character is valid in a query only, and ``[`` in an IPv6 host only."""
    for iri in (f"https://example.org/{chr(0xE000)}", "https://example.org/a[1]", "https://example.org/%zz"):
        assert checked_iri(iri, "Value") == URIRef(iri)


def test_checked_iri_names_its_subject():
    with pytest.raises(ValueError, match="^Identifier 'x' holds a character"):
        checked_iri("https://example.org/a b", "Identifier 'x'")


# The ranges of the code points that the BLANK_NODE_LABEL production of Turtle 1.1 names
_LABEL_RANGES = [
    (0x30, 0x39),
    (0x41, 0x5A),
    (0x5F, 0x5F),
    (0x61, 0x7A),
    (0xB7, 0xB7),
    (0xC0, 0xD6),
    (0xD8, 0xF6),
    (0xF8, 0x2FF),
    (0x300, 0x36F),
    (0x370, 0x37D),
    (0x37F, 0x1FFF),
    (0x200C, 0x200D),
    (0x203F, 0x2040),
    (0x2070, 0x218F),
    (0x2C00, 0x2FEF),
    (0x3001, 0xD7FF),
    (0xF900, 0xFDCF),
    (0xFDF0, 0xFFFD),
    (0x10000, 0xEFFFF),
]
# Each edge of those ranges, the punctuation the production treats apart, and characters that the
# regular expression class \\w holds but the production does not, such as a superscript digit.
_LABEL_CODE_POINTS = sorted(
    {code_point for low, high in _LABEL_RANGES for code_point in (low - 1, low, high, high + 1)}
    | {ord("-"), ord("."), ord(":"), 0xAA, 0xB2, 0xB5, 0x2460}
)


def _turtle_reads_label(label: str) -> bool:
    """Whether a Turtle parser reads *label* as the label of a blank node."""
    try:
        return (
            len(list(pyoxigraph.parse(f"_:{label} <urn:p> <urn:o> .".encode(), format=pyoxigraph.RdfFormat.TURTLE)))
            == 1
        )
    except (SyntaxError, UnicodeError):
        return False


@pytest.mark.parametrize(
    "label_with",
    [lambda c: f"{c}a", lambda c: f"a{c}b", lambda c: f"a{c}", lambda c: c],
    ids=["first", "middle", "last", "alone"],
)
def test_blank_node_label_agrees_with_the_turtle_grammar(sv, label_with):
    """A character's place in a label decides whether it may be there: a dot may not end one, and so on."""
    disagreements = [
        f"U+{code_point:04X}"
        for code_point in _LABEL_CODE_POINTS
        if _accepted(lambda value: value_term(sv, "BlankOnly", value), f"_:{label_with(chr(code_point))}")
        != _turtle_reads_label(label_with(chr(code_point)))
    ]
    assert disagreements == []


@pytest.mark.parametrize("value", ["a b", "line one\nline two", "ends in a newline\n", '<x> "y"'])
def test_literals_keep_what_an_iri_cannot_hold(sv, value):
    """Text is a literal, so rdflib escapes it and neither check applies."""
    assert value_term(sv, "string", value) == Literal(value)
    assert value_term(sv, "FilePath", value) == Literal(value, datatype=XSD.anyURI)


@pytest.mark.parametrize("value", ["ex:a b", "ex:a\n", "ex:a\nb", "undeclared:a\n", "undeclared:a b"])
@pytest.mark.parametrize("type_name", ["uri", "uriorcurie", "nodeidentifier", "ImageLink"])
def test_value_term_checks_a_curie_after_expanding_it(sv, type_name, value):
    """A CURIE with a declared prefix and a value of an undeclared scheme both end up as IRIs."""
    with pytest.raises(ValueError, match="cannot hold"):
        value_term(sv, type_name, value)


def test_value_term_names_the_value_and_type(sv):
    """The refusal says which value and which type, with the line break escaped."""
    with pytest.raises(ValueError, match=r"^Value 'https://example.org/x\\n' of type 'uri' holds"):
        value_term(sv, "uri", "https://example.org/x\n")
    with pytest.raises(ValueError, match=r"^Value '_:a\\n' of type 'BlankOnly' has an invalid"):
        value_term(sv, "BlankOnly", "_:a\n")
