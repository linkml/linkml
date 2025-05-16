import pytest
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.validator.plugins.recommended_slots_plugin import RecommendedSlotsPlugin
from linkml.validator.validation_context import ValidationContext

SCHEMA = """id: https://w3id.org/test/recommended_slots
name: recommended_slots
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
default_range: string
types:
  string:
    uri: xsd:string
    base: str
    description: A character string
    exact_mappings:
      - schema:Text
classes:
  Inlined:
    attributes:
      id:
        identifier: true
      value1:
        recommended: true
      value2:
  Object:
    attributes:
      rec:
        recommended: true
      nonrec:
      nested:
        range: Object
      nested_inline:
        range: Inlined
        multivalued: true
        inlined: true
      nested_inline_list:
        range: Inlined
        multivalued: true
        inlined_as_list: true
      rec_2:
        recommended: true
"""


@pytest.fixture(scope="module")
def validation_context():
    schema = yaml_loader.load(SCHEMA, SchemaDefinition)
    return ValidationContext(schema, "Object")


def test_valid_instance(validation_context):
    """Valid data should not yield any results"""
    plugin = RecommendedSlotsPlugin()
    instance = {"rec": "foo", "rec_2": "bar"}
    result_iter = plugin.process(instance, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_missing_recommended_on_target_class(validation_context):
    """Data missing a recommended slot on the root object should yield a result"""
    plugin = RecommendedSlotsPlugin()
    instance = {"nonrec": "foo"}
    result_iter = plugin.process(instance, validation_context)
    assert next(result_iter).message == "Slot 'rec' is recommended on class 'Object' in /"
    assert next(result_iter).message == "Slot 'rec_2' is recommended on class 'Object' in /"
    with pytest.raises(StopIteration):
        next(result_iter)


def test_missing_recommended_on_nested_class(validation_context):
    """Data missing a recommended slot on a nested object should yield a result"""
    plugin = RecommendedSlotsPlugin()
    instance = {"rec": "foo", "nested": {"nonrec": "foo"}, "rec_2": "bar"}
    result_iter = plugin.process(instance, validation_context)
    assert next(result_iter).message == "Slot 'rec' is recommended on class 'Object' in /nested"
    assert next(result_iter).message == "Slot 'rec_2' is recommended on class 'Object' in /nested"
    with pytest.raises(StopIteration):
        next(result_iter)


def test_incorrect_type_in_slot(validation_context):
    """Data with an incorrect type in a slot should not yield results.

    Type checking is not the responsibility of this plugin. But we want to make
    sure that the implementation of this plugin doesn't implicitly assume it will
    always get correct types.
    """
    plugin = RecommendedSlotsPlugin()
    instance = {"rec": "foo", "rec_2": "bar", "nested": "this is the wrong type"}
    result_iter = plugin.process(instance, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_missing_recommended_inlined(validation_context):
    """Data missing a recommended slot on an object in an inlined collection should yield a result"""

    plugin = RecommendedSlotsPlugin()
    instance = {
        "rec": "foo",
        "rec_2": "foo",
        "nested_inline": {"a": {"value1": "1"}, "b": {"value1": "2"}, "c": {"value2": "3"}},
    }
    result_iter = plugin.process(instance, validation_context)
    assert next(result_iter).message == "Slot 'value1' is recommended on class 'Inlined' in /nested_inline/c"
    with pytest.raises(StopIteration):
        next(result_iter)


def test_incorrect_type_in_multivalued_slot(validation_context):
    """Data with non-inlined multivalued slot with class as range should not yield results.

    Type checking is not the responsibility of this plugin. But we want to make
    sure that the implementation of this plugin doesn't implicitly assume it will
    always get correct types."""

    plugin = RecommendedSlotsPlugin()
    instance = {
        "rec": "foo",
        "rec_2": "foo",
        "nested_inline": [
            {"id": "a", "value1": "1"},
            {"id": "b", "value1": "2"},
            {"id": "c", "value2": "3"},
        ],
        "nested_inline_list": {"a": {"value1": "1"}, "b": {"value1": "2"}, "c": {"value2": "3"}},
    }
    result_iter = plugin.process(instance, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_missing_recommended_inlined_as_list(validation_context):
    """Data missing a recommended slot on an object in an inlined list should yield a result"""

    plugin = RecommendedSlotsPlugin()
    instance = {
        "rec": "foo",
        "rec_2": "foo",
        "nested_inline_list": [
            {"id": "a", "value1": "1"},
            {"id": "b", "value1": "2"},
            {"id": "c", "value2": "3"},
        ],
    }
    result_iter = plugin.process(instance, validation_context)
    assert next(result_iter).message == "Slot 'value1' is recommended on class 'Inlined' in /nested_inline_list/2"
    with pytest.raises(StopIteration):
        next(result_iter)


def test_missing_recommended_multiple_inlined(validation_context):
    """Data missing recommended slots on multiple nested inlined objects should yield a result"""

    plugin = RecommendedSlotsPlugin()
    instance = {
        "rec": "foo",
        "rec_2": "foo",
        "nested_inline": {"a": {"value1": "1"}, "b": {"value1": "2"}, "c": {"value2": "3"}},
        "nested_inline_list": [
            {"id": "a", "value1": "1"},
            {"id": "b", "value1": "2"},
            {"id": "c", "value2": "3"},
        ],
    }
    result_iter = plugin.process(instance, validation_context)
    assert next(result_iter).message == "Slot 'value1' is recommended on class 'Inlined' in /nested_inline/c"
    assert next(result_iter).message == "Slot 'value1' is recommended on class 'Inlined' in /nested_inline_list/2"
    with pytest.raises(StopIteration):
        next(result_iter)


def test_missing_recommended_last_slot_with_nested_objects(validation_context):
    """Data with nested objects missing the last recommended slot in a schema should yield a result"""

    plugin = RecommendedSlotsPlugin()
    instance = {
        "nested": {"rec": "foo", "rec_2": "bar", "nested_inline_list": [{"id": "a", "value1": "1"}]},
        "rec": "foo",
    }
    result_iter = plugin.process(instance, validation_context)
    with pytest.raises(StopIteration):
        assert next(result_iter).message == "Slot 'rec_2' is recommended on class 'Object' in /"
        next(result_iter)
