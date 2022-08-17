import os
from pathlib import Path

import click
import yaml

from .config.datamodel.config import RuleLevel
from .linter import Linter

YAML_SUFFIXES = [".yml", ".yaml"]
DOT_FILE_CONFIG = Path(os.getcwd()) / ".linkmllint.yaml"


@click.command()
@click.argument(
    "schema",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=True, resolve_path=True, path_type=Path
    ),
)
@click.option(
    "-c", "--config", type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
@click.option("--fix/--no-fix", default=False)
def main(schema: Path, fix: bool, config: str):
    if config:
        with open(config) as config_file:
            config_dict = yaml.safe_load(config_file)
    elif DOT_FILE_CONFIG.exists():
        with open(DOT_FILE_CONFIG) as config_file:
            config_dict = yaml.safe_load(config_file)
    else:
        config_dict = {}

    if schema.is_dir():
        raise NotImplementedError("Directory input not implemented yet")
    else:
        if schema.suffix not in YAML_SUFFIXES:
            raise click.UsageError("SCHEMA must be a YAML file")

        linter = Linter(config_dict)
        report = linter.lint(str(schema), fix=fix)
        for problem in report:
            formatted = (
                click.style(
                    str(problem.level).ljust(9),
                    fg="yellow"
                    if str(problem.level) is RuleLevel.warning.text
                    else "red",
                )
                + problem.message
                + "  "
                + click.style(f"({problem.rule_name})", dim=True)
            )
            click.echo(formatted)


if __name__ == "__main__":
    main()
