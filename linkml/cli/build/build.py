"""
CLI command for building based on a project-level configuration

Borrowing some code from pytest for config file locating
"""

from pathlib import Path
from typing import Optional
import tomllib

import click

from linkml.cli.build.models import LinkmlConfig

@click.command(name = "build")
@click.option("-C", help="Execute build for a project in a specific directory "
                             "(or for a specific pyproject.toml config)",
              type=click.Path(exists=True, dir_okay=True),
              required=False)
def build(C: Optional[Path] = None):
    config_file = find_config(C)
    linkml_config = load_config(config_file)



def find_config(base_path: Optional[Path] = None) -> Optional[Path]:
    if base_path is None:
        base_path = Path.cwd()

    if base_path.is_file() and base_path.name == 'pyproject.toml':
        return base_path

    for check_path in (base_path, *base_path.parents):
        if (pyproject_file := check_path / "pyproject.toml") is not None:
            return pyproject_file

def load_config(pyproject_path: Path) -> LinkmlConfig:
    with open(pyproject_path, 'rb') as tfile:
        pyproject = tomllib.load(tfile)

    tool = pyproject.get('tool', {})
    if 'linkml' not in tool:
        raise RuntimeError(f'No [tool.linkml] table found in {pyproject_path}')

    config = LinkmlConfig(**tool['linkml'])
    return config

