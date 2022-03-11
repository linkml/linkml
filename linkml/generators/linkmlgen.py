import logging
import os
from typing import TextIO, Union

import click

from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.utils.schemaview import SchemaView
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.helpers import write_to_file


logger = logging.getLogger(__name__)


class LinkmlGenerator(Generator):
    """This generator provides a direct conversion of a LinkML schema
    into json, optionally merging imports and unrolling induced slots
    into attributes
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "1.0.0"
    valid_formats = ["json", "yaml"]

    def __init__(
        self,
        schema: Union[str, TextIO, SchemaDefinition],
        materialize_attributes: bool,
        mergeimports: bool = None,
        format: str = valid_formats[0],
        **kwargs,
    ):
        self.schemaview = SchemaView(schema)
        self.materialize = materialize_attributes
        self.format = format

        if mergeimports:
            self.schemaview.merge_imports()

    def materialize_classes(self) -> None:
        """Materialize class slots from schema as attribues, in place"""
        all_classes = self.schemaview.all_classes()

        for c_name, c_def in all_classes.items():
            attrs = self.schemaview.class_induced_slots(c_name)
            for attr in attrs:
                c_def.attributes[attr.name] = attr

        return

    def serialize(self, output: str = None, **kwargs) -> str:
        if self.materialize:
            self.materialize_classes()

        if self.format == "json":
            json_str = json_dumper.dumps(self.schemaview.schema)

            if output:
                write_to_file(output, json_str)
                logger.info(f"Materialized file written to: {output}")
                return output

            return json_str
        elif self.format == "yaml":
            yaml_str = yaml_dumper.dumps(self.schemaview.schema)

            if output:
                write_to_file(output, yaml_str)
                logger.info(f"Materialized file written to: {output}")
                return output

            return yaml_str
        else:
            raise ValueError(
                f"{self.format} is an invalid format. Use one of the following "
                f"formats: {self.valid_formats}"
            )


@shared_arguments(LinkmlGenerator)
@click.option(
    "--materialize-attributes/--no-materialize-attributes",
    default=True,
    show_default=True,
    help="Materialize induced slots as attributes",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="""Name of JSON or YAML file to be created""",
)
@click.command()
def cli(yamlfile, materialize_attributes, output, **kwargs):
    gen = LinkmlGenerator(
        yamlfile, materialize_attributes=materialize_attributes, **kwargs
    )
    print(gen.serialize(output=output))


if __name__ == "__main__":
    cli()
