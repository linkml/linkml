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


def test_shapes_are_cached_per_schema(validation_context):
    """Generated shape graphs are reused rather than regenerated per instance."""
    plugin = ShaclValidationPlugin()
    list(plugin.process({"id": "P:1", "name": "One"}, validation_context))
    assert len(plugin._loaded_graphs) == 1
    first = next(iter(plugin._loaded_graphs.values()))

    list(plugin.process({"id": "P:2", "name": "Two"}, validation_context))
    assert len(plugin._loaded_graphs) == 1
    assert next(iter(plugin._loaded_graphs.values())) is first
