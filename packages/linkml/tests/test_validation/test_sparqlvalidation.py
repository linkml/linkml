import logging

import pytest

from linkml.generators.sparqlgen import SparqlGenerator
from linkml.validators.sparqlvalidator import SparqlDataValidator
from tests.test_validation.environment import env

logger = logging.getLogger(__file__)


SCHEMA = env.input_path("kitchen_sink.yaml")
DATA = env.input_path("kitchen_sink_inst_01.ttl")


@pytest.fixture
def validator():
    SparqlGenerator(SCHEMA)
    sv = SparqlDataValidator()
    sv.load_schema(SCHEMA)
    return sv


@pytest.mark.skip(
    reason="ttl file not present; rdflib bug on parsing sparql queries. see: https://github.com/linkml/linkml/issues/2504"
)
def test_sparql_validation(validator):
    """Validate using in-memory sparql"""
    results = validator.validate_file(DATA)
    logger.info(results)
    assert results is not None
