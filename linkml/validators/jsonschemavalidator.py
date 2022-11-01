import json
import sys
from dataclasses import dataclass
from typing import TextIO, Type, Union

import click
import jsonschema
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinitionName
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.dictutils import as_simple_dict
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml._version import __version__
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.utils import datautils
from linkml.utils.datavalidator import DataValidator


@dataclass
class JsonSchemaDataValidator(DataValidator):
    def validate_file(self, input: str, format: str = "json", **kwargs):
        return self.validate_object(obj)

    def validate_object(
        self, data: YAMLRoot, target_class: Type[YAMLRoot] = None, closed: bool = True
    ) -> None:
        """
        validates instance data against a schema

        :param data: LinkML instance to be validates
        :param target_class: class in schema to validate against
        :param closed:
        :return:
        """
        if target_class is None:
            target_class = type(data)
        inst_dict = as_simple_dict(data)
        not_closed = not closed
        if self.schema is None:
            raise ValueError(f"schema object must be set")
        jsonschemastr = JsonSchemaGenerator(
            self.schema,
            mergeimports=True,
            top_class=target_class.class_name,
            not_closed=not_closed,
        ).serialize(not_closed=not_closed)
        jsonschema_obj = json.loads(jsonschemastr)
        return jsonschema.validate(inst_dict, schema=jsonschema_obj, format_checker=jsonschema.Draft7Validator.FORMAT_CHECKER)

    def validate_dict(
        self, data: dict, target_class: ClassDefinitionName = None, closed: bool = True
    ) -> None:
        """
        validates instance data against a schema

        :param data: dictionary object
        :param target_class: class in schema to validate against
        :param closed:
        :return:
        """
        not_closed = not closed
        if self.schema is None:
            raise ValueError(f"schema object must be set")
        if target_class is None:
            roots = [c.name for c in self.schema.classes.values() if c.tree_root]
            if len(roots) != 1:
                raise ValueError(f"Cannot determine tree root: {roots}")
            target_class = roots[0]
        jsonschemastr = JsonSchemaGenerator(
            self.schema,
            mergeimports=True,
            top_class=target_class,
            not_closed=not_closed,
        ).serialize(not_closed=not_closed)
        jsonschema_obj = json.loads(jsonschemastr)
        return jsonschema.validate(data, schema=jsonschema_obj, format_checker=jsonschema.Draft7Validator.FORMAT_CHECKER)


@click.command()
@click.option("--module", "-m", help="Path to python datamodel module")
@click.option("--output", "-o", help="Path to output file")
@click.option(
    "--input-format",
    "-f",
    type=click.Choice(list(datautils.dumpers_loaders.keys())),
    help="Input format. Inferred from input suffix if not specified",
)
@click.option(
    "--target-class",
    "-C",
    help="name of class in datamodel that the root node instantiates",
)
@click.option(
    "--index-slot", "-S", help="top level slot. Required for CSV dumping/loading"
)
@click.option("--schema", "-s", help="Path to schema specified as LinkML yaml")
@click.argument("input")
@click.version_option(__version__, "-V", "--version")
def cli(
    input,
    module,
    target_class,
    output=None,
    input_format=None,
    schema=None,
    index_slot=None,
) -> None:
    """
    Validates instance data
    """
    if module is None:
        if schema is None:
            raise Exception("must pass one of module OR schema")
        else:
            python_module = PythonGenerator(schema).compile_module()
    else:
        python_module = compile_python(module)
    if schema is not None:
        sv = SchemaView(schema)
    if target_class is None:
        target_class = datautils.infer_root_class(sv)
    if target_class is None:
        raise Exception(f"target class not specified and could not be inferred")
    py_target_class = python_module.__dict__[target_class]
    input_format = datautils._get_format(input, input_format)
    loader = datautils.get_loader(input_format)

    inargs = {}
    outargs = {}
    if datautils._is_xsv(input_format):
        if index_slot is None:
            index_slot = infer_index_slot(sv, target_class)
            if index_slot is None:
                raise Exception("--index-slot is required for CSV input")
        inargs["index_slot"] = index_slot
        inargs["schema"] = schema
    if datautils._is_rdf_format(input_format):
        inargs["schemaview"] = sv
        inargs["fmt"] = input_format
    obj = loader.load(source=input, target_class=py_target_class, **inargs)
    # Validation
    if schema is None:
        raise Exception(
            "--schema must be passed in order to validate. Suppress with --no-validate"
        )
    validator = JsonSchemaDataValidator(schema)
    results = validator.validate_object(obj, target_class=py_target_class)
    print(results)


if __name__ == "__main__":
    cli(sys.argv[1:])
