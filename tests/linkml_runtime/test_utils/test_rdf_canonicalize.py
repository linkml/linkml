"""Tests for deterministic RDF serialization via pyoxigraph RDFC-1.0."""

import rdflib
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF

from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph


def _make_graph_with_bnodes() -> Graph:
    """Create a graph with blank nodes for testing."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    subj = URIRef("http://example.com/a")
    bn = BNode()
    g.add((subj, URIRef("http://example.com/p"), Literal("hello")))
    g.add((subj, URIRef("http://example.com/r"), bn))
    g.add((bn, URIRef("http://example.com/q"), Literal("blank_val")))
    return g


def test_determinism():
    """Same graph serialized multiple times produces byte-identical output."""
    g = _make_graph_with_bnodes()
    results = [canonicalize_rdf_graph(g, output_format="turtle") for _ in range(5)]
    assert all(r == results[0] for r in results), "Output was not deterministic across runs"


def test_round_trip_isomorphic():
    """Re-parsing canonicalized output produces an isomorphic graph."""
    g = _make_graph_with_bnodes()
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    g2 = Graph()
    g2.parse(data=ttl, format="turtle")
    assert rdflib.compare.isomorphic(g, g2), "Round-tripped graph is not isomorphic to original"


def test_blank_node_stability():
    """Blank node labels are stable across calls."""
    g = _make_graph_with_bnodes()
    out1 = canonicalize_rdf_graph(g, output_format="turtle")
    out2 = canonicalize_rdf_graph(g, output_format="turtle")
    assert out1 == out2, "Blank node labels differ between calls"


def test_prefix_preservation():
    """Output Turtle contains expected @prefix declarations."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.bind("foaf", "http://xmlns.com/foaf/0.1/")
    g.add((URIRef("http://example.com/a"), URIRef("http://xmlns.com/foaf/0.1/name"), Literal("Alice")))
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    assert "@prefix ex:" in ttl
    assert "@prefix foaf:" in ttl


def test_ntriples_format():
    """N-Triples output is deterministic."""
    g = _make_graph_with_bnodes()
    results = [canonicalize_rdf_graph(g, output_format="nt") for _ in range(5)]
    assert all(r == results[0] for r in results)
    # N-Triples should not contain @prefix
    assert "@prefix" not in results[0]


def test_empty_graph():
    """Empty graph produces valid empty output."""
    g = Graph()
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    # Re-parsing should also be empty
    g2 = Graph()
    g2.parse(data=ttl, format="turtle")
    assert len(g2) == 0


def test_ordering_is_sorted():
    """Subjects appear in sorted order in the output."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.add((URIRef("http://example.com/z"), RDF.type, URIRef("http://example.com/Thing")))
    g.add((URIRef("http://example.com/a"), RDF.type, URIRef("http://example.com/Thing")))
    g.add((URIRef("http://example.com/m"), RDF.type, URIRef("http://example.com/Thing")))
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    # Find positions of subjects in the output
    pos_a = ttl.index("ex:a")
    pos_m = ttl.index("ex:m")
    pos_z = ttl.index("ex:z")
    assert pos_a < pos_m < pos_z, f"Subjects not in sorted order: a@{pos_a}, m@{pos_m}, z@{pos_z}"


def test_multiple_blank_nodes_deterministic():
    """Multiple blank nodes are canonicalized deterministically."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    subj = URIRef("http://example.com/s")
    bn1 = BNode()
    bn2 = BNode()
    g.add((subj, URIRef("http://example.com/p"), bn1))
    g.add((subj, URIRef("http://example.com/q"), bn2))
    g.add((bn1, URIRef("http://example.com/val"), Literal("first")))
    g.add((bn2, URIRef("http://example.com/val"), Literal("second")))
    results = [canonicalize_rdf_graph(g, output_format="turtle") for _ in range(5)]
    assert all(r == results[0] for r in results)


def test_xsd_string_normalized():
    """pyoxigraph drops explicit ^^xsd:string per RDF 1.1; output is still semantically correct."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    XSD = rdflib.Namespace("http://www.w3.org/2001/XMLSchema#")
    g.add((URIRef("http://example.com/a"), URIRef("http://example.com/p"), Literal("hello", datatype=XSD.string)))
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    # pyoxigraph writes plain "hello" without ^^xsd:string
    assert "xsd:string" not in ttl
    # The triple is still present (rdflib reads it back as untyped Literal)
    g2 = Graph()
    g2.parse(data=ttl, format="turtle")
    assert len(g2) == 1
    obj = list(g2.objects())[0]
    assert str(obj) == "hello"


def test_fallback_on_invalid_rdf():
    """Graphs with literal predicates fall back to rdflib serializer."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    # Add a triple with a Literal predicate (non-standard RDF)
    g.add((URIRef("http://example.com/s"), Literal("not_a_predicate"), Literal("value")))
    # Should not raise, falls back to rdflib
    result = canonicalize_rdf_graph(g, output_format="turtle")
    assert "not_a_predicate" in result
