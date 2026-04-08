import pytest
from rdflib import XSD, Graph

from linkml import LOCAL_TYPES_YAML_FILE
from linkml.generators.rdfgen import RDFGenerator
from linkml_runtime.linkml_model.meta import LINKML


@pytest.mark.network
def test_date_time():
    """date datatype should be rdf:date and datetime rdf:datetime"""
    rdf = RDFGenerator(LOCAL_TYPES_YAML_FILE).serialize()
    g = Graph()
    g.parse(data=rdf, format="turtle")
    assert str(XSD.date) == str(g.value(LINKML.date, LINKML.uri))
    assert str(XSD.dateTime) == str(g.value(LINKML.datetime, LINKML.uri))
