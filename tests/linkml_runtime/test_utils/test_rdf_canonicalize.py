"""Tests for deterministic RDF serialization via pyoxigraph RDFC-1.0."""

import os
import re
import subprocess
import sys
import textwrap

import pyoxigraph as ox
import pytest
import rdflib
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF

from linkml_runtime.utils import rdf_canonicalize as rdf_canon_mod
from linkml_runtime.utils.rdf_canonicalize import (
    RDFCanonicalizationWarning,
    canonicalize_rdf_graph,
)


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


def test_curie_shaped_substring_in_literal_not_rewritten():
    """A CURIE-shape with a trailing escaped dot inside a string literal must not be rewritten.

    The pyoxigraph Turtle emitter writes literals containing a backslash as
    ``\\\\``, so a literal whose text is ``see ex:other\\. for context`` appears
    in the serialization as ``"see ex:other\\\\. for context"``. The naive
    regex used to expand trailing-dot CURIEs would false-match the
    ``ex:other\\.`` substring inside the literal, mangle it into ``<...>``
    form, and produce un-parseable Turtle. The tokenizer-aware helper must
    skip ranges that are inside string literals.
    """
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.add(
        (
            URIRef("http://example.com/a"),
            URIRef("http://example.com/note"),
            Literal("see ex:other\\. for context"),
        )
    )
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    # The literal must be preserved verbatim — no `<http://example.com/other...>` rewrite.
    assert "<http://example.com/other" not in ttl
    # And the file must round-trip through rdflib without parse errors.
    g2 = Graph()
    g2.parse(data=ttl, format="turtle")
    assert rdflib.compare.isomorphic(g, g2)


def test_curie_shaped_substring_in_multiline_literal_not_rewritten():
    """Same protection applies to literals across multiple physical lines."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.add(
        (
            URIRef("http://example.com/a"),
            URIRef("http://example.com/note"),
            Literal("line one\nex:bar\\. then more\nline three"),
        )
    )
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    assert "<http://example.com/bar" not in ttl
    g2 = Graph()
    g2.parse(data=ttl, format="turtle")
    assert rdflib.compare.isomorphic(g, g2)


def test_curie_in_literal_with_hash_not_treated_as_comment():
    """A literal containing ``#`` must not cause the tokenizer to treat the rest as a comment.

    The structural-span walker treats ``#`` as a comment opener only outside
    of string literals. This test pins that behavior: a literal containing
    a ``#`` character followed by a CURIE-shape must not lose any content
    in the round-trip.
    """
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.add(
        (
            URIRef("http://example.com/a"),
            URIRef("http://example.com/note"),
            Literal("hash inside: #foo then ex:bar\\. more"),
        )
    )
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    g2 = Graph()
    g2.parse(data=ttl, format="turtle")
    assert rdflib.compare.isomorphic(g, g2)
    # Round-trip the literal text exactly.
    obj = list(g2.objects())[0]
    assert "#foo" in str(obj)
    assert "ex:bar\\. more" in str(obj)


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
        env = {**os.environ, "PYTHONHASHSEED": seed}
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


def test_invalid_prefix_iri_is_swallowed_and_falls_back(monkeypatch):
    """When pyoxigraph rejects a prefix IRI, we serialize without prefixes and warn.

    The fallback path is intentional — pyoxigraph 0.5.x raises a ``ValueError``
    starting with ``Invalid prefix`` for namespace IRIs containing characters
    it considers illegal. Rather than fail the whole serialization, the
    helper drops prefix declarations, retries, and emits a
    ``RDFCanonicalizationWarning`` so the user knows the output is more
    verbose than usual.

    Note: the prefix filter (item #5) drops *unused* prefixes before they
    reach pyoxigraph, so triggering the rejection in real usage requires the
    bad prefix to also be referenced by an IRI — a corner of the input
    surface this test simulates with a monkeypatch on the first
    ``ox.serialize`` call.
    """
    real_serialize = ox.serialize
    calls = {"n": 0}

    def fake_serialize(*args, **kwargs):
        calls["n"] += 1
        # First call (with prefixes) raises the pyoxigraph "Invalid prefix"
        # complaint; the fallback path should retry without prefixes.
        if calls["n"] == 1 and kwargs.get("prefixes"):
            raise ValueError("Invalid prefix bad IRI 'http://example.com/ has space/', Invalid IRI code point ' '")
        return real_serialize(*args, **kwargs)

    monkeypatch.setattr(rdf_canon_mod.ox, "serialize", fake_serialize)

    g = Graph()
    g.bind("ex", "http://example.com/")
    g.add((URIRef("http://example.com/a"), RDF.type, URIRef("http://example.com/Thing")))

    with pytest.warns(RDFCanonicalizationWarning, match="rejected one or more prefix IRIs"):
        ttl = canonicalize_rdf_graph(g, output_format="turtle")
    # Fallback retry should succeed and the output still round-trips.
    g2 = Graph()
    g2.parse(data=ttl, format="turtle")
    assert rdflib.compare.isomorphic(g, g2)


def test_unsupported_format_warns_and_falls_back():
    """A format pyoxigraph doesn't know about falls back to rdflib with a warning."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.add((URIRef("http://example.com/a"), RDF.type, URIRef("http://example.com/Thing")))
    with pytest.warns(RDFCanonicalizationWarning, match="does not support format"):
        result = canonicalize_rdf_graph(g, output_format="json-ld")
    # The fallback should still produce valid output in the requested format.
    assert result


def test_unrelated_value_error_propagates(monkeypatch):
    """Any ``ValueError`` whose message doesn't begin with ``Invalid prefix`` is re-raised.

    Guards against future regressions where a pyoxigraph serializer bug
    raises a different ``ValueError`` and gets silently swallowed by the
    invalid-prefix fallback path.
    """
    real_serialize = ox.serialize
    calls = {"count": 0}

    def fake_serialize(*args, **kwargs):
        calls["count"] += 1
        # First call is the prefixed serialize — raise an unrelated ValueError.
        if calls["count"] == 1:
            raise ValueError("Invalid base IRI 'broken', Invalid IRI code point ' '")
        return real_serialize(*args, **kwargs)

    monkeypatch.setattr(rdf_canon_mod.ox, "serialize", fake_serialize)

    g = Graph()
    g.bind("ex", "http://example.com/")
    g.add((URIRef("http://example.com/a"), RDF.type, URIRef("http://example.com/Thing")))

    with pytest.raises(ValueError, match="Invalid base IRI"):
        canonicalize_rdf_graph(g, output_format="turtle")


def test_unused_prefixes_are_dropped():
    """Prefixes bound on the graph but not referenced by any IRI must not appear in the output.

    rdflib's NamespaceManager auto-binds ~30 well-known vocabularies (foaf,
    skos, dcterms, etc.) on every Graph. Passing all of them to pyoxigraph
    means every serialized file gets padded with @prefix declarations that
    are never used in the body. The canonicalizer filters these out.
    """
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.bind("foaf", "http://xmlns.com/foaf/0.1/")  # bound but not used
    g.bind("skos", "http://www.w3.org/2004/02/skos/core#")  # bound but not used
    g.add((URIRef("http://example.com/a"), RDF.type, URIRef("http://example.com/Thing")))
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    assert "@prefix ex:" in ttl
    assert "@prefix foaf:" not in ttl, "unused foaf prefix should be filtered out"
    assert "@prefix skos:" not in ttl, "unused skos prefix should be filtered out"


def test_used_prefix_with_parent_namespace_is_kept():
    """A prefix is kept when an IRI starts with its namespace, not only on exact match."""
    g = Graph()
    # Use a name that doesn't collide with rdflib's auto-bound `schema` →
    # `https://schema.org/`. The point of the test is the startswith match
    # against an IRI that extends the namespace, not the prefix name.
    g.bind("myorg", "http://my.example.org/vocab/")
    g.add(
        (
            URIRef("http://my.example.org/vocab/Person"),
            RDF.type,
            URIRef("http://www.w3.org/2002/07/owl#Class"),
        )
    )
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    assert "@prefix myorg:" in ttl
    assert "myorg:Person" in ttl


def test_prefix_referenced_only_by_literal_datatype_is_kept():
    """A prefix is kept when its namespace appears only as a literal datatype IRI."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.bind("custom", "http://custom.example.org/types/")
    g.add(
        (
            URIRef("http://example.com/a"),
            URIRef("http://example.com/value"),
            Literal("123", datatype=URIRef("http://custom.example.org/types/MyInt")),
        )
    )
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    assert "@prefix custom:" in ttl


def test_default_namespace_manager_prefixes_dont_bloat_output():
    """Tutorial-style minimal graph stays minimal — no auto-bound vocabularies leak through."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    g.add((URIRef("http://example.com/a"), RDF.type, URIRef("http://example.com/Thing")))
    ttl = canonicalize_rdf_graph(g, output_format="turtle")
    # Only @prefix ex: and possibly @prefix rdf: (used for `a`/`rdf:type`)
    # should appear. Inspect declared prefixes against actually-referenced ones.
    declared = set(re.findall(r"@prefix (\w+):", ttl))
    # rdf is referenced through `a` (rdf:type shortcut) — pyoxigraph may or
    # may not emit the explicit prefix; allow it but don't require it.
    assert declared.issubset({"ex", "rdf"}), f"Unexpected prefixes declared: {declared}"
    assert "ex" in declared


def test_fallback_on_invalid_rdf():
    """Graphs with literal predicates fall back to rdflib serializer and emit a warning."""
    g = Graph()
    g.bind("ex", "http://example.com/")
    # Add a triple with a Literal predicate (non-standard RDF)
    g.add((URIRef("http://example.com/s"), Literal("not_a_predicate"), Literal("value")))
    # Should not raise, falls back to rdflib, and surfaces a warning so users
    # know the output is no longer canonicalized.
    with pytest.warns(RDFCanonicalizationWarning, match="non-standard RDF"):
        result = canonicalize_rdf_graph(g, output_format="turtle")
    assert "not_a_predicate" in result


# --- stable (content-hash) blank-node labels -------------------------------


def _label_of(ttl: str, literal_text: str) -> str:
    """Return the blank-node label on the line carrying ``literal_text``."""
    import re

    for line in ttl.splitlines():
        if f'"{literal_text}"' in line:
            m = re.search(r"_:[A-Za-z0-9_]+", line)
            if m:
                return m.group(0)
    raise AssertionError(f"no blank-node label found for {literal_text!r}")


def test_stable_labels_are_content_hashed():
    """Opt-in labels are content hashes (``_:b...``), not ordinal (``_:c14n...``)."""
    g = _make_graph_with_bnodes()
    ttl = canonicalize_rdf_graph(g, output_format="turtle", stable_blank_node_labels=True)
    assert "_:c14n" not in ttl
    assert _label_of(ttl, "blank_val").startswith("_:b")


def test_stable_labels_isomorphic_to_default():
    """Relabeling changes only blank-node identifiers, never the graph."""
    g = _make_graph_with_bnodes()
    default = canonicalize_rdf_graph(g, output_format="turtle")
    hashed = canonicalize_rdf_graph(g, output_format="turtle", stable_blank_node_labels=True)
    g_default = Graph().parse(data=default, format="turtle")
    g_hashed = Graph().parse(data=hashed, format="turtle")
    assert rdflib.compare.isomorphic(g_default, g_hashed)


def test_stable_labels_deterministic():
    """Content-hash labels are byte-identical across calls."""
    g = _make_graph_with_bnodes()
    results = [canonicalize_rdf_graph(g, output_format="turtle", stable_blank_node_labels=True) for _ in range(5)]
    assert all(r == results[0] for r in results)


def test_stable_labels_change_locality():
    """Adding an unrelated blank-node subtree leaves existing labels unchanged.

    This is the whole point: a blank node's label depends only on its own
    subtree content, so an unrelated insertion is diff-local.  RDFC-1.0's
    ordinal ``c14nN`` labels do not guarantee this.
    """
    q = URIRef("http://example.com/q")
    g1 = Graph()
    keep = BNode()
    g1.add((URIRef("http://example.com/a"), URIRef("http://example.com/r"), keep))
    g1.add((keep, q, Literal("keep")))

    g2 = Graph()
    for t in g1:
        g2.add(t)
    # An unrelated subject + blank node whose IRI sorts after ex:a.
    new = BNode()
    g2.add((URIRef("http://example.com/z"), URIRef("http://example.com/r"), new))
    g2.add((new, q, Literal("brand_new")))

    out1 = canonicalize_rdf_graph(g1, output_format="turtle", stable_blank_node_labels=True)
    out2 = canonicalize_rdf_graph(g2, output_format="turtle", stable_blank_node_labels=True)
    assert _label_of(out1, "keep") == _label_of(out2, "keep")


def test_stable_labels_automorphic_nodes_kept_distinct():
    """Two blank nodes with identical content stay distinct (no accidental merge)."""
    g = Graph()
    q = URIRef("http://example.com/q")
    for subj in ("a", "b"):
        bn = BNode()
        g.add((URIRef(f"http://example.com/{subj}"), URIRef("http://example.com/r"), bn))
        g.add((bn, q, Literal("same")))
    hashed = canonicalize_rdf_graph(g, output_format="turtle", stable_blank_node_labels=True)
    g_hashed = Graph().parse(data=hashed, format="turtle")
    assert len(g_hashed) == 4, "automorphic blank nodes were merged"
    assert rdflib.compare.isomorphic(g, g_hashed)


def test_stable_labels_cycle_falls_back():
    """Blank nodes in a cycle keep their c14n label (no infinite recursion)."""
    g = Graph()
    p = URIRef("http://example.com/p")
    bn1, bn2 = BNode(), BNode()
    g.add((bn1, p, bn2))
    g.add((bn2, p, bn1))
    g.add((URIRef("http://example.com/a"), URIRef("http://example.com/r"), bn1))
    hashed = canonicalize_rdf_graph(g, output_format="turtle", stable_blank_node_labels=True)
    # Cyclic nodes are left with ordinal labels rather than crashing/looping.
    assert "_:c14n" in hashed
    g_hashed = Graph().parse(data=hashed, format="turtle")
    assert rdflib.compare.isomorphic(g, g_hashed)


def test_stable_labels_stable_across_processes():
    """Content-hash labels are byte-identical across PYTHONHASHSEED values."""
    program = textwrap.dedent(
        """
        from rdflib import BNode, Graph, Literal, URIRef
        from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph

        g = Graph()
        g.bind("ex", "http://example.com/")
        for letter in ["z", "y", "x", "m", "f", "a"]:
            bn = BNode()
            g.add((URIRef(f"http://example.com/{letter}"), URIRef("http://example.com/has"), bn))
            g.add((bn, URIRef("http://example.com/q"), Literal(f"val_{letter}")))
        print(canonicalize_rdf_graph(g, output_format="turtle", stable_blank_node_labels=True), end="")
        """
    )

    def run(seed: str) -> str:
        env = {**os.environ, "PYTHONHASHSEED": seed}
        return subprocess.run(
            [sys.executable, "-c", program], check=True, capture_output=True, text=True, env=env
        ).stdout

    assert run("0") == run("42")
