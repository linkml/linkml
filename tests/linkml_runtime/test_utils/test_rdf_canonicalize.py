"""Tests for deterministic RDF serialization via pyoxigraph RDFC-1.0."""

import subprocess
import sys
import textwrap

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


def test_iri_with_trailing_dot_round_trips():
    """IRIs whose local part ends in '.' are emitted as full <IRI> form so rdflib can parse them.

    pyoxigraph emits ``prefix:local\\.`` per the Turtle PN_LOCAL_ESC rule,
    but rdflib's notation3 parser rejects an escaped dot at the end of a
    PN_LOCAL.  The serializer rewrites such CURIEs to full IRI form to
    preserve round-trip parseability.
    """
    g = Graph()
    g.bind("ex", "http://example.com/vocab/")
    iri = URIRef("http://example.com/vocab/Strand#.")
    g.add((iri, RDF.type, URIRef("http://example.com/vocab/Thing")))
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    # CURIE form with trailing escaped dot must not appear; full IRI must
    assert "ex:Strand\\#\\." not in ttl
    assert "<http://example.com/vocab/Strand#.>" in ttl
    g2 = Graph()
    g2.parse(data=ttl, format="turtle")
    assert rdflib.compare.isomorphic(g, g2)


def test_sort_is_load_bearing():
    """Output is byte-identical across subprocesses with different PYTHONHASHSEED values.

    RDFC-1.0 stabilizes blank-node labels, but pyoxigraph's ``Dataset`` iteration
    order is not lexicographic and varies across processes. Without the explicit
    sort step in ``canonicalize_rdf_graph``, output would differ across runs in
    ways that hash randomization can expose. This test runs the canonicalization
    in two subprocesses with deliberately different hash seeds and asserts the
    output is identical, guarding against accidental removal of the sort step or
    introduction of ``id()``-keyed iteration anywhere in the path.
    """
    program = textwrap.dedent(
        """
        from rdflib import BNode, Graph, Literal, URIRef
        from rdflib.namespace import RDF
        from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph

        g = Graph()
        g.bind("ex", "http://example.com/")
        for letter in ["z", "y", "x", "m", "f", "a"]:
            s = URIRef(f"http://example.com/{letter}")
            g.add((s, RDF.type, URIRef("http://example.com/Thing")))
            g.add((s, URIRef("http://example.com/p"), Literal(f"val_{letter}")))
        for i in range(3):
            bn = BNode()
            g.add((URIRef("http://example.com/x"), URIRef("http://example.com/has"), bn))
            g.add((bn, URIRef("http://example.com/q"), Literal(f"bn_{i}")))

        print(canonicalize_rdf_graph(g, output_format="turtle"), end="")
        """
    )

    def run(seed: str) -> str:
        env = {"PYTHONHASHSEED": seed, "PATH": "/usr/bin:/bin"}
        result = subprocess.run(
            [sys.executable, "-c", program],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        return result.stdout

    out_a = run("0")
    out_b = run("42")
    assert out_a == out_b, "Canonical output differs across PYTHONHASHSEED values; sort step may be missing"


def test_fallback_on_invalid_rdf():
    """Graphs with literal predicates fall back to rdflib serializer."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    # Add a triple with a Literal predicate (non-standard RDF)
    g.add((URIRef("http://example.com/s"), Literal("not_a_predicate"), Literal("value")))
    # Should not raise, falls back to rdflib
    result = canonicalize_rdf_graph(g, output_format="turtle")
    assert "not_a_predicate" in result
