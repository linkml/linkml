"""Validate linkml input and optionally emit completely resolved biolink yaml output

"""
import os
from typing import Union, TextIO

import click

from linkml_model.meta import SchemaDefinition
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.utils.yamlutils import as_yaml


class YAMLGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ['yaml']

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], **kwargs) -> None:
        super().__init__(schema, **kwargs)

    def serialize(self, validateonly:bool = False, **kwargs) -> str:
        if validateonly:
            return self.synopsis.summary()
        else:
            return as_yaml(self.schema)


@shared_arguments(YAMLGenerator)
@click.command()
@click.option("--validateonly/--generate", "-v/-g", default=False,
              help="Just validate / generate output (default: generate)")
def cli(yamlfile, **args):
    """ Validate input and produce fully resolved yaml equivalent """
    print(YAMLGenerator(yamlfile, **args).serialize(**args))


if __name__ == '__main__':
    cli()
