import importlib
import sys
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import click
import yaml
from pydantic import BaseModel, Field

from linkml._version import __version__
from linkml.validator import Validator
from linkml.validator.loaders import Loader, default_loader_for_file
from linkml.validator.plugins import ValidationPlugin
from linkml.validator.report import Severity


class Config(BaseModel):
    schema_path: str | Path | None = Field(alias="schema", default=None)
    target_class: str | None = None
    data_sources: Iterable[str | dict[str, dict[str, str]]] = []
    plugins: dict[str, dict[str, Any] | None] | None = {"JsonschemaValidationPlugin": {"closed": True}}


def _resolve_class(full_class_name: str, default_package: str, **kwargs):
    if "." in full_class_name:
        module_name, class_name = full_class_name.rsplit(".", maxsplit=1)
    else:
        module_name = default_package
        class_name = full_class_name
    try:
        module = importlib.import_module(module_name)
        class_inst = getattr(module, class_name)
    except (ModuleNotFoundError, AttributeError):
        raise click.ClickException(f"Unknown class: {full_class_name}")
    return class_inst(**kwargs)


def _resolve_plugins(plugin_config: dict[str, dict[str, Any]]) -> list[ValidationPlugin]:
    plugins = []
    for key, value in plugin_config.items():
        plugin = _resolve_class(key, "linkml.validator.plugins", **value if value else {})
        plugins.append(plugin)
    return plugins


def _resolve_loaders(
    loader_config: Iterable[str | dict[str, dict[str, str]]],
    *,
    schema_path: str | Path | None = None,
    target_class: str | None = None,
) -> list[Loader]:
    loaders = []
    for entry in loader_config:
        if isinstance(entry, str):
            loader = default_loader_for_file(entry, schema_path=schema_path, target_class=target_class)
        elif isinstance(entry, dict):
            if len(entry) > 1:
                raise click.ClickException(f"Invalid config. Dictionary entries should only have one key: {entry}")
            class_name = next(iter(entry.keys()))
            loader = _resolve_class(class_name, "linkml.validator.loaders", **entry[class_name])
        else:
            raise click.ClickException("Invalid config. Data sources must be specified as a string or as dictionary.")
        loaders.append(loader)
    return loaders


def _validate_schema_against_metamodel(schema_paths: tuple[str]) -> int:
    """Validate one or more schema files against the LinkML metamodel.

    :return: number of errors found
    """
    from linkml.linter.linter import Linter

    error_count = 0
    for schema_path in schema_paths:
        for problem in Linter.validate_schema(schema_path):
            error_count += 1
            click.echo(f"[ERROR] [{schema_path}] {problem.message}")
    return error_count


def _normalize_and_validate(
    data_path: str,
    schema_path: str | Path,
    target_class: str | None,
    plugins: list[ValidationPlugin],
    exit_on_first_failure: bool,
    include_context: bool,
) -> Counter:
    """Run ReferenceValidator to normalize data, then validate the result.

    :return: severity counter from JSON Schema validation of normalized output
    """
    from linkml_runtime import SchemaView
    from linkml_runtime.processing.referencevalidator import ReferenceValidator, Report

    sv = SchemaView(str(schema_path))
    normalizer = ReferenceValidator(sv)

    with open(data_path) as f:
        input_object = yaml.safe_load(f)

    report = Report()
    output_object = normalizer.normalize(input_object, target=target_class, report=report)

    # Report normalization actions
    for r in report.normalized_results():
        click.echo(f"[FIXED] {r.type}: {r.instantiates} ({r.info or ''})")

    for r in report.warnings():
        click.echo(f"[WARNING] {r.type}: {r.instantiates}")

    for r in report.errors():
        click.echo(f"[ERROR] {r.type}: {r.instantiates}")

    # Write normalized output
    output_str = yaml.dump(output_object, sort_keys=False)
    click.echo(output_str)

    # Now validate the normalized output with the standard JSON Schema path
    severity_counter = Counter()
    if plugins:
        from linkml.validator.validation_context import ValidationContext
        from linkml_runtime.linkml_model import SchemaDefinition
        from linkml_runtime.loaders import yaml_loader

        schema_def = yaml_loader.load(str(schema_path), SchemaDefinition)
        context = ValidationContext(schema_def, target_class)
        for plugin in plugins:
            plugin.pre_process(context)
            for result in plugin.process(output_object, context):
                severity_counter[result.severity] += 1
                click.echo(f"[{result.severity.value}] {result.message}")
                if include_context:
                    for ctx in result.context:
                        click.echo(f"[CONTEXT] {ctx}")
            plugin.post_process(context)

    return severity_counter


@click.command(name="validate")
@click.option(
    "-s",
    "--schema",
    help="Schema file to validate data against. When omitted, positional arguments "
    "are treated as schemas and validated against the LinkML metamodel.",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True, path_type=Path),
)
@click.option(
    "-C",
    "--target-class",
    help="Class within the schema to validate data against",
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="Validation configuration YAML file.",
)
@click.option(
    "--exit-on-first-failure",
    is_flag=True,
    default=False,
    help="Exit after the first validation failure is found. If not specified all validation failures are reported.",
)
@click.option(
    "--include-context/--no-include-context",
    "-D",
    default=False,
    show_default=True,
    help="Include additional context when reporting of validation errors.",
)
@click.option(
    "--allow-null-for-optional-enums",
    is_flag=True,
    default=False,
    help="Downgrade enum validation errors to warnings when the value is "
    "null/empty and the slot is not required. Prevents 'None is not "
    "one of [...]' and \"'' is not one of [...]\" errors for optional "
    "enum slots.",
)
@click.option(
    "--fix",
    is_flag=True,
    default=False,
    help="Attempt to normalize data to conform to the schema (type coercion, "
    "collection form restructuring) and output the corrected data. "
    "The normalized output is then validated to report any remaining issues.",
)
@click.argument("data_sources", nargs=-1, type=click.Path(exists=True))
@click.version_option(__version__, "-V", "--version")
def cli(
    schema: Path | None,
    target_class: str | None,
    config: str | None,
    data_sources: tuple[str],
    exit_on_first_failure: bool,
    include_context: bool,
    allow_null_for_optional_enums: bool,
    fix: bool,
):
    """Validate data against a LinkML schema, or validate a schema against the metamodel.

    When -s/--schema is provided, positional arguments are data files to validate
    against that schema.

    When -s/--schema is omitted, positional arguments are treated as schema files
    and validated against the LinkML metamodel.
    """
    # Schema-against-metamodel mode: no -s flag
    if schema is None and not config:
        if not data_sources:
            raise click.ClickException("No files specified.")
        error_count = _validate_schema_against_metamodel(data_sources)
        if error_count == 0:
            click.echo("No issues found")
        sys.exit(1 if error_count > 0 else 0)

    # Data validation mode: -s flag or config provided
    config_args = {
        "schema": schema,
        "target_class": target_class,
        "data_sources": data_sources,
    }
    if config:
        with open(config) as config_file:
            config_raw = yaml.safe_load(config_file)
            config_args.update(config_raw)

    if config_args.get("schema") is None:
        raise click.ClickException(
            "No schema specified. Path to schema must be specified by either "
            "the -s/--schema option or in a config file."
        )
    cfg = Config(**config_args)

    # Pass allow_null_for_optional_enums through to JsonschemaValidationPlugin
    if allow_null_for_optional_enums and cfg.plugins and "JsonschemaValidationPlugin" in cfg.plugins:
        if cfg.plugins["JsonschemaValidationPlugin"] is None:
            cfg.plugins["JsonschemaValidationPlugin"] = {}
        cfg.plugins["JsonschemaValidationPlugin"]["allow_null_for_optional_enums"] = True

    if not data_sources and not list(cfg.data_sources):
        raise click.ClickException("No data files specified. Provide data files as positional arguments.")

    plugins = _resolve_plugins(cfg.plugins) if cfg.plugins else []
    severity_counter = Counter()

    if fix:
        for data_path in data_sources:
            severity_counter += _normalize_and_validate(
                data_path, cfg.schema_path, cfg.target_class, plugins, exit_on_first_failure, include_context
            )
    else:
        loaders = _resolve_loaders(cfg.data_sources, schema_path=cfg.schema_path, target_class=cfg.target_class)
        validator = Validator(cfg.schema_path, validation_plugins=plugins, strict=exit_on_first_failure)

        for loader in loaders:
            for result in validator.iter_results_from_source(loader, cfg.target_class):
                severity_counter[result.severity] += 1
                click.echo(f"[{result.severity.value}] [{loader.source}/{result.instance_index}] {result.message}")
                if include_context:
                    for ctx in result.context:
                        click.echo(f"[CONTEXT] {ctx}")

    if sum(severity_counter.values()) == 0:
        click.echo("No issues found")

    exit_code = 1 if severity_counter[Severity.ERROR] > 0 else 0
    sys.exit(exit_code)


if __name__ == "__main__":
    cli()
