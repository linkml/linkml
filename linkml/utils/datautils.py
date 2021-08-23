import os
import sys

import click

from linkml_runtime.utils.compile_python import compile_python

from linkml_runtime.dumpers.yaml_dumper import YAMLDumper
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.dumpers.rdf_dumper import RDFDumper
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.loaders.json_loader import JSONLoader
from linkml_runtime.loaders.rdf_loader import RDFLoader
from linkml_runtime.loaders.loader_root import Loader

from linkml.generators.pythongen import PythonGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
import linkml.utils.validation as validation

dumpers_loaders = {
    'yaml': (YAMLDumper, YAMLLoader),
    'json': (JSONDumper, JSONLoader),
    'rdf': (RDFDumper, RDFLoader),
}

aliases = {
    'ttl': 'rdf'
}

def _get_format(path: str, specified_format: str =None, default=None):
    if specified_format is None:
        if path is None:
            if default is None:
                raise Exception(f'Must pass format option OR pass a filename with known file suffix')
            else:
                specified_format = default
        else:
            _, ext = os.path.splitext(path)
            if ext is not None:
                specified_format = ext.replace('.', '')
            else:
                raise Exception(f'Must pass format option OR use known file suffix: {path}')
    specified_format = specified_format.lower()
    if specified_format in aliases:
        specified_format = aliases[specified_format]
    return specified_format

def get_loader(fmt: str) -> Loader:
    return dumpers_loaders[fmt][1]()
def get_dumper(fmt: str) -> Loader:
    return dumpers_loaders[fmt][0]()

def _get_context(schema) -> str:
    return ContextGenerator(schema).serialize()

@click.command()
@click.option("--module", "-m",
              help="Path to python datamodel module")
@click.option("--output", "-o",
              help="Path to output file")
@click.option("--input-format", "-f",
              type=click.Choice(list(dumpers_loaders.keys())),
              help="Input format. Inferred from input suffix if not specified")
@click.option("--output-format", "-t",
              type=click.Choice(list(dumpers_loaders.keys())),
              help="Output format. Inferred from output suffix if not specified")
@click.option("--target-class", "-C",
              required=True,
              help="name of class in datamodel that the root node instantiates")
@click.option("--schema", "-s",
              help="Path to schema specified as LinkML yaml")
@click.option("--validate/--no-validate",
              default=True,
              help="Validate against the schema")
@click.option("--context", "-c",
              multiple=True,
              help="path to JSON-LD context file. Required for RDF input/output")
@click.argument("input")
def cli(input, module, target_class, context=None, output=None, input_format=None, output_format=None,
        schema=None, validate=None, index_slot=None) -> None:
    """
    Converts instance data to and from different LinkML Runtime serialization formats.

    The instance data must conform to a LinkML model, and there must be python dataclasses
    generated from that model. The converter works by first using a linkml-runtime loader to
    instantiate in-memory model objects, then dumpers are used to serialize.
    When converting to or from RDF, a JSON-lD context must also be passed
    """
    if module is None:
        if schema is None:
            raise Exception('must pass one of module OR schema')
        else:
            pycode = PythonGenerator(schema).serialize()
            python_module = compile_python(pycode)
    else:
        python_module = compile_python(module)
    target_class = python_module.__dict__[target_class]
    input_format = _get_format(input, input_format)
    loader = get_loader(input_format)

    inargs = {}
    outargs = {}
    if input_format == 'rdf':
        if len(context) == 0:
            if schema is not None:
                context = [_get_context(schema)]
            else:
                raise Exception('Must pass in context OR schema for RDF output')
        inargs['contexts'] = list(context)[0]

    obj = loader.load(source=input,  target_class=target_class, **inargs)
    if validate:
        if schema is None:
            raise Exception('--schema must be passed in order to validate. Suppress with --no-validate')
        validation.validate_object(obj, schema)

    output_format = _get_format(output, output_format, default='json')
    if output_format == 'rdf':
        if len(context) == 0:
            if schema is not None:
                context = [_get_context(schema)]
            else:
                raise Exception('Must pass in context OR schema for RDF output')
        outargs['contexts'] = list(context)
    dumper = get_dumper(output_format)
    if output is not None:
        dumper.dump(obj, output, **outargs)
    else:
        print(dumper.dumps(obj, **outargs))


if __name__ == '__main__':
    cli(sys.argv[1:])