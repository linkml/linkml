import logging
import sys
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from typing import Any, Iterable, List, Type, Union

import click
import jsonschema
from jsonschema.exceptions import best_match
from linkml_runtime.linkml_model import ClassDefinitionName, SchemaDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.dictutils import as_simple_dict
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml._version import __version__
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.utils import datautils
from linkml.utils.datavalidator import DataValidator


class HashableSchemaDefinition(SchemaDefinition):
    def __hash__(self) -> int:
        return hash(self.id)


@lru_cache(maxsize=None)
def _generate_jsonschema(schema, top_class, closed, include_range_class_descendants):
    logging.debug("Generating JSON Schema")
    not_closed = not closed
    return JsonSchemaGenerator(
        schema=schema,
        mergeimports=True,
        top_class=top_class,
        not_closed=not_closed,
        include_range_class_descendants=include_range_class_descendants,
    ).generate()


class JsonSchemaDataValidatorError(Exception):
    def __init__(self, validation_messages: List[str]) -> None:
        super().__init__("\n".join(validation_messages))
        self.validation_messages = validation_messages


@dataclass
class JsonSchemaDataValidator(DataValidator):
    """
    Implementation of DataValidator that wraps jsonschema validation
    """

    include_range_class_descendants: bool = False
    _hashable_schema: Union[str, HashableSchemaDefinition] = field(init=False, repr=False)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "schema":
            if isinstance(__value, SchemaDefinition):
                self._hashable_schema = HashableSchemaDefinition(**asdict(__value))
            else:
                self._hashable_schema = __value
        return super().__setattr__(__name, __value)

    def validate_file(self, input: str, format: str = "json", **kwargs):
        # return self.validate_object(obj)
        pass

    def validate_object(self, data: YAMLRoot, target_class: Type[YAMLRoot] = None, closed: bool = True) -> None:
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
        self.validate_dict(inst_dict, target_class.class_name, closed)

    def validate_dict(self, data: dict, target_class: ClassDefinitionName = None, closed: bool = True) -> None:
        """
        validates instance data against a schema

        :param data: dictionary object
        :param target_class: class in schema to validate against
        :param closed:
        :return:
        """
        results = list(self.iter_validate_dict(data, target_class, closed))
        if results:
            raise JsonSchemaDataValidatorError(results)

    def iter_validate_dict(
        self, data: dict, target_class_name: ClassDefinitionName = None, closed: bool = True
    ) -> Iterable[str]:
        if self.schema is None:
            raise ValueError("schema object must be set")
        if target_class_name is None:
            roots = [c.name for c in self.schema.classes.values() if c.tree_root]
            if len(roots) != 1:
                raise ValueError(f"Cannot determine tree root: {roots}")
            target_class_name = roots[0]
        jsonschema_obj = _generate_jsonschema(
            self._hashable_schema, target_class_name, closed, self.include_range_class_descendants
        )
        validator_cls = jsonschema.validators.validator_for(jsonschema_obj, default=jsonschema.Draft7Validator)
        validator = validator_cls(jsonschema_obj, format_checker=validator_cls.FORMAT_CHECKER)
        for error in validator.iter_errors(data):
            best_error = best_match([error])
            # TODO: This should return some kind of standard validation result
            # object, but until that is defined just yield string messages
            yield f"{best_error.message} in {best_error.json_path}"


@click.command()
@click.option("--module", "-m", help="Path to python datamodel module")
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
@click.option("--index-slot", "-S", help="top level slot. Required for CSV dumping/loading")
@click.option("--schema", "-s", help="Path to schema specified as LinkML yaml")
@click.option(
    "--exit-on-first-failure/--no-exit-on-first-failure",
    default=False,
    help="Exit after the first validation failure is found. If not specified all validation failures are reported.",
)
@click.option(
    "--include-range-class-descendants/--no-range-class-descendants",
    default=False,
    show_default=False,
    help="""
When handling range constraints, include all descendants of the range class instead of just the range class
""",
)
@click.argument("input")
@click.version_option(__version__, "-V", "--version")
def cli(
    input,
    module,
    target_class,
    input_format=None,
    schema=None,
    index_slot=None,
    exit_on_first_failure=False,
    include_range_class_descendants=False,
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
        raise Exception("target class not specified and could not be inferred")
    py_target_class = python_module.__dict__[target_class]
    input_format = datautils._get_format(input, input_format)
    loader = datautils.get_loader(input_format)

    inargs = {}
    if datautils._is_xsv(input_format):
        if index_slot is None:
            index_slot = datautils.infer_index_slot(sv, target_class)
            if index_slot is None:
                raise Exception("--index-slot is required for CSV input")
        inargs["index_slot"] = index_slot
        inargs["schema"] = schema
    if datautils._is_rdf_format(input_format):
        inargs["schemaview"] = sv
        inargs["fmt"] = input_format

    try:
        data_as_dict = loader.load_as_dict(source=input, **inargs)
    except NotImplementedError:
        obj = loader.load(source=input, target_class=py_target_class, **inargs)
        data_as_dict = as_simple_dict(obj)

    # Validation
    if schema is None:
        raise Exception("--schema must be passed in order to validate. Suppress with --no-validate")

    validator = JsonSchemaDataValidator(schema, include_range_class_descendants=include_range_class_descendants)
    error_count = 0
    for error in validator.iter_validate_dict(data_as_dict, target_class_name=py_target_class.class_name):
        error_count += 1
        click.echo(click.style("\u2717 ", fg="red") + error)
        if exit_on_first_failure:
            sys.exit(1)

    if not error_count:
        click.echo(click.style("\u2713 ", fg="green") + "No problems found")

    sys.exit(0 if error_count == 0 else 1)


if __name__ == "__main__":
    cli(sys.argv[1:])
