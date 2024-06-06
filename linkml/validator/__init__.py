"""
The ``linkml.validator`` package contains a new LinkML validation framework that is more flexible
than the ``linkml.validators`` package. While that package still exists, it may become deprecated
in the future.
"""

import os
from pathlib import Path
from typing import Any, Optional, Union

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.validator.loaders import default_loader_for_file
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

    validation_plugins = [JsonschemaValidationPlugin(closed=True)]

    return Validator(schema, validation_plugins=validation_plugins, strict=strict)


def validate(
    instance: Any,
    schema: Union[str, dict, SchemaDefinition],
    target_class: Optional[str] = None,
    *,
    strict: bool = False,
) -> ValidationReport:
    """Validate a data instance against a schema

    This function provides a simple interface to do basic validation performed by a JSON Schema
    validator on a single instance. To have more control over the type of validation performed,
    see the :class:`Validator` class.

    :param instance: The instance to validate
    :param schema: The schema used to validate the instance. If a string is
        it will be interpreted as a path, URL, or other loadable location.
        If it is a dict it should be compatible with ``SchemaDefinition``,
        otherwise it should be a ``SchemaDefinition`` instance.
    :param target_class: Name of the class within the schema to validate
        against. If ``None``, the class will be inferred from the schema by
        looked for a class with ``tree_root: true``. Defaults to ``None``.
    :param strict: If ``True``, validation will stop after the first validation
        error is found, Otherwise all validation problems will be reported.
        Defaults to ``False``.
    :raises ValueError: If a valid ``SchemaDefinition`` cannot be constructed
        from the ``schema`` parameter.
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
    """Validate instances loaded from a file against a schema

    This function provides a simple interface to do basic validation performed by a JSON Schema
    validator on instances loaded from a file. Loading is done according to the file's extension.
    Accepted file extensions are: ``.csv``, ``.tsv``, ``.yaml``, ``.yml``, and ``.json``.
    Individual rows of CSV and TSV files are treated as instances to validate. Each document
    within a YAML file is treated as an individual instance to validate. If the top-level of a
    JSON file is an array, each element of the array is treated as an instance to validate.
    Otherwise, if the top-level is an object it is treated as a single instance to validate.

    To have more control over the type of validation performed, see the :class:`Validator` class.

    :param file: Path-like object of the file to be read
    :param schema: The schema used to validate the instance. If a string is
        it will be interpreted as a path, URL, or other loadable location.
        If it is a dict it should be compatible with ``SchemaDefinition``,
        otherwise it should be a ``SchemaDefinition`` instance.
    :param target_class: Name of the class within the schema to validate
        against. If ``None``, the class will be inferred from the schema by
        looked for a class with ``tree_root: true``. Defaults to ``None``.
    :param strict: If ``True``, validation will stop after the first validation
        error is found, Otherwise all validation problems will be reported.
        Defaults to ``False``.
    :return: A validation report
    :rtype: ValidationReport
    """
    loader = default_loader_for_file(file)
    validator = _get_default_validator(schema, strict=strict)
    return validator.validate_source(loader, target_class)


__all__ = ["Validator", "validate", "validate_file"]
