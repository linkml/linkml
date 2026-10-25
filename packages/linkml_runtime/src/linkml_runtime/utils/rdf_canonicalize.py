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

2. **Non-standard RDF**: pyoxigraph's parser rejects a graph with literal
   predicates (for example, SHACL annotation mode) or relative IRIs (for
   example, a ``uriorcurie`` slot holding a bare value such as ``testing``).
   This function then replaces each rejected term with a placeholder IRI
   derived from the term's content, canonicalizes the result with RDFC-1.0,
   restores the original terms and serializes with rdflib, sorting
   line-oriented formats. The output is deterministic, but it is not
   standard RDF, and OWL or SHACL tools may reject it. A graph with a blank
   node in predicate position cannot be encoded this way, so it is serialized
   non-canonically with a warning.

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
import re
import warnings

import pyoxigraph as ox
import rdflib


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


#: Namespace of the placeholder IRIs that stand in for terms pyoxigraph
#: rejects while the fallback canonicalizes a graph.
_PLACEHOLDER_NS = "urn:x-linkml-nonstandard:"


def _placeholder_iri(term: rdflib.term.Node) -> str:
    """Return a placeholder IRI for ``term``, derived from its N3 form.

    The content-derived name keeps the canonicalization deterministic: the
    same relative IRI or literal predicate gets the same placeholder in every
    process.
    """
    return _PLACEHOLDER_NS + hashlib.sha256(term.n3().encode("utf-8")).hexdigest()


def _is_encodable(graph: rdflib.Graph) -> bool:
    """Check whether the fallback can represent ``graph`` in pyoxigraph.

    A blank node in predicate position has no stand-in: RDFC-1.0 labels blank
    nodes in subject and object position only. An IRI already in the
    placeholder namespace would collide with the stand-ins.
    """
    for _, predicate, _ in graph:
        if isinstance(predicate, rdflib.BNode):
            return False
    return not any(isinstance(term, rdflib.URIRef) and term.startswith(_PLACEHOLDER_NS) for term in graph.all_nodes())


def _encode_for_pyoxigraph(
    graph: rdflib.Graph,
) -> tuple[ox.Dataset, dict[str, rdflib.term.Node], dict[ox.Literal, rdflib.Literal]]:
    """Copy ``graph`` into a pyoxigraph Dataset, with placeholders for the terms pyoxigraph rejects.

    Relative IRIs, and literals in subject or predicate position, become
    placeholder IRIs (see :func:`_placeholder_iri`). Blank nodes become fresh
    pyoxigraph blank nodes. Literals in object position become pyoxigraph
    literals. One that pyoxigraph rejects also gets a placeholder.

    :return: The dataset, the placeholder IRIs mapped to the terms they stand
        for, and the pyoxigraph literals mapped to the rdflib literals to
        restore. pyoxigraph follows RDF 1.1 and identifies ``"x"`` with
        ``"x"^^xsd:string``. When a graph holds both, the one with the smaller
        N3 form is kept, so the choice is deterministic.
    """
    bnodes: dict[rdflib.BNode, ox.BlankNode] = {}
    placeholders: dict[str, rdflib.term.Node] = {}
    literals: dict[ox.Literal, rdflib.Literal] = {}

    def placeholder(term: rdflib.term.Node) -> ox.NamedNode:
        iri = _placeholder_iri(term)
        placeholders[iri] = term
        return ox.NamedNode(iri)

    def resource(term: rdflib.term.Node) -> ox.NamedNode | ox.BlankNode:
        if isinstance(term, rdflib.BNode):
            return bnodes.setdefault(term, ox.BlankNode())
        if isinstance(term, rdflib.URIRef):
            try:
                return ox.NamedNode(str(term))
            except ValueError:
                # pyoxigraph rejects the IRI (it is relative or malformed).
                return placeholder(term)
        return placeholder(term)

    def value(term: rdflib.term.Node) -> ox.NamedNode | ox.BlankNode | ox.Literal:
        if not isinstance(term, rdflib.Literal):
            return resource(term)
        try:
            literal = ox.Literal(
                str(term),
                language=term.language,
                datatype=ox.NamedNode(str(term.datatype)) if term.datatype else None,
            )
        except ValueError:
            return placeholder(term)
        kept = literals.get(literal)
        if kept is None or term.n3() < kept.n3():
            literals[literal] = term
        return literal

    dataset = ox.Dataset(ox.Quad(resource(s), resource(p), value(o), ox.DefaultGraph()) for s, p, o in graph)
    return dataset, placeholders, literals


def _decode_term(
    term: ox.NamedNode | ox.BlankNode | ox.Literal,
    placeholders: dict[str, rdflib.term.Node],
    literals: dict[ox.Literal, rdflib.Literal],
) -> rdflib.term.Node:
    """Map a canonicalized pyoxigraph term back to the rdflib term it stands for."""
    if isinstance(term, ox.BlankNode):
        return rdflib.BNode(term.value)
    if isinstance(term, ox.NamedNode):
        return placeholders.get(term.value) or rdflib.URIRef(term.value)
    return literals[term]


def _deterministic_fallback_serialize(graph: rdflib.Graph, output_format: str, diff_stable: bool) -> str:
    """Serialize a graph that pyoxigraph's parser rejects, deterministically.

    pyoxigraph rejects some graphs that rdflib accepts, notably graphs
    containing relative IRIs (for example, ``bibo:status <testing>``) or
    literal predicates (SHACL annotation mode). A plain ``graph.serialize()`` for
    such graphs is *not* reproducible across processes: rdflib assigns
    blank-node labels non-deterministically, so the structure and grouping
    of the output varies run to run.

    The fallback replaces the rejected terms with placeholder IRIs,
    canonicalizes the graph with RDFC-1.0 like any other graph, and restores
    the original terms. rdflib then serializes the result with the source
    graph's prefix and base bindings. For line-oriented formats the fallback
    sorts the serialized lines, since rdflib does not emit N-Triples/N-Quads
    in a stable order.

    Relative IRIs are preserved verbatim (not resolved against the base): the
    goal is deterministic output, and silently rewriting ``<testing>`` into an
    absolute IRI would mask what is really a data problem in the source graph.

    :param graph: The rdflib Graph that pyoxigraph could not parse.
    :param output_format: Target serialization format (for example, ``"turtle"`` or ``"nt"``).
    :param diff_stable: Apply diffable-rdf labels after RDFC-1.0 canonicalization.
    :return: Deterministic string serialization of the graph, unless the graph
        has a blank node in predicate position, which cannot be canonicalized.
    """
    if not _is_encodable(graph):
        warnings.warn(
            "Graph has a blank node in predicate position, which RDFC-1.0 cannot label; "
            "serializing non-canonically. Output is valid for rdflib but blank-node labels "
            "and triple ordering are not guaranteed stable across runs.",
            RDFCanonicalizationWarning,
            stacklevel=3,
        )
        serialized = graph.serialize(format=output_format)
    else:
        dataset, placeholders, literals = _encode_for_pyoxigraph(graph)
        offending = sorted(term.n3() for term in placeholders.values())
        warnings.warn(
            f"Graph contains non-standard RDF ({', '.join(offending[:3])}"
            f"{', ...' if len(offending) > 3 else ''}) that pyoxigraph cannot parse; "
            "OWL and SHACL tools may reject it. Output is canonicalized with RDFC-1.0 over "
            "placeholder IRIs for these terms and serialized by rdflib.",
            RDFCanonicalizationWarning,
            stacklevel=3,
        )
        dataset.canonicalize(ox.CanonicalizationAlgorithm.RDFC_1_0)
        quads = list(dataset)
        if diff_stable:
            from diffable_rdf import wl_relabel_quads

            quads = wl_relabel_quads(quads)
        canonical = rdflib.Graph()
        for quad in quads:
            canonical.add(
                tuple(
                    _decode_term(term, placeholders, literals) for term in (quad.subject, quad.predicate, quad.object)
                )
            )
        # The canonical graph starts without the source's namespace bindings.
        # Rebind them so the output does not fall back to rdflib's
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


def canonicalize_rdf_graph(
    graph: rdflib.Graph,
    output_format: str = "turtle",
    diff_stable: bool = False,
) -> str:
    """Serialize an rdflib Graph deterministically using RDFC-1.0 canonicalization.

    The graph is transferred to pyoxigraph via N-Triples, canonicalized
    with RDFC-1.0, sorted, and serialized back to the requested format.
    Prefix bindings from the rdflib Graph are preserved in the output
    for formats that support them (Turtle, TriG, N3, RDF/XML).

    Falls back to plain rdflib serialization for unsupported formats. A graph
    containing non-standard RDF (for example, literal predicates or relative
    IRIs) is canonicalized over placeholder IRIs and serialized by rdflib
    (see module docstring, limitation 2).

    :param graph: The rdflib Graph to serialize.
    :param output_format: Target serialization format (for example, ``"turtle"`` or ``"nt"``).
    :param diff_stable: Use diffable-rdf labels to reduce blank-node churn across
        edits. Requires the ``diff-stable`` extra; disabled by default.
        See https://linkml.io/linkml/howtos/collaborative-development.html#rdf-in-version-control
    :return: Deterministic string serialization of the graph.
    :raises ImportError: If diff-stable labels are requested without diffable-rdf.
    """
    if diff_stable:
        try:
            from diffable_rdf import wl_relabel_quads
        except ImportError as exc:
            raise ImportError(
                "diff_stable=True requires diffable-rdf. Install "
                "'linkml-runtime[diff-stable]' or 'linkml[diff-stable]'."
            ) from exc

    ox_format = _FORMAT_MAP.get(output_format.lower())
    if ox_format is None:
        warnings.warn(
            f"pyoxigraph does not support format {output_format!r}; falling back to "
            "rdflib serializer. Output will not be deterministically canonicalized.",
            RDFCanonicalizationWarning,
            stacklevel=2,
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
        return _deterministic_fallback_serialize(graph, output_format, diff_stable)

    dataset = ox.Dataset()
    for triple in triples:
        dataset.add(ox.Quad(triple.subject, triple.predicate, triple.object, ox.DefaultGraph()))

    # 3. Canonicalize blank node labels with RDFC-1.0.
    dataset.canonicalize(ox.CanonicalizationAlgorithm.RDFC_1_0)

    quads = list(dataset)

    if diff_stable:
        quads = wl_relabel_quads(quads)

    # 4. Sort triples for deterministic ordering.
    # RDFC-1.0 stabilizes blank-node labels but pyoxigraph's Dataset
    # iteration order is not sorted and varies across processes (verified
    # empirically against pyoxigraph 0.5.8). The explicit string-key sort
    # is load-bearing for byte-identical output across runs; see
    # tests/linkml_runtime/test_utils/test_rdf_canonicalize.py::test_sort_is_load_bearing.
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
        # Drop prefix bindings whose namespace is not referenced by any IRI
        # in the graph. This prevents the rdflib NamespaceManager's default
        # bindings (~30 well-known vocabularies) from being emitted into
        # every output file regardless of whether the schema actually uses
        # them.
        prefixes = _filter_prefixes_to_used(prefixes, _iri_terms(sorted_triples))
    used_prefixes = prefixes
    try:
        result_bytes = ox.serialize(
            sorted_triples,
            format=ox_format,
            prefixes=prefixes,
            base_iri=base_iri,
        )
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
            stacklevel=2,
        )
        result_bytes = ox.serialize(
            sorted_triples,
            format=ox_format,
        )
        used_prefixes = None
    result = result_bytes.decode("utf-8")
    if ox_format in _PREFIX_FORMATS and used_prefixes:
        result = _expand_trailing_dot_curies(result, used_prefixes)
    return result
