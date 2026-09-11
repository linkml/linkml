"""Tests for :class:`ShaclValidationPlugin`.

The plugin was previously exercised only indirectly, through the compliance
suite, so a breaking change in pyshacl surfaced as ~200 confusing compliance
failures rather than a pointed one. These cover the plugin directly.
"""

import pytest

# Imported from the module rather than the package: the plugin is intentionally
# not re-exported, so that pyshacl stays an optional dependency.
from linkml.validator.plugins.shacl_validation_plugin import ShaclValidationPlugin
from linkml.validator.report import Severity
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader


def test_conforming_instance_yields_no_results(validation_context):
    """A conforming instance produces no validation results."""
    plugin = ShaclValidationPlugin()
    result_iter = plugin.process({"id": "P:1", "name": "Person One"}, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_constraint_violation_is_reported(validation_context):
    """A SHACL constraint violation is reported with the pyshacl detail intact.

    ``telephone`` carries a pattern in personinfo.yaml, so this exercises the
    generate-shapes, dump-to-RDF and validate path end to end.
    """
    plugin = ShaclValidationPlugin()
    instance = {"id": "P:1", "name": "Person One", "telephone": "555-CALL-NOW"}

    result = next(plugin.process(instance, validation_context))

    assert result.severity is Severity.ERROR
    assert result.type == "shacl validation"
    # The message is the serialised sh:ValidationResult; assert on the parts that
    # identify the violation rather than the whole blob.
    assert "PatternConstraintComponent" in result.message
    assert "555-CALL-NOW" in result.message


def test_conversion_failure_is_reported_not_raised(validation_context):
    """A value the target class rejects is reported, not raised.

    ``age_in_years`` has maximum_value 999, which fails at class instantiation
    before SHACL is reached.
    """
    plugin = ShaclValidationPlugin()
    instance = {"id": "P:1", "name": "Person One", "age_in_years": 9999}

    result = next(plugin.process(instance, validation_context))

    assert result.severity is Severity.ERROR
    assert "failed at class instantiation stage" in result.message


def test_conversion_failure_raises_when_requested(validation_context):
    """``raise_on_conversion_error`` turns the same case into an exception."""
    plugin = ShaclValidationPlugin(raise_on_conversion_error=True)
    instance = {"id": "P:1", "name": "Person One", "age_in_years": 9999}

    with pytest.raises(Exception):  # noqa: B017 - the class raises its own error type
        next(plugin.process(instance, validation_context))


def test_closed_does_not_reject_a_conforming_instance(validation_context):
    """``closed=True`` still passes an instance that uses only declared slots."""
    plugin = ShaclValidationPlugin(closed=True)
    result_iter = plugin.process({"id": "P:1", "name": "Person One"}, validation_context)
    with pytest.raises(StopIteration):
        next(result_iter)


def test_generated_shapes_are_cached(validation_context):
    """Generating shapes populates the cache, so they are not rebuilt per instance validated.

    Note this does not assert the cache is hit on a subsequent call. The key is
    ``hash(str(context._schema))`` and ``process`` mutates the schema as a side
    effect of running the generators, so a later call can key differently and
    cache a second graph. That is worth knowing about, but it is pre-existing
    behaviour and not something this test should pin either way.
    """
    plugin = ShaclValidationPlugin()
    assert plugin._loaded_graphs == {}

    list(plugin.process({"id": "P:1", "name": "One"}, validation_context))

    assert len(plugin._loaded_graphs) == 1


_RULES_SCHEMA_YAML = """
id: https://example.org/plugin-rules
name: plugin_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/plugin-rules/
imports:
  - linkml:types
default_prefix: ex
default_range: string
enums:
  Color:
    permissible_values:
      Red:
        meaning: ex:Red
      Blue:
        meaning: ex:Blue
  Code:
    permissible_values:
      alpha:
      beta:
classes:
  Base:
    attributes:
      id:
        identifier: true
      guard: {}
      label: {}
      color:
        range: Color
      code:
        range: Code
    rules:
      - preconditions:
          slot_conditions:
            guard:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            label:
              equals_string: x
      - preconditions:
          slot_conditions:
            guard:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            color:
              equals_string: Red
      - preconditions:
          slot_conditions:
            guard:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            code:
              equals_string_in: [alpha]
  Child:
    is_a: Base
"""


@pytest.mark.parametrize("target_class", ["Base", "Child"])
@pytest.mark.parametrize(
    "instance,violates",
    [
        pytest.param({"guard": "g", "label": "x", "color": "Red", "code": "alpha"}, False, id="conforming"),
        pytest.param({"guard": "g", "label": "y", "color": "Red", "code": "alpha"}, True, id="string"),
        pytest.param({"guard": "g", "label": "x", "color": "Blue", "code": "alpha"}, True, id="enum-meaning"),
        pytest.param({"guard": "g", "label": "x", "color": "Red", "code": "beta"}, True, id="enum-literal"),
        pytest.param({"guard": "g", "color": "Red", "code": "alpha"}, True, id="target-absent"),
        pytest.param({"label": "y", "color": "Blue", "code": "beta"}, False, id="unguarded"),
    ],
)
def test_rule_violation_is_reported(target_class, instance, violates):
    """Rules translated to ``sh:sparql`` are enforced through the plugin, whose
    data graph comes from the LinkML RDF dumper, on instances of the declaring
    class and of its subclasses alike."""
    context = ValidationContext(yaml_loader.loads(_RULES_SCHEMA_YAML, SchemaDefinition), target_class)
    results = list(ShaclValidationPlugin().process({"id": "ex:x", **instance}, context))

    assert all(result.severity is Severity.ERROR for result in results)
    assert any("SPARQLConstraintComponent" in result.message for result in results) is violates
