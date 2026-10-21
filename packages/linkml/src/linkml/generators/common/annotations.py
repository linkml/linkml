"""RDF terms of annotation values that a metamodel extension declares.

A schema element can ``instantiates`` a metaclass whose slots describe the
element's annotations (LinkML specification, part 5, "Metamodel refinement using
annotations"). Such a slot gives an annotation value its RDF term by the rule
that applies to slot values (:mod:`linkml_runtime.utils.rdf_terms`): a value of
``nodeidentifier`` or ``uri`` is a node, a value of ``string`` is text, a value
of a type derived from ``string`` with ``uri: xsd:anyURI`` is an ``xsd:anyURI``
literal, and so on. OWL 2 admits IRIs, anonymous individuals and literals as
annotation values (OWL 2 Structural Specification §10.1), so no annotation value
needs a term of another kind.

>>> from linkml_runtime.utils.schemaview import SchemaView
>>> sv = SchemaView('''
... id: https://example.org/m
... name: m
... prefixes: {ex: https://example.org/m/, linkml: https://w3id.org/linkml/}
... default_prefix: ex
... imports: [linkml:types]
... classes:
...   Reviewable:
...     attributes:
...       reviewer: {range: nodeidentifier}
...       review: {range: string}
...   Person:
...     instantiates: [ex:Reviewable]
...     annotations: {reviewer: ex:alice, review: well defined}
... ''')
>>> person = sv.get_class("Person")
>>> declared_annotation(sv, person, "reviewer", "ex:alice")
DeclaredAnnotation(predicate=rdflib.term.URIRef('https://example.org/m/reviewer'), value=rdflib.term.URIRef('https://example.org/m/alice'))
>>> declared_annotation(sv, person, "review", "well defined", language="en").value
rdflib.term.Literal('well defined', lang='en')
>>> declared_annotation(sv, person, "undeclared", "x") is None
True
"""

from dataclasses import dataclass, field
from typing import Any

from rdflib import BNode, Literal, URIRef

from linkml_runtime.linkml_model.meta import Element, PermissibleValue, SlotDefinition
from linkml_runtime.utils.rdf_terms import value_term
from linkml_runtime.utils.schemaview import SchemaView


@dataclass(frozen=True)
class DeclaredAnnotation:
    """The RDF predicate and value of an annotation, and the metaclass slot that declares it."""

    predicate: URIRef
    value: URIRef | BNode | Literal
    slot: SlotDefinition = field(compare=False, hash=False, repr=False)


def declaring_slots(sv: SchemaView, element: Element | PermissibleValue, tag: str) -> list[SlotDefinition]:
    """Return the slots of the metaclasses that *element* instantiates which declare annotation *tag*.

    A metaclass is referenced by its class URI. A tag matches a slot by name or,
    as a CURIE or IRI, by the slot's URI. Inherited and imported slots count.
    """
    expanded_tag = sv.expand_curie(tag)
    slots: list[SlotDefinition] = []
    for reference in element.instantiates:
        metaclass_uri = sv.expand_curie(reference)
        for cls in sv.all_classes().values():
            if sv.get_uri(cls, expand=True) != metaclass_uri:
                continue
            for slot in sv.class_induced_slots(cls.name):
                if slot.name == tag or sv.get_uri(slot, expand=True) == expanded_tag:
                    slots.append(slot)
    return slots


def annotation_term(
    sv: SchemaView, slot: SlotDefinition, value: Any, language: str | None = None
) -> URIRef | BNode | Literal | None:
    """Return the RDF term of annotation *value* according to the range of the declaring *slot*.

    A type range gives the term of a slot value of that type; text, which is a
    plain literal of a type derived from ``string``, carries *language* when one is
    set. An enum range gives the permissible value's text as a plain literal, since
    it is an identifier rather than text. Any other range, such as a class, declares
    no scalar term, and the result is ``None``.

    :raises ValueError: if *value* cannot be a term of the declared kind, for
        example a relative reference for a ``uri`` slot
    """
    if slot.range in sv.all_types():
        term = value_term(sv, slot.range, value)
        is_text = isinstance(term, Literal) and term.datatype is None and "string" in sv.type_ancestors(slot.range)
        return Literal(value, lang=language) if language and is_text else term
    if slot.range in sv.all_enums():
        return Literal(str(value))
    return None


def declared_annotation(
    sv: SchemaView, element: Element | PermissibleValue, tag: str, value: Any, language: str | None = None
) -> DeclaredAnnotation | None:
    """Return the predicate and term of annotation *tag* on *element* if a metaclass declares it.

    The result is ``None`` when no metaclass of *element* declares the tag, when the
    value is not a scalar, or when the declaring slot has no scalar range; the
    caller then keeps its undeclared-annotation behaviour.

    :raises ValueError: if the metaclasses declare the tag with different terms, or
        if the value cannot be a term of the declared kind
    """
    if not isinstance(value, str | bool | int | float):
        return None
    declared: set[DeclaredAnnotation] = set()
    for slot in declaring_slots(sv, element, tag):
        term = annotation_term(sv, slot, value, language)
        if term is not None:
            declared.add(DeclaredAnnotation(URIRef(sv.get_uri(slot, expand=True)), term, slot))
    if len(declared) > 1:
        metaclasses = ", ".join(element.instantiates)
        raise ValueError(f"The metaclasses {metaclasses} declare annotation {tag!r} with different terms")
    return declared.pop() if declared else None
