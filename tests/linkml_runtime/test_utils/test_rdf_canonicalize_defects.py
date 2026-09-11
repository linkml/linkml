"""Correctness properties shared by linkml's RDF canonicalizer and the library behind it.

``linkml_runtime.utils.rdf_canonicalize`` and
``diffable_rdf.canonicalize_rdf_graph`` are the same code: the module was
extracted into a standalone library at the maintainers' request
(linkml/linkml#3295). The two copies then diverged for a while, and this file
is what made the divergence visible -- each test asserts one correctness
property against *both* implementations, so a fix that landed on one side and
not the other showed up as a failure rather than as nothing at all.

Nine properties held only in the library, two of them cases of silent data
corruption where the output parsed cleanly and said something the input never
said. One held only in linkml: the library dropped ``@base`` on the degraded
path. Asserting both directions is what got each of them fixed where it
belonged -- the ``@base`` gap in diffable-rdf 0.4.0, the other nine in linkml
by deleting the in-tree copy and calling the library.

Every case is now unmarked, which is the point: the file is the evidence that
the delegation changed no behaviour it should not have, and it keeps running
against both entry points so that a future divergence fails the suite instead
of going unnoticed.
"""

import os
import subprocess
import sys
import textwrap
import warnings

import diffable_rdf
import pytest
import rdflib
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF

from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph as linkml_canonicalize

EX = Namespace("http://example.org/")

_IMPLEMENTATIONS = (
    (linkml_canonicalize, "linkml"),
    (diffable_rdf.canonicalize_rdf_graph, "diffable-rdf"),
)


def _impls():
    """Parametrize a test over both entry points.

    linkml's is a thin adapter over the library's, so the two agree by
    construction today. Running both anyway is what turns a future re-fork, or
    an adapter that quietly changes behaviour on the way through, into a test
    failure.
    """
    return [pytest.param(fn, id=ident) for fn, ident in _IMPLEMENTATIONS]


def _apply(fn, graph, output_format="turtle"):
    """Call an implementation, ignoring the warnings both emit on the fallback path."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return fn(graph, output_format)


# --------------------------------------------------------------------------
# Silent data corruption
# --------------------------------------------------------------------------


@pytest.mark.parametrize("canonicalize", _impls())
def test_base_with_a_fragment_does_not_rewrite_every_iri(canonicalize):
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
    round_tripped.parse(data=_apply(canonicalize, graph), format="turtle")

    assert {str(s) for s in round_tripped.subjects()} == {"http://ex.org/d#a"}


@pytest.mark.parametrize("canonicalize", _impls())
def test_a_shared_rdf_list_tail_is_not_duplicated(canonicalize):
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
    round_tripped.parse(data=_apply(canonicalize, graph), format="turtle")

    assert len(round_tripped) == len(graph)


# --------------------------------------------------------------------------
# Output that no parser will read
# --------------------------------------------------------------------------


@pytest.mark.parametrize("canonicalize", _impls())
def test_nt_output_either_parses_or_refuses(canonicalize):
    """N-Triples admits only absolute IRIs, so a relative one must not be written.

    The fallback is taken *because* the graph holds a term pyoxigraph rejected.
    Writing it out anyway produces a file that fails on line 1. Refusing with a
    message naming the term and a format that can carry the graph is the fix;
    returning unreadable text is not.
    """
    graph = Graph()
    graph.add((URIRef("testing"), EX.p, Literal("v")))

    try:
        serialized = _apply(canonicalize, graph, "nt")
    except ValueError:
        return  # refused, with an explanation -- the correct outcome

    rdflib.Graph().parse(data=serialized, format="nt")


@pytest.mark.parametrize("canonicalize", _impls())
def test_a_unicode_line_separator_in_a_literal_survives(canonicalize):
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
        serialized = _apply(canonicalize, graph, "nt")
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

    module, output_format, force_fallback = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
    if module == "linkml":
        from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph
    else:
        from diffable_rdf import canonicalize_rdf_graph

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


def _outputs_across_processes(module, output_format, force_fallback):
    """Serialize the same graph in four processes with different hash seeds."""
    outputs = set()
    for seed in ("0", "1", "12345", "999"):
        completed = subprocess.run(
            [sys.executable, "-c", _ACROSS_PROCESSES, module, output_format, "1" if force_fallback else "0"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONHASHSEED": seed},
            check=False,
        )
        if completed.returncode != 0:
            pytest.fail(f"{module}/{output_format} failed:\n{completed.stderr[-2000:]}")
        outputs.add(completed.stdout)
    return outputs


_XML_TRAVERSAL = "degraded RDF/XML is ordered by rdflib's graph traversal, which follows set iteration order"
_NS_NAMES = "auto-generated ns1/ns2 prefix names are allocated in traversal order"
_JSONLD_UNMAPPED = "json-ld is absent from the format map, so it falls through to rdflib with no determinism guarantee"


@pytest.mark.parametrize(
    ("module", "output_format", "force_fallback"),
    [
        pytest.param("linkml", "xml", True, id="linkml-xml-fallback"),
        pytest.param("diffable_rdf", "xml", True, id="diffable-rdf-xml-fallback"),
        pytest.param("linkml", "turtle", True, id="linkml-turtle-fallback"),
        pytest.param("diffable_rdf", "turtle", True, id="diffable-rdf-turtle-fallback"),
        pytest.param("linkml", "json-ld", False, id="linkml-jsonld"),
        pytest.param("diffable_rdf", "json-ld", False, id="diffable-rdf-jsonld"),
    ],
)
def test_output_is_byte_identical_across_processes(module, output_format, force_fallback):
    """The same graph must serialize to the same bytes in any process.

    Three separate causes used to break this in the in-tree copy, and all three
    are fixed by delegating. Degraded RDF/XML was ordered by rdflib's own graph
    traversal, which follows set iteration order. Auto-generated ``ns1``/``ns2``
    prefix names were allocated in traversal order too, so the *names* moved
    even when the triples did not. And ``json-ld`` was not in the format map at
    all, so it fell through to rdflib's serializer, which carries no
    determinism guarantee.
    """
    assert len(_outputs_across_processes(module, output_format, force_fallback)) == 1


# --------------------------------------------------------------------------
# Interface
# --------------------------------------------------------------------------


@pytest.mark.parametrize("canonicalize", _impls())
def test_every_format_ends_with_exactly_one_newline(canonicalize):
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
        serialized = _apply(canonicalize, graph, output_format)
        counts[output_format] = len(serialized) - len(serialized.rstrip("\n"))

    assert counts == dict.fromkeys(counts, 1)


@pytest.mark.parametrize("canonicalize", _impls())
def test_a_dataset_is_refused_rather_than_partly_serialized(canonicalize):
    """A Dataset is a Graph subclass, so it is accepted and quietly flattened.

    Every named graph collapses into one document and the graph names are
    dropped, which is a different dataset. The caller asked for something this
    function cannot express and should be told so.
    """
    dataset = rdflib.Dataset()
    dataset.graph(URIRef("http://ex/g1")).add((EX.a, EX.p, Literal("in-g1")))
    dataset.graph(URIRef("http://ex/g2")).add((EX.b, EX.p, Literal("in-g2")))

    with pytest.raises(TypeError):
        _apply(canonicalize, dataset)


# --------------------------------------------------------------------------
# A property both implementations now hold
# --------------------------------------------------------------------------


@pytest.mark.parametrize("canonicalize", _impls())
def test_base_survives_the_degraded_path(canonicalize):
    """``@base`` must not disappear just because pyoxigraph refused the graph.

    ``rdflib_dumper.dumps(..., prefix_map={"@base": ...})`` is a supported way
    to ask for a document whose IRIs are written relative to a base, and the
    metamodel routinely produces graphs that fall back (a bare ``status:
    testing`` on a ``uriorcurie`` slot serializes to the relative ``<testing>``,
    which pyoxigraph rejects). Losing the directive on exactly that path means
    the feature works only for graphs that never needed the fallback.

    This ran the other way until diffable-rdf 0.4.0. It was the last property
    blocking delegation, because linkml held it and the library did not, so
    adopting the library would have been a regression. Fixing it there rather
    than keeping the in-tree copy alive is what let the other nine gaps close
    at once.
    """
    graph = Graph(base="http://example.org/default/")
    graph.bind("ex", EX)
    graph.add((EX.s, EX.p, Literal("v")))
    graph.add((URIRef("testing"), EX.p, Literal("forces-fallback")))

    assert "@base <http://example.org/default/> ." in _apply(canonicalize, graph)
