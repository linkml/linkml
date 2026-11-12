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

#: The schema that holds the LinkML built-in types, the ones that map onto GraphQL's scalars.
LINKML_TYPES_SCHEMA = "https://w3id.org/linkml/types"

#: The scalars every GraphQL service defines (GraphQL spec, October 2021, section 3.5).
GRAPHQL_BUILTIN_SCALARS = ("Int", "Float", "String", "Boolean", "ID")

#: An object type and an interface each have to define at least one field (GraphQL spec,
#: October 2021, sections 3.6 and 3.7), while a LinkML class may resolve to no slot. Such a
#: class carries this field instead. It is emitted only for a class that contributes no
#: field of its own, or that implements an interface in that position, so it never collides
#: with a field generated from a slot.
PLACEHOLDER_FIELD_NAME = "_placeholder"


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
        self._reset_visit_state()
        super().__post_init__()

    def _reset_visit_state(self) -> None:
        """Clear the names the visitor collects, so that a run never sees those of another.

        Kept on the class, a name outlived the generator that recorded it: the next schema
        holding a class of that name was then closed as if it were a scalar, leaving the
        document a brace short.
        """
        self._types_any: list[str] = []
        self._custom_scalars: set[str] = set()
        self._declared_names: set[str] = set()

    def visit_schema(self, **kwargs) -> str:
        self._reset_visit_state()
        return self.generate_header()

    def generate_header(self) -> str:
        out = f"# metamodel_version: {self.schema.metamodel_version}\n"
        if self.schema.version:
            out += f"# version: {self.schema.version}\n"
        return out

    def end_schema(self, **kwargs) -> str:
        """Declare the types the schema brings itself, which GraphQL carries as custom scalars.

        ``visit_class_slot`` names such a type as the type of a field, and a document has
        to define every type it names; a custom scalar is how GraphQL carries a type that
        it has no built-in for (GraphQL spec, October 2021, section 3.5, Custom Scalars).

        A name the document already carries is left out. Every type of a GraphQL schema
        shares one namespace, in which a name is unique (GraphQL spec, October 2021,
        section 3.3), while LinkML holds its types, classes and enumerations apart and
        lets one name stand in several of them. A built-in scalar is left out as well,
        since every service defines it already (GraphQL spec, October 2021, section 3.5).
        """
        for name in sorted(self._custom_scalars & self._declared_names):
            logging.warning(
                f"The name {name} is already declared by a class or an enumeration of the "
                "schema, so the type of that name is not declared as a scalar. A field "
                "naming it resolves to the class or the enumeration instead."
            )
        declared = self._declared_names.union(GRAPHQL_BUILTIN_SCALARS)
        return "".join(f"scalar {name}\n\n" for name in sorted(self._custom_scalars - declared))

    def implemented_interfaces(self, cls: ClassDefinition) -> list[str]:
        """Return the mixins of a class, including the ones its mixins carry themselves.

        An object type or an interface declares every interface that the interfaces it
        implements declare in turn (GraphQL spec, October 2021, sections 3.6 and 3.7), so
        the direct mixins alone leave out a mixin that is mixed into a mixin.
        """
        interfaces: list[str] = []

        def collect(mixins: list[str]) -> None:
            for mixin in mixins:
                if mixin not in interfaces:
                    interfaces.append(mixin)
                    collect(self.schema.classes[mixin].mixins)

        collect(cls.mixins)
        return interfaces

    def visit_class(self, cls: ClassDefinition) -> str:
        # no type can be declared for subtypes of "Any"
        if cls.class_uri == "linkml:Any":
            self._types_any.append(cls.name)
            self._declared_names.add(camelcase(cls.name))
            return f"scalar {camelcase(cls.name)}"
        self._declared_names.add(camelcase(cls.name))
        # A class that cannot be instantiated is an interface, including when it is mixed
        # into another one: an interface may implement an interface (GraphQL spec, October
        # 2021, section 3.7), and a type implementing it needs it to be one.
        etype = "interface" if cls.abstract or cls.mixin else "type"
        # "implements A & B": the interfaces are separated by "&", a comma does not parse
        # (GraphQL spec, October 2021, section 3.6, ImplementsInterfaces).
        mixins = " & ".join([camelcase(mixin) for mixin in self.implemented_interfaces(cls)])
        out = f"{etype} {camelcase(cls.name)}" + (f" implements {mixins}" if mixins else "")
        out = "\n".join([out, "  {"])
        return out

    def placeholder_field(self, cls: ClassDefinition) -> str:
        """Return the placeholder field a class needs to be well formed, else the empty string.

        A class resolving to no slot would close its body without a field. A class
        implementing an interface in that position carries the field as well, because an
        object type or interface repeats every field of the interfaces it implements
        (GraphQL spec, October 2021, sections 3.6 and 3.7).
        """
        interfaces = (self.all_slots(mixin) for mixin in self.implemented_interfaces(cls))
        needs_placeholder = not self.all_slots(cls) or not all(interfaces)
        return f"\n    {PLACEHOLDER_FIELD_NAME}: Boolean" if needs_placeholder else ""

    def end_class(self, cls: ClassDefinition) -> str:
        if cls.name in self._types_any:
            return "\n\n"
        else:
            return f"{self.placeholder_field(cls)}\n  }}\n\n"

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> str:
        if slot.range in self.schema.classes or slot.range in self.schema.slots or slot.range in self.schema.enums:
            slotrange = camelcase(slot.range)
        elif slot.range in self.schema.types:
            if self.schema.types[slot.range].from_schema != LINKML_TYPES_SCHEMA:
                slotrange = camelcase(slot.range)
                # A type the schema brings itself has no built-in to map onto, so the
                # document has to declare it; ``end_schema`` does, where the names the
                # document already carries are known.
                self._custom_scalars.add(slotrange)
            else:
                if slot.range == "integer":
                    slotrange = "Int"
                elif slot.range == "decimal":
                    slotrange = "Float"
                elif camelcase(slot.range) in GRAPHQL_BUILTIN_SCALARS:
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

    def enum_name(self, enum: EnumDefinition) -> str:
        """Return the name under which an enumeration is carried in the document."""
        return camelcase(enum.name).replace(" ", "")

    def visit_enum(self, enum: EnumDefinition) -> str:
        name = self.enum_name(enum)
        if enum.permissible_values:
            permissible_values = []
            for value in enum.permissible_values:
                permissible_values.append(self.name_compatiblity.compatible(value))
            values = "\n    ".join(permissible_values)
            self._declared_names.add(name)
            return f"enum {name}\n  {{\n    {values}\n  }}\n\n"
        else:
            # An enum type defines one or more values (GraphQL spec, October 2021, section
            # 3.9), so an enumeration whose values are not known at generation time cannot
            # be one. It is carried as a custom scalar instead, which leaves the fields
            # naming it defined rather than pointing at a type the document never declares.
            logging.warning(
                f"Enumeration {enum.name} using `reachable_from` instead of `permissible_values` "
                "to specify permissible values is not supported yet. "
                f"Enumeration {enum.name} is generated as the custom scalar {name} instead."
            )
            self._custom_scalars.add(name)
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
