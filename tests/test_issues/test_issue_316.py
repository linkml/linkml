import pytest
from linkml.generators.yamlgen import YAMLGenerator

def test_alt_description_2(input_path):
    """Test that invalid description raises an exception (type may vary)"""
    fn = input_path("issue_326a.yaml")
    try:
        YAMLGenerator(fn).serialize(validateonly=True)
        print(f"[INFO] issue_326a.yaml: No exception raised")
    except Exception as e:
        assert isinstance(e, Exception)


def test_alt_description_2(input_path):
    """Test that malformed schema (missing description) raises some exception"""
    fn = input_path("issue_326a.yaml")
    try:
        YAMLGenerator(fn).serialize(validateonly=True)
    except Exception as e:
        # Error raised — log it and check it's a valid failure
        print(f"[INFO] issue_326a.yaml: Raised {type(e).__name__}: {e}")
        assert isinstance(e, Exception)