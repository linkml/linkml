import logging
import os
import sys

import click
from linkml_runtime.linkml_model import Prefix
from linkml_runtime.utils import inference_utils
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.inference_utils import infer_all_slot_values
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.generators.pythongen import PythonGenerator
from linkml.utils import datautils, validation
from linkml.utils.datautils import (
    _get_context,
    _get_format,
    _is_xsv,
    dumpers_loaders,
    get_dumper,
    get_loader,
    infer_index_slot,
    infer_root_class,
)


@click.command()
@click.option("--module", "-m", help="Path to python datamodel module")
@click.option("--output", "-o", help="Path to output file")
@click.option(
    "--input-format",
    "-f",
    type=click.Choice(list(dumpers_loaders.keys())),
    help="Input format. Inferred from input suffix if not specified",
)
@click.option(
    "--output-format",
    "-t",
    type=click.Choice(list(dumpers_loaders.keys())),
    help="Output format. Inferred from output suffix if not specified",
)
@click.option(
    "--target-class",
    "-C",
    help="name of class in datamodel that the root node instantiates",
)
@click.option(
    "--target-class-from-path/--no-target-class-from-path",
    default=False,
    show_default=True,
    help="Infer the target class from the filename, should be ClassName-<other-chars>.{yaml,json,...}",
)
@click.option("--index-slot", "-S", help="top level slot. Required for CSV dumping/loading")
@click.option("--schema", "-s", help="Path to schema specified as LinkML yaml")
@click.option("--prefix", "-P", multiple=True, help="Prefixmap base=URI pairs")
@click.option(
    "--validate/--no-validate",
    default=True,
    show_default=True,
    help="Validate against the schema",
)
@click.option(
    "--infer/--no-infer",
    default=False,
    show_default=True,
    help="Infer missing slot values",
)
@click.option("--context", "-c", multiple=True, help="path to JSON-LD context file")
@click.version_option(__version__, "-V", "--version")
@click.argument("input")
def cli(
    input,
    module,
    target_class,
    context=None,
    output=None,
    input_format=None,
    output_format=None,
    prefix=None,
    target_class_from_path=None,
    schema=None,
    validate=None,
    infer=None,
    index_slot=None,
) -> None:
    """
    Converts instance data to and from different LinkML Runtime serialization formats.

    The instance data must conform to a LinkML model, and either a path to a python
    module must be passed, or a path to a schema.

    The converter works by first using a linkml-runtime *loader* to
    instantiate in-memory model objects, then a *dumper* is used to serialize.
    A validation step is optionally performed in between

    When converting to or from RDF, a path to a schema must be provided.

    For more information, see https://linkml.io/linkml/data/index.html
    """
    if prefix is None:
        prefix = []
    if module is None:
        if schema is None:
            raise Exception("must pass one of module OR schema")
        else:
            python_module = PythonGenerator(schema).compile_module()
    else:
        python_module = compile_python(module)
    prefix_map = {}
    if prefix:
        for p in prefix:
            base, uri = p.split("=")
            prefix_map[base] = uri
    if schema is not None:
        sv = SchemaView(schema)
        if prefix_map:
            for k, v in prefix_map.items():
                sv.schema.prefixes[k] = Prefix(k, v)
                sv.set_modified()
    if target_class is None and target_class_from_path:
        target_class = os.path.basename(input).split("-")[0]
        logging.info(f"inferred target class = {target_class} from {input}")
    if target_class is None:
        target_class = infer_root_class(sv)
    if target_class is None:
        raise Exception("target class not specified and could not be inferred")
    py_target_class = python_module.__dict__[target_class]
    input_format = _get_format(input, input_format)
    loader = get_loader(input_format)

    inargs = {}
    outargs = {}
    if datautils._is_rdf_format(input_format):
        if sv is None:
            raise Exception("Must pass schema arg")
        inargs["schemaview"] = sv
        inargs["fmt"] = input_format
    if _is_xsv(input_format):
        if index_slot is None:
            index_slot = infer_index_slot(sv, target_class)
            if index_slot is None:
                raise Exception("--index-slot is required for CSV input")
        inargs["index_slot"] = index_slot
        inargs["schema"] = schema
    obj = loader.load(source=input, target_class=py_target_class, **inargs)
    if infer:
        infer_config = inference_utils.Config(use_expressions=True, use_string_serialization=True)
        infer_all_slot_values(obj, schemaview=sv, config=infer_config)
    if validate:
        if schema is None:
            raise Exception("--schema must be passed in order to validate. Suppress with --no-validate")
        # TODO: use validator framework
        validation.validate_object(obj, schema)

    output_format = _get_format(output, output_format, default="json")
    if output_format == "json-ld":
        if len(context) == 0:
            if schema is not None:
                context = [_get_context(schema)]
            else:
                raise Exception("Must pass in context OR schema for RDF output")
        outargs["contexts"] = list(context)
    if output_format == "rdf" or output_format == "ttl":
        if sv is None:
            raise Exception("Must pass schema arg")
        outargs["schemaview"] = sv
    if _is_xsv(output_format):
        if index_slot is None:
            index_slot = infer_index_slot(sv, target_class)
            if index_slot is None:
                raise Exception("--index-slot is required for CSV output")
        outargs["index_slot"] = index_slot
        outargs["schema"] = schema
    dumper = get_dumper(output_format)
    if output is not None:
        dumper.dump(obj, output, **outargs)
    else:
        print(dumper.dumps(obj, **outargs))


if __name__ == "__main__":
    cli(sys.argv[1:])
