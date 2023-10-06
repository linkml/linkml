import json

import pytest
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.validation_context import ValidationContext


@pytest.fixture
def validation_context(input_path) -> ValidationContext:
    schema = yaml_loader.load(input_path("personinfo.yaml"), SchemaDefinition)
    return ValidationContext(schema, "Person")


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
