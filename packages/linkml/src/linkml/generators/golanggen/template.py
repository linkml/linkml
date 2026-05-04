"""Template models for Golang code generation."""

from typing import Any, ClassVar, Literal, get_args

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field, computed_field, field_validator

from linkml.generators.common.template import (
    Import as Import_,
)
from linkml.generators.common.template import (
    Imports as Imports_,
)
from linkml.generators.common.template import (
    ObjectImport,  # noqa: F401
    TemplateModel,
)

IMPORT_GROUPS = Literal["stdlib", "thirdparty", "local"]
"""
Import groups for organizing Go imports

Order of this literal is used in sort and therefore not arbitrary.
"""


class GolangTemplateModel(TemplateModel):
    """
    Metaclass to render Golang models with jinja templates.

    Each subclass needs to declare a :class:`typing.ClassVar` for a
    jinja template within the `templates` directory.

    Templates are written expecting each of the other TemplateModels
    to already be rendered to strings.
    """

    template: ClassVar[str]
    _environment: ClassVar[Environment] = Environment(
        loader=PackageLoader("linkml.generators.golanggen", "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    _environment.filters["go_comment"] = lambda text, indent="": (
        "\n".join(f"{indent}// {line}" if line.strip() else f"{indent}//" for line in text.splitlines())
    )

    meta_exclude: ClassVar[list[str]] = None

    def render(self, environment: Environment | None = None, **kwargs) -> str:
        """
        Recursively render a template model to a string.

        For each field in the model, recurse through, rendering each :class:`.GolangTemplateModel`
        using the template set in :attr:`.GolangTemplateModel.template` , but preserving the structure
        of lists and dictionaries.

        Args:
            environment (:class:`jinja2.Environment`): Template environment
            **kwargs: Additional arguments (ignored, for compatibility with parent classes)
        """
        if environment is None:
            environment = self.environment()

        return super().render(environment=environment)


class GolangConstant(BaseModel):
    """
    A single constant value within an enum-like const block
    """

    name: str
    value: str | None = None
    description: str | None = None


class GolangEnum(GolangTemplateModel):
    """
    Model used to render a Go const block for enum-like values
    """

    template: ClassVar[str] = "enum.go.jinja"

    name: str
    type: str = "string"
    description: str | None = None
    values: dict[str, GolangConstant] = Field(default_factory=dict)


class GolangField(GolangTemplateModel):
    """
    Reduced version of SlotDefinition for Go struct fields
    """

    template: ClassVar[str] = "field.go.jinja"
    meta_exclude: ClassVar[list[str]] = ["from_schema", "owner", "range", "inlined", "inlined_as_list"]

    name: str
    go_name: str  # CamelCase name for Go
    json_name: str  # snake_case name for JSON tag
    type: str
    required: bool = False
    identifier: bool = False
    key: bool = False
    description: str | None = None
    pattern: str | None = None
    meta: dict[str, Any] | None = None
    omitempty: bool = True  # Whether to add omitempty to JSON tag
    omitzero: bool = False  # Whether to add omitzero to JSON tag (Go 1.24+)


class GolangStruct(GolangTemplateModel):
    """
    Reduced version of ClassDefinition for Go structs
    """

    template: ClassVar[str] = "struct.go.jinja"
    meta_exclude: ClassVar[list[str]] = ["slots", "is_a"]

    name: str
    description: str | None = None
    embedded_structs: list[str] | None = None  # For inheritance via embedding
    fields: dict[str, GolangField] | None = None
    meta: dict[str, Any] | None = None
    is_type_alias: bool = False
    type_alias_value: str | None = None


class Import(Import_, GolangTemplateModel):
    """
    A Go import statement.

    Examples:
        Simple import:
            >>> print(Import(module='fmt').render(), end='')
            "fmt"

        Aliased import:
            >>> print(Import(module='github.com/example/pkg', alias='mypkg').render(), end='')
            mypkg "github.com/example/pkg"
    """

    template: ClassVar[str] = "imports.go.jinja"

    @computed_field
    def group(self) -> IMPORT_GROUPS:
        """
        Import group used when sorting

        * ``stdlib`` - standard library packages
        * ``thirdparty`` - external dependencies
        * ``local`` - local/relative imports
        """
        # Standard library packages don't have dots
        if "/" not in self.module:
            return "stdlib"
        elif self.module.startswith("."):
            return "local"
        else:
            return "thirdparty"


class Imports(Imports_, GolangTemplateModel):
    """
    Container class for Go imports that can handle merging and sorting
    """

    template: ClassVar[str] = "imports.go.jinja"

    imports: list[Import] = Field(default_factory=list)
    group_order: tuple[str, ...] = get_args(IMPORT_GROUPS)
    """Order in which to sort imports by their :attr:`.Import.group`"""

    @computed_field
    def import_groups(self) -> list[IMPORT_GROUPS]:
        """
        List of what group each import belongs to
        """
        return [i.group for i in self.imports]

    def sort(self) -> None:
        """
        Sort imports by group and then alphabetically
        """

        def _sort_key(i: Import) -> tuple[int, str]:
            return (self.group_order.index(i.group), i.module)

        imports = sorted(self.imports, key=_sort_key)
        for i in imports:
            i.sort()
        self.imports = imports


class GolangModule(GolangTemplateModel):
    """
    Top-level container model for generating a Go module/package
    """

    template: ClassVar[str] = "module.go.jinja"
    meta_exclude: ClassVar[str] = ["slots"]

    package_name: str
    imports: Imports | list[Import] = Imports()
    enums: dict[str, GolangEnum] = Field(default_factory=dict)
    structs: dict[str, GolangStruct] = Field(default_factory=dict)
    meta: dict[str, Any] | None = None

    @field_validator("imports", mode="after")
    @classmethod
    def cast_imports(cls, imports: Imports | list[Import]) -> Imports:
        if isinstance(imports, list):
            imports = Imports(imports=imports)
        return imports

    @computed_field
    def struct_names(self) -> list[str]:
        """All non-alias struct names."""
        return [s.name for s in self.structs.values() if not getattr(s, "is_type_alias", False)]

    @computed_field
    def root_struct_names(self) -> list[str]:
        """Struct names that are never used as a field type in any other struct.

        A "root class" is one that only appears at the top level of a document,
        i.e. it is never referenced as the type of a field (directly, as a
        pointer, or as a slice element) in any struct.

        When a slot references a class by its identifier (non-inlined), the
        field type is a type-alias like ``PersonId`` rather than ``Person``.
        This method resolves such aliases back to their original struct name
        so that the original class is correctly excluded from root structs.
        """
        # Build a mapping from type-alias names back to the original struct
        # name.  Type aliases follow the convention ``{ClassName}Id``.
        alias_to_struct: dict[str, str] = {}
        real_struct_names = set(self.struct_names)
        for s in self.structs.values():
            if s.is_type_alias and s.name.endswith("Id"):
                original = s.name[:-2]
                if original in real_struct_names:
                    alias_to_struct[s.name] = original

        # Collect every struct name that appears as a field type somewhere
        referenced: set[str] = set()
        for struct in self.structs.values():
            if not struct.fields:
                continue
            for field in struct.fields.values():
                # Strip slice prefix ``[]`` and pointer prefix ``*``
                base = field.type.lstrip("*")
                if base.startswith("[]"):
                    base = base[2:].lstrip("*")
                if base in self.structs:
                    referenced.add(base)
                    # If the field type is a type alias, also mark the
                    # original struct as referenced.
                    if base in alias_to_struct:
                        referenced.add(alias_to_struct[base])

        return [name for name in self.struct_names if name not in referenced]
