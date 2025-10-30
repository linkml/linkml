import sys
from importlib.util import find_spec
from keyword import iskeyword
from typing import Any, ClassVar, Literal, Optional, Union, get_args

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.version import VERSION as PYDANTIC_VERSION

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
from linkml.utils.deprecation import deprecation_warning

try:
    if find_spec("black") is not None:
        from linkml.generators.pydanticgen.black import format_black
    else:
        # no warning, having black is optional, we only warn when someone tries to import it explicitly
        format_black = None
except ImportError:
    # we can also get an import error from find_spec during testing because that's how we mock not having it installed
    format_black = None

if int(PYDANTIC_VERSION[0]) >= 2:
    from pydantic import computed_field
else:
    deprecation_warning("pydantic-v1")

    def computed_field(f):
        """No-op decorator to allow this module to not break imports until 1.9.0"""
        return f


IMPORT_GROUPS = Literal["future", "stdlib", "thirdparty", "local", "conditional"]
"""
See :attr:`.Import.group` and :attr:`.Imports.sort`

Order of this literal is used in sort and therefore not arbitrary.
"""


class PydanticTemplateModel(TemplateModel):
    """
    Metaclass to render pydantic models with jinja templates.

    Each subclass needs to declare a :class:`typing.ClassVar` for a
    jinja template within the `templates` directory.

    Templates are written expecting each of the other TemplateModels
    to already be rendered to strings - ie. rather than the ``class.py.jinja``
    template receiving a full :class:`.PydanticAttribute` object or dictionary,
    it receives it having already been rendered to a string. See the :meth:`.render` method.

    .. admonition:: Black Formatting

        Template models will try to use ``black`` to format results when it is available in the
        environment when render is called with ``black = True`` . If it isn't, then the string is
        returned without any formatting beyond the template.
        This is mostly important for complex annotations like those produced for arrays,
        as otherwise the templates are acceptable looking.

        To install linkml with black, use the extra ``black`` dependency.

        e.g. with pip::

            pip install linkml[black]

        or with poetry::

            poetry install -E black

    """

    template: ClassVar[str]
    _environment: ClassVar[Environment] = Environment(
        loader=PackageLoader("linkml.generators.pydanticgen", "templates"), trim_blocks=True, lstrip_blocks=True
    )

    meta_exclude: ClassVar[list[str]] = None

    def render(self, environment: Optional[Environment] = None, black: bool = False) -> str:
        """
        Recursively render a template model to a string.

        For each field in the model, recurse through, rendering each :class:`.PydanticTemplateModel`
        using the template set in :attr:`.PydanticTemplateModel.template` , but preserving the structure
        of lists and dictionaries. Regular :class:`.BaseModel` s are rendered to dictionaries.
        Any other value is passed through unchanged.

        Args:
            environment (:class:`jinja2.Environment`): Template environment - see :meth:`.environment`
            black (bool): if ``True`` , format template with black. (default False)
        """
        if environment is None:
            environment = self.environment()

        rendered = super().render(environment=environment)

        if format_black is not None and black:
            try:
                return format_black(rendered)
            except Exception:
                # TODO: it would nice to have a standard logging module here ;)
                return rendered
        elif black and format_black is None:
            raise ValueError("black formatting was requested, but black is not installed in this environment")
        else:
            return rendered


class EnumValue(BaseModel):
    """
    A single value within an :class:`.Enum`
    """

    label: str
    alias: Optional[str] = None
    value: str
    description: Optional[str] = None

    @model_validator(mode="after")
    def alias_python_keywords(self) -> Self:
        """Mask Python keywords used for `label` by appending `_`"""
        if iskeyword(self.label):
            if self.alias is None:
                self.alias = self.label
            self.label = self.label + "_"
        return self


class PydanticEnum(PydanticTemplateModel):
    """
    Model used to render a :class:`enum.Enum`
    """

    template: ClassVar[str] = "enum.py.jinja"

    name: str
    description: Optional[str] = None
    values: dict[str, EnumValue] = Field(default_factory=dict)


class PydanticBaseModel(PydanticTemplateModel):
    """
    Parameterization of the base model that generated pydantic classes inherit from
    """

    template: ClassVar[str] = "base_model.py.jinja"

    default_name: ClassVar[str] = "ConfiguredBaseModel"
    name: str = Field(default_factory=lambda: PydanticBaseModel.default_name)
    extra_fields: Literal["allow", "forbid", "ignore"] = "forbid"
    """
    Sets the ``extra`` model for pydantic models
    """
    fields: Optional[list[str]] = None
    """
    Extra fields that are typically injected into the base model via
    :attr:`~linkml.generators.pydanticgen.PydanticGenerator.injected_fields`
    """
    strict: bool = False
    """
    Enable strict mode in the base model.

    .. note::

        Pydantic 2 only! Pydantic 1 only has strict types, not strict mode. See: https://github.com/linkml/linkml/issues/1955

    References:
        https://docs.pydantic.dev/latest/concepts/strict_mode
    """


class PydanticAttribute(PydanticTemplateModel):
    """
    Reduced version of SlotDefinition that carries all and only the information
    needed by the template
    """

    template: ClassVar[str] = "attribute.py.jinja"
    meta_exclude: ClassVar[list[str]] = ["from_schema", "owner", "range", "inlined", "inlined_as_list"]

    name: str
    alias: Optional[str] = None
    required: bool = False
    identifier: bool = False
    key: bool = False
    predefined: Optional[str] = None
    """Fixed string to use in body of field"""
    range: Optional[str] = None
    """Type annotation used for model field"""
    title: Optional[str] = None
    description: Optional[str] = None
    equals_number: Optional[Union[int, float]] = None
    minimum_value: Optional[Union[int, float]] = None
    maximum_value: Optional[Union[int, float]] = None
    exact_cardinality: Optional[int] = None
    minimum_cardinality: Optional[int] = None
    maximum_cardinality: Optional[int] = None
    multivalued: Optional[bool] = None
    pattern: Optional[str] = None
    meta: Optional[dict[str, Any]] = None
    """
    Metadata for the slot to be included in a Field annotation
    """

    @computed_field
    def field(self) -> str:
        """Computed value to use inside of the generated Field"""
        if self.predefined:
            return self.predefined
        elif self.required or self.identifier or self.key:
            return "..."
        else:
            if self.range and self.range.startswith("Optional[list"):
                return "[]"
            return "None"

    @model_validator(mode="after")
    def alias_python_keywords(self) -> Self:
        """Mask Python keywords used for `name` by appending `_`"""
        if iskeyword(self.name):
            if self.alias is None:
                self.alias = self.name
            self.name = self.name + "_"
        return self


class PydanticValidator(PydanticAttribute):
    """
    Trivial subclass of :class:`.PydanticAttribute` that uses the ``validator.py.jinja`` template instead
    """

    template: ClassVar[str] = "validator.py.jinja"


class PydanticClass(PydanticTemplateModel):
    """
    Reduced version of ClassDefinition that carries all and only the information
    needed by the template.

    On instantiation and rendering, will create any additional :attr:`.validators`
    that are implied by the given :attr:`.attributes`. Currently the only kind of
    slot-level validators that are created are for those slots that have a ``pattern``
    property.
    """

    template: ClassVar[str] = "class.py.jinja"
    meta_exclude: ClassVar[list[str]] = ["slots", "is_a"]

    name: str
    bases: Union[list[str], str] = PydanticBaseModel.default_name
    description: Optional[str] = None
    attributes: Optional[dict[str, PydanticAttribute]] = None
    meta: Optional[dict[str, Any]] = None
    """
    Metadata for the class to be included in a linkml_meta class attribute
    """

    def _validators(self) -> Optional[dict[str, PydanticValidator]]:
        if self.attributes is None:
            return None

        return {k: PydanticValidator(**v.model_dump()) for k, v in self.attributes.items() if v.pattern is not None}

    @computed_field
    def validators(self) -> Optional[dict[str, PydanticValidator]]:
        return self._validators()

    @computed_field
    def slots(self) -> Optional[dict[str, PydanticAttribute]]:
        """alias of attributes"""
        return self.attributes


class Import(Import_, PydanticTemplateModel):
    """
    A python module, or module and classes to be imported.

    Examples:

        Module import:

        .. code-block:: python

            >>> Import(module='sys').render()
            import sys
            >>> Import(module='numpy', alias='np').render()
            import numpy as np

        Class import:

        .. code-block:: python

            >>> Import(module='pathlib', objects=[
            >>>     ObjectImport(name="Path"),
            >>>     ObjectImport(name="PurePath", alias="RenamedPurePath")
            >>> ]).render()
            from pathlib import (
                Path,
                PurePath as RenamedPurePath
            )

    """

    template: ClassVar[str] = "imports.py.jinja"

    @computed_field
    def group(self) -> IMPORT_GROUPS:
        """
        Import group used when sorting

        * ``future`` - from `__future__` import...
        * ``stdlib`` - ... the standard library
        * ``thirdparty`` - other dependencies not in the standard library
        * ``local`` - relative imports (eg. from split generation)
        * ``conditional`` - a :class:`.ConditionalImport`
        """
        if self.module == "__future__":
            return "future"
        elif sys.version_info.minor >= 10 and self.module in sys.stdlib_module_names:
            return "stdlib"
        elif sys.version_info.minor < 10 and self.module in _some_stdlib_module_names:
            return "stdlib"
        elif self.module.startswith("."):
            return "local"
        else:
            return "thirdparty"


class ConditionalImport(ConditionalImport_, PydanticTemplateModel):
    """
    Import that depends on some condition in the environment, common when
    using backported features or straddling dependency versions.

    Make sure that everything that is needed to evaluate the condition is imported
    before this is added to the injected imports!

    Examples:

        conditionally import Literal from ``typing_extensions`` if on python <= 3.8

        .. code-block:: python
            :force:

            imports = (Imports() +
                 Import(module='sys') +
                 ConditionalImport(
                 module="typing",
                 objects=[ObjectImport(name="Literal")],
                 condition="sys.version_info >= (3, 8)",
                 alternative=Import(
                     module="typing_extensions",
                     objects=[ObjectImport(name="Literal")]
                 )
             )

        Renders to:

        .. code-block:: python
            :force:

            import sys
            if sys.version_info >= (3, 8):
                from typing import Literal
            else:
                from typing_extensions import Literal

    """

    template: ClassVar[str] = "conditional_import.py.jinja"

    @computed_field
    def group(self) -> Literal["conditional"]:
        return "conditional"


class Imports(Imports_, PydanticTemplateModel):
    """
    Container class for imports that can handle merging!

    See :class:`.Import` and :class:`.ConditionalImport` for examples of declaring individual imports

    Useful for generation, because each build stage will potentially generate
    overlapping imports. This ensures that we can keep a collection of imports
    without having many duplicates.

    Defines methods for adding, iterating, and indexing from within the :attr:`Imports.imports` list.

    Examples:

        .. code-block:: python
            :force:

            imports = (Imports() +
                Import(module="sys") +
                Import(module="pathlib", objects=[ObjectImport(name="Path")]) +
                Import(module="sys")
            )

        Renders to:

        .. code-block:: python

            from pathlib import Path
            import sys

    """

    template: ClassVar[str] = "imports.py.jinja"

    imports: list[Union[Import, ConditionalImport]] = Field(default_factory=list)
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
        Sort imports recursively, mimicking isort:

        * First by :attr:`.Import.group` according to :attr:`.Imports.group_order`
        * Then by whether the :class:`.Import` has any objects
          (``import module`` comes before ``from module import name``)
        * Then alphabetically by module name
        """

        def _sort_key(i: Import) -> tuple[int, int, str]:
            return (self.group_order.index(i.group), int(i.objects is not None), i.module)

        imports = sorted(self.imports, key=_sort_key)
        for i in imports:
            i.sort()
        self.imports = imports


class PydanticModule(PydanticTemplateModel):
    """
    Top-level container model for generating a pydantic module :)
    """

    template: ClassVar[str] = "module.py.jinja"
    meta_exclude: ClassVar[str] = ["slots"]

    metamodel_version: Optional[str] = None
    version: Optional[str] = None
    base_model: PydanticBaseModel = PydanticBaseModel()
    injected_classes: Optional[list[str]] = None
    python_imports: Union[Imports, list[Union[Import, ConditionalImport]]] = Imports()
    enums: dict[str, PydanticEnum] = Field(default_factory=dict)
    classes: dict[str, PydanticClass] = Field(default_factory=dict)
    meta: Optional[dict[str, Any]] = None
    """
    Metadata for the schema to be included in a linkml_meta module-level instance of LinkMLMeta
    """

    @field_validator("python_imports", mode="after")
    @classmethod
    def cast_imports(cls, imports: Union[Imports, list[Union[Import, ConditionalImport]]]) -> Imports:
        if isinstance(imports, list):
            imports = Imports(imports=imports)
        return imports

    @computed_field
    def class_names(self) -> list[str]:
        return [c.name for c in self.classes.values()]


_some_stdlib_module_names = {
    "copy",
    "datetime",
    "decimal",
    "enum",
    "inspect",
    "os",
    "re",
    "sys",
    "typing",
    "dataclasses",
}
"""
sys.stdlib_module_names is only present in 3.10 and later
so we make a cheap copy of the stdlib modules that we commonly use here,
but this should be removed whenever support for 3.9 is dropped.
"""
