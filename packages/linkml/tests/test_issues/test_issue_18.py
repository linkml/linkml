import pytest
from linkml_runtime.utils.yamlutils import as_yaml

from linkml.utils.schemaloader import SchemaLoader


def test_issue_18(input_path, snapshot):
    """Make sure that inverses are automatically generated"""
    output = as_yaml(SchemaLoader(input_path("issue_18.yaml")).resolve())
    assert output == snapshot("issue_18.yaml")


def test_inverse_mismatch(input_path):
    """Test error detection when inverses don't match"""
    with pytest.raises(ValueError, match=r"Slot s1.inverse \(s2\) does not match slot s2.inverse \(s3\)"):
        SchemaLoader(input_path("issue_18_error1.yaml")).resolve()


def test_missing_inverse(input_path):
    with pytest.raises(ValueError, match=r"Slot s1.inverse \(s2\) is not defined"):
        SchemaLoader(input_path("issue_18_error2.yaml")).resolve()


def test_no_inverse_domain(input_path):
    match = r"Unable to determine the range of slot `s1'. Its inverse \(s2\) has no declared domain"
    with pytest.raises(ValueError, match=match):
        SchemaLoader(input_path("issue_18_error3.yaml")).resolve()


def test_multi_domains(caplog, input_path):
    SchemaLoader(input_path("issue_18_warning1.yaml")).resolve()
    assert "Slot s2.inverse (s1), has multi domains (c1, c2)  Multi ranges not yet implemented" in caplog.text
