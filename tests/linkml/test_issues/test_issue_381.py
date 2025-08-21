import pytest
from linkml_runtime.linkml_model.meta import LINKML
from rdflib import Graph, Namespace

from linkml.generators.rdfgen import RDFGenerator

NS = Namespace("https://example.org/test/")

schema = f"""id: {NS}
enums:
  test_enum:
    permissible_values:
      a b:
"""


@pytest.mark.network
def test_non_url_pv():
    """Test URL generation w/ non-mangled values"""
    g = Graph()
    g.parse(data=RDFGenerator(schema).serialize(), format="ttl")
    assert str(g.value(NS.test_enum, LINKML.permissible_values)) == "https://example.org/test/a%20b"
