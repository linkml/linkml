import pytest
import yaml

from linkml.validator import validate


@pytest.fixture
def personinfo_schema_path(input_path):
    return str(input_path("personinfo.yaml"))


def test_valid_instance_against_schema_file(personinfo_schema_path):
    instance = {
        "persons": [
            {"id": "1", "name": "Person A"},
            {"id": "2", "name": "Person B"},
        ]
    }
    report = validate(instance, personinfo_schema_path)
    assert len(report.results) == 0


def test_valid_instance_against_schema_instance(personinfo_schema_path):
    with open(personinfo_schema_path) as schema_file:
        schema = yaml.safe_load(schema_file)
    instance = {
        "persons": [
            {"id": "1", "name": "Person A"},
            {"id": "2", "name": "Person B"},
        ]
    }
    report = validate(instance, schema)
    assert len(report.results) == 0


def test_invalid_instance(personinfo_schema_path):
    instance = {
        "persons": [
            {"name": "Person A"},
            {"name": "Person B"},
        ]
    }
    report = validate(instance, personinfo_schema_path)
    assert len(report.results) == 2
    assert "'id' is a required property" in report.results[0].message
    assert "'id' is a required property" in report.results[1].message


def test_valid_instance_specified_class(personinfo_schema_path):
    instance = {"id": "1", "name": "Person A"}
    report = validate(instance, personinfo_schema_path, "Person")
    assert len(report.results) == 0


def test_invalid_instance_specified_class(personinfo_schema_path):
    instance = {"name": "Person A"}
    report = validate(instance, personinfo_schema_path, "Person")
    assert len(report.results) == 1
    assert "'id' is a required property" in report.results[0].message


def test_invalid_instance_strict(personinfo_schema_path):
    instance = {
        "persons": [
            {"name": "Person A"},
            {"name": "Person B"},
        ]
    }
    report = validate(instance, personinfo_schema_path, strict=True)
    assert len(report.results) == 1
    assert "'id' is a required property" in report.results[0].message


def test_not_a_valid_schema():
    """Ensure that schema validation fails for a structurally invalid schema"""
    instance = {}
    schema = {"foo": "bar"}
    try:
        validate(instance, schema)
        assert False, "Expected an exception due to invalid schema, but none was raised"
    except Exception:
        pass  # This is expected


def test_importmap_forwarded_to_validator():
    """The module-level ``validate`` forwards ``importmap`` so a schema with a
    custom import URI resolves against an in-memory imported schema dict."""
    base_schema = {
        "id": "https://example.org/base_schema/0.1.0",
        "name": "base_schema",
        "prefixes": {"linkml": "https://w3id.org/linkml/"},
        "imports": ["linkml:types"],
        "classes": {"Record": {"tree_root": True, "attributes": {"code": {"equals_string": "OK"}}}},
    }
    user_schema = {
        "id": "https://example.org/user_schema",
        "name": "user_schema",
        "prefixes": {"linkml": "https://w3id.org/linkml/"},
        "imports": ["linkml:types", "https://example.org/base_schema/0.1.0"],
    }
    importmap = {"https://example.org/base_schema/0.1.0": base_schema}

    bad = validate({"code": "nope"}, user_schema, "Record", importmap=importmap)
    assert [r.message for r in bad.results] == ["'OK' was expected in /code"]

    good = validate({"code": "OK"}, user_schema, "Record", importmap=importmap)
    assert good.results == []
