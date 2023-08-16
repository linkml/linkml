"""
**Experimental**

The linkml.validator package contains a new LinkML validation framework that is still under
active development. Eventually it will be the recommended replacement for classes in the
linkml.validators package. You may use this package in the meantime but the behavior is subject
to change, even in patch releases.

See: https://github.com/linkml/linkml/issues/1494
"""
import os
from pathlib import Path
from typing import Any, Optional, Union

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.validator.loaders import (
    default_loader_for_file,
)
from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.report import ValidationReport
from linkml.validator.validator import Validator


def _get_default_validator(
    schema: Union[str, dict, Path, SchemaDefinition],
    *,
    strict: bool = False,
) -> Validator:
    try:
        if isinstance(schema, Path):
            schema = str(schema)
        if isinstance(schema, dict):
            schema = SchemaDefinition(**schema)
        elif isinstance(schema, str):
            schema = yaml_loader.load(schema, target_class=SchemaDefinition)

        if not isinstance(schema, SchemaDefinition):
            raise ValueError(f"Schema could not be loaded from {schema}")
    except ValueError as e:
        raise ValueError(f"Invalid schema: {schema}") from e

    validation_plugins = [JsonschemaValidationPlugin(closed=True, strict=strict)]

    return Validator(schema, validation_plugins=validation_plugins)


def validate(
    instance: Any,
    schema: Union[str, dict, SchemaDefinition],
    target_class: Optional[str] = None,
    *,
    strict: bool = False,
) -> ValidationReport:
    """Validate a data instance against a schema

    This function provides a simple interface to basic validation performed
    by a JSON Schema validator. To have more control over the type of
    validation performed, see the `Validator` class.

    :param instance: The instance to validate
    :param schema: The schema used to validate the instance. If a string is
        it will be interpreted as a path, URL, or other loadable location.
        If it is a dict it should be compatible with `SchemaDefinition`,
        otherwise it should be a `SchemaDefinition` instance.
    :param target_class: Name of the class within the schema to validate
        against. If None, the class will be inferred from the schema by
        looked for a class with `tree_root: true`. Defaults to None.
    :param strict: If True, validation will stop after the first validation
        error is found, Otherwise all validation problems will be reported.
        Defaults to False.
    :raises ValueError: If a valid `SchemaDefinition` cannot be constructed
        from the `schema` parameter.
    :return: A validation report
    :rtype: ValidationReport
    """
    validator = _get_default_validator(schema, strict=strict)
    return validator.validate(instance, target_class)


def validate_file(
    file: Union[str, bytes, os.PathLike],
    schema: Union[str, dict, SchemaDefinition],
    target_class: Optional[str] = None,
    *,
    strict: bool = False,
) -> ValidationReport:
    loader = default_loader_for_file(file)
    validator = _get_default_validator(schema, strict=strict)
    return validator.validate_source(loader, target_class)


__all__ = ["Validator", "validate", "validate_file"]
