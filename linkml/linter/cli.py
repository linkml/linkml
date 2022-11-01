import os
import sys
from pathlib import Path
from typing import Iterable

import click
import yaml

from linkml._version import __version__

from .config.datamodel.config import RuleLevel
from .formatters import (JsonFormatter, MarkdownFormatter, TerminalFormatter,
                         TsvFormatter)
from .linter import Linter

YAML_SUFFIXES = [".yml", ".yaml"]
DEFAULT_CONFIG_FILES = [".linkmllint.yaml", ".linkmllint.yml"]


def get_yaml_files(root: Path) -> Iterable[str]:
    if root.is_file():
        if root.suffix not in YAML_SUFFIXES:
            raise click.UsageError("SCHEMA must be a YAML file")
        yield str(root)
    else:
        for dir, _, files in os.walk(root):
            for file in files:
                if file in DEFAULT_CONFIG_FILES:
                    continue
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
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="Custom linter configuration file.",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["terminal", "markdown", "json", "tsv"]),
    default="terminal",
    help="Report format.",
    show_default=True,
)
@click.option("-v", "--verbose", is_flag=True)
@click.option(
    "-o", "--output", type=click.File("w"), default="-", help="Report file name."
)
@click.option(
    "--ignore-warnings",
    is_flag=True,
    default=False,
    help="Do not exit with an error status if only warnings are found.",
)
@click.option(
    "--max-warnings",
    type=int,
    default=0,
    show_default=True,
    help="Do not exit with an error status if up to this number of warnings (and no errors) are found.",
)
@click.option("--fix/--no-fix", default=False)
@click.version_option(__version__, "-V", "--version")
def main(
    schema: Path,
    fix: bool,
    config: str,
    format: str,
    output,
    ignore_warnings: bool,
    max_warnings: int,
    verbose: bool
):
    """Run linter on SCHEMA.

    SCHEMA can be a single LinkML YAML file or a directory. If it is a directory
    every YAML file found in the directory (recursively) will be linted."""
    config_file = None
    if config:
        config_file = config
    else:
        for default_config in DEFAULT_CONFIG_FILES:
            path = Path(os.getcwd()) / default_config
            if path.exists():
                config_file = path
                break

    if config_file:
        with open(config_file) as f:
            config_dict = yaml.safe_load(f)
    else:
        config_dict = {"extends": "recommended"}

    linter = Linter(config_dict)
    if format == "terminal":
        formatter = TerminalFormatter(output, verbose)
    elif format == "markdown":
        formatter = MarkdownFormatter(output)
    elif format == "json":
        formatter = JsonFormatter(output)
    elif format == "tsv":
        formatter = TsvFormatter(output)

    error_count = 0
    warning_count = 0
    formatter.start_report()
    for path in get_yaml_files(schema):
        formatter.start_schema(path)
        report = linter.lint(path, fix=fix)
        for problem in report:
            if str(problem.level) is RuleLevel.error.text:
                error_count += 1
            elif str(problem.level) is RuleLevel.warning.text:
                warning_count += 1
            formatter.handle_problem(problem)
        formatter.end_schema()
    formatter.end_report()

    exit_code = 0
    if error_count > 0:
        exit_code = 2
    elif not ignore_warnings and warning_count > max_warnings:
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
