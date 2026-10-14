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

import hashlib
import io
import json
import re
import warnings
from collections.abc import Iterable

import pyoxigraph as ox
import rdflib
from rdflib.compare import to_canonical_graph
from rdflib.namespace import RDF
from rdflib.plugins.serializers.jsonld import from_rdf
from rdflib.plugins.serializers.n3 import N3Serializer
from rdflib.plugins.serializers.trig import TrigSerializer
from rdflib.plugins.serializers.turtle import TurtleSerializer


class RDFCanonicalizationWarning(UserWarning):
    """Issued when ``canonicalize_rdf_graph`` produces output via a degraded path.

    Surfaced via ``warnings.warn`` (not the ``logging`` module) so that it is
    visible by default to both CLI users and library API consumers regardless
    of logging configuration. Filterable with
    ``warnings.filterwarnings("ignore", category=RDFCanonicalizationWarning)``.
    """


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

# JSON-LD has no pyoxigraph serializer here; it is written by rdflib from a
# graph built in canonical order.
_JSONLD_FORMATS = frozenset({"json-ld", "jsonld"})

# rdflib parser names for the pyoxigraph formats that can carry a base IRI.
_RDFLIB_PARSE_FORMAT: dict[ox.RdfFormat, str] = {
    ox.RdfFormat.TURTLE: "turtle",
    ox.RdfFormat.TRIG: "trig",
    ox.RdfFormat.N3: "n3",
    ox.RdfFormat.RDF_XML: "xml",
}

# An IRI is absolute when it starts with a scheme (RFC 3986 section 3.1).
_ABSOLUTE_IRI = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")


def _without_shared_list_tails(serializer: type[TurtleSerializer]) -> type[TurtleSerializer]:
    """Return a subclass of ``serializer`` that will not inline a list with a shared tail.

    rdflib writes ``( ... )`` collection syntax after checking only that the
    list *head* is referenced once. A tail shared by two lists is then written
    inline in both, as two separate blank nodes, and the output asserts more
    triples than the graph holds.
    """

    class _Serializer(serializer):
        def isValidList(self, l_: rdflib.term.Node) -> bool:
            """Refuse collection syntax when any node after the head is shared."""
            seen: set[rdflib.term.Node] = set()
            node = self.store.value(l_, RDF.rest)
            while node is not None and node != RDF.nil:
                if node in seen or self._references[node] > 1:
                    return False
                seen.add(node)
                node = self.store.value(node, RDF.rest)
            return super().isValidList(l_)

    return _Serializer


# Fallback serializers for the Turtle family, which share rdflib's list writer.
_TURTLE_FAMILY_SERIALIZERS: dict[str, type[TurtleSerializer]] = {
    "turtle": _without_shared_list_tails(TurtleSerializer),
    "ttl": _without_shared_list_tails(TurtleSerializer),
    "n3": _without_shared_list_tails(N3Serializer),
    "trig": _without_shared_list_tails(TrigSerializer),
}


def _with_one_trailing_newline(serialized: str) -> str:
    """End every format with exactly one newline, whatever its serializer produced."""
    return serialized.rstrip("\n") + "\n"


def _in_sorted_order(triples: Iterable[tuple[rdflib.term.Node, ...]], source: rdflib.Graph) -> rdflib.Graph:
    """Copy ``triples`` into a fresh graph, inserting them in sorted order.

    rdflib's RDF/XML, Turtle and JSON-LD writers follow the store's iteration
    order. The default ``Memory`` store indexes triples in sets, whose order
    depends on the hash seed; ``SimpleMemory`` keeps insertion order, so
    inserting in sorted order makes iteration the same in every process.

    The RDF/XML writer also allocates ``ns1``/``ns2`` prefixes while walking a
    set of predicates, so prefixes for unbound predicate namespaces are
    allocated here first, in sorted order. The source graph's prefix and base
    bindings are carried over.
    """
    ordered = rdflib.Graph(store="SimpleMemory")
    for prefix, namespace in source.namespace_manager.namespaces():
        ordered.namespace_manager.bind(prefix, namespace, replace=True)
    ordered.base = source.base
    for triple in sorted(triples, key=lambda t: tuple(term.n3() for term in t)):
        ordered.add(triple)
    for predicate in sorted({p for _, p, _ in ordered if isinstance(p, rdflib.URIRef)}):
        ordered.namespace_manager.compute_qname(predicate, generate=True)
    return ordered


def _jsonld_in_sorted_order(graph: rdflib.Graph) -> str:
    """Write ``graph`` as expanded JSON-LD with its node objects sorted by ``@id``.

    rdflib's JSON-LD writer collects subjects into a set, so node order varies
    by hash seed, and its formatting depends on whether ``orjson`` is
    installed. Building the document with :func:`from_rdf` and writing it here
    fixes both.
    """
    document = from_rdf(graph)
    nodes = document["@graph"] if isinstance(document, dict) else document
    nodes.sort(key=lambda node: node.get("@id", ""))
    return json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False)


def _to_rdflib(term: "ox.Term") -> rdflib.term.Node:
    """Convert a pyoxigraph term to rdflib, keeping its blank-node label.

    Re-parsing serialized triples would not do: rdflib's parsers mint fresh
    random blank-node ids, which undoes canonicalization.
    """
    if isinstance(term, ox.NamedNode):
        return rdflib.URIRef(term.value)
    if isinstance(term, ox.BlankNode):
        return rdflib.BNode(term.value)
    if term.language:
        return rdflib.Literal(term.value, lang=term.language)
    if term.datatype.value == str(rdflib.XSD.string):
        return rdflib.Literal(term.value)
    return rdflib.Literal(term.value, datatype=rdflib.URIRef(term.datatype.value))


def _refuse_terms_line_formats_cannot_carry(graph: rdflib.Graph, output_format: str) -> None:
    """Raise ``ValueError`` for a term N-Triples or N-Quads cannot represent.

    Both formats admit only absolute IRIs and IRI predicates (N-Triples 1.1
    section 2.2). Writing such a term anyway produces a file no parser reads.
    """
    for subject, predicate, obj in graph:
        if not isinstance(predicate, rdflib.URIRef):
            raise ValueError(
                f"{output_format} cannot represent this graph: the predicate {predicate!r} is not an IRI. "
                "Use turtle, which can carry this graph."
            )
        for term in (subject, predicate, obj):
            if isinstance(term, rdflib.URIRef) and not _ABSOLUTE_IRI.match(term):
                raise ValueError(
                    f"{output_format} cannot represent this graph: {term!r} is not an absolute IRI, and "
                    "N-Triples and N-Quads accept only absolute IRIs. Use turtle, trig or xml, which can "
                    "carry this graph, or make the term absolute."
                )


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
    which uses a content-derived hash, not run-local ids), rebuild the graph in
    sorted order with the original prefix and base bindings, and sort the lines
    of line-oriented formats.

    Relative IRIs are preserved verbatim (not resolved against the base): the
    goal is deterministic output, and silently rewriting ``<testing>`` into an
    absolute IRI would mask what is really a data problem in the source graph.
    N-Triples and N-Quads cannot carry them at all, so those formats refuse.

    :param graph: The rdflib Graph that pyoxigraph could not parse.
    :param output_format: Target serialization format (e.g. ``"turtle"``, ``"nt"``).
    :return: Deterministic string serialization of the graph.
    :raises ValueError: If a line-oriented format is asked for a term it cannot represent.
    """
    fmt = output_format.lower()
    canonical = _in_sorted_order(to_canonical_graph(graph), graph)
    if fmt in _LINE_ORIENTED_FORMATS:
        _refuse_terms_line_formats_cannot_carry(canonical, output_format)
        # Split on newlines only: str.splitlines() also breaks on U+2028 and
        # other separators that N-Triples allows raw inside a literal.
        lines = [line for line in canonical.serialize(format=output_format).split("\n") if line.strip()]
        return "\n".join(sorted(lines)) + "\n"
    if fmt in _JSONLD_FORMATS:
        return _jsonld_in_sorted_order(canonical)
    serializer = _TURTLE_FAMILY_SERIALIZERS.get(fmt)
    if serializer is None:
        return canonical.serialize(format=output_format)
    stream = io.BytesIO()
    serializer(canonical).serialize(stream, base=canonical.base, encoding="utf-8")
    return stream.getvalue().decode("utf-8")


# Characters that may appear escaped in a Turtle PN_LOCAL via PN_LOCAL_ESC.
_PN_LOCAL_ESC_UNESCAPE = re.compile(r"\\([_~.\-!$&'()*+,;=/?#@%])")


_CURIE_TRAILING_DOT_PATTERN = re.compile(
    r"(?<![<\w])"
    r"([A-Za-z_][\w.-]*?):"
    r"([^\s,;()<>\"'\[\]]*?\\\.)"
    r"(?=\s)"
)


def _iter_turtle_structural_spans(turtle_text: str):
    """Yield ``(start, end, is_structural)`` spans of a Turtle string.

    Structural spans are regions outside of string literals, IRI refs, and
    line comments — i.e. the only places where a CURIE can syntactically
    appear. Non-structural spans (literal contents, IRI bodies, comments)
    are yielded as-is so they round-trip unchanged.

    Handles single- and triple-quoted literals with backslash escapes for
    both ``"`` and ``'`` delimiters, ``<...>`` IRI refs, and ``#...`` line
    comments.
    """
    n = len(turtle_text)
    i = 0
    while i < n:
        ch = turtle_text[i]
        if ch in ('"', "'"):
            # String literal — find matching delimiter, respecting triple-
            # quote form and backslash escapes.
            delim = ch
            triple = turtle_text[i : i + 3] == delim * 3
            end_marker = delim * 3 if triple else delim
            j = i + len(end_marker)
            while j < n:
                if turtle_text[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if turtle_text[j : j + len(end_marker)] == end_marker:
                    j += len(end_marker)
                    break
                j += 1
            yield i, j, False
            i = j
        elif ch == "<":
            # IRI ref — find closing '>' on the same logical line.
            j = turtle_text.find(">", i + 1)
            if j == -1:
                yield i, n, False
                i = n
            else:
                yield i, j + 1, False
                i = j + 1
        elif ch == "#":
            # Line comment — to end of line.
            j = turtle_text.find("\n", i)
            j = n if j == -1 else j
            yield i, j, False
            i = j
        else:
            # Structural region — accumulate until the next literal / IRI /
            # comment opener. Treat ``\X`` as a PN_LOCAL_ESC escape (two
            # chars) so that ``\#`` and ``\.`` inside a CURIE local part
            # don't trigger comment / boundary handling.
            start = i
            while i < n:
                c = turtle_text[i]
                if c == "\\" and i + 1 < n:
                    i += 2
                    continue
                if c in ('"', "'", "<", "#"):
                    break
                i += 1
            yield start, i, True


def _expand_trailing_dot_curies(turtle_text: str, prefixes: dict[str, str]) -> str:
    """Replace CURIEs whose local part ends in ``\\.`` with full ``<IRI>`` form.

    rdflib's notation3 parser rejects PN_LOCAL ending in an escaped dot
    even though Turtle permits it (PN_LOCAL_ESC). pyoxigraph emits this
    form for IRIs ending in ``.`` (e.g. ``biolink:StrandEnum#.``). We
    rewrite each such CURIE to its expanded ``<IRI>`` form so the output
    round-trips through rdflib.

    The rewrite is applied only to *structural* spans of the document —
    string literals, IRI refs, and comments are left untouched. This is
    what prevents the regex from mangling CURIE-shaped substrings that
    happen to appear inside a literal value.
    """
    if not prefixes:
        return turtle_text

    def replace(match: re.Match[str]) -> str:
        prefix = match.group(1)
        local_escaped = match.group(2)
        namespace = prefixes.get(prefix)
        if namespace is None:
            return match.group(0)
        local = _PN_LOCAL_ESC_UNESCAPE.sub(r"\1", local_escaped)
        return f"<{namespace}{local}>"

    parts: list[str] = []
    for start, end, is_structural in _iter_turtle_structural_spans(turtle_text):
        chunk = turtle_text[start:end]
        if is_structural:
            chunk = _CURIE_TRAILING_DOT_PATTERN.sub(replace, chunk)
        parts.append(chunk)
    return "".join(parts)


def _iri_terms(triples: list["ox.Triple"]) -> set[str]:
    """Return the set of IRI strings appearing anywhere in ``triples``.

    Walks subjects, predicates, non-literal objects, and literal datatypes.
    Used to filter the prefix dict down to namespaces that are actually
    referenced by the canonicalized graph, so the output isn't padded with
    unused ``@prefix`` declarations.
    """
    iris: set[str] = set()
    for t in triples:
        for term in (t.subject, t.predicate, t.object):
            if isinstance(term, ox.NamedNode):
                iris.add(term.value)
            elif isinstance(term, ox.Literal):
                dt = term.datatype
                if dt is not None:
                    iris.add(dt.value)
    return iris


def _filter_prefixes_to_used(prefixes: dict[str, str], used_iris: set[str]) -> dict[str, str]:
    """Drop prefix bindings whose namespace is not a prefix of any used IRI.

    A prefix is kept if at least one IRI in ``used_iris`` starts with its
    namespace string. Parent-namespace matches are honored (e.g. a prefix
    bound to ``http://schema.org/`` is kept when ``http://schema.org/Person``
    appears in the graph).
    """
    return {prefix: ns for prefix, ns in prefixes.items() if any(iri.startswith(ns) for iri in used_iris)}


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
    are left with their ``c14n`` label (correctness over locality).  Blank nodes
    with no outgoing triples hash to the empty content.  Genuinely
    automorphic siblings (identical subtree content) share a hash and are kept
    distinct with a bare counter suffix, mirroring the label contract of
    oxigraph's ``UnstableHashedIds`` variant (oxigraph#1824).

    :param triples: RDFC-1.0 canonicalized triples (blank nodes labeled ``c14nN``).
    :return: Triples with content-derived blank-node labels where computable.
    """
    out_edges: dict[str, list[tuple[str, ox.Term]]] = {}
    for t in triples:
        if isinstance(t.subject, ox.BlankNode):
            out_edges.setdefault(t.subject.value, []).append((str(t.predicate), t.object))

    # Merkle hash per blank node; None marks a node that reaches a cycle.
    memo: dict[str, str | None] = {}

    def node_hash(bid: str) -> str | None:
        """Hash ``bid`` after its blank-node children, iteratively so long RDF lists cannot exhaust the stack."""
        on_path = {bid}
        stack = [bid]
        while stack:
            node = stack[-1]
            pending = [
                obj.value
                for _, obj in out_edges.get(node, [])
                if isinstance(obj, ox.BlankNode) and obj.value not in memo
            ]
            if any(child in on_path for child in pending):
                memo[node] = None  # back-edge: this closure contains a cycle
            elif pending:
                on_path.add(pending[0])
                stack.append(pending[0])
                continue
            elif any(isinstance(obj, ox.BlankNode) and memo[obj.value] is None for _, obj in out_edges.get(node, [])):
                memo[node] = None
            else:
                reprs = [
                    pred + "\x00" + ("B:" + memo[obj.value] if isinstance(obj, ox.BlankNode) else "T:" + str(obj))
                    for pred, obj in out_edges.get(node, [])
                ]
                memo[node] = hashlib.sha256("\x01".join(sorted(reprs)).encode("utf-8")).hexdigest()
            on_path.discard(node)
            stack.pop()
        return memo[bid]

    # Include blank nodes that only appear as objects: with no outgoing triples
    # they hash to the empty content and are told apart by the counter suffix.
    blank_nodes = {term.value for t in triples for term in (t.subject, t.object) if isinstance(term, ox.BlankNode)}
    for bid in blank_nodes:
        if bid not in memo:
            node_hash(bid)

    # Group by the label prefix actually emitted, so two digests that share it
    # still get distinct labels; this also keeps automorphic siblings apart.
    by_hash: dict[str, list[str]] = {}
    for bid, digest in memo.items():
        if digest is not None:
            by_hash.setdefault(digest[:24], []).append(bid)

    # Label contract matches oxigraph's UnstableHashedIds variant (oxigraph#1824,
    # merged upstream but unreleased): the label is the bare hash, and colliding
    # (automorphic) siblings get a bare counter suffix -- ``hash``, ``hash1``, ...
    # Keeping the same shape means swapping to the real oxigraph hashes later
    # changes only the hash values, not the labeling contract.
    label_map: dict[str, str] = {}
    for prefix, bids in by_hash.items():
        # Order by the numeric c14n index; a text sort puts c14n10 between c14n1 and c14n2.
        for k, bid in enumerate(sorted(bids, key=lambda b: int(b.removeprefix("c14n")))):
            label_map[bid] = prefix if k == 0 else f"{prefix}{k}"

    def remap(term: "ox.Term") -> "ox.Term":
        if isinstance(term, ox.BlankNode) and term.value in label_map:
            return ox.BlankNode(label_map[term.value])
        return term

    return [ox.Triple(remap(t.subject), t.predicate, remap(t.object)) for t in triples]


def _canonical_sorted_triples(triples: list["ox.Triple"], diff_stable: bool) -> list["ox.Triple"]:
    """Canonicalize blank nodes with RDFC-1.0, optionally relabel them, and sort.

    RDFC-1.0 stabilizes blank-node labels but pyoxigraph's Dataset iteration
    order is not sorted and varies across processes (verified empirically
    against pyoxigraph 0.5.8). The explicit string-key sort is load-bearing for
    byte-identical output across runs; see
    tests/linkml_runtime/test_utils/test_rdf_canonicalize.py::test_sort_is_load_bearing.
    """
    dataset = ox.Dataset()
    for triple in triples:
        dataset.add(ox.Quad(triple.subject, triple.predicate, triple.object, ox.DefaultGraph()))
    dataset.canonicalize(ox.CanonicalizationAlgorithm.RDFC_1_0)
    canonical_triples = [ox.Triple(q.subject, q.predicate, q.object) for q in dataset]
    if diff_stable:
        canonical_triples = _relabel_blank_nodes_by_hash(canonical_triples)
    return sorted(canonical_triples, key=lambda t: (str(t.subject), str(t.predicate), str(t.object)))


def _usable_prefixes(graph: rdflib.Graph, triples: list["ox.Triple"], base_iri: str | None) -> dict[str, str]:
    """Collect the graph's prefix bindings that pyoxigraph can write and the triples use."""
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
    # Drop prefix bindings whose namespace is not referenced by any IRI
    # in the graph. This prevents the rdflib NamespaceManager's default
    # bindings (~30 well-known vocabularies) from being emitted into
    # every output file regardless of whether the schema actually uses
    # them.
    return _filter_prefixes_to_used(prefixes, _iri_terms(triples))


def _serialize_with_pyoxigraph(
    triples: list["ox.Triple"], ox_format: "ox.RdfFormat", prefixes: dict[str, str] | None, base_iri: str | None
) -> str:
    """Serialize sorted triples, retrying without prefixes if pyoxigraph rejects one."""
    used_prefixes = prefixes
    try:
        result_bytes = ox.serialize(triples, format=ox_format, prefixes=prefixes, base_iri=base_iri)
    except ValueError as e:
        # pyoxigraph 0.5.x reports rejected prefix IRIs with a message
        # that begins with "Invalid prefix" (verified empirically). Only
        # swallow that case and retry without prefixes — any other
        # ValueError (e.g. invalid base IRI, or an unrelated future
        # serializer bug) must propagate so it surfaces as a stack trace
        # rather than silently dropping all prefix declarations.
        if not str(e).startswith("Invalid prefix"):
            raise
        warnings.warn(
            f"pyoxigraph rejected one or more prefix IRIs ({e}); serializing without "
            "prefix declarations. Output remains canonicalized but is more verbose.",
            RDFCanonicalizationWarning,
            stacklevel=4,
        )
        result_bytes = ox.serialize(triples, format=ox_format, base_iri=base_iri)
        used_prefixes = None
    result = result_bytes.decode("utf-8")
    if ox_format in _PREFIX_FORMATS and used_prefixes:
        result = _expand_trailing_dot_curies(result, used_prefixes)
    return result


def _iris_read_back(serialized: str, ox_format: "ox.RdfFormat") -> set[str]:
    """Return the IRIs rdflib reads from ``serialized``, resolving any base it declares."""
    dataset = rdflib.Dataset()
    dataset.parse(data=serialized, format=_RDFLIB_PARSE_FORMAT[ox_format])
    return {str(term) for quad in dataset.quads() for term in quad[:3] if isinstance(term, rdflib.URIRef)}


def _serialize_canonical(graph: rdflib.Graph, triples: list["ox.Triple"], ox_format: "ox.RdfFormat") -> str:
    """Serialize canonical triples with the graph's prefixes, keeping its base only if that is safe.

    Writing IRIs relative to a base is a string operation, while reading them
    back resolves references by RFC 3986 rules that rdflib does not fully
    follow: against a base ending in ``#``, ``<#a>`` reads back as
    ``...##a``, so every term silently changes. The output is therefore
    re-read, and if any IRI does not survive, the base is dropped.
    """
    base_iri = str(graph.base) if graph.base else None
    prefixes = _usable_prefixes(graph, triples, base_iri) if ox_format in _PREFIX_FORMATS else None
    result = _serialize_with_pyoxigraph(triples, ox_format, prefixes, base_iri)
    if base_iri and ox_format in _RDFLIB_PARSE_FORMAT:
        written = {
            term.value for t in triples for term in (t.subject, t.predicate, t.object) if isinstance(term, ox.NamedNode)
        }
        if _iris_read_back(result, ox_format) != written:
            warnings.warn(
                f"Writing IRIs relative to the base {base_iri!r} changes what they mean when read back; "
                "serializing without the base.",
                RDFCanonicalizationWarning,
                stacklevel=3,
            )
            result = _serialize_with_pyoxigraph(triples, ox_format, prefixes, None)
    return result


def _serialize_jsonld(graph: rdflib.Graph, triples: list["ox.Triple"]) -> str:
    """Write canonical triples as JSON-LD, keeping their canonical blank-node labels."""
    converted = [(_to_rdflib(t.subject), _to_rdflib(t.predicate), _to_rdflib(t.object)) for t in triples]
    return _jsonld_in_sorted_order(_in_sorted_order(converted, graph))


def canonicalize_rdf_graph(
    graph: rdflib.Graph,
    output_format: str = "turtle",
    diff_stable: bool = False,
) -> str:
    """Serialize an rdflib Graph deterministically using RDFC-1.0 canonicalization.

    The graph is transferred to pyoxigraph via N-Triples, canonicalized
    with RDFC-1.0, sorted, and serialized back to the requested format.
    Prefix bindings from the rdflib Graph are preserved in the output
    for formats that support them (Turtle, TriG, N3, RDF/XML). JSON-LD is
    written by rdflib from the canonical triples. Every format ends with
    exactly one newline.

    Falls back to rdflib serialization for unsupported formats or
    graphs containing non-standard RDF (e.g. literal predicates).

    :param graph: The rdflib Graph to serialize.
    :param output_format: Target serialization format (e.g. ``"turtle"``, ``"nt"``).
    :param diff_stable: If True, relabel blank nodes by a hash of their subtree
        content instead of RDFC-1.0's ordinal ``c14nN`` labels, so a small graph
        change yields a small diff. Disabled by default. The non-standard RDF
        fallback warns when it cannot apply these labels.
        See https://linkml.io/linkml/howtos/collaborative-development.html#rdf-in-version-control
    :return: Deterministic string serialization of the graph.
    :raises TypeError: If ``graph`` holds named graphs, which a single document would flatten.
    :raises ValueError: If N-Triples or N-Quads are asked for a term they cannot represent.
    """
    if isinstance(graph, rdflib.ConjunctiveGraph):
        raise TypeError(
            f"canonicalize_rdf_graph serializes a single graph, but got a {type(graph).__name__}; "
            "serializing it would merge its named graphs and drop their names."
        )
    fmt = output_format.lower()
    ox_format = _FORMAT_MAP.get(fmt)
    if ox_format is None and fmt not in _JSONLD_FORMATS:
        warnings.warn(
            f"pyoxigraph does not support format {output_format!r}; falling back to "
            "rdflib serializer. Output will not be deterministically canonicalized.",
            RDFCanonicalizationWarning,
            stacklevel=2,
        )
        return _with_one_trailing_newline(graph.serialize(format=output_format))

    # Transfer the graph to pyoxigraph via N-Triples. Fall back to rdflib if
    # the graph contains non-standard RDF (e.g. literal predicates from
    # annotations) that pyoxigraph rejects.
    nt_data = graph.serialize(format="nt")
    nt_bytes = nt_data.encode("utf-8") if isinstance(nt_data, str) else nt_data
    try:
        triples = list(ox.parse(io.BytesIO(nt_bytes), format=ox.RdfFormat.N_TRIPLES))
    except SyntaxError:
        warnings.warn(
            "Graph contains non-standard RDF (e.g. relative IRIs or literal predicates) "
            "that pyoxigraph cannot parse; falling back to rdflib. Output is still "
            "deterministic (blank-node labels are canonicalized via rdflib) but is not "
            "canonicalized with pyoxigraph RDFC-1.0.",
            RDFCanonicalizationWarning,
            stacklevel=2,
        )
        if diff_stable:
            warnings.warn(
                "diff_stable=True was requested but this graph took the rdflib fallback, "
                "which cannot apply content-hash blank-node labels. Output is "
                "deterministic but NOT diff-stable: an unrelated edit may still renumber "
                "blank nodes. Make the offending terms standard RDF (absolute IRIs, IRI "
                "predicates) to get diff-stable labels.",
                RDFCanonicalizationWarning,
                stacklevel=2,
            )
        return _with_one_trailing_newline(_deterministic_fallback_serialize(graph, output_format))

    canonical_triples = _canonical_sorted_triples(triples, diff_stable)
    if ox_format is None:
        return _with_one_trailing_newline(_serialize_jsonld(graph, canonical_triples))
    return _with_one_trailing_newline(_serialize_canonical(graph, canonical_triples, ox_format))
