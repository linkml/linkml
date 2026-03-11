import pytest
from yaml.constructor import ConstructorError

from linkml.generators.yamlgen import YAMLGenerator


def test_empty_list(input_path):
    """Check the local import behavior"""
    with pytest.raises(ConstructorError, match="Empty list elements are not allowed"):
        YAMLGenerator(input_path("issue_276.yaml")).serialize(validateonly=True)
