import os
import json
from typing import TextIO, Union

import click

from linkml_runtime.dumpers import json_dumper

from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition

from linkml_runtime.utils.schemaview import SchemaView

from linkml.utils.generator import Generator, shared_arguments


class JsonGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "1.0.0"
    valid_formats = ["json"]

    def __init__(
        self,
        schema: Union[str, TextIO, SchemaDefinition],
        class_name: str,
        output_path: str = None,
        **kwargs
    ):
        self.schemaview = SchemaView(schema)
        self.class_name = class_name

    def _get_class_defn(self, class_name: str) -> ClassDefinition:
        """Return ClassDefinition representation of class

        :param class_name: class name from supplied schema, as string
        :type class_name: str
        :return: class object representation, as ClassDefinition
        :rtype: ClassDefinition
        """
        return self.schemaview.get_class(class_name)

    def json(self) -> str:
        """Return unfolded JSON with all induced slots as attributes

        :return: JSON serialization of ClassDefinition object
        :rtype: str
        """
        c = self._get_class_defn(self.class_name)
        attrs = self.schemaview.class_induced_slots(c.name)
        for a in attrs:
            c.attributes[a.name] = a
        c.slots = []

        return json_dumper.dumps(c)

    def serialize(self, output=None, **args) -> str:
        json_str = self.json()

        if output:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(json_str, ensure_ascii=False, indent=4)
        else:
            return json_str


@shared_arguments(JsonGenerator)
@click.option(
    "--class_name", "-c", required=True, help="Class to retrieve all induced slots on"
)
@click.option("--output", "-o", type=click.Path(), help="Path to output JSON file")
@click.command()
def cli(yamlfile, class_name, output, **args):
    gen = JsonGenerator(yamlfile, class_name, **args)
    print(gen.serialize(output))


if __name__ == "__main__":
    cli()
