"""Generate Summary Spreadsheets"""

import os
from csv import DictWriter
from dataclasses import dataclass
from io import StringIO

import click

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore


@dataclass
class SummaryGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["tsv"]
    uses_schemaloader = False

    dirname: str = None
    classtab: DictWriter | None = None
    slottab: DictWriter | None = None
    dialect: str = "excel-tab"

    _str_io: StringIO | None = None

    def serialize(self, **kwargs) -> str:
        self._str_io = StringIO()
        self.classtab = DictWriter(
            self._str_io,
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
        for cls in sorted(self.schemaview.all_classes().values(), key=lambda c: c.name.lower()):
            self._add_class(cls)
        return self._str_io.getvalue().rstrip() + "\n"

    def _add_class(self, cls: ClassDefinition) -> None:
        self.classtab.writerow(
            {
                "Class Name": camelcase(cls.name),
                "Parent Class": camelcase(cls.is_a) if cls.is_a else "",
                "YAML Class Name": cls.name,
                "Description": cls.description,
            }
        )
        # own slots: not inherited from the is_a parent, unless redefined via slot_usage
        parent_slot_names = set(self.schemaview.class_slots(cls.is_a)) if cls.is_a else set()
        for slot in self.induced_slots_legacy_order(cls.name):
            if slot.name not in parent_slot_names or slot.name in cls.slot_usage:
                self._add_class_slot(slot)

    def _range_name(self, name: str) -> str:
        """camelcase name for a class/enum/non-base type range, base for base types."""
        sv = self.schemaview
        if name in sv.all_enums() or name in sv.all_classes():
            return camelcase(name)
        if name in sv.all_types():
            typ = sv.all_types()[name]
            return camelcase(name) if typ.typeof else typ.base
        return "Unknown_" + camelcase(name)

    def _add_class_slot(self, slot: SlotDefinition) -> None:
        # induced slots derive an underscored alias; the summary shows only
        # user-declared aliases, so treat the derived form as no alias
        aliased_slot_name = slot.alias if slot.alias and slot.alias != underscore(slot.name) else slot.name
        min_card = 1 if slot.required else 0
        max_card = "*" if slot.multivalued else 1
        abstract = "A" if slot.abstract or slot.mixin else ""
        key = "K" if slot.key else ""
        identifier = "I" if slot.identifier else ""
        readonly = "R" if slot.readonly else ""
        ref = "*" if slot.range in self.schemaview.all_classes() and not self.schemaview.is_inlined(slot) else ""
        range_name = self._range_name(slot.range)
        slot_uri = slot.slot_uri if slot.slot_uri else self.schemaview.get_uri(slot)
        self.classtab.writerow(
            {
                "Slot Name": aliased_slot_name,
                "Flags": abstract + key + identifier + readonly,
                "Card": f"{min_card}..{max_card}",
                "YAML Slot Name": slot.name if slot.name != aliased_slot_name else "",
                "Range": ref + range_name,
                "Slot Description": slot.description,
                "URI": slot_uri,
            }
        )


@shared_arguments(SummaryGenerator)
@click.version_option(__version__, "-V", "--version")
@click.command(name="summary")
def cli(yamlfile, **args):
    """Generate TSV summary files for viewing in Excel and the like"""
    print(SummaryGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
