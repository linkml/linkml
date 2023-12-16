import pytest
import yaml

from linkml.validator import validate


@pytest.fixture
def personinfo_schema_path(input_path):
    return str(input_path("personinfo.yaml"))


def test_valid_instance_against_schema_file(personinfo_schema_path):
    instance = {
        "persons": [
            {"id": "1", "full_name": "Person A"},
            {"id": "2", "full_name": "Person B"},
        ]
    }
    report = validate(instance, personinfo_schema_path)
    assert len(report.results) == 0


def test_valid_instance_against_schema_instance(personinfo_schema_path):
    with open(personinfo_schema_path) as schema_file:
        schema = yaml.safe_load(schema_file)
    instance = {
        "persons": [
            {"id": "1", "full_name": "Person A"},
            {"id": "2", "full_name": "Person B"},
        ]
    }
    report = validate(instance, schema)
    assert len(report.results) == 0


def test_invalid_instance(personinfo_schema_path):
    instance = {
        "persons": [
            {"full_name": "Person A"},
            {"full_name": "Person B"},
        ]
    }
    report = validate(instance, personinfo_schema_path)
    assert len(report.results) == 2
    assert "'id' is a required property" in report.results[0].message
    assert "'id' is a required property" in report.results[1].message


def test_valid_instance_specified_class(personinfo_schema_path):
    instance = {"id": "1", "full_name": "Person A"}
    report = validate(instance, personinfo_schema_path, "Person")
    assert len(report.results) == 0


def test_invalid_instance_specified_class(personinfo_schema_path):
    instance = {"full_name": "Person A"}
    report = validate(instance, personinfo_schema_path, "Person")
    assert len(report.results) == 1
    assert "'id' is a required property" in report.results[0].message


def test_invalid_instance_strict(personinfo_schema_path):
    instance = {
        "persons": [
            {"full_name": "Person A"},
            {"full_name": "Person B"},
        ]
    }
    report = validate(instance, personinfo_schema_path, strict=True)
    assert len(report.results) == 1
    assert "'id' is a required property" in report.results[0].message


def test_not_a_valid_schema():
    instance = {}
    schema = {"foo": "bar"}
    with pytest.raises(ValueError, match="Invalid schema"):
        validate(instance, schema)
