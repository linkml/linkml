import io
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Tuple

from json_flattener import flatten_to_csv

from linkml_runtime.linkml_model import Element
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.dumpers import json_dumper, yaml_dumper
import click
import yaml

DEFAULT_DISPLAY_COLS = [
    'name',
    'is_a',
    'description',
    'owner'
]

schema_option = click.option(
    "-s", "--schema", help="Path to schema in LinkML yaml."
)
columns_option = click.option(
    "-c", "--columns",
    default=','.join(DEFAULT_DISPLAY_COLS),
    help="Comma separate list of columns to display."
)

@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """Main

    """
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    if quiet:
        logging.basicConfig(level=logging.ERROR)


@main.command()
@schema_option
@columns_option
@click.option('-t', '--element-type', help='Element type')
def list(schema, columns, element_type):
    """List elements in schema

    Example:
        list -s personinfo.yaml -c name,description -t class

    """
    schema_view = SchemaView(schema)
    logging.info(f'id={schema_view.schema.id}')
    logging.info(f'name={schema_view.schema.name}')
    enames = schema_view.all_element()
    elements = [schema_view.get_element(ename) for ename in enames]
    if element_type is not None:
        elements = [e for e in elements if element_type in type(e).class_name]
    _show_elements(elements, columns=columns)

@main.command()
@schema_option
@columns_option
@click.argument('class_names', nargs=-1)
def islot(schema, columns, class_names):
    """Show induced slots for a list of classes

    Example:
        schemaview islot -s personinfo.yaml Person

    """
    schema_view = SchemaView(schema)
    for cn in class_names:
        logging.info(f'Class: {cn}')
        islots = schema_view.class_induced_slots(cn)
        _show_elements(islots, columns=columns)

@main.command()
@schema_option
@click.option('--is-a/--no-is-a', default=True, help='Include is_a')
@click.option('--mixins/--no-mixins', default=True, help='Include mixins')
@click.argument('class_names', nargs=-1)
def ancs(schema, class_names, is_a, mixins):
    """Show ancestors for classes

    Example:
        schemaview ancs -s personinfo.yaml Person

    """
    schema_view = SchemaView(schema)
    for cn in class_names:
        logging.info(f'Class: {cn}')
        ancs = schema_view.class_ancestors(cn, is_a=is_a, mixins=mixins)
        for a in ancs:
            print(f'{cn}\t{a}')

@main.command()
@schema_option
@click.option('--is-a/--no-is-a', default=True, help='Include is_a')
@click.option('--mixins/--no-mixins', default=True, help='Include mixins')
@click.argument('class_names', nargs=-1)
def descs(schema, class_names, is_a, mixins):
    """Show descendants for classes

    Example:
        schemaview ancs -s personinfo.yaml NamedThing

    """
    schema_view = SchemaView(schema)
    for cn in class_names:
        logging.info(f'Class: {cn}')
        ds = schema_view.class_descendants(cn, is_a=is_a, mixins=mixins)
        for d in ds:
            print(f'{cn}\t{d}')

@main.command()
@schema_option
@click.argument('class_names', nargs=-1)
def delete(schema, class_names):
    """Deletes classes

    """
    schema_view = SchemaView(schema)
    for cn in class_names:
        logging.info(f'Class: {cn}')
        schema_view.delete_class(cn)
    print(yaml_dumper.dumps(schema_view.schema))


def _show_elements(elements: List[Element], columns=None, output = io.StringIO()) -> None:
    elements_j = json.loads(json_dumper.dumps(elements, inject_type=False))
    if columns is not None and columns != '' and columns != [] and columns != '%':
        if isinstance(columns, str):
            columns = columns.split(',')
        def filter_columns(row: dict):
            return {k: row.get(k, None) for k in columns}
        elements_j = [filter_columns(e) for e in elements_j]
    flatten_to_csv(elements_j, output)
    print(output.getvalue())

if __name__ == "__main__":
    main()
