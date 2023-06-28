from typing import Dict, List

import json
import click
from linkml.validator.utils import import_plugin
from linkml.validator.models import ValidationReport
from linkml.validator.parsers.json_parser import JsonParser
from linkml.validator.parsers.tsv_parser import TsvParser

from linkml.validator.plugins.base import BasePlugin


class Validator:
    """
    Validator to validate incoming data against a given linkml schema.

    Validator is responsible for dealing with:
        - instantiating the validation plugins
        - fetching objects for validation (file or endpoint) by calling
          the appropriate parser
        - transforming objects by calling an appropriate converter (if needed)
        - calling the validation plugins and collect validation results
        - creation of validation reports

    From the Validator standpoint,
        - the parser is flexible
        - the converter is flexible
        - the generator is flexible
        - the plugins are flexible

    """

    def __init__(self, schema: str, plugins: List[Dict] = [], **kwargs) -> None:
        """
        Initialize the validator with the schema and a list of plugins.

        Args:
            schema: The schema YAML
            plugins: A list of plugin definitions
            kwargs: Additional arguments

        """
        self.schema = schema
        self.plugins = []
        for plugin in plugins:
            plugin_class = plugin["plugin_class"]
            plugin_args = {}
            if "args" in plugin:
                plugin_args = plugin["args"]
            if not issubclass(plugin_class, BasePlugin):
                raise Exception(f"{plugin_class} must be a subclass of {BasePlugin}")
            instance = plugin_class(schema=self.schema, **plugin_args)
            self.plugins.append(instance)

    def validate(self, obj: Dict, target_class: str = None, strict: bool = False, **kwargs) -> ValidationReport:
        """
        Validate an object.

        Args:
            object: The object to validate
            target_class: The target class
            strict: Whether to perform strict validation (i.e. fail on first error)
            kwargs: Additional arguments

        Returns:
            An instance of ValidationReport for the given object

        """
        results = []
        if target_class is None:
            raise Exception("'target_class' must be provided")
        # if target_class is None and target_class_field is None:
        #     raise Exception("'target_class' or 'target_class_field' must be provided")
        # if target_class_field:
        #     if target_class_field not in obj:
        #         raise Exception(f"`target_class_field` provided by the given object does not have a '{target_class_field}' field")
        #    target_class = obj[target_class_field]
        for plugin in self.plugins:
            results.extend(plugin.process(obj=obj, target_class=target_class, **kwargs))
            # if report and strict:
            #     raise Exception()
        validation_report = ValidationReport(
            results=results
        )
        return validation_report

    def validate_file(self, filename: str, format: str, compressed: bool = False, target_class: str = None, strict: bool = False, **kwargs) -> List[ValidationReport]:
        """
        Validate all objects from a given file.

        Args:
            filename: The filename
            format: The file format
            compressed: Whether or not the file is compressed
            target_class: The target class
            strict: Whether to perform strict validation (i.e. fail on first error)
            kwargs: Additional arguments

        Returns a list of ValidationReport instances where each report
        corresponds to validation outcome for an object.
        """
        args = {'compressed': compressed}
        if format == 'tsv':
            parser = TsvParser()
            args['delimiter'] = '\t'
        elif format == 'csv':
            parser = TsvParser()
            args['delimiter'] = ','
        elif format == 'json':
            parser = JsonParser()

        print(parser)
        reports = []
        stream = parser.parse(filename, format=format, **args)
        for obj in stream:
            report = self.validate(obj, target_class=target_class, **kwargs)
            reports.append(report)
        return reports



PLUGIN_DEFS = {
    "JsonSchemaValidationPlugin": {
        "plugin_class": "linkml.validator.plugins.jsonschema_validation.JsonSchemaValidationPlugin",
        "plugin_args": {}
    }
}

DEFAULT_PLUGINS = ["JsonSchemaValidationPlugin"]


@click.command()
@click.option(
    "--inputs",
    "-i",
    required=True,
    multiple=True,
    type=click.Path(exists=True),
    help="Files to validate",
)
@click.option(
    "--format",
    "-f",
    required=True,
    help="The input file format"
)
@click.option(
    "--compressed",
    "-c",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Whether the input file is a gzip compressed file"
)
@click.option("--schema", "-s", required=True, help="The LinkML schema YAML")
@click.option(
    "--output",
    "-o",
    required=False,
    help="Output file to write validation reports",
    type=click.Path(exists=False),
)
@click.option(
    "--target-class",
    "-t",
    required=False,
    help="The target class which all objects from the input data are an instance of",
)
@click.option(
    "--plugins",
    "-p",
    multiple=True,
    default=DEFAULT_PLUGINS,
    help="The plugins to use for validation",
)
@click.option(
    "--strict",
    default=False,
    is_flag=True,
    help="Whether or not to perform strict validation",
)
def cli(inputs, format, compressed, schema, output, target_class, plugins, strict):
    """
    Run the Validator on data from one or more files.
    """
    plugin_class_references = []
    if not plugins:
        plugins = DEFAULT_PLUGINS
    for plugin in plugins:
        plugin_def = PLUGIN_DEFS[plugin]
        plugin_module_name = ".".join(plugin_def['plugin_class'].split(".")[:-1])
        plugin_class_name = plugin_def['plugin_class'].split(".")[-1]
        plugin_class = import_plugin(plugin_module_name, plugin_class_name)
        plugin_class_references.append({'plugin_class': plugin_class, 'plugin_args': plugin_def['plugin_args']})

    validator = Validator(schema=schema, plugins=plugin_class_references)
    for filename in inputs:
        reports = [x for x in validator.validate_file(filename=filename, format=format, compressed=compressed, target_class=target_class, strict=strict)]
        if output:
            with open(output, "w", encoding="UTF-8") as file:
                json.dump([x.dict() for x in reports], file, indent=2)
        else:
            print(json.dumps([x.dict() for x in reports], indent=2))