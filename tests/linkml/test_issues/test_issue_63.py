import pytest

from linkml.utils.schemaloader import SchemaLoader


def test_issue_63(input_path):
    """We should get an error from this -- we have a list as an object"""
    with pytest.raises(ValueError, match=r"\['s3'\] is not a valid URI or CURIE"):
        SchemaLoader(input_path("issue_63.yaml"))
