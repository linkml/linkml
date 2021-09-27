import os
from typing import Union, TextIO, Optional, List

import click
import openpyxl

from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition
from linkml_runtime.utils.formatutils import camelcase


class ExcelGenerator(Generator):
    """This class is a blueprint for the generator module that is responsible
    for automatically creating Excel spreadsheets from the LinkML schema.

    :param schema: LinkML schema object
    :type schema: class:`SchemaDefinition`
    :param output: LinkML schema specification in YAML format
    :type output: str
    """

    generator_name = os.path.splitext(os.path.basename(__file__))[0]
    generator_version = "0.0.1"
    valid_formats = ["xlsx"]
    sheet_name_cols = []

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

    def __init__(
        self,
        schema: Union[str, TextIO, SchemaDefinition],
        output: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.wb_name = self._workbook_path(yaml_filename=schema, wb_name=output)
        self.workbook = openpyxl.Workbook()
        self.workbook.remove(self.workbook["Sheet"])
        super().__init__(schema, **kwargs)

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
        """Overridden from generator framework."""
        self._create_spreadsheet(ws_name=camelcase(cls.name), columns=cls.slots)

        return True


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
