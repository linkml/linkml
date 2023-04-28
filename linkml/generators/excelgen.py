import os
import logging

from dataclasses import dataclass
from typing import List

import click

from linkml_runtime.utils.schemaview import SchemaView
from linkml.utils.generator import Generator, shared_arguments
from linkml._version import __version__
from linkml.utils.helpers import convert_to_snake_case
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter


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
        self.logger = logging.getLogger(__name__)
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

    def create_worksheet(self, workbook: Workbook, worksheet_name: str) -> Worksheet:
        """
        Creates an Excel worksheet with the given name in the given workbook.

        :param workbook: The workbook to which the worksheet should be added.
        :param worksheet_name: Name of the worksheet to be created.
        """
        worksheet = workbook.create_sheet(worksheet_name)
        workbook_name = self.get_workbook_name(workbook)
        workbook.save(workbook_name)

        return worksheet

    def create_schema_worksheets(self, workbook: str) -> None:
        """
        Creates worksheets in a given Excel workbook based on the classes in the
        schema.

        :param workbook: The workbook to which the worksheet should be added.
        """
        sv = self.schemaview
        for cls_name, cls in sv.all_classes(imports=self.mergeimports).items():
            if not cls.mixin and not cls.abstract:
                self.create_worksheet(workbook, cls_name)

    def add_columns_to_worksheet(
        self, workbook: Workbook, worksheet_name: str, sheet_headings: List[str]
    ) -> None:
        """
        Get a worksheet by name and add a column to it in an existing workbook.

        :param workbook: The workbook to which the worksheet should be added.
        :param worksheet_name: Name of the worksheet to add the column to.
        :param column_data: List of data to populate the column with.
        """
        # Get the worksheet by name
        worksheet = workbook[worksheet_name]

        # Add the headings to the worksheet
        for i, heading in enumerate(sheet_headings):
            worksheet.cell(row=1, column=i + 1, value=heading)

        # Save the changes to the workbook
        workbook_name = self.get_workbook_name(workbook)
        workbook.save(workbook_name)

    def column_enum_validation(
        self,
        workbook: Workbook,
        worksheet_name: str,
        column_name: str,
        dropdown_values: List[str],
    ) -> None:
        """
        Get worksheet by name and add a dropdown to a specific column in it
        based on a list of values.

        :param workbook: The workbook to which the worksheet should be added.
        :param worksheet_name: Name of the worksheet to add the column dropdown to.
        :param column_name: Name of the worksheet column to add the dropdown to.
        :param dropdown_values: List of dropdown values to add to a column in a worksheet.
        """
        worksheet = workbook[worksheet_name]

        column_list = [cell.value for cell in worksheet[1]]
        column_number = column_list.index(column_name) + 1
        column_letter = get_column_letter(column_number)

        # Create the data validation object and set the dropdown values
        dv = DataValidation(
            type="list", formula1=f'"{",".join(dropdown_values)}"', allow_blank=True
        )

        worksheet.add_data_validation(dv)

        dv.add(f"{column_letter}2:{column_letter}1048576")

        workbook_name = self.get_workbook_name(workbook)
        workbook.save(workbook_name)

    def serialize(self, **kwargs) -> str:
        self.output = (
            os.path.abspath(convert_to_snake_case(self.schema.name) + ".xlsx")
            if not self.output
            else self.output
        )

        workbook = self.create_workbook(self.output)
        self.remove_worksheet_by_name(workbook, "Sheet")
        self.create_schema_worksheets(workbook)

        sv = self.schemaview
        for cls_name, cls in sv.all_classes(imports=self.mergeimports).items():
            if not cls.mixin and not cls.abstract:
                slots = [
                    s.name
                    for s in sv.class_induced_slots(cls_name, imports=self.mergeimports)
                ]
                self.add_columns_to_worksheet(workbook, cls_name, slots)

        enum_list = [
            e_name for e_name, _ in sv.all_enums(imports=self.mergeimports).items()
        ]
        for cls_name, cls in sv.all_classes(imports=self.mergeimports).items():
            if not cls.mixin and not cls.abstract:
                for s in sv.class_induced_slots(cls_name, imports=self.mergeimports):
                    if s.range in enum_list:
                        pv_list = []
                        for pv_name, _ in sv.get_enum(
                            s.range
                        ).permissible_values.items():
                            pv_list.append(pv_name)
                        self.column_enum_validation(workbook, cls_name, s.name, pv_list)
        self.logger.info(f"The Excel workbook has been written to {self.output}")


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
    ExcelGenerator(yamlfile, **kwargs).serialize(**kwargs)


if __name__ == "__main__":
    cli()
