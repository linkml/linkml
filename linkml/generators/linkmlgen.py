import logging
import os
from dataclasses import dataclass, field
from typing import TextIO, Union

import click
from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.helpers import write_to_file
from linkml_runtime.utils.pattern import generate_patterns

logger = logging.getLogger(__name__)


@dataclass
class LinkmlGenerator(Generator):
    """This generator provides a direct conversion of a LinkML schema
    into json, optionally merging imports and unrolling induced slots
    into attributes
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "1.0.0"
    valid_formats = ["json", "yaml"]
    uses_schemaloader = False
    requires_metamodel = False

    materialize_attributes: bool = field(default_factory=lambda: False)
    materialize_patterns: bool = field(default_factory=lambda: False)


    def __post_init__(self):
        # TODO: consider moving up a level
        self.schemaview = SchemaView(self.schema)
        super().__post_init__()


    def materialize_classes(self) -> None:
        """Materialize class slots from schema as attribues, in place"""
        all_classes = self.schemaview.all_classes()

        for c_name, c_def in all_classes.items():
            attrs = self.schemaview.class_induced_slots(c_name)
            for attr in attrs:
                c_def.attributes[attr.name] = attr

    def serialize(self, output: str = None, **kwargs) -> str:
        if self.materialize_attributes:
            self.materialize_classes()
        if self.materialize_patterns:
            self.schemaview.materialize_patterns()

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
    "--materialize-patterns/--no-materialize-patterns",
    default=False,
    show_default=True,
    help="Materialize structured patterns as patterns",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="""Name of JSON or YAML file to be created""",
)
@click.command()
def cli(yamlfile, materialize_attributes: bool, output, **kwargs):
    gen = LinkmlGenerator(
        yamlfile,
        materialize_attributes=materialize_attributes,
        **kwargs
    )
    print(gen.serialize(output=output))


if __name__ == "__main__":
    cli()
