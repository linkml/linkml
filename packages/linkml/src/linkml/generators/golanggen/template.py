"""Template models for Golang code generation."""

from keyword import iskeyword
from typing import Any, ClassVar, Literal, Optional, Union, get_args

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator

from linkml.generators.common.template import (
    ConditionalImport as ConditionalImport_,
)
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

    meta_exclude: ClassVar[list[str]] = None

    def render(self, environment: Optional[Environment] = None, **kwargs) -> str:
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
    value: Optional[str] = None
    description: Optional[str] = None


class GolangEnum(GolangTemplateModel):
    """
    Model used to render a Go const block for enum-like values
    """

    template: ClassVar[str] = "enum.go.jinja"

    name: str
    type: str = "string"
    description: Optional[str] = None
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
    description: Optional[str] = None
    pattern: Optional[str] = None
    meta: Optional[dict[str, Any]] = None
    omitempty: bool = True  # Whether to add omitempty to JSON tag


class GolangStruct(GolangTemplateModel):
    """
    Reduced version of ClassDefinition for Go structs
    """

    template: ClassVar[str] = "struct.go.jinja"
    meta_exclude: ClassVar[list[str]] = ["slots", "is_a"]

    name: str
    description: Optional[str] = None
    embedded_structs: Optional[list[str]] = None  # For inheritance via embedding
    fields: Optional[dict[str, GolangField]] = None
    meta: Optional[dict[str, Any]] = None
    is_type_alias: bool = False
    type_alias_value: Optional[str] = None


class Import(Import_, GolangTemplateModel):
    """
    A Go import statement.

    Examples:
        Simple import:
            >>> Import(module='fmt').render()
            import "fmt"

        Aliased import:
            >>> Import(module='github.com/example/pkg', alias='mypkg').render()
            import mypkg "github.com/example/pkg"
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
    imports: Union[Imports, list[Import]] = Imports()
    enums: dict[str, GolangEnum] = Field(default_factory=dict)
    structs: dict[str, GolangStruct] = Field(default_factory=dict)
    meta: Optional[dict[str, Any]] = None

    @field_validator("imports", mode="after")
    @classmethod
    def cast_imports(cls, imports: Union[Imports, list[Import]]) -> Imports:
        if isinstance(imports, list):
            imports = Imports(imports=imports)
        return imports

    @computed_field
    def struct_names(self) -> list[str]:
        return [s.name for s in self.structs.values() if not getattr(s, "is_type_alias", False)]
