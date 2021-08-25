from typing import Union, TextIO, Optional

import click
from openpyxl import Workbook

from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition
from linkml_runtime.utils.formatutils import camelcase, be


class ExcelGenerator(Generator):
    valid_formats = ["xlsx"]

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], filename: Optional[str] = None, **kwargs) -> None:
        self.wb_name = filename
        self.workbook = Workbook()
        super().__init__(schema, **kwargs)

    def create_spreadsheet(self, ws_name: str = None):
        self.workbook.create_sheet(ws_name)
        self.workbook.save(self.wb_name)

    def visit_class(self, cls: ClassDefinition) -> str:
        self.create_spreadsheet(ws_name=camelcase(cls.name))


@shared_arguments(ExcelGenerator)
@click.command()
@click.option("-f", "--filename", help="""Name of Excel spreadsheet to be created""")
def cli(yamlfile, **kwargs):
    """Generate Excel representation of a LinkML model"""
    print(ExcelGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
