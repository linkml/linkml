"""The RDF term that a value of a LinkML type becomes.

A slot whose range is a type holds IRIs, blank nodes or literals, never a mix:
RDF keeps the three kinds of term distinct (RDF 1.1 Concepts §3.1), and OWL 2 DL
types every property as either an object or a data property (OWL 2 Structural
Specification §5.8.1). One rule decides the kind for the RDF generators and for
the RDF dumper and loader:

1. A type whose datatype is a node kind has nodes of that kind. The node kinds
   are those of ShEx (``shex:iri``, ``shex:bnode``, ``shex:nonliteral``;
   ShEx 2.1 §5.4.2), which ``objectidentifier`` and ``nodeidentifier`` use, and
   ``rdfs:Resource``, which marks a type whose values are nodes.
2. A type whose datatype is ``xsd:anyURI`` and that is ``uri`` or ``uriorcurie``
   from ``linkml:types``, or is derived from one of them, has IRIs.
3. Every other type has literals of its datatype. That includes a type derived
   from ``string`` with ``uri: xsd:anyURI``: a URI reference held as text, which
   may be relative (XSD 1.1 Part 2 §3.3.17), whereas an RDF IRI must be absolute
   (RDF 1.1 Concepts §3.2).

>>> from linkml_runtime.utils.schemaview import SchemaView
>>> sv = SchemaView('''
... id: https://example.org/t
... name: t
... prefixes:
...   linkml: https://w3id.org/linkml/
...   ex: https://example.org/t/
... default_prefix: ex
... imports: [linkml:types]
... types:
...   ImageLink:
...     typeof: uri
...   FilePath:
...     typeof: string
...     uri: xsd:anyURI
... ''')
>>> type_term(sv, "uri")
TypeTerm(kind=<TermKind.IRI: 'iri'>, datatype=None)
>>> type_term(sv, "ImageLink").kind
<TermKind.IRI: 'iri'>
>>> type_term(sv, "FilePath")
TypeTerm(kind=<TermKind.LITERAL: 'literal'>, datatype='http://www.w3.org/2001/XMLSchema#anyURI')
>>> type_term(sv, "nodeidentifier").kind
<TermKind.BLANK_NODE_OR_IRI: 'nonliteral'>
>>> value_term(sv, "ImageLink", "ex:me.jpg")
rdflib.term.URIRef('https://example.org/t/me.jpg')
>>> value_term(sv, "FilePath", "./docs/cv.pdf")
rdflib.term.Literal('./docs/cv.pdf', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#anyURI'))
"""

import re
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from rdflib import RDFS, XSD, BNode, Literal, URIRef
from rdflib.term import Node

from linkml_runtime.linkml_model.types import SHEX
from linkml_runtime.utils.schemaview import SchemaView


class TermKind(Enum):
    """The kind of RDF term a value becomes (RDF 1.1 Concepts §3.1)."""

    IRI = "iri"
    BLANK_NODE = "bnode"
    BLANK_NODE_OR_IRI = "nonliteral"
    LITERAL = "literal"

    @property
    def is_node(self) -> bool:
        """Whether values of this kind are nodes (IRIs or blank nodes) rather than literals."""
        return self is not TermKind.LITERAL


# Datatype IRIs that name a kind of node rather than a literal datatype. ShEx
# spells the non-literal kind ``nonliteral``; ``linkml:types`` declares
# ``nodeidentifier`` with ``shex:nonLiteral``, so both spellings are listed.
NODE_KINDS: dict[str, TermKind] = {
    str(SHEX.iri): TermKind.IRI,
    str(SHEX.bnode): TermKind.BLANK_NODE,
    str(SHEX.nonliteral): TermKind.BLANK_NODE_OR_IRI,
    str(SHEX.nonLiteral): TermKind.BLANK_NODE_OR_IRI,
    str(RDFS.Resource): TermKind.BLANK_NODE_OR_IRI,
}

# The types of ``linkml:types`` whose values are IRIs, with the Python base their
# definitions declare. A link root is matched by name and definition: the name
# alone would admit a user type that happens to be called ``uri``, and
# ``from_schema`` cannot be used because merging imports rewrites it.
LINK_ROOTS: dict[str, str] = {"uri": "URI", "uriorcurie": "URIorCURIE"}

# The vocabularies the built-in datatypes and the node kinds above come from.
# A schema may use their usual prefixes without declaring them; a declaration
# in the schema takes precedence.
VOCABULARY_PREFIXES: dict[str, str] = {"xsd": str(XSD), "shex": str(SHEX), "rdfs": str(RDFS)}

# RFC 3986 §3.1: an absolute URI starts with a scheme followed by ":".
_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


@dataclass(frozen=True)
class TypeTerm:
    """The RDF term kind of a type's values and, for literals, their datatype IRI."""

    kind: TermKind
    datatype: str | None = None


def _expand(sv: SchemaView, uri: str, type_name: str) -> str:
    """Expand the datatype *uri* of *type_name*, a CURIE or an IRI, with the schema's prefixes.

    A declared prefix is expanded even when the local part contains a colon, which
    ``SchemaView.expand_curie`` leaves alone. An IRI is recognised by ``://``; one of
    another form, such as ``urn:``, needs its scheme declared as a prefix.

    :raises ValueError: if the prefix is neither declared nor one of :data:`VOCABULARY_PREFIXES`
    """
    if "://" in uri:
        return uri
    prefix, _, local = uri.partition(":")
    namespaces = sv.namespaces()
    if prefix in namespaces:
        return str(namespaces[prefix]) + local
    if prefix in VOCABULARY_PREFIXES:
        return VOCABULARY_PREFIXES[prefix] + local
    raise ValueError(f"Type {type_name!r} has datatype {uri!r}, but the schema does not declare prefix {prefix!r}")


def expanded_datatype(sv: SchemaView, type_name: str) -> str | None:
    """Return the expanded IRI of the datatype that *type_name* declares or inherits.

    :raises ValueError: if the datatype is a CURIE whose prefix the schema does not declare
    """
    uri = sv.induced_type(type_name).uri
    return _expand(sv, uri, type_name) if uri else None


@lru_cache(maxsize=4096)
def link_root(sv: SchemaView, type_name: str) -> str | None:
    """Return the link root of ``linkml:types`` that *type_name* is or derives from, else ``None``.

    The link roots are ``uri``, whose values are complete URIs, and ``uriorcurie``,
    whose values may be written as CURIEs. A root is matched by name and definition
    (:data:`LINK_ROOTS`), through the ``typeof`` chain.
    """
    for ancestor_name in sv.type_ancestors(type_name, reflexive=True):
        base = LINK_ROOTS.get(ancestor_name)
        if base is None:
            continue
        ancestor = sv.get_type(ancestor_name)
        if (
            ancestor.typeof is None
            and ancestor.base == base
            and ancestor.uri is not None
            and _expand(sv, ancestor.uri, ancestor_name) == str(XSD.anyURI)
        ):
            return ancestor_name
    return None


@lru_cache(maxsize=4096)
def type_term(sv: SchemaView, type_name: str) -> TypeTerm:
    """Return the RDF term kind of the values of the type *type_name* (see the module rules).

    :raises ValueError: if the type's datatype uses an undeclared prefix
    """
    datatype = expanded_datatype(sv, type_name)
    if datatype in NODE_KINDS:
        return TypeTerm(NODE_KINDS[datatype])
    if datatype == str(XSD.anyURI) and link_root(sv, type_name) is not None:
        return TypeTerm(TermKind.IRI)
    return TypeTerm(TermKind.LITERAL, datatype)


def value_term(sv: SchemaView, type_name: str, value: Any) -> Node:
    """Return the RDF term for *value* of the type *type_name*.

    IRIs are expanded from CURIEs. A value of a node type may name a blank node
    (``_:b1``) when its kind allows blank nodes. A literal keeps the Python value,
    so rdflib writes its canonical lexical form (``True`` becomes ``"true"``);
    ``xsd:string`` values become plain literals, which RDF 1.1 gives that datatype.

    :raises ValueError: if a value of an IRI type is a relative reference, which
        cannot be an RDF IRI (RDF 1.1 Concepts §3.2)
    """
    term = type_term(sv, type_name)
    if not term.kind.is_node:
        if term.datatype is None or term.datatype == str(XSD.string):
            return Literal(value)
        return Literal(value, datatype=URIRef(term.datatype))
    text = str(value)
    if text.startswith("_:") and term.kind in (TermKind.BLANK_NODE, TermKind.BLANK_NODE_OR_IRI):
        return BNode(text[2:])
    if term.kind is TermKind.BLANK_NODE:
        raise ValueError(f"Value {text!r} of type {type_name!r} must be a blank node label such as '_:b1'")
    if text.startswith("_:"):
        raise ValueError(f"Value {text!r} of type {type_name!r} is a blank node, but values of this type are IRIs")
    iri = sv.expand_curie(text)
    if not _SCHEME.match(iri):
        raise ValueError(
            f"Value {text!r} of type {type_name!r} is a relative reference, but values of this type are "
            "IRIs, which must be absolute. Use a type derived from string with uri: xsd:anyURI to keep "
            "URI references as text."
        )
    return URIRef(iri)
