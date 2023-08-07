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
  Object:
    attributes:
      rec:
        recommended: true
      nonrec:
      nested:
        range: Object
"""


@pytest.fixture(scope="module")
def validation_context():
    schema = yaml_loader.load(SCHEMA, SchemaDefinition)
    return ValidationContext(schema, "Object")


def test_valid_instance(validation_context):
    """Valid data should not yield any results"""
    plugin = RecommendedSlotsPlugin()
    instance = {"rec": "foo"}
    result_iter = plugin.process(instance, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_missing_recommended_on_target_class(validation_context):
    """Data missing a recommended slot on the root object should yield a result"""
    plugin = RecommendedSlotsPlugin()
    instance = {"nonrec": "foo"}
    result_iter = plugin.process(instance, validation_context)
    assert next(result_iter).message == "Slot 'rec' is recommended on class 'Object'"


def test_missing_recommended_on_nested_class(validation_context):
    """Data missing a recommended slot on a nested object should yield a result"""
    plugin = RecommendedSlotsPlugin()
    instance = {"rec": "foo", "nested": {"nonrec": "foo"}}
    result_iter = plugin.process(instance, validation_context)
    assert next(result_iter).message == "Slot 'rec' is recommended on class 'Object'"


def test_incorrect_type_in_slot(validation_context):
    """Data with an incorrect type in a slot should not yield results.

    Type checking is not the responsibility of this plugin. But we want to make
    sure that the implementation of this plugin doesn't implicitly assume it will
    always get correct types.
    """
    plugin = RecommendedSlotsPlugin()
    instance = {"rec": "foo", "nested": "this is the wrong type"}
    result_iter = plugin.process(instance, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)
