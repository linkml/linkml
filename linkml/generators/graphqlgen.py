import logging
import os
import re
from dataclasses import dataclass

import click
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, lcamelcase

from linkml._version import __version__
from linkml.generators.common.naming import NameCompatibility, NamingProfiles
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

    strict_naming: bool = False
    _permissible_value_valid_characters = re.compile("^[_A-Za-z][_0-9A-Za-z]*?$")

    def __post_init__(self):
        self.name_compatiblity = NameCompatibility(profile=NamingProfiles.graphql, do_not_fix=self.strict_naming)
        super().__post_init__()

    def visit_schema(self, **kwargs) -> str:
        return self.generate_header()

    def generate_header(self) -> str:
        out = f"# metamodel_version: {self.schema.metamodel_version}\n"
        if self.schema.version:
            out += f"# version: {self.schema.version}\n"
        return out

    def visit_class(self, cls: ClassDefinition) -> str:
        etype = "interface" if (cls.abstract or cls.mixin) and not cls.mixins else "type"
        mixins = ", ".join([camelcase(mixin) for mixin in cls.mixins])
        out = f"{etype} {camelcase(cls.name)}" + (f" implements {mixins}" if mixins else "")
        out = "\n".join([out, "  {"])
        return out

    def end_class(self, cls: ClassDefinition) -> str:
        return "\n  }\n\n"

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> str:
        slotrange = (
            camelcase(slot.range)
            if slot.range in self.schema.classes or slot.range in self.schema.types or slot.range in self.schema.enums
            else "String"
        )
        if slot.multivalued:
            slotrange = f"[{slotrange}]"
        if slot.required:
            slotrange = slotrange + "!"
        return f"\n    {lcamelcase(aliased_slot_name)}: {slotrange}"

    def visit_enum(self, enum: EnumDefinition):
        if enum.permissible_values:
            permissible_values = []
            for value in enum.permissible_values:
                permissible_values.append(self.name_compatiblity.compatible(value))
            values = "\n    ".join(permissible_values)
            return f"enum {camelcase(enum.name).replace(' ','')}\n  {{\n    {values}\n  }}\n\n"
        else:
            logging.warning(
                f"Enumeration {enum.name} using `reachable_from` instead of `permissible_values` "
                + "to specify permissible values is not supported yet."
                + "Enumeration {enum.name} will be silently ignored!!"
            )
            return ""


@shared_arguments(GraphqlGenerator)
@click.command(name="graphql")
@click.option(
    "--strict-naming",
    is_flag=True,
    show_default=True,
    help="Treat warnings about invalid names or schema elements as errors.",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate graphql representation of a LinkML model"""
    generator = GraphqlGenerator(yamlfile, **args)
    print(generator.serialize(**args))


if __name__ == "__main__":
    cli()
