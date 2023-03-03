import os

from dataclasses import dataclass, field
from typing import List, Dict, Union

import click

from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.linkml_model import SchemaDefinition
from linkml.utils.generator import Generator, shared_arguments
from linkml._version import __version__
from linkml.utils.helpers import convert_to_snake_case
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class ExcelGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["xlsx"]
    uses_schemaloader = False
    requires_metamodel = False

    def __post_init__(self) -> None:
        super().__post_init__()
        self.schemaview = SchemaView(self.schema)

    def create_workbook(self, workbook_name: str) -> Workbook:
        """
        Creates an Excel workbook using the openpyxl library and returns it.

        :param workbook_name: Name of the workbook to be created.
        :return: An openpyxl Workbook object representing the newly created workbook.
        """
        workbook = Workbook()
        workbook.title = workbook_name
        return workbook

    def get_workbook_name(self, workbook: Workbook) -> str:
        """
        Returns the name of the given workbook.

        :param workbook: The workbook whose name should be returned.
        :return: Name of the workbook.
        """
        return workbook.title

    def remove_worksheet_by_name(self, workbook: Workbook, worksheet_name: str) -> None:
        """
        Remove worksheet from workbook by name.
        """
        worksheet = workbook[worksheet_name]
        workbook.remove(worksheet)

    def create_worksheet(self, workbook: Workbook, worksheet_name: str) -> None:
        """
        Creates an Excel worksheet with the given name in the given workbook.

        :param workbook: The workbook to which the worksheet should be added.
        :param worksheet_name: Name of the worksheet to be created.
        """
        worksheet = workbook.create_sheet(worksheet_name)
        workbook_name = self.get_workbook_name(workbook)
        workbook.save(workbook_name)

    def create_schema_worksheets(self, workbook: str):
        """
        Creates worksheets in a given Excel workbook based on the classes in the
        schema.

        :param workbook: The workbook to which the worksheet should be added.
        """
        sv = self.schemaview
        for c in sv.all_classes(imports=self.mergeimports).values():
            self.create_worksheet(workbook, c.name)

    def populate_worksheet_columns(self):
        pass

    def column_enum_validation(self):
        pass

    def serialize(self, **kwargs) -> str:
        output = (
            convert_to_snake_case(self.schema.name) + ".xlsx"
            if not self.output
            else self.output
        )

        workbook = self.create_workbook(output)
        self.remove_worksheet_by_name(workbook, "Sheet")
        self.create_schema_worksheets(workbook)


@shared_arguments(ExcelGenerator)
@click.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="""Name of Excel spreadsheet to be created""",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate Excel representation of a LinkML model"""
    print(ExcelGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
