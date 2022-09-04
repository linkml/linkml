import os
from dataclasses import dataclass
from typing import TextIO, Union

import click
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              SchemaDefinition, SlotDefinition)
from linkml_runtime.utils.formatutils import camelcase, lcamelcase

from linkml.utils.generator import Generator, shared_arguments


@dataclass
class GraphqlGenerator(Generator):

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["graphql"]
    visit_all_class_slots = True
    uses_schemaloader = True
    requires_metamodel = False

    def __post_init__(self):
        super().__post_init__()
        # TODO: move this
        self.generate_header()

    def generate_header(self):
        print(f"# metamodel_version: {self.schema.metamodel_version}")
        if self.schema.version:
            print(f"# version: {self.schema.version}")

    def visit_class(self, cls: ClassDefinition) -> bool:
        etype = (
            "interface" if (cls.abstract or cls.mixin) and not cls.mixins else "type"
        )
        mixins = ", ".join([camelcase(mixin) for mixin in cls.mixins])
        print(
            f"{etype} {camelcase(cls.name)}"
            + (f" implements {mixins}" if mixins else "")
        )
        print("  {")
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        print("  }")
        print()

    def visit_class_slot(
        self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition
    ) -> None:
        slotrange = (
            camelcase(slot.range)
            if slot.range in self.schema.classes
            or slot.range in self.schema.types
            or slot.range in self.schema.enums
            else "String"
        )
        if slot.multivalued:
            slotrange = f"[{slotrange}]"
        if slot.required:
            slotrange = slotrange + "!"
        print(f"    {lcamelcase(aliased_slot_name)}: {slotrange}")


@shared_arguments(GraphqlGenerator)
@click.command()
def cli(yamlfile, **args):
    """Generate graphql representation of a LinkML model"""
    print(GraphqlGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
