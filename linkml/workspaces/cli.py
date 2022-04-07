"""Command line interface for LinkML.
"""

import os
import logging
import shutil
import sys
import tarfile
import tempfile
from contextlib import contextmanager
from pathlib import Path
from shutil import copyfile
import re

import click
from jinja2 import Template
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.formatutils import underscore

from linkml.workspaces.datamodel.workspaces import Project, Workspace
import yaml
import requests

TEMPLATE_SUFFIX = ".jinja"
ABOUT_FILE = 'about.yaml'

def download_template_directory(tmpdir: tempfile.TemporaryDirectory):
    r = requests.get('https://api.github.com/repos/linkml/linkml-project-template/releases/latest')
    if r.status_code == 200:
        url = r.json()['tarball_url']
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            logging.info(f'uncompressing {url}')
            file = tarfile.open(fileobj=r.raw, mode="r|gz")
            file.extractall(path=tmpdir.name)
    logging.info(f'TMP: {tmpdir.name}')



@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def project_name_as_directory(name: str) -> str:
    toks = name.split()
    return '-'.join(toks)

def project_name_as_underscore(name: str) -> str:
    return underscore(name)

def get_project_info(directory='.') -> Project:
    return yaml_loader.load(str(Path(directory) / ABOUT_FILE) , target_class=Project)

def save_project_info(project: Project, directory='.') -> None:
    yaml_dumper.dump(project, str(Path(directory) / ABOUT_FILE ))

def _rename_project(new_name: str):
    """
    Renames a project:

    - moves source yaml file
    - updates about.yaml

    :param new_name:
    :return:
    """
    new_dir = project_name_as_directory(new_name)
    project = get_project_info()
    project.name = new_name
    path_toks = project.source_schema_path.split('/')
    old_filename = path_toks.pop()
    new_filename = underscore(new_name)
    new_source_schema_path = Path('/'.join(path_toks)) / new_filename
    new_source_schema_path = f'{new_source_schema_path}.yaml'
    shutil.move(project.source_schema_path, new_source_schema_path)
    project.source_schema_path = str(new_source_schema_path)
    save_project_info(project,)


# Click input options common across commands
input_argument = click.argument("input", required=True, type=click.Path())

input_format_option = click.option(
    "-I",
    "--input-format",
    help=f'The string denoting the input format',
)
output_option = click.option(
    "-o",
    "--output",
    help="Output file.",
    type=click.File(mode="w"),
    default=sys.stdout,
)
output_format_option = click.option(
    "-O",
    "--output-format",
    help=f'Desired output format,',
)
output_directory_option = click.option(
    "-d",
    "--output-directory",
    type=click.Path(),
    help="Output directory path.",
)
metadata_option = click.option(
    "-m",
    "--metadata",
    required=False,
    type=click.Path(),
    help="The path to a file containing the sssom metadata (including prefix_map) to be used.",
)
transpose_option = click.option("-t", "--transpose/--no-transpose", default=False)
fields_option = click.option(
    "-F",
    "--fields",
    nargs=2,
    default=("subject_category", "object_category"),
    help="Fields.",
)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """Run the SSSOM CLI."""
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    if quiet:
        logging.basicConfig(level=logging.ERROR)




@main.command()
@click.option("-T", "--template-directory",
              help="Path to a template directory.")
@click.option("-V", "--template-version",
              help="Version of template.")
@click.option('--force/--no-force',
              default=False,
              show_default=True,
              help="overwrite project dir if exists already")
@click.argument("name")
def new(
        name,
        template_directory,
        template_version,
        force: bool
):
    """
    Create a new project
    """
    tmpdir = tempfile.TemporaryDirectory()
    if template_directory is None:
        download_template_directory(tmpdir)
        entries = list(os.listdir(tmpdir.name))
        print(entries)
        if len(entries) == 1:
            template_directory = str(Path(tmpdir.name) / entries[0])
        else:
            raise ValueError(f'Expected one subfolder: {entries} in {tmpdir}')
    project_dir = project_name_as_directory(name)
    if Path(project_dir).exists() and not force:
        logging.info(f'Project dir {project_dir} exists')
        raise PermissionError(f'Will not overrid {project_dir}')
    output_directory = project_dir
    logging.info(f'Walking: {template_directory}')
    for root, dirs, files in os.walk(template_directory, topdown=True):
        logging.info(f'Dirs: {dirs} {files}')
        dirs[:] = [d for d in dirs if d not in ['.git', 'project']]
        logging.info(f'R={root}')
        target_directory = root.replace(template_directory, output_directory)
        os.makedirs(target_directory, exist_ok=True)
        for f in files:
            source_path = os.path.join(root, f)
            target_path = os.path.join(target_directory, f)
            if Path(source_path + TEMPLATE_SUFFIX).exists():
                logging.info(f'Skipping {source_path}, will be written from {TEMPLATE_SUFFIX}')
                continue
            if target_path.endswith(TEMPLATE_SUFFIX):
                with open(source_path) as stream:
                    template = Template(stream.read())
                    target_path = target_path.replace(TEMPLATE_SUFFIX, "")
                    logging.info('  Applying j2: {} -> {}'.format(source_path, target_path))
                    with open(target_path, "w", encoding="utf-8") as out:
                        out.write(template.render(name=name))
                pass
            else:
                logging.info('  Copying: {} -> {}'.format(source_path, target_path))
                copyfile(source_path, target_path)
    with cd(project_dir):
        _rename_project(name)

@main.command()
@click.argument("name")
def rename(
        name
):
    _rename_project(name)


if __name__ == "__main__":
    main()
