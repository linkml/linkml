import os
from dataclasses import dataclass

import click
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, lcamelcase

from linkml._version import __version__
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
        if slot.range in self.schema.classes or slot.range in self.schema.slots or slot.range in self.schema.enums:
            slotrange = camelcase(slot.range)
        elif slot.range in self.schema.types:
            if self.schema.types[slot.range].from_schema != "https://w3id.org/linkml/types":
                slotrange = camelcase(slot.range)
            else:
                graphql_scalars = ["Int", "Float", "String", "Boolean", "ID"]
                if slot.range == "integer":
                    slotrange = "Int"
                elif slot.range == "decimal":
                    slotrange = "Float"
                elif camelcase(slot.range) in graphql_scalars:
                    slotrange = camelcase(slot.range)
                else:
                    if self.schema.types[slot.range].repr:
                        python_type = self.schema.types[slot.range].repr
                    elif self.schema.types[slot.range].base:
                        python_type = self.schema.types[slot.range].base
                    if str(python_type) == "float":
                        slotrange = "Float"
                    elif str(python_type) == "str":
                        slotrange = "String"

        if slot.multivalued:
            slotrange = f"[{slotrange}]"
        if slot.required:
            slotrange = slotrange + "!"
        return f"\n    {lcamelcase(aliased_slot_name)}: {slotrange}"

    def visit_enum(self, enum: EnumDefinition):
        out = f"enum {enum.name}\n  {{"
        for permissible_value in enum.permissible_values:
            out = "\n    ".join([out, permissible_value])
        out = "\n".join([out, "  }\n\n"])
        return out


@shared_arguments(GraphqlGenerator)
@click.command(name="graphql")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate graphql representation of a LinkML model"""
    print(GraphqlGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
