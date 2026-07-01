"""Deterministic RDF serialization via pyoxigraph RDFC-1.0 canonicalization.

This module provides a function to canonicalize an rdflib Graph using
pyoxigraph's RDFC-1.0 implementation, producing deterministic output
with stable blank node labels and sorted triples.

**Known limitations:**

1. **xsd:string normalization**: pyoxigraph follows RDF 1.1, where plain
   string literals and ``"text"^^xsd:string`` are identical.  The output
   will never contain explicit ``^^xsd:string`` annotations.  Code that
   re-parses the output with rdflib will see ``Literal("x")`` (datatype
   ``None``) rather than ``Literal("x", datatype=XSD.string)``.

2. **Non-standard RDF**: Graphs with literal predicates (e.g. SHACL
   annotation mode) or relative IRIs (e.g. the metamodel's
   ``bibo:status <testing>``) are rejected by pyoxigraph.  This function
   falls back to rdflib's serializer for such graphs, but still
   canonicalizes blank-node labels (and sorts line-oriented formats) so
   the fallback output remains deterministic across processes.

3. **Numeric short forms**: pyoxigraph uses Turtle short forms for
   ``xsd:integer`` (``42``), ``xsd:boolean`` (``true``), and
   ``xsd:decimal`` (``1.23``).  rdflib parses these back with the
   correct datatype, so this is lossless.

4. **Base IRI / prefix collision**: When a graph has ``@base`` and a
   prefix whose namespace equals the base IRI (e.g. rdflib's auto-bound
   ``base:`` prefix), pyoxigraph emits CURIEs like ``base:label`` that
   rdflib rejects.  We skip such prefixes during serialization.

5. **Trailing escaped dot in PN_LOCAL**: pyoxigraph emits CURIEs like
   ``prefix:local\\.`` for IRIs whose local part ends with ``.``.  This
   is valid Turtle (PN_LOCAL_ESC), but rdflib's notation3 parser rejects
   it because it conflicts with the statement-terminator dot.  We
   post-process the output to expand such CURIEs to full ``<IRI>`` form.
"""

import io
import logging
import re

import pyoxigraph as ox
import rdflib
from rdflib.compare import to_canonical_graph

logger = logging.getLogger(__name__)

# Mapping from rdflib/LinkML format strings to pyoxigraph RdfFormat objects.
_FORMAT_MAP: dict[str, ox.RdfFormat] = {
    "turtle": ox.RdfFormat.TURTLE,
    "ttl": ox.RdfFormat.TURTLE,
    "nt": ox.RdfFormat.N_TRIPLES,
    "ntriples": ox.RdfFormat.N_TRIPLES,
    "n-triples": ox.RdfFormat.N_TRIPLES,
    "nt11": ox.RdfFormat.N_TRIPLES,
    "nquads": ox.RdfFormat.N_QUADS,
    "n-quads": ox.RdfFormat.N_QUADS,
    "xml": ox.RdfFormat.RDF_XML,
    "rdf/xml": ox.RdfFormat.RDF_XML,
    "trig": ox.RdfFormat.TRIG,
    "n3": ox.RdfFormat.N3,
}

# Formats that support prefix declarations.
_PREFIX_FORMATS = frozenset({ox.RdfFormat.TURTLE, ox.RdfFormat.TRIG, ox.RdfFormat.N3, ox.RdfFormat.RDF_XML})

# Line-oriented formats (one triple/quad per line) whose fallback output must
# be sorted, because rdflib does not emit them in a stable order even after
# blank-node canonicalization.
_LINE_ORIENTED_FORMATS = frozenset({"nt", "ntriples", "n-triples", "nt11", "nquads", "n-quads"})


def _deterministic_fallback_serialize(graph: rdflib.Graph, output_format: str) -> str:
    """Serialize a graph that pyoxigraph cannot canonicalize, deterministically.

    pyoxigraph rejects some graphs that rdflib accepts -- notably graphs
    containing relative IRIs (e.g. the metamodel's ``bibo:status <testing>``)
    or literal predicates (SHACL annotation mode).  A plain
    ``graph.serialize()`` for such graphs is *not* reproducible across
    processes: rdflib assigns blank-node labels non-deterministically, so the
    structure and grouping of the output varies run to run.

    To degrade gracefully instead of silently emitting non-deterministic
    output, we canonicalize blank-node labels with rdflib's own
    isomorphism-based canonicalization (:func:`rdflib.compare.to_canonical_graph`,
    which uses a content-derived hash, not run-local ids) and preserve the
    original prefix and base bindings that the canonical graph drops.  For
    line-oriented formats we additionally sort the serialized lines, since
    rdflib does not emit N-Triples/N-Quads in a stable order.

    Relative IRIs are preserved verbatim (not resolved against the base): the
    goal is deterministic output, and silently rewriting ``<testing>`` into an
    absolute IRI would mask what is really a data problem in the source graph.

    :param graph: The rdflib Graph that pyoxigraph could not parse.
    :param output_format: Target serialization format (e.g. ``"turtle"``, ``"nt"``).
    :return: Deterministic string serialization of the graph.
    """
    canonical = to_canonical_graph(graph)
    # to_canonical_graph builds a fresh graph without the source's namespace
    # bindings; rebind them so the output does not fall back to rdflib's
    # non-deterministic auto-generated ``ns1:``/``ns2:`` prefixes.
    for prefix, namespace in graph.namespace_manager.namespaces():
        canonical.namespace_manager.bind(prefix, namespace, replace=True)
    canonical.base = graph.base
    serialized = canonical.serialize(format=output_format)
    if output_format.lower() in _LINE_ORIENTED_FORMATS:
        lines = [line for line in serialized.splitlines() if line.strip()]
        return "\n".join(sorted(lines)) + "\n"
    return serialized


# Characters that may appear escaped in a Turtle PN_LOCAL via PN_LOCAL_ESC.
_PN_LOCAL_ESC_UNESCAPE = re.compile(r"\\([_~.\-!$&'()*+,;=/?#@%])")


def _expand_trailing_dot_curies(turtle_text: str, prefixes: dict[str, str]) -> str:
    """Replace CURIEs whose local part ends in ``\\.`` with full ``<IRI>`` form.

    rdflib's notation3 parser rejects PN_LOCAL ending in an escaped dot
    even though Turtle permits it (PN_LOCAL_ESC).  pyoxigraph emits this
    form for IRIs ending in ``.`` (e.g. ``biolink:StrandEnum#.``).  We
    rewrite each such CURIE to its expanded ``<IRI>`` form so the output
    round-trips through rdflib.
    """
    if not prefixes:
        return turtle_text

    # Match: a prefix name, ':', a local part (no whitespace or token
    # delimiters), ending in ``\.``, followed by whitespace.  Use a
    # negative lookbehind to avoid matching inside ``<...>`` or word
    # characters that would make this a substring of something else.
    pattern = re.compile(
        r"(?<![<\w])"
        r"([A-Za-z_][\w.-]*?):"
        r"([^\s,;()<>\"'\[\]]*?\\\.)"
        r"(?=\s)"
    )

    def replace(match: re.Match[str]) -> str:
        prefix = match.group(1)
        local_escaped = match.group(2)
        namespace = prefixes.get(prefix)
        if namespace is None:
            return match.group(0)
        local = _PN_LOCAL_ESC_UNESCAPE.sub(r"\1", local_escaped)
        return f"<{namespace}{local}>"

    return pattern.sub(replace, turtle_text)


def _is_safe_prefix_iri(iri: str) -> bool:
    """Check whether a namespace IRI is safe for prefix serialization.

    pyoxigraph rejects IRIs with invalid code-points (e.g. double ``#``),
    and rdflib's Turtle parser cannot round-trip CURIEs whose namespace
    contains query parameters or fragments in unexpected positions.  This
    function returns ``False`` for such IRIs so they can be skipped during
    prefix collection.
    """
    # A namespace IRI should end with '/' or '#'.  If '#' appears
    # *before* the final character, the IRI contains an embedded
    # fragment which produces unusable CURIEs.
    if "#" in iri[:-1]:
        return False
    # Query parameters in namespace IRIs produce CURIEs that rdflib
    # cannot parse back.
    if "?" in iri:
        return False
    return True


def canonicalize_rdf_graph(
    graph: rdflib.Graph,
    output_format: str = "turtle",
) -> str:
    """Serialize an rdflib Graph deterministically using RDFC-1.0 canonicalization.

    The graph is transferred to pyoxigraph via N-Triples, canonicalized
    with RDFC-1.0, sorted, and serialized back to the requested format.
    Prefix bindings from the rdflib Graph are preserved in the output
    for formats that support them (Turtle, TriG, N3, RDF/XML).

    Falls back to plain rdflib serialization for unsupported formats or
    graphs containing non-standard RDF (e.g. literal predicates).

    :param graph: The rdflib Graph to serialize.
    :param output_format: Target serialization format (e.g. ``"turtle"``, ``"nt"``).
    :return: Deterministic string serialization of the graph.
    """
    ox_format = _FORMAT_MAP.get(output_format.lower())
    if ox_format is None:
        logger.warning(
            "pyoxigraph does not support format %r; falling back to rdflib serializer",
            output_format,
        )
        return graph.serialize(format=output_format)

    # 1. Transfer rdflib graph to pyoxigraph via N-Triples.
    nt_data = graph.serialize(format="nt")
    nt_bytes = nt_data.encode("utf-8") if isinstance(nt_data, str) else nt_data

    # 2. Parse into pyoxigraph and build a Dataset for canonicalization.
    #    Fall back to rdflib if the graph contains non-standard RDF
    #    (e.g. literal predicates from annotations) that pyoxigraph rejects.
    try:
        triples = list(ox.parse(io.BytesIO(nt_bytes), format=ox.RdfFormat.N_TRIPLES))
    except SyntaxError:
        logger.warning(
            "Graph contains non-standard RDF that pyoxigraph cannot parse "
            "(e.g. relative IRIs or literal predicates); falling back to rdflib "
            "with blank-node canonicalization for deterministic output"
        )
        return _deterministic_fallback_serialize(graph, output_format)

    dataset = ox.Dataset()
    for triple in triples:
        dataset.add(ox.Quad(triple.subject, triple.predicate, triple.object, ox.DefaultGraph()))

    # 3. Canonicalize blank node labels with RDFC-1.0.
    dataset.canonicalize(ox.CanonicalizationAlgorithm.RDFC_1_0)

    # 4. Sort triples for deterministic ordering.
    # RDFC-1.0 stabilizes blank-node labels but pyoxigraph's Dataset
    # iteration order is not sorted and varies across processes (verified
    # empirically against pyoxigraph 0.5.8). The explicit string-key sort
    # is load-bearing for byte-identical output across runs; see
    # tests/linkml_runtime/test_utils/test_rdf_canonicalize.py::test_sort_is_load_bearing.
    quads = list(dataset)
    sorted_triples = sorted(
        (ox.Triple(q.subject, q.predicate, q.object) for q in quads),
        key=lambda t: (str(t.subject), str(t.predicate), str(t.object)),
    )

    # 5. Collect prefixes for formats that support them.
    base_iri = str(graph.base) if graph.base else None
    prefixes: dict[str, str] | None = None
    if ox_format in _PREFIX_FORMATS:
        prefixes = {}
        for prefix, namespace in graph.namespace_manager.namespaces():
            if not prefix:  # skip empty prefix (base)
                continue
            ns_str = str(namespace)
            # Skip prefixes whose namespace matches the base IRI to avoid
            # pyoxigraph emitting CURIEs like `base:label` that conflict
            # with the @base directive.
            if base_iri and ns_str == base_iri:
                continue
            # Skip namespace IRIs that pyoxigraph rejects or that produce
            # CURIEs rdflib cannot round-trip.  Valid namespace IRIs for
            # prefix use should end with '/' or '#' and contain no query
            # parameters or fragment-like characters in the middle.
            if not _is_safe_prefix_iri(ns_str):
                continue
            prefixes[str(prefix)] = ns_str
    used_prefixes = prefixes
    try:
        result_bytes = ox.serialize(
            sorted_triples,
            format=ox_format,
            prefixes=prefixes,
            base_iri=base_iri,
        )
    except ValueError:
        # pyoxigraph rejects prefixes with invalid IRIs (e.g. containing
        # fragment-like characters such as double '#').  Retry without
        # the offending prefixes by falling back to no prefixes, which
        # still produces valid (if verbose) Turtle.
        logger.warning("pyoxigraph rejected one or more prefix IRIs; serializing without prefix declarations")
        result_bytes = ox.serialize(
            sorted_triples,
            format=ox_format,
        )
        used_prefixes = None
    result = result_bytes.decode("utf-8")
    if ox_format in _PREFIX_FORMATS and used_prefixes:
        result = _expand_trailing_dot_curies(result, used_prefixes)
    return result
