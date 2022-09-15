import os
from dataclasses import dataclass, field
from typing import TextIO, Union

import click
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              SchemaDefinition, SlotDefinition)
from linkml_runtime.utils.formatutils import camelcase, lcamelcase

from linkml.utils.generator import Generator, shared_arguments


@dataclass
class ProtoGenerator(Generator):
    """
    A `Generator` for creating Protobuf schemas from a linkml schema.

    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["proto"]
    visit_all_class_slots = True
    uses_schemaloader = True

    # ObjectVars
    relative_slot_num: int = field(default_factory=lambda: 0)

    def __post_init__(self):
        super().__post_init__()
        self.generate_header()

    def generate_header(self):
        print(f' syntax="proto3";')
        print(f" package")
        print(f"// metamodel_version: {self.schema.metamodel_version}")
        if self.schema.version:
            print(f"// version: {self.schema.version}")

    def visit_class(self, cls: ClassDefinition) -> bool:
        if cls.mixin or cls.abstract or not cls.slots:
            return False
        if cls.description:
            for dline in cls.description.split("\n"):
                print(f"// {dline}")
        print(f"message {camelcase(cls.name)}")
        print(" {")
        self.relative_slot_num = 0
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        print(" }")

    def visit_class_slot(
        self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition
    ) -> None:
        qual = "repeated " if slot.multivalued else ""
        slotname = lcamelcase(aliased_slot_name)
        slot_range = camelcase(slot.range)
        if slot.rank is None:
            # numbering of slots is important in the proto implementation
            # and should be determined by the rank param.
            slot.rank = 0
        print(f" {qual} {lcamelcase(slot_range)} {(slotname)} = {slot.rank}")


@shared_arguments(ProtoGenerator)
@click.command()
def cli(yamlfile, **args):
    """Generate proto representation of LinkML model"""
    print(ProtoGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
