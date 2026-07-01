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
   annotation mode) are rejected by pyoxigraph.  This function falls
   back to rdflib's serializer for such graphs.

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

import hashlib
import io
import logging
import re

import pyoxigraph as ox
import rdflib

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


def _relabel_blank_nodes_by_hash(triples: list["ox.Triple"]) -> list["ox.Triple"]:
    """Relabel blank nodes by a Merkle hash of their canonical subtree.

    RDFC-1.0 gives each blank node a *stable content-derived hash* internally,
    but then labels them ``_:c14n0, _:c14n1, ...`` by ordinal position in a
    global sort.  That ordinal is what makes diffs churn: inserting one blank
    node shifts every later label.  This pass re-derives a label from each
    blank node's own subtree content, so unrelated nodes keep their identifier
    across edits (change-locality).

    The label is a hash over the node's outgoing triples, substituting each
    blank-node object with its own (recursively computed) hash.  This is
    well-defined for acyclic blank-node structure (trees/DAGs), which covers
    essentially all LinkML-generated RDF (OWL restrictions, SHACL property
    shapes, RDF lists).  Blank nodes whose reachable closure contains a cycle
    are left with their ``c14n`` label (correctness over locality).  Genuinely
    automorphic siblings (identical subtree content) share a hash and are kept
    distinct with a deterministic index suffix.

    :param triples: RDFC-1.0 canonicalized triples (blank nodes labeled ``c14nN``).
    :return: Triples with content-derived blank-node labels where computable.
    """
    out_edges: dict[str, list[tuple[str, ox.Term]]] = {}
    for t in triples:
        if isinstance(t.subject, ox.BlankNode):
            out_edges.setdefault(t.subject.value, []).append((str(t.predicate), t.object))

    # Merkle hash per blank node; None marks a node that reaches a cycle.
    memo: dict[str, str | None] = {}

    def node_hash(bid: str, stack: frozenset[str]) -> str | None:
        if bid in memo:
            return memo[bid]
        if bid in stack:
            return None  # back-edge: this closure contains a cycle
        inner_stack = stack | {bid}
        reprs: list[str] = []
        for pred, obj in out_edges.get(bid, []):
            if isinstance(obj, ox.BlankNode):
                child = node_hash(obj.value, inner_stack)
                if child is None:
                    memo[bid] = None
                    return None
                obj_repr = "B:" + child
            else:
                obj_repr = "T:" + str(obj)
            reprs.append(pred + "\x00" + obj_repr)
        digest = hashlib.sha256("\x01".join(sorted(reprs)).encode("utf-8")).hexdigest()
        memo[bid] = digest
        return digest

    for bid in out_edges:
        node_hash(bid, frozenset())

    # Group by hash to disambiguate genuine automorphic collisions.
    by_hash: dict[str, list[str]] = {}
    for bid, digest in memo.items():
        if digest is not None:
            by_hash.setdefault(digest, []).append(bid)

    label_map: dict[str, str] = {}
    for digest, bids in by_hash.items():
        if len(bids) == 1:
            label_map[bids[0]] = "b" + digest[:24]
        else:
            for k, bid in enumerate(sorted(bids)):
                label_map[bid] = f"b{digest[:24]}_{k}"

    def remap(term: "ox.Term") -> "ox.Term":
        if isinstance(term, ox.BlankNode) and term.value in label_map:
            return ox.BlankNode(label_map[term.value])
        return term

    return [ox.Triple(remap(t.subject), t.predicate, remap(t.object)) for t in triples]


def canonicalize_rdf_graph(
    graph: rdflib.Graph,
    output_format: str = "turtle",
    stable_blank_node_labels: bool = False,
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
    :param stable_blank_node_labels: If True, relabel blank nodes by a hash of
        their subtree content instead of RDFC-1.0's ordinal ``c14nN`` labels,
        so a small graph change yields a small diff (change-locality).
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
            "Graph contains non-standard RDF that pyoxigraph cannot parse; falling back to rdflib serializer"
        )
        return graph.serialize(format=output_format)

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
    canonical_triples = [ox.Triple(q.subject, q.predicate, q.object) for q in quads]
    if stable_blank_node_labels:
        canonical_triples = _relabel_blank_nodes_by_hash(canonical_triples)
    sorted_triples = sorted(
        canonical_triples,
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
