"""Tests for the ``closed`` and ``config`` kwargs of ``_get_default_validator``."""

import yaml

from linkml.validator import _get_default_validator
from linkml.validator.plugins import JsonschemaValidationPlugin


def _has_additional_props_error(report) -> bool:
    return any("Additional properties" in r.message for r in report.results)


def test_default_is_closed(input_path):
    """By default, the validator runs closed-world JSON Schema validation."""
    validator = _get_default_validator(input_path("personinfo.yaml"))
    instance = {"id": "1", "name": "A", "whoops": "extra"}
    report = validator.validate(instance, "Person")
    assert _has_additional_props_error(report), [r.message for r in report.results]


def test_closed_false_kwarg_allows_extra_properties(input_path):
    """``closed=False`` should suppress 'Additional properties are not allowed' errors."""
    validator = _get_default_validator(input_path("personinfo.yaml"), closed=False)
    instance = {"id": "1", "name": "A", "whoops": "extra"}
    report = validator.validate(instance, "Person")
    assert not _has_additional_props_error(report), [r.message for r in report.results]


def test_config_path_overrides_closed(input_path, tmp_path):
    """A ``--config``-style YAML mapping should override the bundled default."""
    config_path = tmp_path / "validation-config.yaml"
    config_path.write_text(yaml.safe_dump({"plugins": {"JsonschemaValidationPlugin": {"closed": False}}}))
    validator = _get_default_validator(input_path("personinfo.yaml"), config=config_path)
    instance = {"id": "1", "name": "A", "whoops": "extra"}
    report = validator.validate(instance, "Person")
    assert not _has_additional_props_error(report), [r.message for r in report.results]


def test_config_dict_overrides_closed(input_path):
    """An in-memory config dict is accepted equivalently to a YAML path."""
    config = {"plugins": {"JsonschemaValidationPlugin": {"closed": False}}}
    validator = _get_default_validator(input_path("personinfo.yaml"), config=config)
    instance = {"id": "1", "name": "A", "whoops": "extra"}
    report = validator.validate(instance, "Person")
    assert not _has_additional_props_error(report), [r.message for r in report.results]


def test_config_takes_precedence_over_closed_kwarg(input_path):
    """When both are passed, plugins from ``config`` win and ``closed`` is ignored."""
    config = {"plugins": {"JsonschemaValidationPlugin": {"closed": False}}}
    validator = _get_default_validator(input_path("personinfo.yaml"), closed=True, config=config)
    plugins = validator._validation_plugins  # noqa: SLF001
    assert len(plugins) == 1
    assert isinstance(plugins[0], JsonschemaValidationPlugin)
    assert plugins[0].closed is False
