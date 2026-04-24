"""Template models for C++ header code generation."""

from typing import ClassVar

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field, field_validator

from linkml.generators.common.template import (
    TemplateModel,
)


class CppTemplateModel(TemplateModel):
    """Metaclass to render C++ models with jinja templates.

    Each subclass declares a :class:`typing.ClassVar` for a
    jinja template within the ``templates`` directory.

    Templates are written expecting each of the other TemplateModels
    to already be rendered to strings.
    """

    template: ClassVar[str]
    _environment: ClassVar[Environment] = Environment(
        loader=PackageLoader("linkml.generators.cppgen", "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    _environment.filters["cpp_comment"] = lambda text, indent="": "\n".join(
        f"{indent}/// {line}" if line.strip() else f"{indent}///" for line in text.splitlines()
    )

    meta_exclude: ClassVar[list[str]] = None

    def render(self, environment: Environment | None = None, **kwargs) -> str:
        """Recursively render a template model to a string."""
        if environment is None:
            environment = self.environment()
        return super().render(environment=environment)


class CppEnumValue(BaseModel):
    """A single value within a C++ enum class."""

    name: str
    """The enum constant name (UPPER_SNAKE_CASE)."""

    value: str | None = None
    """String value for to_string/from_string mappings."""

    description: str | None = None


class CppEnum(CppTemplateModel):
    """Model used to render a C++ ``enum class`` with string conversion helpers."""

    template: ClassVar[str] = "enum.h.jinja"

    name: str
    """CamelCase enum name."""

    description: str | None = None
    values: dict[str, CppEnumValue] = Field(default_factory=dict)


class CppField(CppTemplateModel):
    """Reduced version of SlotDefinition for C++ struct members."""

    template: ClassVar[str] = "field.h.jinja"
    meta_exclude: ClassVar[list[str]] = ["from_schema", "owner", "range", "inlined", "inlined_as_list"]

    name: str
    """snake_case field name."""

    cpp_type: str
    """Fully resolved C++ type expression (e.g. ``std::string``, ``std::optional<int32_t>``)."""

    required: bool = False
    identifier: bool = False
    multivalued: bool = False
    description: str | None = None
    default_value: str | None = None
    """Default value expression (e.g. ``{}`` or ``0``)."""

    pattern: str | None = None
    """Regex pattern constraint (stored as static constexpr for runtime validation)."""

    minimum_value: float | None = None
    maximum_value: float | None = None


class CppStruct(CppTemplateModel):
    """Reduced version of ClassDefinition for C++ structs."""

    template: ClassVar[str] = "struct.h.jinja"
    meta_exclude: ClassVar[list[str]] = ["slots", "is_a"]

    name: str
    """CamelCase struct name."""

    description: str | None = None
    base_classes: list[str] | None = None
    """Base classes for public inheritance."""

    fields: dict[str, CppField] | None = None
    is_abstract: bool = False
    is_type_alias: bool = False
    type_alias_value: str | None = None


class CppInclude(BaseModel):
    """A single C++ ``#include`` directive."""

    header: str
    """Header path (e.g. ``<string>`` or ``"my_header.h"``)."""

    system: bool = True
    """Whether this is a system include (angle brackets) or local (quotes)."""


class Includes(CppTemplateModel):
    """Container for C++ include directives."""

    template: ClassVar[str] = "includes.h.jinja"

    includes: list[CppInclude] = Field(default_factory=list)

    def __add__(self, other: "CppInclude | Includes | list[CppInclude]") -> "Includes":
        existing = {inc.header for inc in self.includes}
        new_includes = list(self.includes)
        if isinstance(other, Includes):
            items = other.includes
        elif isinstance(other, list):
            items = other
        else:
            items = [other]
        for inc in items:
            if inc.header not in existing:
                new_includes.append(inc)
                existing.add(inc.header)
        return Includes(includes=new_includes)

    def __len__(self) -> int:
        return len(self.includes)

    def sort(self) -> None:
        """Sort includes: system first, then local, alphabetically within each group."""
        self.includes = sorted(self.includes, key=lambda i: (not i.system, i.header))


class CppModule(CppTemplateModel):
    """Top-level container model for generating a C++ header file."""

    template: ClassVar[str] = "module.h.jinja"
    meta_exclude: ClassVar[str] = ["slots"]

    namespace: str
    """C++ namespace (e.g. ``logosphere::ontology``)."""

    schema_name: str
    """Original schema name for the header comment."""

    includes: Includes = Includes()
    enums: dict[str, CppEnum] = Field(default_factory=dict)
    structs: dict[str, CppStruct] = Field(default_factory=dict)

    @field_validator("includes", mode="after")
    @classmethod
    def cast_includes(cls, includes: Includes | list[CppInclude]) -> Includes:
        if isinstance(includes, list):
            includes = Includes(includes=includes)
        return includes
