import os
from dataclasses import dataclass, field
from typing import List, Optional, TextIO, Union

import click
from linkml_runtime.linkml_model.meta import (ClassDefinition, EnumDefinition,
                                              PermissibleValue,
                                              PermissibleValueText,
                                              SchemaDefinition, SlotDefinition)
from linkml_runtime.utils.formatutils import camelcase
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from linkml.utils.generator import Generator, shared_arguments


@dataclass
class ExcelGenerator(Generator):
    """This class is a blueprint for the generator module that is responsible
    for automatically creating Excel spreadsheets from the LinkML schema.

    :param schema: LinkML schema object
    :type schema: class:`SchemaDefinition`
    :param output: LinkML schema specification in YAML format
    :type output: str
    """

    # ClassVars
    generator_name = os.path.splitext(os.path.basename(__file__))[0]
    generator_version = "0.0.1"
    valid_formats = ["xlsx"]
    uses_schemaloader = True
    requires_metamodel = False

    # ObjectVars
    sheet_name_cols: List[str] = field(default_factory=lambda: [])
    output: str = None
    workbook: Workbook = field(default_factory=lambda: Workbook())
    wb_name: str = None
    enum_dict: dict = field(default_factory=lambda: dict())
    """dictionary with slot types and possibles values for those types"""

    def _workbook_path(self, yaml_filename: str, wb_name: str = None):
        """Internal method that computes the path where the Excel workbook
        should be stored.

        :param yaml_filename: Name of provided LinkML schema
        :type yaml_filename: str
        :param wb_name: Prefix for the generated Excel spreadsheet name
        :type wb_name: str
        """
        # handle the case when an output filename is not provided
        if not wb_name:
            prefix, _ = os.path.splitext(os.path.basename(yaml_filename))
            prefix_root, prefix_ext = os.path.splitext(prefix)

            if prefix_ext == ".yaml":
                prefix = prefix_root

            output_xlsx = (
                f"{prefix}_{self.generator_name}_{self.generator_version}.xlsx"
            )

            return output_xlsx

        return wb_name

    def __post_init__(self):
        super().__post_init__()
        self.wb_name = self._workbook_path(yaml_filename=self.schema, wb_name=self.output)
        self.workbook.remove(self.workbook["Sheet"])

    def _create_spreadsheet(self, ws_name: str, columns: List[str]) -> None:
        """Method to add worksheets to the Excel workbook.

        :param ws_name: Name of each of the worksheets
        :type ws_name: str
        :param columns: Columns that are relevant to each of the worksheets
        :type columns: List[str]
        """
        ws = self.workbook.create_sheet(ws_name)
        self.workbook.active = ws
        ws.append(columns)
        self.workbook.save(self.wb_name)

    def visit_class(self, cls: ClassDefinition) -> bool:
        """Overridden method to intercept classes from generator framework."""
        self._create_spreadsheet(ws_name=camelcase(cls.name), columns=cls.slots)

        return True

    def visit_enum(self, enum: EnumDefinition) -> bool:
        """Overridden method to intercept enums from generator framework."""

        def extract_permissible_text(pv):
            if type(pv) is str:
                return pv
            if type(pv) is PermissibleValue:
                return pv.text.code
            if type(pv) is PermissibleValueText:
                return pv
            raise ValueError(f"Invalid permissible value in enum {enum}: {pv}")

        permissible_values_texts = list(
            map(extract_permissible_text, enum.permissible_values or [])
        )

        self.enum_dict[enum.name] = permissible_values_texts

    def visit_class_slot(
        self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition
    ) -> None:
        """Overridden method to intercept classes and associated slots from generator
        framework."""
        self.workbook = load_workbook(self.wb_name)

        if cls.name in self.workbook.sheetnames:
            if slot.range in self.enum_dict:

                valid = ",".join(self.enum_dict[slot.range])
                valid = '"' + valid + '"'

                ws = self.workbook[cls.name]

                rows = ws.iter_rows(min_row=1, max_row=1)  # returns a generator of rows
                first_row = next(rows)  # get the first row
                headings = [
                    c.value for c in first_row
                ]  # extract the values from the cells

                idx = headings.index(slot.name)
                col_letter = get_column_letter(idx + 1)

                dv = DataValidation(type="list", formula1=valid, allow_blank=True)
                ws.add_data_validation(dv)

                dv.add(f"{col_letter}2:{col_letter}1048576")

                self.workbook.save(self.wb_name)


@shared_arguments(ExcelGenerator)
@click.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="""Name of Excel spreadsheet to be created""",
)
def cli(yamlfile, **kwargs):
    """Generate Excel representation of a LinkML model"""
    print(ExcelGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
