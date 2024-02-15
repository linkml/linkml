import inspect
from typing import ClassVar, Dict, Optional, List, Union, Type
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from pydantic import BaseModel, Field
from pydantic.version import VERSION as PYDANTIC_VERSION

if int(PYDANTIC_VERSION[0]) >= 2:
    from pydantic import computed_field


class TemplateModel(BaseModel):
    """Metaclass to group template models"""

    pydantic_ver: int = int(PYDANTIC_VERSION[0])


class EnumValue(TemplateModel):
    label: str
    value: str
    description: Optional[str] = None


class Enum(TemplateModel):
    """
    Model of enum definition used with enum template

    (not intended to be used as an enum!)

    TODO: use this with OOCodeGenerator when we decide where to put shared models :)
    """

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
    default_name: ClassVar[str] = "ConfiguredBaseModel"
    name: str = Field(default_factory=lambda: PydanticBaseModel.default_name)
    extra_fields: Literal["allow", "forbid", "ignore"] = "forbid"
    fields: Optional[List[str]] = None


class PydanticAttribute(TemplateModel):
    """
    Reduced version of SlotDefinition that carries all and only the information
    needed by the template
    """

    name: str
    required: bool = False
    identifier: bool = False
    key: bool = False
    predefined: Optional[str] = None
    """Fixed string to use in body of field"""
    annotations: Optional[dict] = None
    title: Optional[str] = None
    description: Optional[str] = None
    equals_number: Optional[int | float] = None
    minimum_value: Optional[int | float] = None
    maximum_value: Optional[int | float] = None
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


class PydanticClass(TemplateModel):
    """
    Reduced version of ClassDefinition that carries all and only the information
    needed by the template
    """

    name: str
    bases: List[str] | str = PydanticBaseModel.default_name
    attributes: Optional[Dict[str, PydanticAttribute]] = None


class ObjectImport(TemplateModel):
    name: str
    alias: Optional[str] = None


class Import(TemplateModel):
    module: str
    alias: Optional[str] = None
    objects: Optional[List[ObjectImport]] = None

    def merge(self, other: "Import") -> List["Import"]:
        # return both if we are orthogonal
        if self.module != other.module:
            return [self, other]

        # handle conditionals
        if isinstance(self, ConditionalImport) and isinstance(other, ConditionalImport):
            # we don't have a good way of combining conditionals, update with the other
            return [other]
        elif isinstance(self, ConditionalImport) or isinstance(other, ConditionalImport):
            # conditionals and nonconditionals are orthogonal
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
    condition: str
    alternative: Import


class Imports(TemplateModel):
    """Container class for imports that can handle merging!"""

    imports: List[Import] = Field(default_factory=list)

    def __add__(self, other: Import) -> "Imports":
        # check if we have one of these already
        existing = [i for i in self.imports if i.module == other.module]

        # if we have nothing importing from this module yet, add it!
        if len(existing) == 0:
            self.imports.append(other)
        else:
            merged = []
            for e in existing:
                self.imports.remove(e)
                merged.extend(e.merge(other))
            self.imports.extend(merged)
        return self


class PydanticModule(TemplateModel):
    """
    Top-level container model for generating a pydantic module
    """

    metamodel_version: Optional[str] = None
    version: Optional[str] = None
    base_model: PydanticBaseModel = PydanticBaseModel()
    injected_classes: Optional[List[str]] = None
    imports: List[Import] = Field(default_factory=list)
    enums: Dict[str, Enum] = Field(default_factory=dict)
    classes: Dict[str, PydanticClass] = Field(default_factory=dict)
