import os
from typing import Union, TextIO, Optional, List, Dict, Tuple

import click
import openpyxl

from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.helpers import remove_duplicates
from linkml_runtime.linkml_model.meta import (
    SchemaDefinition,
    ClassDefinition,
    SlotDefinition,
)
from linkml_runtime.utils.formatutils import camelcase


class ExcelGenerator(Generator):
    """This class is a blueprint for the generator module that is responsible
    for automatically creating Excel spreadsheets from the LinkML schema.

    :param schema: LinkML schema object
    :type schema: class:`SchemaDefinition`
    :param filename: LinkML schema specification in YAML format
    :type filename: str
    """

    generator_name = os.path.basename(__file__)
    generator_version = "0.0.1"
    valid_formats = ["xlsx"]
    sheet_name_cols = []

    def _workbook_path(self, wb_name: str = None):
        """Internal method that computes the path where the Excel workbook
        should be stored.

        :param wb_name: Prefix for the generated Excel spreadsheet name
        :type wb_name: str

        TODO: Decide whether to use :param wb_name as prefix or full file name?
        """
        if not wb_name:
            return os.path.normpath(
                os.path.join(
                    self.generator_name,
                    "_",
                    self.generator_version,
                    ".xlsx",
                )
            )

        return os.path.normpath(
            os.path.join(
                wb_name,
                "_",
                self.generator_name,
                "_",
                self.generator_version,
                "_",
                ".xlsx",
            )
        )

    @staticmethod
    def _slot_formatting(slots_list: List[Tuple[str, str]]) -> Dict[str, List[str]]:
        """Static internal method for formatting the slot information read in visit_slot()
        in a parseable format.

        :param slots_list: List of tuples with each tuple containing information in the
            ``(slot_owner, slot_name)`` format
        :type slots_list: List[Tuple[str, str]]
        :return: A dictionary with the same information, with ``slot_owner`` as keys, and
            the slot names as associated lists
        :rtype: Dict[str, List[str]]

        TODO: This is basically a utility method, so it can be moved to ``utils``
        """
        formatted_slots_dict: Dict = {}

        slots_list = remove_duplicates(slots_list)

        for slot_owner, slot_name in slots_list:
            formatted_slots_dict.setdefault(camelcase(slot_owner), []).append(slot_name)

        return formatted_slots_dict

    def _write_to_excel(self, slots_dict: Dict[str, List[str]]) -> None:
        """Internal method to write slot names to Excel worksheets.

        :param slots_dict: Formatted dictionary as returned by call to
            ``self._slot_formatting()``
        :type slots_dict: Dict[str, List[str]]
        """
        wb = openpyxl.load_workbook(self.wb_name)

        for slot_owner, slot_name in slots_dict.items():
            if slot_owner in wb.sheetnames:
                wb[slot_owner].append(slot_name)

                wb.save(self.wb_name)

    def __init__(
        self,
        schema: Union[str, TextIO, SchemaDefinition],
        filename: Optional[str] = None,
        **kwargs
    ) -> None:
        self.wb_name = self._workbook_path(wb_name=filename)
        self.workbook = openpyxl.Workbook()
        self.workbook.remove(self.workbook["Sheet"])
        super().__init__(schema, **kwargs)

    def create_spreadsheet(self, ws_name: str = None) -> None:
        """Method to add worksheets to the Excel workbook.

        :param ws_name: Name of each of the worksheets
        :type ws_name: str, optional
        """
        self.workbook.create_sheet(ws_name)
        self.workbook.save(self.wb_name)

    def visit_class(self, cls: ClassDefinition) -> bool:
        """Overridden from generator framework."""
        self.create_spreadsheet(ws_name=camelcase(cls.name))

        slots = ExcelGenerator._slot_formatting(
            slots_list=ExcelGenerator.sheet_name_cols
        )

        self._write_to_excel(slots_dict=slots)

        return True

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        """Overridden from generator framework."""
        for slot_owner in slot.domain_of:
            ExcelGenerator.sheet_name_cols.append((slot_owner, aliased_slot_name))


@shared_arguments(ExcelGenerator)
@click.command()
@click.option("-f", "--filename", help="""Name of Excel spreadsheet to be created""")
def cli(yamlfile, **kwargs):
    """Generate Excel representation of a LinkML model"""
    print(ExcelGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
