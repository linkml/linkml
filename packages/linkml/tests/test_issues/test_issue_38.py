import pytest

from linkml.generators.csvgen import CsvGenerator
from tests import DEFAULT_LOG_LEVEL


@pytest.mark.skip("issue_38.yaml clinical profile conflicts with latest Biolink Model")
def test_domain_slots(input_path):
    """Subsets need to be imported as well"""
    CsvGenerator(
        input_path("issue_38.yaml"),
        log_level=DEFAULT_LOG_LEVEL,
        importmap=input_path("biolink-model-importmap.json"),
    ).serialize()
