import logging

import pytest
from linkml_runtime.dumpers import yaml_dumper

from linkml.validators.sparqlvalidator import SparqlDataValidator
from tests import SKIP_REMOTE_SPARQL_TESTS
from tests.test_validation.environment import env

logger = logging.getLogger(__name__)

SCHEMA = env.input_path("omo.yaml")
REPORT = env.expected_path("omo-report.yaml")

NGS = [
    "<http://purl.obolibrary.org/obo/merged/OBI>",
    "<http://purl.obolibrary.org/obo/merged/GO>",
]


@pytest.fixture
def validator():
    sv = SparqlDataValidator()
    sv.load_schema(SCHEMA)
    return sv


def test_sparql_validation_load_schema(validator):
    """Only load a schema"""
    assert validator.schema is not None


@pytest.mark.skipif(SKIP_REMOTE_SPARQL_TESTS, reason="Skipping ontobee test")
def test_remote_sparql_validation(validator):
    """Validate a schema"""
    results = validator.validate_endpoint("http://sparql.hegroup.org/sparql", named_graphs=NGS)
    logger.info(results)
    yaml_dumper.dump(results, to_file=REPORT)
