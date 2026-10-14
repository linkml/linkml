"""Correctness properties of RDF canonicalization.

Each test asserts one property -- for example that a base IRI ending in ``#``
does not rewrite other IRIs, that a shared ``rdf:List`` tail is not
duplicated, or that output is byte-identical across processes.

Ported from linkml/linkml#3986 and #3987 (Carlo van Driesten), which recorded
these against both linkml's canonicalizer and the diffable-rdf library.
"""

import os
import subprocess
import sys
import textwrap
import warnings

import pytest
import rdflib
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF

from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph

EX = Namespace("http://example.org/")


def _apply(graph, output_format="turtle"):
    """Canonicalize, ignoring the warnings emitted on the fallback path."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return canonicalize_rdf_graph(graph, output_format)


# --------------------------------------------------------------------------
# Silent data corruption
# --------------------------------------------------------------------------


def test_base_with_a_fragment_does_not_rewrite_every_iri():
    """A base IRI ending in ``#`` must not change the graph's terms.

    Relativizing ``http://ex.org/d#a`` against base ``http://ex.org/d#`` gives
    ``<#a>``, which is correct per RFC 3986 -- but rdflib's parser resolves a
    fragment reference by concatenation and reads it back as
    ``http://ex.org/d##a``. Every term of the graph silently changes, and the
    output parses cleanly, so nothing reports it.
    """
    graph = Graph(base="http://ex.org/d#")
    graph.add((URIRef("http://ex.org/d#a"), EX.p, Literal("v")))

    round_tripped = Graph()
    round_tripped.parse(data=_apply(graph), format="turtle")

    assert {str(s) for s in round_tripped.subjects()} == {"http://ex.org/d#a"}


def test_a_shared_rdf_list_tail_is_not_duplicated():
    """Two lists sharing a tail must not gain triples on the way out.

    rdflib's Turtle writer renders ``( ... )`` collection syntax per list, so a
    tail referenced from two lists is written twice as two separate blank
    nodes. The result asserts more than the input did.
    """
    graph = Graph()
    graph.bind("ex", EX)
    tail = BNode()
    graph.add((tail, RDF.first, Literal("shared")))
    graph.add((tail, RDF.rest, RDF.nil))
    for name in ("l1", "l2"):
        head = BNode()
        graph.add((EX[name], EX.list, head))
        graph.add((head, RDF.first, Literal(name)))
        graph.add((head, RDF.rest, tail))
    # A relative IRI is non-standard RDF, so pyoxigraph refuses the graph and
    # both implementations degrade to rdflib -- the path this defect lives on.
    graph.add((URIRef("testing"), EX.p, Literal("forces-fallback")))

    round_tripped = Graph()
    round_tripped.parse(data=_apply(graph), format="turtle")

    assert len(round_tripped) == len(graph)


# --------------------------------------------------------------------------
# Output that no parser will read
# --------------------------------------------------------------------------


def test_nt_output_either_parses_or_refuses():
    """N-Triples admits only absolute IRIs, so a relative one must not be written.

    The fallback is taken *because* the graph holds a term pyoxigraph rejected.
    Writing it out anyway produces a file that fails on line 1. Refusing with a
    message naming the term and a format that can carry the graph is the fix;
    returning unreadable text is not.
    """
    graph = Graph()
    graph.add((URIRef("testing"), EX.p, Literal("v")))

    try:
        serialized = _apply(graph, "nt")
    except ValueError:
        return  # refused, with an explanation -- the correct outcome

    rdflib.Graph().parse(data=serialized, format="nt")


def test_a_unicode_line_separator_in_a_literal_survives():
    """Sorting N-Triples lines must split on newlines only.

    N-Triples permits U+2028 raw inside a quoted literal, but
    ``str.splitlines()`` breaks on it as well as on U+2029, U+0085, U+000B,
    U+000C and U+001C-1E. One statement becomes two lines, the halves sort
    independently, the separator is rewritten as a newline, and the document
    no longer parses.
    """
    graph = Graph()
    graph.add((EX.s, EX.p, Literal("a\u2028b")))
    graph.add((URIRef("testing"), EX.p, Literal("forces-fallback")))

    try:
        serialized = _apply(graph, "nt")
    except ValueError:
        return  # refused because of the relative IRI, before the sort

    assert "\u2028" in serialized
    rdflib.Graph().parse(data=serialized, format="nt")


# --------------------------------------------------------------------------
# Non-determinism, which is the property the module exists to provide
# --------------------------------------------------------------------------

_ACROSS_PROCESSES = textwrap.dedent(
    """
    import sys, warnings
    warnings.simplefilter("ignore")
    from rdflib import BNode, Graph, Literal, Namespace, URIRef
    from rdflib.namespace import RDF

    from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph

    output_format, force_fallback = sys.argv[1], sys.argv[2] == "1"

    EX = Namespace("http://example.org/")
    g = Graph()
    if force_fallback:
        g.add((URIRef("testing"), EX.p, Literal("forces-fallback")))
    for i in range(12):
        b = BNode()
        g.add((EX["s%02d" % i], EX.child, b))
        g.add((b, EX.k, Literal("v%d" % i)))
        g.add((b, RDF.type, EX.T))
    for host in "abcdefgh":
        g.add((URIRef("http://%s.example/s" % host),
               URIRef("http://%s.example/p" % host),
               URIRef("http://%s.example/o" % host)))
    sys.stdout.write(canonicalize_rdf_graph(g, output_format))
    """
)


def _outputs_across_processes(output_format, force_fallback):
    """Serialize the same graph in four processes with different hash seeds."""
    outputs = set()
    for seed in ("0", "1", "12345", "999"):
        completed = subprocess.run(
            [sys.executable, "-c", _ACROSS_PROCESSES, output_format, "1" if force_fallback else "0"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONHASHSEED": seed},
            check=False,
        )
        if completed.returncode != 0:
            pytest.fail(f"{output_format} failed:\n{completed.stderr[-2000:]}")
        outputs.add(completed.stdout)
    return outputs


@pytest.mark.parametrize(
    ("output_format", "force_fallback"),
    [
        pytest.param("xml", True, id="xml-fallback"),
        pytest.param("turtle", True, id="turtle-fallback"),
        pytest.param("json-ld", False, id="jsonld"),
    ],
)
def test_output_is_byte_identical_across_processes(output_format, force_fallback):
    """The same graph must serialize to the same bytes in any process.

    Three separate causes break this. Degraded RDF/XML was ordered by rdflib's own graph
    traversal, which follows set iteration order. Auto-generated ``ns1``/``ns2``
    prefix names were allocated in traversal order too, so the *names* moved
    even when the triples did not. And ``json-ld`` was not in the format map at
    all, so it fell through to rdflib's serializer, which carries no
    determinism guarantee.
    """
    assert len(_outputs_across_processes(output_format, force_fallback)) == 1


# --------------------------------------------------------------------------
# Interface
# --------------------------------------------------------------------------


def test_every_format_ends_with_exactly_one_newline():
    """A committed artifact should not depend on which format wrote it.

    Passing through whatever the serializer produced gives no trailing newline
    for RDF/XML and one for Turtle, so POSIX text tools disagree about whether
    the file has a last line.
    """
    counts = {}
    for output_format in ("turtle", "nt", "xml", "trig", "n3"):
        graph = Graph()
        graph.bind("ex", EX)
        graph.add((EX.s, EX.p, Literal("v")))
        serialized = _apply(graph, output_format)
        counts[output_format] = len(serialized) - len(serialized.rstrip("\n"))

    assert counts == dict.fromkeys(counts, 1)


def test_a_dataset_is_refused_rather_than_partly_serialized():
    """A Dataset is a Graph subclass, so it is accepted and quietly flattened.

    Every named graph collapses into one document and the graph names are
    dropped, which is a different dataset. The caller asked for something this
    function cannot express and should be told so.
    """
    dataset = rdflib.Dataset()
    dataset.graph(URIRef("http://ex/g1")).add((EX.a, EX.p, Literal("in-g1")))
    dataset.graph(URIRef("http://ex/g2")).add((EX.b, EX.p, Literal("in-g2")))

    with pytest.raises(TypeError):
        _apply(dataset)


# --------------------------------------------------------------------------
# A property that already held
# --------------------------------------------------------------------------


def test_base_survives_the_degraded_path():
    """``@base`` must not disappear just because pyoxigraph refused the graph.

    ``rdflib_dumper.dumps(..., prefix_map={"@base": ...})`` is a supported way
    to ask for a document whose IRIs are written relative to a base, and the
    metamodel routinely produces graphs that fall back (a bare ``status:
    testing`` on a ``uriorcurie`` slot serializes to the relative ``<testing>``,
    which pyoxigraph rejects). Losing the directive on exactly that path means
    the feature works only for graphs that never needed the fallback.
    """
    graph = Graph(base="http://example.org/default/")
    graph.bind("ex", EX)
    graph.add((EX.s, EX.p, Literal("v")))
    graph.add((URIRef("testing"), EX.p, Literal("forces-fallback")))

    assert "@base <http://example.org/default/> ." in _apply(graph)
