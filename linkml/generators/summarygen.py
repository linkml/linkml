"""Generate Summary Spreadsheets

"""
import os
import sys
from csv import DictWriter
from dataclasses import dataclass, field
from typing import Optional, TextIO, Union

import click
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              SchemaDefinition, SlotDefinition)
from linkml_runtime.utils.formatutils import camelcase

from linkml.utils.generator import Generator, shared_arguments


@dataclass
class SummaryGenerator(Generator):

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["tsv"]

    dirname: str = None
    classtab: Optional[DictWriter] = None
    slottab: Optional[DictWriter] = None
    dialect: str = field(default_factory=lambda: "excel-tab")

    def visit_schema(self, **_) -> None:
        self.classtab = DictWriter(
            sys.stdout,
            [
                "Class Name",
                "Parent Class",
                "YAML Class Name",
                "Description",
                "Flags",
                "Slot Name",
                "YAML Slot Name",
                "Range",
                "Card",
                "Slot Description",
                "URI",
            ],
            dialect=self.dialect,
        )
        self.classtab.writeheader()

    def visit_class(self, cls: ClassDefinition) -> bool:
        self.classtab.writerow(
            {
                "Class Name": camelcase(cls.name),
                "Parent Class": camelcase(cls.is_a) if cls.is_a else "",
                "YAML Class Name": cls.name,
                "Description": cls.description,
            }
        )
        return True

    def visit_class_slot(
        self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition
    ) -> None:
        min_card = 1 if slot.required else 0
        max_card = "*" if slot.multivalued else 1
        abstract = "A" if slot.abstract or slot.mixin else ""
        key = "K" if slot.key else ""
        identifier = "I" if slot.identifier else ""
        readonly = "R" if slot.readonly else ""
        ref = "*" if slot.range in self.schema.classes and not slot.inlined else ""
        self.classtab.writerow(
            {
                "Slot Name": aliased_slot_name,
                "Flags": abstract + key + identifier + readonly,
                "Card": f"{min_card}..{max_card}",
                "YAML Slot Name": slot.name if slot.name != aliased_slot_name else "",
                "Range": ref + self.class_or_type_name(slot.range),
                "Slot Description": slot.description,
                "URI": slot.slot_uri,
            }
        )


@shared_arguments(SummaryGenerator)
@click.command()
def cli(yamlfile, **args):
    """Generate TSV summary files for viewing in Excel and the like"""
    print(SummaryGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
