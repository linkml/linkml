"""
Golang code generator for LinkML schemas.

Based on the PydanticGenerator architecture.
"""

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import click
from jinja2 import ChoiceLoader, Environment, FileSystemLoader

from linkml._version import __version__
from linkml.generators.golanggen.build import FieldResult, StructResult
from linkml.generators.golanggen.template import (
    GolangConstant,
    GolangEnum,
    GolangField,
    GolangModule,
    GolangStruct,
    Import,
    Imports,
)
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)


# Type mapping from LinkML base types to Go types
TYPE_MAP = {
    "str": "string",
    "string": "string",
    "int": "int",
    "integer": "int",
    "Bool": "bool",
    "boolean": "bool",
    "float": "float64",
    "double": "float64",
    "XSDDate": "time.Time",
    "XSDDateTime": "time.Time",
    "date": "time.Time",
    "datetime": "time.Time",
    "time": "time.Time",
    "uri": "string",
    "uriorcurie": "string",
    "ncname": "string",
}

# Go primitive types eligible for pointer promotion via ``nullable_primitives``
GO_PRIMITIVE_TYPES = frozenset({
    "string",
    "int",
    "int8",
    "int16",
    "int32",
    "int64",
    "float32",
    "float64",
    "bool",
})


@dataclass
class GolangGenerator(OOCodeGenerator):
    """
    Generates Golang code from a LinkML schema.

    This generator creates idiomatic Go structs with JSON tags from LinkML class definitions.
    It supports:
    - Struct generation from classes
    - Const blocks from enums
    - Inheritance via struct embedding
    - Proper type mappings
    - Multivalued fields as slices
    - Required vs optional fields
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.0"
    valid_formats = ["go", "golang"]
    file_extension = "go"

    # ObjectVars
    package_name: str | None = None
    """Override the package name. If None, derived from schema name."""

    gen_slots: bool = True
    """Generate struct fields"""

    sort_imports: bool = True
    """Sort imports by group (stdlib, thirdparty, local)"""

    add_json_tags: bool = True
    """Add JSON struct tags to fields"""

    use_time_package: bool = True
    """Import time package when needed for date/datetime types"""

    alphabetical_sort: bool = False
    """Sort structs and enums alphabetically by name for deterministic output."""

    nullable_primitives: bool = False
    """
    Use pointer types for optional primitive fields (e.g. ``*string``, ``*int``, ``*bool``).

    When False (default), optional primitives use bare Go types and ``omitempty``
    omits zero values (``""``, ``0``, ``false``).  When True, optional primitives
    become pointers so that ``omitempty`` only omits ``nil``, preserving
    intentional zero values.
    """

    template_dir: str | Path | None = None
    """
    Override templates for each GolangTemplateModel.

    Directory with templates that override the default templates.
    If a matching template is not found in the override directory,
    the default templates will be used.
    """

    # Private attributes
    _needs_time: bool = field(default=False, init=False)

    # Go zero-value defaults by type
    GO_TYPE_DEFAULTS = {
        "string": '""',
        "int": "0",
        "int8": "0",
        "int16": "0",
        "int32": "0",
        "int64": "0",
        "float32": "0.0",
        "float64": "0.0",
        "bool": "false",
        "time.Time": "time.Time{}",
    }

    def __post_init__(self):
        super().__post_init__()

    def default_value_for_type(self, typ: str) -> str:
        """
        Return the Go zero value for a given type.

        Args:
            typ: The Go type string

        Returns:
            The zero value literal for that type
        """
        return self.GO_TYPE_DEFAULTS.get(typ, "nil")

    @staticmethod
    def sort_classes(clist: list[ClassDefinition]) -> list[ClassDefinition]:
        """
        Sort classes such that if C is a child of P then C appears after P in the list
        """
        clist = list(clist)
        slist = []  # sorted
        while len(clist) > 0:
            can_add = False
            for i in range(len(clist)):
                candidate = clist[i]
                can_add = False
                if candidate.is_a:
                    candidates = [candidate.is_a] + candidate.mixins
                else:
                    candidates = candidate.mixins

                if not candidates:
                    can_add = True
                else:
                    if set(candidates) <= set([p.name for p in slist]):
                        can_add = True
                if can_add:
                    slist = slist + [candidate]
                    del clist[i]
                    break
            if not can_add:
                raise ValueError(f"could not find suitable element in {clist} that does not ref {slist}")
        return slist

    def generate_struct(self, cls: ClassDefinition) -> StructResult:
        """
        Generate a Go struct from a LinkML class definition.

        Args:
            cls: The class definition to convert

        Returns:
            StructResult containing the generated struct and any imports needed
        """
        struct_name = camelcase(cls.name)

        # Handle embedded structs for inheritance
        embedded_structs = []
        if cls.is_a:
            embedded_structs.append(camelcase(cls.is_a))
        if cls.mixins:
            embedded_structs.extend([camelcase(m) for m in cls.mixins])

        go_struct = GolangStruct(
            name=struct_name,
            description=cls.description if cls.description else None,
            embedded_structs=embedded_structs if embedded_structs else None,
        )

        result = StructResult(struct=go_struct, source=cls)

        # Generate fields — only direct slots, inherited ones come via embedding
        if self.gen_slots:
            direct = bool(embedded_structs)
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

    def generate_field(self, slot: SlotDefinition, cls: ClassDefinition) -> FieldResult:
        """
        Generate a Go struct field from a LinkML slot definition.

        Args:
            slot: The slot definition to convert
            cls: The parent class definition

        Returns:
            FieldResult containing the generated field
        """
        slot_alias = slot.alias if slot.alias else slot.name
        go_name = camelcase(slot_alias)
        json_name = underscore(slot_alias)

        go_type = self.generate_go_type(slot, cls)

        field = GolangField(
            name=slot.name,
            go_name=go_name,
            json_name=json_name,
            type=go_type,
            required=slot.required or False,
            identifier=slot.identifier or False,
            key=slot.key or False,
            description=slot.description if slot.description else None,
            pattern=slot.pattern if slot.pattern else None,
        )

        result = FieldResult(field=field, source=slot)
        return result

    def generate_go_type(self, slot: SlotDefinition, cls: ClassDefinition) -> str:
        """
        Generate the Go type for a slot.

        Args:
            slot: The slot definition
            cls: The parent class definition

        Returns:
            The Go type string (e.g., "string", "[]Person", "*Address")
        """
        sv = self.schemaview
        slot_range = slot.range

        # Determine base type
        if slot_range in sv.all_classes():
            # Reference to another class
            base_type = camelcase(slot_range)
            # Use pointer for optional complex types
            if not (slot.required or slot.identifier or slot.key):
                base_type = f"*{base_type}"
        elif slot_range in sv.all_enums():
            # Reference to enum
            base_type = camelcase(slot_range)
        elif slot_range in sv.all_types():
            # Built-in or custom type
            t = sv.get_type(slot_range)
            if t.base and t.base in TYPE_MAP:
                base_type = TYPE_MAP[t.base]
                # Track if we need time package
                if base_type == "time.Time":
                    self._needs_time = True
            else:
                logger.warning(f"Unknown type base: {t.name}, defaulting to string")
                base_type = "string"
        else:
            # Default to string
            base_type = "string"

        # Use pointer for optional primitive types when nullable_primitives is enabled.
        # Slices are already nil-able, so skip multivalued slots.
        if (
            self.nullable_primitives
            and not slot.multivalued
            and base_type in GO_PRIMITIVE_TYPES
            and not (slot.required or slot.identifier or slot.key)
        ):
            base_type = f"*{base_type}"

        # Handle multivalued slots
        if slot.multivalued:
            return f"[]{base_type}"

        return base_type

    def generate_enum(self, enum: EnumDefinition) -> GolangEnum:
        """
        Generate a Go const block from a LinkML enum definition.

        Args:
            enum: The enum definition to convert

        Returns:
            GolangEnum model
        """
        enum_name = camelcase(enum.name)
        constants = {}

        if enum.permissible_values:
            for pv_name, pv in enum.permissible_values.items():
                const_name = camelcase(pv_name)
                # Use the text value if available, otherwise the name
                const_value = pv.text if pv.text else pv_name

                constants[pv_name] = GolangConstant(
                    name=f"{enum_name}{const_name}",
                    value=const_value,
                    description=pv.description if pv.description else None,
                )

        return GolangEnum(
            name=enum_name,
            type="string",  # Default to string type for enums
            description=enum.description if enum.description else None,
            values=constants,
        )

    def render(self) -> GolangModule:
        """
        Render the schema to a GolangModule model.

        Returns:
            GolangModule containing all generated structs and enums
        """
        sv: SchemaView = self.schemaview

        # Determine package name
        package_name = self.package_name
        if package_name is None:
            schema_name = sv.schema.name
            # Extract package name from schema name (e.g., "kitchen_sink" -> "kitchen")
            if "_" in schema_name:
                package_name = schema_name[: schema_name.find("_")]
            else:
                package_name = schema_name
            # Make it valid Go package name (lowercase, alphanumeric + underscore)
            package_name = re.sub(r"[^a-z0-9_]", "", package_name.lower())

        # Generate enums
        enums = {}
        for enum_def in sv.all_enums().values():
            enum_model = self.generate_enum(enum_def)
            enums[enum_model.name] = enum_model

        # Generate structs
        structs = {}
        all_classes = list(sv.all_classes().values())
        sorted_classes = self.sort_classes(all_classes)

        for cls in sorted_classes:
            struct_result = self.generate_struct(cls)
            structs[struct_result.struct.name] = struct_result.struct

        # Sort alphabetically for deterministic output
        if self.alphabetical_sort:
            enums = dict(sorted(enums.items()))
            structs = dict(sorted(structs.items()))

        # Build imports
        imports = Imports()
        if self._needs_time and self.use_time_package:
            imports += Import(module="time")

        if self.sort_imports:
            imports.sort()

        module = GolangModule(
            package_name=package_name,
            imports=imports,
            enums=enums,
            structs=structs,
        )

        return module

    def serialize(self, rendered_module: GolangModule | None = None) -> str:
        """
        Serialize the schema to a Go source code string.

        Args:
            rendered_module: Optional pre-rendered module

        Returns:
            Go source code as a string
        """
        if rendered_module is not None:
            module = rendered_module
        else:
            module = self.render()

        return module.render(environment=self._template_environment())

    def _template_environment(self) -> Environment:
        """Get the Jinja2 template environment.

        If :attr:`template_dir` is set, templates in that directory take
        priority over the built-in defaults via a :class:`jinja2.ChoiceLoader`.
        """
        env = GolangModule.environment()
        if self.template_dir is not None:
            loader = ChoiceLoader([FileSystemLoader(self.template_dir), env.loader])
            env.loader = loader
        return env


_TEMPLATE_NAMES = [
    "module.go.jinja",
    "struct.go.jinja",
    "field.go.jinja",
    "enum.go.jinja",
    "imports.go.jinja",
]


@shared_arguments(GolangGenerator)
@click.option(
    "--package-name",
    type=str,
    help="Override the Go package name (default: derived from schema name)",
)
@click.option(
    "--alphabetical-sort/--no-alphabetical-sort",
    default=False,
    show_default=True,
    help="Sort structs and enums alphabetically for deterministic output.",
)
@click.option(
    "--nullable-primitives/--no-nullable-primitives",
    default=False,
    show_default=True,
    help="Use pointer types for optional primitives so omitempty only triggers on nil.",
)
@click.option(
    "--template-dir",
    type=click.Path(),
    help="""
Optional jinja2 template directory to use for Go code generation.

Pass a directory containing templates with the same name as any of the default
GolangTemplateModel templates to override them. The given directory will be
searched for matching templates, and use the default templates as a fallback
if an override is not found.

Available templates to override:

\b
"""
    + "\n".join(["- " + name for name in _TEMPLATE_NAMES]),
)
@click.version_option(__version__, "-V", "--version")
@click.command(name="golang")
def cli(
    yamlfile,
    package_name: str | None = None,
    alphabetical_sort: bool = False,
    nullable_primitives: bool = False,
    template_dir: str | None = None,
    **args,
):
    """
    Generate Golang structs from a LinkML schema.

    This generator produces idiomatic Go code with:
    - Structs for classes
    - Const blocks for enums
    - JSON tags for serialization
    - Struct embedding for inheritance
    """
    if template_dir is not None:
        if not Path(template_dir).exists():
            raise FileNotFoundError(f"The template directory {template_dir} does not exist!")

    gen = GolangGenerator(
        yamlfile,
        package_name=package_name,
        alphabetical_sort=alphabetical_sort,
        nullable_primitives=nullable_primitives,
        template_dir=template_dir,
        **args,
    )
    print(gen.serialize())


if __name__ == "__main__":
    cli()
