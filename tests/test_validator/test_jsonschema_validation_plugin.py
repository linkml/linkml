import json
from pathlib import Path

import pytest
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.validator.loaders import default_loader_for_file
from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.validation_context import ValidationContext


def test_valid_instance(validation_context):
    plugin = JsonschemaValidationPlugin()
    instance = {"id": "1", "full_name": "Person One"}
    result_iter = plugin.process(instance, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_invalid_instance(validation_context):
    plugin = JsonschemaValidationPlugin()
    instance = {"id": "1", "full_name": "Person One", "phone": "555-CALL-NOW"}
    result_iter = plugin.process(instance, validation_context)
    assert "'555-CALL-NOW' does not match" in next(result_iter).message
    with pytest.raises(StopIteration):
        next(result_iter)


def test_invalid_instance_closed(validation_context):
    plugin = JsonschemaValidationPlugin(closed=True)
    instance = {
        "id": "1",
        "full_name": "Person One",
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

    plugin = JsonschemaValidationPlugin(include_range_class_descendants=True)
    results = list(plugin.process({"thing": {"a": "1"}}, validation_context))
    assert results == []

    results = list(plugin.process({"thing": {"a": "1", "b": "2"}}, validation_context))
    assert results == []

    plugin = JsonschemaValidationPlugin(include_range_class_descendants=False)
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
