import os
from typing import Union, TextIO, Optional, List, Dict, Tuple

import click
import openpyxl

from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import (
    SchemaDefinition,
    ClassDefinition,
    SlotDefinition,
)
from linkml_runtime.utils.formatutils import camelcase


class ExcelGenerator(Generator):
    generator_name = os.path.basename(__file__)
    generator_version = "0.0.1"
    valid_formats = ["xlsx"]
    sheet_name_cols = []

    def _workbook_path(self, wb_name: str = None):
        if not wb_name:
            return os.path.join(
                os.path.basename(self.generator_name),
                "_",
                self.generator_version,
                ".xlsx",
            )

        return os.path.join(
            os.path.basename(self.generator_name),
            "_",
            self.generator_version,
            "_",
            ".xlsx",
        )

    @staticmethod
    def _slot_formatting(slots_list: List[Tuple[str, str]]) -> Dict[str, List[str]]:
        formatted_slots_dict: Dict = {}

        for slot_owner, slot_name in slots_list:
            formatted_slots_dict.setdefault(camelcase(slot_owner), []).append(slot_name)

        return formatted_slots_dict

    def _write_to_excel(self, slots_dict: Dict[str, List[str]]) -> None:
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
        self.workbook.create_sheet(ws_name)
        self.workbook.save(self.wb_name)

    def visit_class(self, cls: ClassDefinition) -> None:
        self.create_spreadsheet(ws_name=camelcase(cls.name))

        slots = ExcelGenerator._slot_formatting(slots_list=self.sheet_name_cols)

        self._write_to_excel(slots_dict=slots)

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        self.sheet_name_cols.append((slot.owner, slot.name))


@shared_arguments(ExcelGenerator)
@click.command()
@click.option("-f", "--filename", help="""Name of Excel spreadsheet to be created""")
def cli(yamlfile, **kwargs):
    """Generate Excel representation of a LinkML model"""
    print(ExcelGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
