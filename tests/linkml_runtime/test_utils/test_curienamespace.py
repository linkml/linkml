import pytest
from rdflib import URIRef

from linkml_runtime.utils.curienamespace import CurieNamespace


def test_basics():
    BFO = CurieNamespace("bfo", "http://purl.obolibrary.org/obo/BFO_")
    assert URIRef("http://purl.obolibrary.org/obo/BFO_test") == BFO.test
    assert "http://purl.obolibrary.org/obo/BFO_" == BFO
    assert "bfo:test" == BFO.curie("test")
    assert "bfo:" == BFO.curie()


@pytest.mark.xfail(reason="curie can't be a local name at the moment")
def test_curie_as_curie():
    """curie can't be a local name at the moment"""
    BFO = CurieNamespace("bfo", "http://purl.obolibrary.org/obo/BFO_")
    assert "bfo:curie" == BFO.curie
