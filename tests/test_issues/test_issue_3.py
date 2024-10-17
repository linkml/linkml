import pytest
from linkml_runtime.linkml_model.meta import LINKML
from rdflib import XSD, Graph

from linkml import LOCAL_TYPES_YAML_FILE
from linkml.generators.rdfgen import RDFGenerator


@pytest.mark.network
def test_date_time():
    """date datatype should be rdf:date and datetime rdf:datetime"""
    rdf = RDFGenerator(LOCAL_TYPES_YAML_FILE).serialize()
    g = Graph()
    g.parse(data=rdf, format="turtle")
    assert XSD.date == g.value(LINKML.date, LINKML.uri)
    assert XSD.dateTime == g.value(LINKML.datetime, LINKML.uri)
