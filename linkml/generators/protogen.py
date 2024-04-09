import os
from dataclasses import dataclass
from typing import Optional

import click
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, lcamelcase

from linkml._version import __version__
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
    relative_slot_num: int = 0

    def visit_schema(self, **kwargs) -> Optional[str]:
        return self.generate_header()

    def generate_header(self) -> str:
        items = []
        items.append(' syntax="proto3";')
        items.append(" package")
        items.append(f"// metamodel_version: {self.schema.metamodel_version}")
        if self.schema.version:
            items.append(f"// version: {self.schema.version}")
        out = "\n".join(items) + "\n"
        return out

    def visit_class(self, cls: ClassDefinition) -> Optional[str]:
        if cls.mixin or cls.abstract or not cls.slots:
            return None
        items = []
        if cls.description:
            for dline in cls.description.split("\n"):
                items.append(f"// {dline}")
        items.append(f"message {camelcase(cls.name)}")
        items.append(" {")
        out = "\n".join(items)
        self.relative_slot_num = 0
        return out

    def end_class(self, cls: ClassDefinition) -> str:
        return "\n }\n"

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> str:
        qual = "repeated " if slot.multivalued else ""
        slotname = lcamelcase(aliased_slot_name)
        slot_range = camelcase(slot.range)
        if slot.rank is None:
            # numbering of slots is important in the proto implementation
            # and should be determined by the rank param.
            slot.rank = 0
        return f"\n {qual} {lcamelcase(slot_range)} {(slotname)} = {slot.rank}"


@shared_arguments(ProtoGenerator)
@click.version_option(__version__, "-V", "--version")
@click.command()
def cli(yamlfile, **args):
    """Generate proto representation of LinkML model"""
    print(ProtoGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
