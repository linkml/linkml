from email.policy import default
import logging
import os
import json
from typing import Dict, List, TextIO, Union

import click

from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition
from linkml_runtime.utils.schemaview import SchemaView
from linkml.utils.generator import Generator, shared_arguments


logger = logging.getLogger(__name__)


class JsonGenerator(Generator):
    """This generator provides a direct conversion of a LinkML schema
    into json, optionally merging imports and unrolling induced slots
    into attributes
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "1.0.0"
    valid_formats = ["json"]

    def __init__(
        self,
        schema: Union[str, TextIO, SchemaDefinition],
        materialize_attributes: bool,
        **kwargs,
    ):
        self.schemaview = SchemaView(schema)
        self.materialize = materialize_attributes

    def materialized_classes(self) -> List[ClassDefinition]:
        """Return list of ClassDefinition objects with each of
        the classes having their slots materialized as attribues

        :return: List of ClassDefinition objects
        :rtype: List[ClassDefinition]
        """
        all_classes = self.schemaview.all_classes()

        # class definition objects with slots materialized as attributes
        c_def_list = []

        for c_name, c_def in all_classes.items():
            attrs = self.schemaview.class_induced_slots(c_name)
            for attr in attrs:
                c_def.attributes[attr.name] = attr
            c_def.slots = []
            c_def_list.append(c_def)

        return c_def_list

    def json(self) -> List[Dict[str, Union[str, dict]]]:
        """Create list of JSON strings in dictionary format

        :return: List of JSON dicts
        :rtype: List[Dict[str, Union[str, dict]]]
        """        
        json_str_list = []

        if self.materialize:
            for c_def in self.materialized_classes():
                json_str_list.append(json_dumper.dumps(c_def))
        else:
            for c_name, c_def in self.schemaview.all_classes().items():
                json_str_list.append(json_dumper.dumps(c_def))

        json_dict_list = []

        for json_str in json_str_list:
            json_dict_list.append(json.loads(json_str))

        return json_dict_list

    def serialize(
        self, output=None, **args
    ) -> Union[str, Dict[str, Union[str, List[str], Dict]]]:
        json_dict_list = self.json()

        if output:
            with open(output, "w") as f:
                json.dump(
                    json_dict_list,
                    f,
                    sort_keys=False,
                    ensure_ascii=False,
                    indent=4,
                    separators=(",", ": "),
                )
            logger.info(f"The JSON file has been written to {output}")
        else:
            return json_dict_list


@shared_arguments(JsonGenerator)
@click.option(
    "--materialize-attributes/--no-materialize-attributes",
    default=True,
    required=True,
    help="Materialize induced slots as attributes",
)
@click.option("--output", "-o", type=click.Path(), help="Path to output JSON file")
@click.command()
def cli(yamlfile, materialize_attributes, output, **args):
    gen = JsonGenerator(yamlfile, materialize_attributes, **args)
    print(gen.serialize(output))


if __name__ == "__main__":
    cli()
