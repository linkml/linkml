"""Correctness differences between linkml's RDF canonicalizer and the extracted library.

``linkml_runtime.utils.rdf_canonicalize`` and
``diffable_rdf.canonicalize_rdf_graph`` are the same code: the module was
extracted into a standalone library at the maintainers' request
(linkml/linkml#3295). The two copies have since diverged, so each test here
asserts one correctness property against *both* implementations and marks the
one that does not hold it as a strict xfail.

Every remaining gap runs one way -- the extracted copy received fixes the local
one did not -- and two of them are silent data corruption, where the output
parses cleanly and says something the input never said. That is worse than a
crash, because a generated artifact gets committed and reviewed on the
assumption that it means what the schema meant.

One gap used to run the other way: the library dropped ``@base`` on the
degraded path. That was the last property blocking delegation, and
diffable-rdf 0.4.0 fixed it, so the case now passes on both sides and is kept
unmarked. Asserting both directions is what made the fix land where it
belongs.

The xfails are strict, so this file is a ratchet in both directions: when a fix
lands on either side, its case starts passing and the suite fails until the
mark is removed.
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


def _impls(**known_failures: str):
    """Parametrize over both implementations, xfailing the ones named.

    :param known_failures: implementation id (``linkml`` / ``diffable_rdf``)
        mapped to why that implementation does not hold the property.
    """
    params = []
    for fn, ident in _IMPLEMENTATIONS:
        reason = known_failures.get(ident.replace("-", "_"))
        marks = [pytest.mark.xfail(strict=True, reason=reason)] if reason else []
        params.append(pytest.param(fn, id=ident, marks=marks))
    return params


def _apply(fn, graph, output_format="turtle"):
    """Call an implementation, ignoring the warnings both emit on the fallback path."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return fn(graph, output_format)


# --------------------------------------------------------------------------
# Silent data corruption
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "canonicalize",
    _impls(linkml="passes graph.base to the serializer without checking it is safe to relativize against"),
)
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


@pytest.mark.parametrize(
    "canonicalize",
    _impls(linkml="rdflib's collection syntax materializes a shared list tail once per referencing list"),
)
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


@pytest.mark.parametrize(
    "canonicalize",
    _impls(linkml="the rdflib fallback writes N-Triples for a graph pyoxigraph already refused"),
)
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


@pytest.mark.parametrize(
    "canonicalize",
    _impls(linkml="sorts fallback output with str.splitlines(), which breaks on U+2028 and five other characters"),
)
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
        pytest.param(
            "linkml", "xml", True, id="linkml-xml-fallback", marks=pytest.mark.xfail(strict=True, reason=_XML_TRAVERSAL)
        ),
        pytest.param("diffable_rdf", "xml", True, id="diffable-rdf-xml-fallback"),
        pytest.param(
            "linkml",
            "turtle",
            True,
            id="linkml-turtle-fallback",
            marks=pytest.mark.xfail(strict=True, reason=_NS_NAMES),
        ),
        pytest.param("diffable_rdf", "turtle", True, id="diffable-rdf-turtle-fallback"),
        pytest.param(
            "linkml",
            "json-ld",
            False,
            id="linkml-jsonld",
            marks=pytest.mark.xfail(strict=True, reason=_JSONLD_UNMAPPED),
        ),
        pytest.param("diffable_rdf", "json-ld", False, id="diffable-rdf-jsonld"),
    ],
)
def test_output_is_byte_identical_across_processes(module, output_format, force_fallback):
    """The same graph must serialize to the same bytes in any process.

    Three separate causes break this in the local copy. Degraded RDF/XML is
    ordered by rdflib's own graph traversal, which follows set iteration order.
    Auto-generated ``ns1``/``ns2`` prefix names are allocated in traversal order
    too, so the *names* move even when the triples do not. And ``json-ld`` is
    not in the format map at all, so it falls through to rdflib's serializer,
    which carries no determinism guarantee.
    """
    assert len(_outputs_across_processes(module, output_format, force_fallback)) == 1


# --------------------------------------------------------------------------
# Interface
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "canonicalize",
    _impls(linkml="returns the serializer's own trailing whitespace, which differs by format"),
)
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


@pytest.mark.parametrize(
    "canonicalize",
    _impls(linkml="Dataset is a Graph subclass, so the type check accepts it and the named graphs are flattened"),
)
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

    This ran the other way until diffable-rdf 0.4.0, which was the last
    property blocking delegation. The case is kept because it is the one the
    two implementations reach differently: linkml passes ``graph.base`` to the
    serializer unconditionally, which is why it also fails
    :func:`test_base_with_a_fragment_does_not_rewrite_every_iri` above, while
    the library keeps the base only after confirming that re-reading the
    result still yields every absolute IRI of the source.
    """
    graph = Graph(base="http://example.org/default/")
    graph.bind("ex", EX)
    graph.add((EX.s, EX.p, Literal("v")))
    graph.add((URIRef("testing"), EX.p, Literal("forces-fallback")))

    assert "@base <http://example.org/default/> ." in _apply(canonicalize, graph)
