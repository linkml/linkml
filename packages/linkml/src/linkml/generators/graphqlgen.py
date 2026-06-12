import logging
import os
import re
from dataclasses import dataclass

import click

from linkml._version import __version__
from linkml.generators.common.naming import NameCompatibility, NamingProfiles
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, lcamelcase


@dataclass
class GraphqlGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["graphql"]
    uses_schemaloader = False

    strict_naming: bool = False
    _permissible_value_valid_characters = re.compile("^[_A-Za-z][_0-9A-Za-z]*?$")
    _types_any = []

    def __post_init__(self):
        self.name_compatiblity = NameCompatibility(profile=NamingProfiles.graphql, do_not_fix=self.strict_naming)
        super().__post_init__()

    def serialize(self, **kwargs) -> str:
        out = self.generate_header()
        for enum in sorted(self.schemaview.all_enums().values(), key=lambda e: e.name.lower()):
            out += self.generate_enum(enum)
        for cls in sorted(self.schemaview.all_classes().values(), key=lambda c: c.name.lower()):
            out += self.generate_class(cls)
        return out.rstrip() + "\n"

    def generate_header(self) -> str:
        out = f"# metamodel_version: {self.schema.metamodel_version}\n"
        if self.schema.version:
            out += f"# version: {self.schema.version}\n"
        return out

    def generate_class(self, cls: ClassDefinition) -> str:
        # no type can be declared for subtypes of "Any"
        if cls.class_uri == "linkml:Any":
            self._types_any.append(cls.name)
            return f"scalar {cls.name}\n\n"
        etype = "interface" if (cls.abstract or cls.mixin) and not cls.mixins else "type"
        mixins = ", ".join([camelcase(mixin) for mixin in cls.mixins])
        out = f"{etype} {camelcase(cls.name)}" + (f" implements {mixins}" if mixins else "")
        out = "\n".join([out, "  {"])
        for slot in self.induced_slots_legacy_order(cls.name):
            out += self.generate_class_slot(cls, slot)
        return out + "\n  }\n\n"

    def _is_builtin_type(self, type_name: str) -> bool:
        """True if the type is defined by the standard linkml types schema."""
        type_def = self.schemaview.get_type(type_name)
        if type_def.from_schema:
            return type_def.from_schema == "https://w3id.org/linkml/types"
        defining_schema = self.schemaview.schema_map.get(self.schemaview.in_schema(type_def.name))
        return defining_schema is not None and str(defining_schema.id) == "https://w3id.org/linkml/types"

    def generate_class_slot(self, cls: ClassDefinition, slot: SlotDefinition) -> str:
        sv = self.schemaview
        aliased_slot_name = slot.alias if slot.alias else slot.name
        if slot.range in sv.all_classes() or slot.range in sv.all_slots() or slot.range in sv.all_enums():
            slotrange = camelcase(slot.range)
        elif slot.range in sv.all_types():
            if not self._is_builtin_type(slot.range):
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
                    induced_type = sv.induced_type(slot.range)
                    if induced_type.repr:
                        python_type = induced_type.repr
                    elif induced_type.base:
                        python_type = induced_type.base
                    if str(python_type) == "float":
                        slotrange = "Float"
                    elif str(python_type) == "str":
                        slotrange = "String"
        else:
            # unresolvable or absent range: the loader defaulted to string
            slotrange = "String"

        if slot.multivalued:
            slotrange = f"[{slotrange}]"
        if slot.required:
            slotrange = slotrange + "!"
        return f"\n    {lcamelcase(aliased_slot_name)}: {slotrange}"

    def generate_enum(self, enum: EnumDefinition):
        if enum.permissible_values:
            permissible_values = []
            for value in enum.permissible_values:
                permissible_values.append(self.name_compatiblity.compatible(value))
            values = "\n    ".join(permissible_values)
            return f"enum {camelcase(enum.name).replace(' ', '')}\n  {{\n    {values}\n  }}\n\n"
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
