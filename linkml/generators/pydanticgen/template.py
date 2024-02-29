import sys
from typing import Any, ClassVar, Dict, Generator, List, Optional, Tuple, Union, get_origin, overload

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field
from pydantic.version import VERSION as PYDANTIC_VERSION

if int(PYDANTIC_VERSION[0]) >= 2:
    from pydantic import computed_field


class TemplateModel(BaseModel):
    """Metaclass to group template models"""

    template: ClassVar[str]
    pydantic_ver: int = int(PYDANTIC_VERSION[0])

    def render(self, environment: Optional[Environment] = None) -> str:
        """
        Recursively render to a string.
        """
        if environment is None:
            environment = TemplateModel.environment()

        data = {k: _render(getattr(self, k, None), environment) for k in self.model_fields.keys()}
        template = environment.get_template(self.template)
        return template.render(**data)

    @classmethod
    def environment(cls) -> Environment:
        return Environment(
            loader=PackageLoader("linkml.generators.pydanticgen", "templates"), trim_blocks=True, lstrip_blocks=True
        )

    if int(PYDANTIC_VERSION[0]) < 2:

        @property
        def model_fields(self) -> Dict[str, Any]:
            return self.__fields__

        @overload
        def model_dump(self, mode: Literal["python"] = "python") -> dict: ...

        @overload
        def model_dump(self, mode: Literal["json"] = "json") -> str: ...

        def model_dump(self, mode: Literal["python", "json"] = "python", **kwargs) -> Union[dict, str]:
            if mode == "json":
                return self.json(**kwargs)
            return self.dict(**kwargs)


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
    label: str
    value: str
    description: Optional[str] = None


class Enum(TemplateModel):
    """
    Model of enum definition used with enum template

    (not intended to be used as an enum!)

    TODO: use this with OOCodeGenerator when we decide where to put shared models :)
    """

    template: ClassVar[str] = "enum.py.jinja"

    name: str
    description: Optional[str] = None
    values: Dict[str, EnumValue] = Field(default_factory=dict)

    @classmethod
    def from_dict(cls, enums: dict) -> Dict[str, "Enum"]:
        """
        Generate types enum models from dict form of enums created by
        :meth:`~linkml.generators.OOCodeGenerator.generate_enums`
        """
        return {k: Enum(**v) for k, v in enums.items()}


class PydanticBaseModel(TemplateModel):
    """
    Parameterization of the base model that generated pydantic classes inherit from
    """

    template: ClassVar[str] = "base_model.py.jinja"

    default_name: ClassVar[str] = "ConfiguredBaseModel"
    name: str = Field(default_factory=lambda: PydanticBaseModel.default_name)
    extra_fields: Literal["allow", "forbid", "ignore"] = "forbid"
    fields: Optional[List[str]] = None


class PydanticAttribute(TemplateModel):
    """
    Reduced version of SlotDefinition that carries all and only the information
    needed by the template
    """

    template: ClassVar[str] = "attribute.py.jinja"

    name: str
    required: bool = False
    identifier: bool = False
    key: bool = False
    predefined: Optional[str] = None
    """Fixed string to use in body of field"""
    annotations: Optional[dict] = None
    title: Optional[str] = None
    description: Optional[str] = None
    equals_number: Optional[Union[int, float]] = None
    minimum_value: Optional[Union[int, float]] = None
    maximum_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None

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
    template: ClassVar[str] = "validator.py.jinja"


class PydanticClass(TemplateModel):
    """
    Reduced version of ClassDefinition that carries all and only the information
    needed by the template
    """

    template: ClassVar[str] = "class.py.jinja"

    name: str
    bases: Union[List[str], str] = PydanticBaseModel.default_name
    description: Optional[str] = None
    attributes: Optional[Dict[str, PydanticAttribute]] = None

    def _validators(self) -> Optional[Dict[str, PydanticValidator]]:
        if self.attributes is None:
            return None

        return {k: PydanticValidator(**v.model_dump()) for k, v in self.attributes.items() if v.pattern is not None}

    if int(PYDANTIC_VERSION[0]) >= 2:

        @computed_field
        def validators(self) -> Optional[Dict[str, PydanticValidator]]:
            return self._validators()

    else:
        validators: Optional[Dict[str, PydanticValidator]]

        def __init__(self, **kwargs):
            super(PydanticClass, self).__init__(**kwargs)
            self.validators = self._validators()

        def render(self, environment: Optional[Environment] = None) -> str:
            # refresh in case attributes have changed since init
            self.validators = self._validators()
            return super(PydanticClass, self).render(environment)


class ObjectImport(BaseModel):
    name: str
    alias: Optional[str] = None


class Import(TemplateModel):
    template: ClassVar[str] = "imports.py.jinja"
    module: str
    alias: Optional[str] = None
    objects: Optional[List[ObjectImport]] = None

    def merge(self, other: "Import") -> List["Import"]:
        # return both if we are orthogonal
        if self.module != other.module:
            return [self, other]

        # handle conditionals
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
    template: ClassVar[str] = "conditional_import.py.jinja"
    condition: str
    alternative: Import


class Imports(TemplateModel):
    """Container class for imports that can handle merging!"""

    imports: List[Union[Import, ConditionalImport]] = Field(default_factory=list)

    def __add__(self, other: Import) -> "Imports":
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
        return Imports(imports=imports)

    def __len__(self) -> int:
        return len(self.imports)

    def __iter__(self) -> Generator[Import, None, None]:
        for i in self.imports:
            yield i

    def __getitem__(self, item: int) -> Import:
        return self.imports[item]

    def render(self, environment: Optional[Environment] = None) -> str:
        if environment is None:
            environment = TemplateModel.environment()
        return "\n".join([i.render() for i in self.imports])


class PydanticModule(TemplateModel):
    """
    Top-level container model for generating a pydantic module
    """

    template: ClassVar[str] = "module.py.jinja"

    metamodel_version: Optional[str] = None
    version: Optional[str] = None
    base_model: PydanticBaseModel = PydanticBaseModel()
    injected_classes: Optional[List[str]] = None
    imports: List[Union[Import, ConditionalImport]] = Field(default_factory=list)
    enums: Dict[str, Enum] = Field(default_factory=dict)
    classes: Dict[str, PydanticClass] = Field(default_factory=dict)

    if int(PYDANTIC_VERSION[0]) >= 2:

        @computed_field
        def class_names(self) -> List[str]:
            return [c.name for c in self.classes.values()]

    else:
        class_names: List[str] = Field(default_factory=list)

        def __init__(self, **kwargs):
            super(PydanticModule, self).__init__(**kwargs)
            self.class_names = [c.name for c in self.classes.values()]

        def render(self, environment: Optional[Environment] = None) -> str:
            # refresh in case attributes have changed since init
            self.class_names = [c.name for c in self.classes.values()]
            return super(PydanticModule, self).render(environment)
