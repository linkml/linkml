from typing import Union, TextIO

import click

from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import SchemaDefinition


class ExcelGenerator(Generator):
    valid_formats = ["xlsx"]

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], **kwargs) -> None:
        super().__init__(schema, **kwargs)


@shared_arguments(ExcelGenerator)
@click.command()
def cli(yamlfile, **kwargs):
    """Generate Excel representation of a LinkML model"""
    print(ExcelGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
