"""Command line interface for LinkML.
"""

import os
import logging
import shutil
import subprocess
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

VERSION_STR = str
TEMPLATE_SUFFIX = ".jinja"
ABOUT_FILE = 'about.yaml'
SKIP_FILES = ["poetry.lock"]
PROJECT_TEMPLATE_API_URL = 'https://api.github.com/repos/linkml/linkml-project-template/releases/latest'


def download_template_directory(tmpdir: tempfile.TemporaryDirectory) -> VERSION_STR:
    r = requests.get(PROJECT_TEMPLATE_API_URL)
    if r.status_code == 200:
        url = r.json()['tarball_url']
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            logging.info(f'uncompressing {url}')
            file = tarfile.open(fileobj=r.raw, mode="r|gz")
            file.extractall(path=tmpdir.name)
        logging.info(f'TMP: {tmpdir.name}')
        return str(url).split('/')[-1]
    else:
        raise FileNotFoundError(f'{PROJECT_TEMPLATE_API_URL} responded with {r.code} // {r.text}')



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

    Assumes you are in the project directory

    :param new_name:
    :return:
    """
    logging.info(f'Renaming to {new_name}')
    cwd = os.getcwd()
    logging.info(f'Current dir: {cwd}')
    project = get_project_info()
    project.name = new_name
    new_filename = underscore(new_name)
    new_source_schema_path = Path(project.source_schema_path).parent / f'{new_filename}.yaml'
    logging.info(f'Moving from {project.source_schema_path} ==> {new_source_schema_path}')
    shutil.move(project.source_schema_path, new_source_schema_path)
    project.source_schema_path = str(new_source_schema_path)
    save_project_info(project,)

def _get_default_author_name():
    """Use git config to make an educated guess for the default author string"""
    try:
        user_name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
        user_email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
        return f"{user_name.stdout.strip()} <{user_email.stdout.strip()}>"
    except subprocess.CalledProcessError:
        return ""

def _validate_author(ctx, param, value):
    match = re.fullmatch("[^<]+ <[^@]+@[^>]+>", value)
    if match == None:
        raise click.BadParameter("format must be \"name <email>\"")
    return value

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


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """Run the linkML CLI."""
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
              help="Path to a template directory. If empty, then the default linkml-project-template will be used")
@click.option("-d", "--directory",
              help="Path to a target directory")
@click.option("-U", "--organization",
              default='my_org',
              show_default=True,
              help="Name of github organization")
@click.option("-V", "--template-version",
              help="Version of template.")
@click.option("-D", "--description",
              default="my awesome datamodel is for awesome things",
              show_default=True,
              help="Description of project")
@click.option('--force/--no-force',
              default=False,
              show_default=True,
              help="overwrite project dir if exists already")
@click.option("-A", "--author",
              default=_get_default_author_name(),
              show_default="determined by git config",
              help="Author of the schema in the form \"name <email>\"",
              callback=_validate_author)
@click.argument("name")
def new(
        name,
        description,
        organization,
        directory,
        template_directory,
        template_version,
        force: bool,
        author: str,
):
    """
    Create a new project

    This will use:
    https://github.com/linkml/linkml-project-template

    Example:

        linkml-ws new my-awesome-project
    """
    if '/' in name:
        raise ValueError(f'Name cannot contain slashes')
    template_version = None
    tmpdir = tempfile.TemporaryDirectory()
    if template_directory is None:
        template_version = download_template_directory(tmpdir)
        entries = list(os.listdir(tmpdir.name))
        print(entries)
        if len(entries) == 1:
            template_directory = str(Path(tmpdir.name) / entries[0])
        else:
            raise ValueError(f'Expected a single subfolder: {entries} in {tmpdir}')
    else:
        template_version = 'snapshot'
    project_dir = project_name_as_directory(name)
    if directory is not None:
        project_dir = str(Path(directory) / project_dir)
    if Path(project_dir).exists() and not force:
        logging.info(f'Project dir {project_dir} exists')
        raise PermissionError(f'Will not override existing folder: {project_dir}')
    output_directory = project_dir
    logging.info(f'Walking: {template_directory}')
    params = dict(name=name,
                  dash_name=project_name_as_directory(name),
                  organization=organization,
                  namespace=underscore(organization),
                  underscore_name=project_name_as_underscore(name),
                  description=description,
                  template_version=template_version,
                  author=author)
    for root, dirs, files in os.walk(template_directory, topdown=True):
        logging.info(f'Dirs: {dirs} {files}')
        dirs[:] = [d for d in dirs if d not in ['.git', 'project']]
        logging.info(f'R={root}')
        target_directory = root.replace(template_directory, output_directory)
        os.makedirs(target_directory, exist_ok=True)
        for f in files:
            source_path = os.path.join(root, f)
            target_path = os.path.join(target_directory, f)
            if f in SKIP_FILES:
                logging.info(f'Skipping {source_path}')
                continue
            if Path(source_path + TEMPLATE_SUFFIX).exists():
                logging.info(f'Skipping {source_path}, will be written from {TEMPLATE_SUFFIX}')
                continue
            if target_path.endswith(TEMPLATE_SUFFIX):
                with open(source_path) as stream:
                    template = Template(stream.read())
                    target_path = target_path.replace(TEMPLATE_SUFFIX, "")
                    logging.info('  Applying j2: {} -> {}'.format(source_path, target_path))
                    with open(target_path, "w", encoding="utf-8") as out:
                        out.write(template.render(**params))
                pass
            else:
                logging.info('  Copying: {} -> {}'.format(source_path, target_path))
                copyfile(source_path, target_path)
    with cd(project_dir):
        _rename_project(name)
    print(f'** NEW PROJECT CREATED **')
    print(f'Next steps:\n')
    print(f'cd {project_dir}')
    print(f'make setup')

@main.command()
@click.argument("name")
def rename(
        name
):
    """
    Rename a project
    """
    _rename_project(name)


if __name__ == "__main__":
    main()
