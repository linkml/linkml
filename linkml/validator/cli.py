import importlib
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import click
import yaml
from pydantic import BaseModel, Field

from linkml._version import __version__
from linkml.validator import Validator
from linkml.validator.loaders import Loader, default_loader_for_file
from linkml.validator.plugins import ValidationPlugin
from linkml.validator.report import Severity


class Config(BaseModel):
    schema_path: Union[str, Path] = Field(alias="schema")
    target_class: Optional[str] = None
    data_sources: Iterable[Union[str, Dict[str, Dict[str, str]]]] = []
    plugins: Optional[Dict[str, Optional[Dict[str, Any]]]] = {
        "JsonschemaValidationPlugin": {"closed": True}
    }


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


def _resolve_loaders(
    loader_config: Iterable[Union[str, Dict[str, Dict[str, str]]]]
) -> List[Loader]:
    loaders = []
    for entry in loader_config:
        if isinstance(entry, str):
            loader = default_loader_for_file(entry)
        elif isinstance(entry, dict):
            if len(entry) > 1:
                raise click.ClickException(
                    f"Invalid config. Dictionary entries should only have one key: {entry}"
                )
            class_name = next(iter(entry.keys()))
            loader = _resolve_class(class_name, "linkml.validator.loaders", **entry[class_name])
        else:
            raise click.ClickException(
                "Invalid config. Data sources must be specified as a string or as dictionary."
            )
        loaders.append(loader)
    return loaders


@click.command()
@click.option(
    "-S",
    "--schema",
    help="Schema file to validate data against",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True, path_type=Path),
)
@click.option(
    "-T",
    "--target-class",
    help="Class within the schema to validate data against",
)
@click.option(
    "-C",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="Validation configuration YAML file.",
)
@click.argument("data_sources", nargs=-1, type=click.Path(exists=True))
@click.version_option(__version__, "-V", "--version")
def cli(
    schema: Optional[Path],
    target_class: Optional[str],
    config: Optional[str],
    data_sources: Tuple[str],
):
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
            "the -S/--schema option or in a config file."
        )
    config = Config(**config_args)

    plugins = _resolve_plugins(config.plugins) if config.plugins else []
    loaders = _resolve_loaders(config.data_sources)
    validator = Validator(config.schema_path, validation_plugins=plugins)
    severity_counter = Counter()
    for loader in loaders:
        for result in validator.iter_results_from_source(loader, config.target_class):
            severity_counter[result.severity] += 1
            click.echo(
                f"[{result.severity.value}] {result.message} of {loader.source}#{result.instance_index}"
            )

    if sum(severity_counter.values()) == 0:
        click.echo("No issues found!")

    exit_code = 1 if severity_counter[Severity.ERROR] > 0 else 0
    sys.exit(exit_code)


if __name__ == "__main__":
    cli()
