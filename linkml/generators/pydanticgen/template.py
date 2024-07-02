from copy import copy
from importlib.util import find_spec
from typing import Any, ClassVar, Dict, Generator, List, Literal, Optional, Union, overload

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field
from pydantic.version import VERSION as PYDANTIC_VERSION

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
    from pydantic.fields import ModelField


class TemplateModel(BaseModel):
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

    pydantic_ver: int = int(PYDANTIC_VERSION[0])
    meta_exclude: ClassVar[List[str]] = None

    def render(self, environment: Optional[Environment] = None, black: bool = False) -> str:
        """
        Recursively render a template model to a string.

        For each field in the model, recurse through, rendering each :class:`.TemplateModel`
        using the template set in :attr:`.TemplateModel.template` , but preserving the structure
        of lists and dictionaries. Regular :class:`.BaseModel` s are rendered to dictionaries.
        Any other value is passed through unchanged.

        Args:
            environment (:class:`jinja2.Environment`): Template environment - see :meth:`.environment`
            black (bool): if ``True`` , format template with black. (default False)
        """
        if environment is None:
            environment = TemplateModel.environment()

        if int(PYDANTIC_VERSION[0]) >= 2:
            fields = {**self.model_fields, **self.model_computed_fields}
        else:
            fields = self.model_fields

        data = {k: _render(getattr(self, k, None), environment) for k in fields}
        template = environment.get_template(self.template)
        rendered = template.render(**data)
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

    @classmethod
    def environment(cls) -> Environment:
        """
        Default environment for Template models.
        uses a :class:`jinja2.PackageLoader` for the templates directory within this module
        with the ``trim_blocks`` and ``lstrip_blocks`` parameters set to ``True`` so that the
        default templates could be written in a more readable way.
        """
        return copy(cls._environment)

    if int(PYDANTIC_VERSION[0]) < 2:
        # simulate pydantic 2's model_fields behavior
        # without using classmethod + property decorators
        # see:
        # - https://docs.python.org/3/whatsnew/3.11.html#language-builtins
        # - https://github.com/python/cpython/issues/89519
        # and:
        # - https://docs.python.org/3/reference/datamodel.html#customizing-class-creation
        # for this version.
        model_fields: ClassVar[Dict[str, "ModelField"]]

        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            cls.model_fields = cls.__fields__

        @overload
        def model_dump(self, mode: Literal["python"] = "python") -> dict: ...

        @overload
        def model_dump(self, mode: Literal["json"] = "json") -> str: ...

        def model_dump(self, mode: Literal["python", "json"] = "python", **kwargs) -> Union[dict, str]:
            if mode == "json":
                return self.json(**kwargs)
            return self.dict(**kwargs)

    @classmethod
    def exclude_from_meta(cls: "TemplateModel") -> List[str]:
        """
        Attributes in the source definition to exclude from linkml_meta
        """
        ret = [*cls.model_fields.keys()]
        if cls.meta_exclude is not None:
            ret = ret + cls.meta_exclude
        return ret


def _render(
    item: Union[TemplateModel, Any, List[Union[Any, TemplateModel]], Dict[str, Union[Any, TemplateModel]]],
    environment: Environment,
) -> Union[str, List[str], Dict[str, str]]:
    if isinstance(item, TemplateModel):
        return item.render(environment)
    elif isinstance(item, list):
        return [_render(i, environment) for i in item]
    elif isinstance(item, dict):
        return {k: _render(v, environment) for k, v in item.items()}
    elif isinstance(item, BaseModel):
        if int(PYDANTIC_VERSION[0]) >= 2:
            fields = item.model_fields
        else:
            fields = item.__fields__
        return {k: _render(getattr(item, k, None), environment) for k in fields.keys()}
    else:
        return item


class EnumValue(BaseModel):
    """
    A single value within an :class:`.Enum`
    """

    label: str
    value: str
    description: Optional[str] = None


class PydanticEnum(TemplateModel):
    """
    Model used to render a :class:`enum.Enum`
    """

    template: ClassVar[str] = "enum.py.jinja"

    name: str
    description: Optional[str] = None
    values: Dict[str, EnumValue] = Field(default_factory=dict)


class PydanticBaseModel(TemplateModel):
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
    fields: Optional[List[str]] = None
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


class PydanticAttribute(TemplateModel):
    """
    Reduced version of SlotDefinition that carries all and only the information
    needed by the template
    """

    template: ClassVar[str] = "attribute.py.jinja"
    meta_exclude: ClassVar[List[str]] = ["from_schema", "owner", "range", "multivalued", "inlined", "inlined_as_list"]

    name: str
    required: bool = False
    identifier: bool = False
    key: bool = False
    predefined: Optional[str] = None
    """Fixed string to use in body of field"""
    annotations: Optional[dict] = None
    """
    Of the form::

        annotations = {'python_range': {'value': 'int'}}

    .. todo::

        simplify when refactoring pydanticgen, should just be a string or a model

    """
    title: Optional[str] = None
    description: Optional[str] = None
    equals_number: Optional[Union[int, float]] = None
    minimum_value: Optional[Union[int, float]] = None
    maximum_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    """
    Metadata for the slot to be included in a Field annotation
    """

    if int(PYDANTIC_VERSION[0]) >= 2:

        @computed_field
        def field(self) -> str:
            """Computed value to use inside of the generated Field"""
            if self.predefined:
                return self.predefined
            elif self.required or self.identifier or self.key:
                return "..."
            else:
                return "None"

    else:
        field: Optional[str] = None

        def __init__(self, **kwargs):
            super(PydanticAttribute, self).__init__(**kwargs)
            if self.predefined:
                self.field = self.predefined
            elif self.required or self.identifier or self.key:
                self.field = "..."
            else:
                self.field = "None"


class PydanticValidator(PydanticAttribute):
    """
    Trivial subclass of :class:`.PydanticAttribute` that uses the ``validator.py.jinja`` template instead
    """

    template: ClassVar[str] = "validator.py.jinja"


class PydanticClass(TemplateModel):
    """
    Reduced version of ClassDefinition that carries all and only the information
    needed by the template.

    On instantiation and rendering, will create any additional :attr:`.validators`
    that are implied by the given :attr:`.attributes`. Currently the only kind of
    slot-level validators that are created are for those slots that have a ``pattern``
    property.
    """

    template: ClassVar[str] = "class.py.jinja"
    meta_exclude: ClassVar[List[str]] = ["slots", "is_a"]

    name: str
    bases: Union[List[str], str] = PydanticBaseModel.default_name
    description: Optional[str] = None
    attributes: Optional[Dict[str, PydanticAttribute]] = None
    meta: Optional[Dict[str, Any]] = None
    """
    Metadata for the class to be included in a linkml_meta class attribute
    """

    def _validators(self) -> Optional[Dict[str, PydanticValidator]]:
        if self.attributes is None:
            return None

        return {k: PydanticValidator(**v.model_dump()) for k, v in self.attributes.items() if v.pattern is not None}

    if int(PYDANTIC_VERSION[0]) >= 2:

        @computed_field
        def validators(self) -> Optional[Dict[str, PydanticValidator]]:
            return self._validators()

        @computed_field
        def slots(self) -> Optional[Dict[str, PydanticAttribute]]:
            """alias of attributes"""
            return self.attributes

    else:
        validators: Optional[Dict[str, PydanticValidator]]

        def __init__(self, **kwargs):
            super(PydanticClass, self).__init__(**kwargs)
            self.validators = self._validators()

        def render(self, environment: Optional[Environment] = None, black: bool = False) -> str:
            """Overridden in pydantic 1 to ensure that validators are regenerated at rendering time"""
            # refresh in case attributes have changed since init
            self.validators = self._validators()
            return super(PydanticClass, self).render(environment, black)


class ObjectImport(BaseModel):
    """
    An object to be imported from within a module.

    See :class:`.Import` for examples
    """

    name: str
    alias: Optional[str] = None


class Import(TemplateModel):
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
    module: str
    alias: Optional[str] = None
    objects: Optional[List[ObjectImport]] = None

    def merge(self, other: "Import") -> List["Import"]:
        """
        Merge one import with another, see :meth:`.Imports` for an example.

        * If module don't match, return both
        * If one or the other are a :class:`.ConditionalImport`, return both
        * If modules match, neither contain objects, but the other has an alias, return the other
        * If modules match, one contains objects but the other doesn't, return both
        * If modules match, both contain objects, merge the object lists, preferring objects with aliases
        """
        # return both if we are orthogonal
        if self.module != other.module:
            return [self, other]

        # handle conditionals
        if isinstance(self, ConditionalImport) and isinstance(other, ConditionalImport):
            # If our condition is the same, return the newer version
            if self.condition == other.condition:
                return [other]
        if isinstance(self, ConditionalImport) or isinstance(other, ConditionalImport):
            # we don't have a good way of combining conditionals, just return both
            return [self, other]

        # handle module vs. object imports
        elif other.objects is None and self.objects is None:
            # both are modules, return the other only if it updates the alias
            if other.alias:
                return [other]
            else:
                return [self]
        elif other.objects is not None and self.objects is not None:
            # both are object imports, merge and return
            alias = self.alias if other.alias is None else other.alias
            # FIXME: super awkward implementation
            # keep ours if it has an alias and the other doesn't,
            # otherwise take the other's version
            self_objs = {obj.name: obj for obj in self.objects}
            other_objs = {
                obj.name: obj for obj in other.objects if obj.name not in self_objs or self_objs[obj.name].alias is None
            }
            self_objs.update(other_objs)

            return [Import(module=self.module, alias=alias, objects=list(self_objs.values()))]
        else:
            # one is a module, the other imports objects, keep both
            return [self, other]


class ConditionalImport(Import):
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
    condition: str
    alternative: Import


class Imports(TemplateModel):
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

    imports: List[Union[Import, ConditionalImport]] = Field(default_factory=list)

    def __add__(self, other: Union[Import, "Imports", List[Import]]) -> "Imports":
        if isinstance(other, Imports) or (isinstance(other, list) and all([isinstance(i, Import) for i in other])):
            if hasattr(self, "model_copy"):
                self_copy = self.model_copy(deep=True)
            else:
                self_copy = self.copy()

            for i in other:
                self_copy += i
            return self_copy

        # check if we have one of these already
        imports = self.imports.copy()

        existing = [i for i in imports if i.module == other.module]

        # if we have nothing importing from this module yet, add it!
        if len(existing) == 0:
            imports.append(other)
        elif len(existing) == 1:
            imports.remove(existing[0])
            imports.extend(existing[0].merge(other))
        else:
            # we have both a conditional and at least one nonconditional already.
            # If this is another conditional, we just add it, otherwise, we merge it
            # with the single nonconditional
            if isinstance(other, ConditionalImport):
                imports.append(other)
            else:
                for e in existing:
                    if isinstance(e, Import):
                        imports.remove(e)
                        merged = e.merge(other)
                        imports.extend(merged)
                        break

        # SPECIAL CASE - __future__ annotations must happen at the top of a file
        imports = sorted(imports, key=lambda i: i.module == "__future__", reverse=True)

        return Imports(imports=imports)

    def __len__(self) -> int:
        return len(self.imports)

    def __iter__(self) -> Generator[Import, None, None]:
        for i in self.imports:
            yield i

    def __getitem__(self, item: int) -> Import:
        return self.imports[item]


class PydanticModule(TemplateModel):
    """
    Top-level container model for generating a pydantic module :)
    """

    template: ClassVar[str] = "module.py.jinja"
    meta_exclude: ClassVar[str] = ["slots"]

    metamodel_version: Optional[str] = None
    version: Optional[str] = None
    base_model: PydanticBaseModel = PydanticBaseModel()
    injected_classes: Optional[List[str]] = None
    python_imports: List[Union[Import, ConditionalImport]] = Field(default_factory=list)
    enums: Dict[str, PydanticEnum] = Field(default_factory=dict)
    classes: Dict[str, PydanticClass] = Field(default_factory=dict)
    meta: Optional[Dict[str, Any]] = None
    """
    Metadata for the schema to be included in a linkml_meta module-level instance of LinkMLMeta
    """

    if int(PYDANTIC_VERSION[0]) >= 2:

        @computed_field
        def class_names(self) -> List[str]:
            return [c.name for c in self.classes.values()]

    else:
        class_names: List[str] = Field(default_factory=list)

        def __init__(self, **kwargs):
            super(PydanticModule, self).__init__(**kwargs)
            self.class_names = [c.name for c in self.classes.values()]

        def render(self, environment: Optional[Environment] = None, black: bool = False) -> str:
            """
            Trivial override of parent method for pydantic 1 to ensure that
            :attr:`.class_names` are correct at render time
            """
            self.class_names = [c.name for c in self.classes.values()]
            return super(PydanticModule, self).render(environment, black)
