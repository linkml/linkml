import pytest

from linkml.utils.schemaloader import SchemaLoader


def test_issue_58(input_path):
    """Reject non NSNAME model names"""
    with pytest.raises(ValueError, match="issue 58: Not a valid NCName"):
        SchemaLoader(input_path("issue_58_error1.yaml")).resolve()
