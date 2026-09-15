import re
from contextlib import redirect_stdout
from io import StringIO

from rdflib import RDF, Graph

from linkml_runtime.linkml_model.meta import LINKML
from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph

# TODO: Find out why test_issue_namespace is emitting generation_date in the TYPE namespace
from tests import SKIP_RDF_COMPARE, SKIP_RDF_COMPARE_REASON

TYPE = LINKML


def to_graph(inp: Graph | str, fmt: str | None = "turtle") -> Graph:
    """
    Convert inp into a graph
    :param inp: Graph, file name, url or text
    :param fmt: expected format of inp
    :return: Graph representing inp
    """
    if isinstance(inp, Graph):
        return inp
    g = Graph()
    # If there is no input then return an empty graph
    if not inp.strip():
        return g
    if not inp.strip().startswith("{") and "\n" not in inp and "\r" not in inp:
        with open(inp) as f:
            inp = f.read()
    g.parse(data=inp, format=fmt)
    return g


def print_triples(g: Graph) -> None:
    """
    Print the contents of g into stdout
    :param g: graph to print
    """
    g_text = re.sub(r"@prefix.*\n", "", canonicalize_rdf_graph(g, output_format="turtle"))
    print(g_text)


def compare_rdf(
    expected: Graph | str,
    actual: Graph | str,
    fmt: str | None = "turtle",
) -> str | None:
    """
    Compare expected to actual, returning a string if there is a difference
    :param expected: expected RDF. Can be Graph, file name, uri or text
    :param actual: actual RDF. Can be Graph, file name, uri or text
    :param fmt: RDF format
    :return: None if they match else summary of difference
    """

    def rem_metadata(g: Graph) -> Graph:
        # Remove list declarations from target
        for s in g.subjects(RDF.type, RDF.List):
            g.remove((s, RDF.type, RDF.List))
        for t in g:
            if t[1] in (
                LINKML.generation_date,
                LINKML.source_file_date,
                LINKML.source_file_size,
                TYPE.generation_date,
                TYPE.source_file_date,
                TYPE.source_file_size,
            ):
                g.remove(t)
        return g

    def to_subgraph(lines: set[str], source_graph: Graph) -> Graph:
        # Rebuild a Graph from a subset of canonical N-Triples lines,
        # keeping the source graph's prefixes so print_triples() output
        # stays readable.
        sub = Graph()
        for prefix, namespace in source_graph.namespace_manager.namespaces():
            sub.bind(prefix, namespace)
        if lines:
            sub.parse(data="\n".join(lines), format="nt")
        return sub

    # Bypass compare if settings have turned it off
    if SKIP_RDF_COMPARE:
        print(f"tests/utils/compare_rdf.py: {SKIP_RDF_COMPARE_REASON}")
        return None

    expected_graph = rem_metadata(to_graph(expected, fmt))
    actual_graph = rem_metadata(to_graph(actual, fmt))

    # Isomorphism check via canonical N-Triples: same canonicalizer the
    # generators use (fast pyoxigraph RDFC-1.0 path in the common case,
    # timeout-bounded rdflib fallback otherwise -- see rdf_canonicalize.py),
    # instead of rdflib.compare.graph_diff/to_isomorphic, which has no
    # complexity bound and can hang on graphs with symmetric blank-node
    # structure.
    expected_nt = canonicalize_rdf_graph(expected_graph, output_format="nt")
    actual_nt = canonicalize_rdf_graph(actual_graph, output_format="nt")
    if expected_nt == actual_nt:
        return None

    expected_lines = set(expected_nt.splitlines())
    actual_lines = set(actual_nt.splitlines())
    missing_lines = expected_lines - actual_lines
    added_lines = actual_lines - expected_lines

    in_old = to_subgraph(missing_lines, expected_graph)
    in_new = to_subgraph(added_lines, actual_graph)

    txt = StringIO()
    with redirect_stdout(txt):
        print("----- Missing Triples -----")
        if missing_lines:
            print_triples(in_old)
        print("----- Added Triples -----")
        if added_lines:
            print_triples(in_new)
    return txt.getvalue()
