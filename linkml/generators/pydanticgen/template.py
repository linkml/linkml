import inspect
from typing import ClassVar, Dict, Optional, List, Union, Type
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from pydantic import BaseModel, Field
from pydantic.version import VERSION as PYDANTIC_VERSION


class TemplateModel(BaseModel):
    """Metaclass to group template models"""

    pydantic_ver: Literal[1, 2] = int(PYDANTIC_VERSION[0])


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


class BaseModel(TemplateModel):
    name: ClassVar[str] = "ConfiguredBaseModel"
    extra_fields: Literal["allow", "forbid", "ignore"] = "forbid"
    fields: Optional[List[str]] = None


class PydanticAttribute(TemplateModel):
    """
    Reduced version of SlotDefinition that carries all and only the information
    needed by the template
    """

    required: bool = False
    identifier: bool = False
    key: bool = False
    predefined: Optional[str] = None
    """Fixed string to use in body of field"""

    @property
    def field(self) -> str:
        """Computed value to use inside of the generated Field"""
        if self.predefined:
            return self.predefined
        elif self.required or self.identifier or self.key:
            return "..."
        else:
            return "None"


class PydanticClass(TemplateModel):
    """
    Reduced version of ClassDefinition that carries all and only the information
    needed by the template
    """

    name: str
    bases: List[str] = Field(default_factory=lambda: list(BaseModel.name))
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
    base_model: BaseModel = BaseModel()
    injected_classes: Optional[List[str]] = None
    imports: List[Import] = Field(default_factory=list)
    enums: Dict[str, Enum] = Field(default_factory=dict)
    classes: Dict[str, PydanticClass] = Field(default_factory=dict)


def default_template(
    pydantic_ver: str = "1", extra_fields: str = "forbid", injected_classes: Optional[List[Union[Type, str]]] = None
) -> str:
    """Constructs a default template for pydantic classes based on the version of pydantic"""
    ### HEADER ###
    template = """
{#-

  Jinja2 Template for a pydantic classes
-#}
from __future__ import annotations
from datetime import datetime, date
from enum import Enum
{% if uses_numpy -%}
import numpy as np
{%- endif %}
from decimal import Decimal
from typing import List, Dict, Optional, Any, Union"""
    if pydantic_ver == "1":
        template += """
from pydantic import BaseModel as BaseModel, Field, validator"""
    elif pydantic_ver == "2":
        template += """
from pydantic import BaseModel as BaseModel, ConfigDict,  Field, field_validator"""
    template += """
import re
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

{% if imports is not none %}
{%- for import_module, import_classes in imports.items() -%}
{% if import_classes is none -%}
import {{ import_module }}
{% elif import_classes is mapping -%}
import {{ import_module }} as {{ import_classes['as'] }}
{% else -%}
from {{ import_module }} import (
    {% for imported_class in import_classes %}
    {%- if imported_class is string -%}
    {{ imported_class }}
    {%- else -%}
    {{ imported_class['name'] }} as {{ imported_class['as'] }}
    {%- endif -%}
    {%- if not loop.last %},{{ '\n    ' }}{% else %}{{ '\n' }}{%- endif -%}
    {% endfor -%}
)
{% endif -%}
{% endfor -%}
{% endif %}
metamodel_version = "{{metamodel_version}}"
version = "{{version if version else None}}"
"""
    ### BASE MODEL ###
    if pydantic_ver == "1":
        template += f"""
class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True,
                validate_all = True,
                underscore_attrs_are_private = True,
                extra = '{extra_fields}',
                arbitrary_types_allowed = True,
                use_enum_values = True):
"""
    else:
        template += f"""
class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra = '{extra_fields}',
        arbitrary_types_allowed=True,
        use_enum_values = True)
"""

    ### Fields injected into base model
    template += """{% if injected_fields is not none %}
    {% for field in injected_fields -%}
    {{ field }}
    {% endfor %}
{% else %}
    pass
{% endif %}
        """

    ### Extra classes
    if injected_classes is not None and len(injected_classes) > 0:
        template += """{{ '\n\n' }}"""
        for cls in injected_classes:
            if isinstance(cls, str):
                template += cls + "\n\n"
            else:
                template += inspect.getsource(cls) + "\n\n"

    ### ENUMS ###
    template += """
{% for e in enums.values() %}
class {{ e.name }}(str{% if e['values'] %}, Enum{% endif %}):
    {% if e.description -%}
    \"\"\"
    {{ e.description }}
    \"\"\"
    {%- endif %}
    {% for _, pv in e['values'].items() -%}
    {% if pv.description -%}
    # {{pv.description}}
    {%- endif %}
    {{pv.label}} = "{{pv.value}}"
    {% endfor %}
    {% if not e['values'] -%}
    dummy = "dummy"
    {% endif %}
{% endfor %}
"""
    ### CLASSES ###
    if pydantic_ver == "1":
        template += """
{%- for c in schema.classes.values() %}
class {{ c.name }}
    {%- if class_isa_plus_mixins[c.name] -%}
        ({{class_isa_plus_mixins[c.name]|join(', ')}})
    {%- else -%}
        (ConfiguredBaseModel)
    {%- endif -%}
                  :
    {% if c.description -%}
    \"\"\"
    {{ c.description }}
    \"\"\"
    {%- endif %}
    {% for attr in c.attributes.values() if c.attributes -%}
    {{attr.name}}: {{ attr.annotations['python_range'].value }} = Field(
    {%- if predefined_slot_values[c.name][attr.name] is not callable -%}
        {{ predefined_slot_values[c.name][attr.name] }}
    {%- elif (attr.required or attr.identifier or attr.key) -%}
        ...
    {%- else -%}
        None
    {%- endif -%}
    {%- if attr.title != None %}, title="{{attr.title}}"{% endif -%}
    {%- if attr.description %}, description=\"\"\"{{attr.description}}\"\"\"{% endif -%}
    {%- if attr.equals_number != None %}, le={{attr.equals_number}}, ge={{attr.equals_number}}
    {%- else -%}
     {%- if attr.minimum_value != None %}, ge={{attr.minimum_value}}{% endif -%}
     {%- if attr.maximum_value != None %}, le={{attr.maximum_value}}{% endif -%}
    {%- endif -%}
    )
    {% else -%}
    None
    {% endfor %}
    {% for attr in c.attributes.values() if c.attributes -%}
    {%- if attr.pattern %}
    @validator('{{attr.name}}', allow_reuse=True)
    def pattern_{{attr.name}}(cls, v):
        pattern=re.compile(r"{{attr.pattern}}")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid {{attr.name}} format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid {{attr.name}} format: {v}")
        return v
    {% endif -%}
    {% endfor %}
{% endfor %}
"""
    elif pydantic_ver == "2":
        template += """
{%- for c in schema.classes.values() %}
class {{ c.name }}
    {%- if class_isa_plus_mixins[c.name] -%}
        ({{class_isa_plus_mixins[c.name]|join(', ')}})
    {%- else -%}
        (ConfiguredBaseModel)
    {%- endif -%}
                  :
    {% if c.description -%}
    \"\"\"
    {{ c.description }}
    \"\"\"
    {%- endif %}
    {% for attr in c.attributes.values() if c.attributes -%}
    {{attr.name}}: {{ attr.annotations['python_range'].value }} = Field(
    {%- if predefined_slot_values[c.name][attr.name] is not callable -%}
        {{ predefined_slot_values[c.name][attr.name] }}
    {%- elif (attr.required or attr.identifier or attr.key) -%}
        ...
    {%- else -%}
        None
    {%- endif -%}
    {%- if attr.title != None %}, title="{{attr.title}}"{% endif -%}
    {%- if attr.description %}, description=\"\"\"{{attr.description}}\"\"\"{% endif -%}
    {%- if attr.equals_number != None %}, le={{attr.equals_number}}, ge={{attr.equals_number}}
    {%- else -%}
     {%- if attr.minimum_value != None %}, ge={{attr.minimum_value}}{% endif -%}
     {%- if attr.maximum_value != None %}, le={{attr.maximum_value}}{% endif -%}
    {%- endif -%}
    )
    {% else -%}
    None
    {% endfor %}
    {% for attr in c.attributes.values() if c.attributes -%}
    {%- if attr.pattern %}
    @field_validator('{{attr.name}}')
    def pattern_{{attr.name}}(cls, v):
        pattern=re.compile(r"{{attr.pattern}}")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid {{attr.name}} format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid {{attr.name}} format: {v}")
        return v
    {% endif -%}
    {% endfor %}
{% endfor %}
"""

    ### FWD REFS / REBUILD MODEL ###
    if pydantic_ver == "1":
        template += """
# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
{% for c in schema.classes.values() -%}
{{ c.name }}.update_forward_refs()
{% endfor %}
"""
    else:
        template += """
# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
{% for c in schema.classes.values() -%}
{{ c.name }}.model_rebuild()
{% endfor %}
"""
    return template
