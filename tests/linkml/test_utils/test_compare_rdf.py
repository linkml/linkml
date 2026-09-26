from rdflib import BNode, Graph, URIRef

from tests.linkml.utils.compare_rdf import compare_rdf


def _pathological_ttl(n_pairs: int) -> str:
    """Turtle text with ``n_pairs`` disjoint symmetric blank-node pairs.

    Same structural pattern used in
    ``tests/linkml_runtime/test_utils/test_rdf_canonicalize.py`` to
    reproduce the OWL metamodel hang: this shape is what makes
    ``rdflib.compare.to_canonical_graph``/``graph_diff`` blow up.
    """
    g = Graph()
    g.bind("ex", "http://example.com/")
    p = URIRef("http://example.com/p")
    for _ in range(n_pairs):
        b1, b2 = BNode(), BNode()
        g.add((b1, p, b2))
        g.add((b2, p, b1))
    return g.serialize(format="turtle")


def test_compare_rdf_matches_identical_graphs():
    ttl = "@prefix ex: <http://example.com/> .\nex:a ex:p ex:b .\n"
    assert compare_rdf(ttl, ttl) is None


def test_compare_rdf_reports_differences():
    expected = "@prefix ex: <http://example.com/> .\nex:a ex:p ex:b, ex:c .\n"
    actual = "@prefix ex: <http://example.com/> .\nex:a ex:p ex:b, ex:d .\n"
    result = compare_rdf(expected, actual)
    assert result is not None
    assert "Missing Triples" in result
    assert "Added Triples" in result
    assert "ex:c" in result
    assert "ex:d" in result


def test_compare_rdf_on_pathological_graph_completes_quickly():
    """Regression test: comparing two graphs with symmetric blank-node
    structure must not hang.

    This is the exact shape (minus the literal-predicate trigger, which is
    irrelevant here since ``compare_rdf`` no longer routes through
    pyoxigraph at all) that made ``rdflib.compare.graph_diff``/
    ``to_isomorphic`` -- previously called directly by ``compare_rdf`` --
    take an unbounded amount of time on the real OWL metamodel graph.
    """
    ttl = _pathological_ttl(8)
    assert compare_rdf(ttl, ttl) is None
