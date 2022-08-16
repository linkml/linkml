from pathlib import Path

import click
from linkml_runtime.loaders.yaml_loader import YAMLLoader

from .config.datamodel.config import Config, RuleLevel
from .linter import Linter

YAML_SUFFIXES = [".yml", ".yaml"]


@click.command()
@click.argument(
    "schema",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=True, resolve_path=True, path_type=Path
    ),
)
@click.option("--fix/--no-fix", default=False)
def main(schema: Path, fix: bool):
    config_path = str(Path(__file__).parent / "config/default.yaml")
    loader = YAMLLoader()
    config = loader.load(config_path, target_class=Config)

    if schema.is_dir():
        raise NotImplementedError("Directory input not implemented yet")
    else:
        if schema.suffix not in YAML_SUFFIXES:
            raise click.UsageError("SCHEMA must be a YAML file")

        linter = Linter(config)
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
