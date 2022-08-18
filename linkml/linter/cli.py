import os
from pathlib import Path
from typing import Iterable

import click
import yaml

from .formatters import (JsonFormatter, MarkdownFormatter, TerminalFormatter,
                         TsvFormatter)
from .linter import Linter

YAML_SUFFIXES = [".yml", ".yaml"]
DOT_FILE_CONFIG = Path(os.getcwd()) / ".linkmllint.yaml"


def get_yaml_files(root: Path) -> Iterable[str]:
    if root.is_file():
        if root.suffix not in YAML_SUFFIXES:
            raise click.UsageError("SCHEMA must be a YAML file")
        yield str(root)
    else:
        for dir, _, files in os.walk(root):
            for file in files:
                path = Path(dir, file)
                if path.suffix in YAML_SUFFIXES:
                    yield str(path)


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
@click.option(
    "-f",
    "--format",
    type=click.Choice(["terminal", "markdown", "json", "tsv"]),
    default="terminal",
)
@click.option("-o", "--output", type=click.File("w"), default="-")
@click.option("--fix/--no-fix", default=False)
def main(schema: Path, fix: bool, config: str, format: str, output):
    if config:
        with open(config) as config_file:
            config_dict = yaml.safe_load(config_file)
    elif DOT_FILE_CONFIG.exists():
        with open(DOT_FILE_CONFIG) as config_file:
            config_dict = yaml.safe_load(config_file)
    else:
        config_dict = {}

    linter = Linter(config_dict)
    if format == "terminal":
        formatter = TerminalFormatter(output)
    elif format == "markdown":
        formatter = MarkdownFormatter(output)
    elif format == "json":
        formatter = JsonFormatter(output)
    elif format == "tsv":
        formatter = TsvFormatter(output)

    formatter.start_report()
    for path in get_yaml_files(schema):
        formatter.start_schema(path)
        report = linter.lint(path, fix=fix)
        for problem in report:
            formatter.handle_problem(problem)
        formatter.end_schema()
    formatter.end_report()


if __name__ == "__main__":
    main()
