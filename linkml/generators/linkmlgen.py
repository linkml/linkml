import logging
import os
from typing import TextIO, Union

import click

from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.utils.schemaview import SchemaView
from linkml.utils.generator import Generator, shared_arguments


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
        mergeimports: bool,
        format: str,
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

    def serialize(self, **kwargs) -> str:
        if self.materialize:
            self.materialize_classes()

        if self.format == "json":
            return json_dumper.dumps(self.schemaview.schema)
        elif self.format == "yaml":
            return yaml_dumper.dumps(self.schemaview.schema)
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
@click.command()
def cli(yamlfile, materialize_attributes, **kwargs):
    gen = LinkmlGenerator(
        yamlfile, materialize_attributes=materialize_attributes, **kwargs
    )
    print(gen.serialize())


if __name__ == "__main__":
    cli()
