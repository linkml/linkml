"""Unit / regression tests for owlgen bug-fixes.

Covers:
- Fix 1: equals_string on an enum-ranged slot (is_literal=None) must not silently
  drop the constraint; it should produce an owl:oneOf expression with a Literal.
- Fix 2: _complement_of_union_of must filter None operands instead of passing them
  to rdflib.Graph.add(), which raises an AssertionError.
"""

import os

import pytest
from rdflib import OWL, RDF, Graph, Literal, URIRef
from rdflib.collection import Collection

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml_runtime.utils.schema_builder import SchemaBuilder


def _input_path(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "input", name)


def _owl_graph(sb: SchemaBuilder, **gen_kwargs) -> Graph:
    gen = OwlSchemaGenerator(sb.schema, mergeimports=False, metaclasses=False, type_objects=False, **gen_kwargs)
    g = Graph()
    g.parse(data=gen.serialize(), format="turtle")
    return g


def _literal_values_in_complement_filler(g: Graph) -> set[str]:
    """Return all literal values inside datatypeComplementOf owl:oneOf fillers.

    The fix produces: neg_expr owl:datatypeComplementOf [a rdfs:Datatype; owl:oneOf ("Red")].
    We traverse: datatypeComplementOf → filler → owl:oneOf → RDF list → literals.
    """
    values: set[str] = set()
    for filler in g.objects(None, OWL.datatypeComplementOf):
        for list_node in g.objects(filler, OWL.oneOf):
            try:
                for v in Collection(g, list_node):
                    if isinstance(v, Literal):
                        values.add(str(v))
            except Exception:
                pass
    return values


# Fix 1 — equals_string on an enum-ranged slot must not be silently dropped


def test_equals_string_enum_none_of_no_crash():
    """Regression: gen-owl on owlgen/slot_conditions.yaml must not raise an AssertionError.

    The bug was that equals_string on an enum-ranged slot produced is_literal=None,
    which caused the constraint to be dropped, leaving None in the expression list
    and ultimately triggering rdflib's assertion inside graph.add().
    """
    owl = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml")).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    # Schema parses without error and the Item class is present.
    assert any(str(s).endswith("Item") for s, _, _ in g.triples((None, RDF.type, OWL.Class)))


def test_equals_string_enum_slot_emits_one_of_literal():
    """equals_string on an enum-ranged slot must produce an owl:oneOf with a Literal.

    Before the fix, is_literal=None caused a warning and the expression was skipped.
    After the fix, the value is treated like equals_string_in (single-item list).
    """
    owl = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml")).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    assert "Red" in _literal_values_in_complement_filler(g), (
        "Expected owl:oneOf with literal 'Red' for equals_string on enum-ranged slot"
    )


def test_equals_string_enum_produces_complement_expression():
    """A none_of rule using equals_string on an enum slot must produce a complement axiom.

    The complement (owl:complementOf / owl:datatypeComplementOf) wraps the oneOf
    expression, expressing "value is not Red".
    """
    owl = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml")).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    # There must be at least one owl:datatypeComplementOf or owl:complementOf triple.
    complement_triples = list(g.triples((None, OWL.datatypeComplementOf, None))) + list(
        g.triples((None, OWL.complementOf, None))
    )
    assert complement_triples, "Expected an owl:complementOf/datatypeComplementOf axiom from none_of rule"


# Fix 2 — _complement_of_union_of must handle None operands gracefully


def test_complement_of_union_of_filters_none(caplog):
    """_complement_of_union_of([None]) must return None and log a warning, not crash.

    Without the guard, [None] is passed to _union_of which propagates None into
    graph.add(), raising an AssertionError from rdflib.
    """
    import logging

    gen = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml"))
    gen.as_graph()  # initialises self.graph

    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        result = gen._complement_of_union_of([None])

    assert result is None, "_complement_of_union_of([None]) should return None"
    assert any("None" in rec.message or "complement" in rec.message.lower() for rec in caplog.records), (
        "Expected a warning about unresolvable complement operands"
    )


@pytest.mark.parametrize(
    "exprs,expect_none",
    [
        ([None], True),
        ([None, None], True),
    ],
)
def test_complement_of_union_of_all_none_returns_none(exprs, expect_none):
    """_complement_of_union_of with only None operands must return None without crashing."""
    gen = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml"))
    gen.as_graph()
    result = gen._complement_of_union_of(exprs)
    assert (result is None) == expect_none


def test_complement_of_union_of_mixed_none_filters_silently():
    """_complement_of_union_of with some valid and some None operands uses only valid ones."""
    from rdflib import BNode

    gen = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml"))
    gen.as_graph()
    valid_node = URIRef("http://example.org/Foo")
    result = gen._complement_of_union_of([None, valid_node])
    # Should succeed and return a BNode (the complement expression).
    assert result is not None
    assert isinstance(result, BNode)
