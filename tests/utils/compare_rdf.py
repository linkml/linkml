import re
from contextlib import redirect_stdout
from io import StringIO
from typing import Union, Optional

from rdflib import Graph, RDF, Namespace
from rdflib.compare import to_isomorphic, IsomorphicGraph, graph_diff

from linkml_runtime.linkml_model.meta import LINKML

# TODO: Find out why test_issue_namespace is emitting generation_date in the TYPE namespace
from tests import SKIP_RDF_COMPARE, SKIP_RDF_COMPARE_REASON

TYPE = LINKML


def to_graph(inp: Union[Graph, str], fmt: Optional[str] = "turtle") -> Graph:
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
    if not inp.strip().startswith('{') and '\n' not in inp and '\r' not in inp:
        with open(inp) as f:
            inp = f.read()
    g.parse(data=inp, format=fmt)
    return g


def print_triples(g: Graph) -> None:
    """
    Print the contents of g into stdout
    :param g: graph to print
    """
    g_text = re.sub(r'@prefix.*\n', '', g.serialize(format="turtle").decode())
    print(g_text)


def compare_rdf(expected: Union[Graph, str], actual: Union[Graph, str], fmt: Optional[str] = "turtle") -> Optional[str]:
    """
    Compare expected to actual, returning a string if there is a difference
    :param expected: expected RDF. Can be Graph, file name, uri or text
    :param actual: actual RDF. Can be Graph, file name, uri or text
    :param fmt: RDF format
    :return: None if they match else summary of difference
    """
    def rem_metadata(g: Graph) -> IsomorphicGraph:
        # Remove list declarations from target
        for s in g.subjects(RDF.type, RDF.List):
            g.remove((s, RDF.type, RDF.List))
        for t in g:
            if t[1] in (LINKML.generation_date, LINKML.source_file_date, LINKML.source_file_size,
                        TYPE.generation_date, TYPE.source_file_date, TYPE.source_file_size):
                g.remove(t)
        g_iso = to_isomorphic(g)
        return g_iso

    # Bypass compare if settings have turned it off
    if SKIP_RDF_COMPARE:
        print(f"tests/utils/compare_rdf.py: {SKIP_RDF_COMPARE_REASON}")
        return None

    expected_graph = to_graph(expected, fmt)
    expected_isomorphic = rem_metadata(expected_graph)
    actual_graph = to_graph(actual, fmt)
    actual_isomorphic = rem_metadata(actual_graph)

    # Graph compare takes a Looong time
    in_both, in_old, in_new = graph_diff(expected_isomorphic, actual_isomorphic)
    # if old_iso != new_iso:
    #     in_both, in_old, in_new = graph_diff(old_iso, new_iso)
    old_len = len(list(in_old))
    new_len = len(list(in_new))
    if old_len or new_len:
        txt = StringIO()
        with redirect_stdout(txt):
            print("----- Missing Triples -----")
            if old_len:
                print_triples(in_old)
            print("----- Added Triples -----")
            if new_len:
                print_triples(in_new)
        return txt.getvalue()
    return None
