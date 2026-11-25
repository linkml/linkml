import json
from pathlib import Path

import pytest

from linkml.validator.loaders import default_loader_for_file
from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.report import Severity
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition
from linkml_runtime.loaders import yaml_loader


def test_valid_instance(validation_context):
    plugin = JsonschemaValidationPlugin()
    instance = {"id": "1", "name": "Person One"}
    result_iter = plugin.process(instance, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_invalid_instance(validation_context):
    plugin = JsonschemaValidationPlugin()
    instance = {"id": "1", "name": "Person One", "telephone": "555-CALL-NOW"}
    result_iter = plugin.process(instance, validation_context)
    assert "'555-CALL-NOW' does not match" in next(result_iter).message
    with pytest.raises(StopIteration):
        next(result_iter)


def test_invalid_instance_closed(validation_context):
    plugin = JsonschemaValidationPlugin(closed=True)
    instance = {
        "id": "1",
        "name": "Person One",
        "whoops": "my bad",
    }
    result_iter = plugin.process(instance, validation_context)
    message = next(result_iter).message
    assert "Additional properties" in message
    assert "whoops" in message
    with pytest.raises(StopIteration):
        next(result_iter)


def test_path_override(validation_context, tmp_file_factory):
    cached_json_schema = tmp_file_factory(
        "schema.json",
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2019-09/schema",
                "type": "object",
                "properties": {"a": {"type": "number"}},
                "required": ["a"],
            }
        ),
    )
    plugin = JsonschemaValidationPlugin(json_schema_path=cached_json_schema)

    # with the cached json schema path provided, we're *not* validating against personinfo anymore
    invalid_instance = {"id": "1", "full_name": "Person One"}
    result_iter = plugin.process(invalid_instance, validation_context)
    message = next(result_iter).message
    assert "required property" in message
    assert "a" in message

    valid_instance = {"a": 1}
    result_iter = plugin.process(valid_instance, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_include_range_class_descendants():
    schema = SchemaDefinition(
        id="test_include_range_class_descendants",
        name="test_include_range_class_descendants",
        classes=[
            ClassDefinition(
                name="Root",
                attributes=[SlotDefinition(name="thing", range="A")],
                tree_root=True,
            ),
            ClassDefinition(name="A", attributes=[SlotDefinition(name="a")]),
            ClassDefinition(name="B", is_a="A", attributes=[SlotDefinition(name="b")]),
        ],
    )
    validation_context = ValidationContext(schema)

    plugin = JsonschemaValidationPlugin(include_range_class_descendants=True, closed=True)
    results = list(plugin.process({"thing": {"a": "1"}}, validation_context))
    assert results == []

    results = list(plugin.process({"thing": {"a": "1", "b": "2"}}, validation_context))
    assert results == []

    plugin = JsonschemaValidationPlugin(include_range_class_descendants=False, closed=True)
    results = list(plugin.process({"thing": {"a": "1"}}, validation_context))
    assert results == []

    results = list(plugin.process({"thing": {"a": "1", "b": "2"}}, validation_context))
    assert len(results) == 1
    assert "'b' was unexpected" in results[0].message


@pytest.mark.parametrize("closed", [True, False])
def test_null_for_optional_slots(input_path, closed):
    """
    Null values for optional slots should be valid
    """

    data = input_path("not_required_data.yaml")
    data_loader = default_loader_for_file(data)

    # borrow the schema from the generator tests
    schema_file = str(Path(__file__).parents[1] / "test_generators" / "input" / "not_required.yaml")
    schema = yaml_loader.load(schema_file, SchemaDefinition)
    ctx = ValidationContext(schema, "Optionals")

    plugin = JsonschemaValidationPlugin(closed=closed)

    results = []
    for index, instance in enumerate(data_loader.iter_instances()):
        results.extend(plugin.process(instance, ctx))

    assert len(results) == 0


OPEN_ENUM_SCHEMA = """
id: https://example.org/open_enum
name: open_enum
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
enums:
  Family:
    is_open: true
    permissible_values:
      GATEWAY:
      DAEMON:
  Status:
    permissible_values:
      ACTIVE:
classes:
  Component:
    tree_root: true
    attributes:
      family:
        range: Family
      families:
        range: Family
        multivalued: true
      status:
        range: Status
      family_or_count:
        any_of:
          - range: Family
          - range: integer
"""


@pytest.fixture(scope="module")
def open_enum_context() -> ValidationContext:
    return ValidationContext(yaml_loader.load(OPEN_ENUM_SCHEMA, SchemaDefinition), "Component")


def _unlisted(value: str, path: str) -> tuple[Severity, str]:
    return Severity.WARN, f"{value!r} is not among the permissible values of open enum 'Family' in {path}"


@pytest.mark.parametrize(
    ("instance", "expected"),
    [
        ({"family": "GATEWAY", "families": ["DAEMON"], "status": "ACTIVE", "family_or_count": 3}, []),
        ({"family": "UNLISTED"}, [_unlisted("UNLISTED", "/family")]),
        ({"families": ["GATEWAY", "OTHER"]}, [_unlisted("OTHER", "/families/1")]),
        ({"family_or_count": "OTHER"}, [_unlisted("OTHER", "/family_or_count")]),
        (
            {"family": "UNLISTED", "status": "RETIRED"},
            [(Severity.ERROR, "'RETIRED' is not one of ['ACTIVE'] in /status"), _unlisted("UNLISTED", "/family")],
        ),
    ],
)
def test_open_enum_unlisted_value_warns(open_enum_context, instance, expected):
    """A value an open enum does not list is a warning; a closed enum's is still an error."""
    plugin = JsonschemaValidationPlugin(closed=True)
    results = list(plugin.process(instance, open_enum_context))
    assert [(r.severity, r.message) for r in results] == expected


def test_open_enum_validator_needs_an_open_enum(validation_context, open_enum_context):
    """Only a schema with an open enum gets the second validation pass."""
    options = {"closed": True, "include_range_class_descendants": True}
    assert validation_context.open_enum_validator(**options) is None
    assert open_enum_context.open_enum_validator(**options) is not None
