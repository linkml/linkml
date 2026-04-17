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
from linkml.utils.mergeutils import merge_includes, resolve_merged_imports
from linkml.validator import Validator
from linkml.validator.loaders import Loader, default_loader_for_file
from linkml.validator.plugins import ValidationPlugin
from linkml.validator.report import Severity
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader


class Config(BaseModel):
    schema_path: str | Path = Field(alias="schema")
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


@click.command(name="validate")
@click.option(
    "-s",
    "--schema",
    help="Schema file to validate data against",
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
    "--include",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True, path_type=Path),
    help="Additional schema files to include. Rules and classification rules "
    "from these schemas are additively merged onto matching classes in the "
    "base schema. May be specified multiple times.",
)
@click.argument("data_sources", nargs=-1, type=click.Path(exists=True))
@click.version_option(__version__, "-V", "--version")
def cli(
    schema: Path | None,
    target_class: str | None,
    config: str | None,
    include: tuple[Path, ...],
    data_sources: tuple[str, ...],
    exit_on_first_failure: bool,
    include_context: bool,
    allow_null_for_optional_enums: bool,
):
    """
    Validate data according to a LinkML Schema
    """
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
    config = Config(**config_args)

    # Pass allow_null_for_optional_enums through to JsonschemaValidationPlugin
    if allow_null_for_optional_enums and config.plugins and "JsonschemaValidationPlugin" in config.plugins:
        if config.plugins["JsonschemaValidationPlugin"] is None:
            config.plugins["JsonschemaValidationPlugin"] = {}
        config.plugins["JsonschemaValidationPlugin"]["allow_null_for_optional_enums"] = True

    plugins = _resolve_plugins(config.plugins) if config.plugins else []
    loaders = _resolve_loaders(config.data_sources, schema_path=config.schema_path, target_class=config.target_class)

    # Load schema and merge any included schemas
    schema_def = yaml_loader.load(str(config.schema_path), SchemaDefinition)
    schema_source = str(config.schema_path)
    if "\n" not in schema_source:
        schema_def.source_file = schema_source
    for include_path in include:
        include_schema = yaml_loader.load(str(include_path), SchemaDefinition)
        try:
            resolve_merged_imports(
                schema_def, include_schema, imported_from=getattr(include_schema, "source_file", None)
            )
            merge_includes(schema_def, include_schema)
        except ValueError as e:
            raise click.ClickException(str(e)) from e

    validator = Validator(schema_def, validation_plugins=plugins, strict=exit_on_first_failure)
    severity_counter = Counter()

    for loader in loaders:
        for result in validator.iter_results_from_source(loader, config.target_class):
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
