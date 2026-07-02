"""
C++ header generator for LinkML schemas.

Generates idiomatic C++17 header files from LinkML class definitions.
Based on the GolangGenerator architecture.
"""

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import click
from jinja2 import ChoiceLoader, Environment, FileSystemLoader

from linkml._version import __version__
from linkml.generators.cppgen.build import FieldResult, StructResult
from linkml.generators.cppgen.template import (
    CppEnum,
    CppEnumValue,
    CppField,
    CppInclude,
    CppModule,
    CppStruct,
    Includes,
)
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)

# Type mapping from LinkML base types to C++ types
TYPE_MAP: dict[str, str] = {
    "str": "std::string",
    "string": "std::string",
    "int": "int32_t",
    "integer": "int32_t",
    "Bool": "bool",
    "boolean": "bool",
    "Decimal": "double",
    "decimal": "double",
    "float": "float",
    "double": "double",
    "XSDDate": "std::string",
    "XSDDateTime": "std::string",
    "date": "std::string",
    "datetime": "std::string",
    "time": "std::string",
    "uri": "std::string",
    "uriorcurie": "std::string",
    "ncname": "std::string",
}

# Headers required by each C++ type
TYPE_INCLUDES: dict[str, str] = {
    "std::string": "string",
    "std::optional": "optional",
    "std::vector": "vector",
    "int32_t": "cstdint",
    "int64_t": "cstdint",
    "uint32_t": "cstdint",
    "uint64_t": "cstdint",
}

# Default values for C++ types
TYPE_DEFAULTS: dict[str, str] = {
    "std::string": '""',
    "int32_t": "0",
    "int64_t": "0",
    "uint32_t": "0",
    "uint64_t": "0",
    "float": "0.0f",
    "double": "0.0",
    "bool": "false",
}


def _to_upper_snake(name: str) -> str:
    """Convert a name to UPPER_SNAKE_CASE.

    Examples:

        >>> _to_upper_snake("MaterialType")
        'MATERIAL_TYPE'
        >>> _to_upper_snake("RED")
        'RED'
        >>> _to_upper_snake("wood_soft")
        'WOOD_SOFT'
    """
    # Insert underscore before uppercase letters preceded by lowercase
    result = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    # Insert underscore between consecutive uppercase followed by lowercase
    result = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", result)
    return result.upper()


@dataclass
class CppGenerator(OOCodeGenerator):
    """Generates C++17 header files from a LinkML schema.

    This generator creates idiomatic C++ headers with:
    - ``enum class`` definitions from enums with ``to_string``/``from_string`` helpers
    - ``struct`` definitions from classes with public inheritance
    - ``std::optional<T>`` for optional fields, ``std::vector<T>`` for multivalued
    - Namespace wrapping derived from schema name
    - ``#pragma once`` include guards
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["h", "hpp", "header"]
    file_extension = "h"

    # ObjectVars
    namespace: str | None = None
    """Override the C++ namespace. If None, derived from schema name."""

    gen_slots: bool = True
    """Generate struct fields."""

    alphabetical_sort: bool = False
    """Sort structs and enums alphabetically for deterministic output."""

    use_optional: bool = True
    """Use ``std::optional<T>`` for optional non-multivalued fields."""

    gen_string_conversions: bool = True
    """Generate ``to_string``/``from_string`` functions for enums."""

    template_dir: str | Path | None = None
    """Override templates directory."""

    # Private attributes
    _needed_includes: set[str] = field(default_factory=set, init=False)
    _type_defs: dict[str, tuple[str, str | None]] = field(default_factory=dict, init=False)

    def __post_init__(self):
        super().__post_init__()

    def default_value_for_type(self, typ: str) -> str:
        """Return the C++ default value for a given type.

        Args:
            typ: The C++ type string.

        Returns:
            The default value literal for that type.
        """
        return TYPE_DEFAULTS.get(typ, "{}")

    @staticmethod
    def sort_classes(clist: list[ClassDefinition]) -> list[ClassDefinition]:
        """Sort classes so that parents appear before children.

        Args:
            clist: Unsorted class definitions.

        Returns:
            Topologically sorted list.
        """
        clist = list(clist)
        slist: list[ClassDefinition] = []
        while len(clist) > 0:
            can_add = False
            for i in range(len(clist)):
                candidate = clist[i]
                parents = []
                if candidate.is_a:
                    parents.append(candidate.is_a)
                if candidate.mixins:
                    parents.extend(candidate.mixins)

                if not parents or set(parents) <= {p.name for p in slist}:
                    can_add = True
                    slist.append(candidate)
                    del clist[i]
                    break
            if not can_add:
                raise ValueError(
                    f"Could not topologically sort classes: {[c.name for c in clist]} "
                    f"not resolvable given {[s.name for s in slist]}"
                )
        return slist

    def _track_include(self, cpp_type: str) -> None:
        """Track which system headers are needed for a C++ type."""
        for type_prefix, header in TYPE_INCLUDES.items():
            if type_prefix in cpp_type:
                self._needed_includes.add(header)

    def generate_cpp_type(self, slot: SlotDefinition, cls: ClassDefinition) -> str:
        """Generate the C++ type expression for a slot.

        Args:
            slot: The slot definition.
            cls: The parent class definition.

        Returns:
            The C++ type string (e.g. ``std::string``, ``std::optional<int32_t>``,
            ``std::vector<Person>``).
        """
        sv = self.schemaview
        slot_range = slot.range

        # Determine base type
        if slot_range in sv.all_classes():
            base_type = camelcase(slot_range)
        elif slot_range in sv.all_enums():
            base_type = camelcase(slot_range)
        elif slot_range in sv.all_types():
            t = sv.get_type(slot_range)
            if t.base and t.base in TYPE_MAP:
                base_type = TYPE_MAP[t.base]
            else:
                logger.warning("Unknown type base: %s, defaulting to std::string", t.name)
                base_type = "std::string"
        else:
            base_type = "std::string"

        self._track_include(base_type)

        # Handle multivalued slots
        if slot.multivalued:
            result = f"std::vector<{base_type}>"
            self._track_include(result)
            return result

        # Handle optional fields
        is_required = slot.required or slot.identifier or slot.key
        if not is_required and self.use_optional:
            result = f"std::optional<{base_type}>"
            self._track_include(result)
            return result

        return base_type

    def generate_field(self, slot: SlotDefinition, cls: ClassDefinition) -> FieldResult:
        """Generate a C++ struct field from a LinkML slot definition.

        Args:
            slot: The slot definition to convert.
            cls: The parent class definition.

        Returns:
            FieldResult containing the generated field.
        """
        slot_alias = slot.alias if slot.alias else slot.name
        field_name = underscore(slot_alias)
        cpp_type = self.generate_cpp_type(slot, cls)

        # Determine default value
        default_value = None
        if slot.multivalued:
            default_value = "{}"
        elif not (slot.required or slot.identifier or slot.key) and self.use_optional:
            default_value = "std::nullopt"
        elif slot.ifabsent:
            default_value = self._parse_ifabsent(slot.ifabsent)

        cpp_field = CppField(
            name=field_name,
            cpp_type=cpp_type,
            required=slot.required or False,
            identifier=slot.identifier or False,
            multivalued=slot.multivalued or False,
            description=slot.description if slot.description else None,
            default_value=default_value,
            pattern=slot.pattern if slot.pattern else None,
            minimum_value=float(slot.minimum_value) if slot.minimum_value is not None else None,
            maximum_value=float(slot.maximum_value) if slot.maximum_value is not None else None,
        )

        return FieldResult(field=cpp_field, source=slot)

    def _parse_ifabsent(self, ifabsent: str) -> str | None:
        """Parse a LinkML ``ifabsent`` expression into a C++ default value.

        Args:
            ifabsent: The ifabsent expression (e.g. ``string(unknown)``).

        Returns:
            C++ literal string or None.
        """
        if ifabsent.startswith("string(") and ifabsent.endswith(")"):
            value = ifabsent[7:-1]
            return f'"{value}"'
        elif ifabsent.startswith("int(") and ifabsent.endswith(")"):
            return ifabsent[4:-1]
        elif ifabsent.startswith("float(") and ifabsent.endswith(")"):
            value = ifabsent[6:-1]
            return f"{value}f"
        elif ifabsent == "true":
            return "true"
        elif ifabsent == "false":
            return "false"
        return None

    def generate_struct(self, cls: ClassDefinition) -> StructResult:
        """Generate a C++ struct from a LinkML class definition.

        Args:
            cls: The class definition to convert.

        Returns:
            StructResult containing the generated struct.
        """
        struct_name = camelcase(cls.name)

        # Handle inheritance
        base_classes = []
        if cls.is_a:
            base_classes.append(camelcase(cls.is_a))
        if cls.mixins:
            base_classes.extend(camelcase(m) for m in cls.mixins)

        cpp_struct = CppStruct(
            name=struct_name,
            description=cls.description if cls.description else None,
            base_classes=base_classes if base_classes else None,
            is_abstract=cls.abstract or False,
        )

        result = StructResult(struct=cpp_struct, source=cls)

        # Generate fields — only direct slots (inherited come via base class)
        if self.gen_slots:
            direct = bool(base_classes)
            slots = [
                self.schemaview.induced_slot(sn, cls.name)
                for sn in self.schemaview.class_slots(cls.name, direct=direct)
            ]

            field_results = []
            for slot in slots:
                field_result = self.generate_field(slot, cls)
                field_results.append(field_result)
                result = result.merge(field_result)

            fields = {fr.field.name: fr.field for fr in field_results}
            result.struct.fields = fields if fields else None

        return result

    def generate_enum(self, enum: EnumDefinition) -> CppEnum:
        """Generate a C++ ``enum class`` from a LinkML enum definition.

        Args:
            enum: The enum definition to convert.

        Returns:
            CppEnum model.
        """
        enum_name = camelcase(enum.name)
        values: dict[str, CppEnumValue] = {}

        if enum.permissible_values:
            for pv_name, pv in enum.permissible_values.items():
                const_name = _to_upper_snake(pv_name)
                const_value = pv.text if pv.text else pv_name

                values[pv_name] = CppEnumValue(
                    name=const_name,
                    value=const_value,
                    description=pv.description if pv.description else None,
                )

        return CppEnum(
            name=enum_name,
            description=enum.description if enum.description else None,
            values=values,
        )

    def render(self) -> CppModule:
        """Render the schema to a CppModule model.

        Returns:
            CppModule containing all generated enums and structs.
        """
        sv: SchemaView = self.schemaview
        self._type_defs = {}
        self._needed_includes = set()

        # Determine namespace
        namespace = self.namespace
        if namespace is None:
            schema_name = sv.schema.name
            namespace = re.sub(r"[^a-z0-9_]", "_", schema_name.lower())

        # Generate enums
        enums: dict[str, CppEnum] = {}
        for enum_def in sv.all_enums().values():
            enum_model = self.generate_enum(enum_def)
            enums[enum_model.name] = enum_model

        # If we have enums with string conversions, we need cstring
        if enums and self.gen_string_conversions:
            self._needed_includes.add("cstring")

        # Generate structs
        structs: dict[str, CppStruct] = {}
        all_classes = list(sv.all_classes().values())
        sorted_classes = self.sort_classes(all_classes)

        for cls in sorted_classes:
            struct_result = self.generate_struct(cls)
            structs[struct_result.struct.name] = struct_result.struct

        # Sort enums alphabetically for deterministic output.
        # Structs always stay in topological order (base before derived)
        # because C++ requires types to be declared before use.
        if self.alphabetical_sort:
            enums = dict(sorted(enums.items()))

        # Build includes
        include_list = [CppInclude(header=h, system=True) for h in sorted(self._needed_includes)]
        includes = Includes(includes=include_list)

        module = CppModule(
            namespace=namespace,
            schema_name=sv.schema.name,
            includes=includes,
            enums=enums,
            structs=structs,
        )

        return module

    def serialize(self, rendered_module: CppModule | None = None) -> str:
        """Serialize the schema to a C++ header string.

        Args:
            rendered_module: Optional pre-rendered module.

        Returns:
            C++ header source code as a string.
        """
        if rendered_module is not None:
            module = rendered_module
        else:
            module = self.render()

        return module.render(environment=self._template_environment())

    def _template_environment(self) -> Environment:
        """Get the Jinja2 template environment.

        If :attr:`template_dir` is set, templates in that directory take
        priority over the built-in defaults.
        """
        env = CppModule.environment()
        if self.template_dir is not None:
            loader = ChoiceLoader([FileSystemLoader(self.template_dir), env.loader])
            env.loader = loader
        return env


_TEMPLATE_NAMES = [
    "module.h.jinja",
    "struct.h.jinja",
    "field.h.jinja",
    "enum.h.jinja",
    "includes.h.jinja",
]


@shared_arguments(CppGenerator)
@click.option(
    "--namespace",
    type=str,
    help="Override the C++ namespace (default: derived from schema name)",
)
@click.option(
    "--alphabetical-sort/--no-alphabetical-sort",
    default=False,
    show_default=True,
    help="Sort structs and enums alphabetically for deterministic output.",
)
@click.option(
    "--use-optional/--no-use-optional",
    default=True,
    show_default=True,
    help="Use std::optional<T> for optional fields (requires C++17).",
)
@click.option(
    "--gen-string-conversions/--no-gen-string-conversions",
    default=True,
    show_default=True,
    help="Generate to_string/from_string functions for enum classes.",
)
@click.option(
    "--template-dir",
    type=click.Path(),
    help="""
Optional jinja2 template directory to use for C++ header generation.

Pass a directory containing templates with the same name as any of the default
CppTemplateModel templates to override them.

\b
Available templates to override:
"""
    + "\n".join(["- " + name for name in _TEMPLATE_NAMES]),
)
@click.version_option(__version__, "-V", "--version")
@click.command(name="gen-cpp-header")
def cli(
    yamlfile,
    namespace: str | None = None,
    alphabetical_sort: bool = False,
    use_optional: bool = True,
    gen_string_conversions: bool = True,
    template_dir: str | None = None,
    **args,
):
    """Generate C++ header files from a LinkML schema.

    This generator produces idiomatic C++17 headers with:
    - ``enum class`` for enums with to_string/from_string helpers
    - structs for classes with public inheritance
    - std::optional<T> for optional fields
    - std::vector<T> for multivalued fields
    """
    if template_dir is not None:
        if not Path(template_dir).exists():
            raise FileNotFoundError(f"The template directory {template_dir} does not exist!")

    gen = CppGenerator(
        yamlfile,
        namespace=namespace,
        alphabetical_sort=alphabetical_sort,
        use_optional=use_optional,
        gen_string_conversions=gen_string_conversions,
        template_dir=template_dir,
        **args,
    )
    print(gen.serialize())


if __name__ == "__main__":
    cli()
