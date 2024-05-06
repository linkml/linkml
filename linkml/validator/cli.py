import importlib
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import click
import yaml
from pydantic import BaseModel, Field

from linkml._version import __version__
from linkml.utils import datautils
from linkml.validator import Validator
from linkml.validator.loaders import Loader, default_loader_for_file
from linkml.validator.plugins import ValidationPlugin
from linkml.validator.report import Severity


class Config(BaseModel):
    schema_path: Union[str, Path] = Field(alias="schema")
    target_class: Optional[str] = None
    data_sources: Iterable[Union[str, Dict[str, Dict[str, str]]]] = []
    plugins: Optional[Dict[str, Optional[Dict[str, Any]]]] = {"JsonschemaValidationPlugin": {"closed": True}}


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


def _resolve_plugins(plugin_config: Dict[str, Dict[str, Any]]) -> List[ValidationPlugin]:
    plugins = []
    for key, value in plugin_config.items():
        plugin = _resolve_class(key, "linkml.validator.plugins", **value if value else {})
        plugins.append(plugin)
    return plugins


def _resolve_loaders(loader_config: Iterable[Union[str, Dict[str, Dict[str, str]]]]) -> List[Loader]:
    loaders = []
    for entry in loader_config:
        if isinstance(entry, str):
            loader = default_loader_for_file(entry)
        elif isinstance(entry, dict):
            if len(entry) > 1:
                raise click.ClickException(f"Invalid config. Dictionary entries should only have one key: {entry}")
            class_name = next(iter(entry.keys()))
            loader = _resolve_class(class_name, "linkml.validator.loaders", **entry[class_name])
        else:
            raise click.ClickException("Invalid config. Data sources must be specified as a string or as dictionary.")
        loaders.append(loader)
    return loaders


DEPRECATED = "[DEPRECATED: only used in legacy mode]"


@click.command()
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
    "--legacy-mode",
    is_flag=True,
    default=False,
    help="Use legacy linkml-validate behavior.",
)
@click.option("--module", "-m", help=f"{DEPRECATED} Path to python datamodel module")
@click.option(
    "--input-format",
    "-f",
    type=click.Choice(list(datautils.dumpers_loaders.keys())),
    help=f"{DEPRECATED} Input format. Inferred from input suffix if not specified",
)
@click.option("--index-slot", "-S", help=f"{DEPRECATED} top level slot. Required for CSV dumping/loading")
@click.option(
    "--include-range-class-descendants/--no-range-class-descendants",
    default=False,
    show_default=False,
    help=f"{DEPRECATED} When handling range constraints, include all descendants of the range "
    "class instead of just the range class",
)
@click.option(
    "--include-context/--no-include-context",
    "-D",
    default=False,
    show_default=True,
    help="Include additional context when reporting of validation errors.",
)
@click.argument("data_sources", nargs=-1, type=click.Path(exists=True))
@click.version_option(__version__, "-V", "--version")
@click.pass_context
def cli(
    context: click.Context,
    schema: Optional[Path],
    target_class: Optional[str],
    config: Optional[str],
    data_sources: Tuple[str],
    exit_on_first_failure: bool,
    legacy_mode: bool,
    module: Optional[str],
    input_format: Optional[str],
    index_slot: Optional[str],
    include_range_class_descendants: bool,
    include_context: bool,
):
    if legacy_mode:
        from linkml.validators import jsonschemavalidator

        return context.invoke(
            jsonschemavalidator.cli,
            input=data_sources[0] if len(data_sources) > 0 else None,
            module=module,
            target_class=target_class,
            input_format=input_format,
            schema=str(schema) if schema else None,
            index_slot=index_slot,
            exit_on_first_failure=exit_on_first_failure,
            include_range_class_descendants=include_range_class_descendants,
        )

    if module is not None:
        click.secho("Warning: the -m/--module option is deprecated except in legacy mode.", fg="yellow")
    if input_format is not None:
        click.secho(
            "Warning: the -f/--input-format option is deprecated except in legacy mode. By "
            "default source loaders are automatically chosen based on file extension. If a loader "
            "needs to manually specified use the data_sources section of a custom config file.",
            fg="yellow",
        )
    if index_slot is not None:
        click.secho("Warning: the -S/--index-slot option is deprecated except in legacy mode.", fg="yellow")
    if include_range_class_descendants:
        click.secho(
            "Warning: the --include-range-class-descendants deprecated except in legacy mode. "
            "This behavior is now the default of the JsonschemaValidationPlugin. If you need to "
            "disable it use the plugins section of a custom config file.",
            fg="yellow",
        )

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

    plugins = _resolve_plugins(config.plugins) if config.plugins else []
    loaders = _resolve_loaders(config.data_sources)
    validator = Validator(config.schema_path, validation_plugins=plugins, strict=exit_on_first_failure)
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
