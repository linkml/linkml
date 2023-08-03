import pytest

from linkml.generators.yamlgen import YAMLGenerator


def test_alt_description(input_path):
    """Check alt descriptions"""
    YAMLGenerator(input_path("issue_326.yaml")).serialize(validateonly=True)


def test_alt_description_2(input_path):
    with pytest.raises(ValueError, match="description must be supplied"):
        YAMLGenerator(input_path("issue_326a.yaml")).serialize(validateonly=True)
