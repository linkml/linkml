import os
from collections import defaultdict
from copy import deepcopy
from dataclasses import field, dataclass
from typing import Dict, List, TextIO, Union

import click
from jinja2 import Template
# from linkml.generators import pydantic_GEN_VERSION
from linkml_runtime.linkml_model.meta import (Annotation, ClassDefinition,
                                              EnumDefinition,
                                              EnumDefinitionName,
                                              SchemaDefinition, TypeDefinition)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments

default_template = """
{#-

  Jinja2 Template for a pydantic classes
-#}
from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel as BaseModel, Field

metamodel_version = "{{metamodel_version}}"
version = "{{version if version else None}}"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'
    
class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True, 
                validate_all = True, 
                underscore_attrs_are_private = True, 
                extra = {% if allow_extra %}'allow'{% else %}'forbid'{% endif %}, 
                arbitrary_types_allowed = True):
    pass                    

{% for e in enums.values() %}
class {{ e.name }}(str, Enum):
    {% if e.description -%}
    \"\"\"
    {{ e.description }}
    \"\"\"
    {%- endif %}
    {% for label, value in e['values'].items() -%}
    {{label}} = "{{value}}"
    {% endfor %}
    {% if not e['values'] -%}
    dummy = "dummy"
    {% endif %}
{% endfor %}

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
    {%- if predefined_slot_values[c.name][attr.name] -%} 
        {{ predefined_slot_values[c.name][attr.name] }}
    {%- else -%}
        None
    {%- endif -%}    
    {%- if attr.title != None %}, title="{{attr.title}}"{% endif -%}
    {%- if attr.description %}, description=\"\"\"{{attr.description}}\"\"\"{% endif -%}
    {%- if attr.minimum_value != None %}, ge={{attr.minimum_value}}{% endif -%}
    {%- if attr.maximum_value != None %}, le={{attr.maximum_value}}{% endif -%}
    )
    {% else -%}
    None
    {% endfor %}

{% endfor %}

# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
{% for c in schema.classes.values() -%} 
{{ c.name }}.update_forward_refs()
{% endfor %}
"""


def _get_pyrange(t: TypeDefinition, sv: SchemaView) -> str:
    pyrange = t.repr
    if pyrange is None:
        pyrange = t.base
    if t.base == "XSDDateTime":
        pyrange = "datetime "
    if t.base == "XSDDate":
        pyrange = "date"
    if pyrange is None and t.typeof is not None:
        pyrange = _get_pyrange(sv.get_type(t.typeof), sv)
    if pyrange is None:
        raise Exception(f"No python type for range: {s.range} // {t}")
    return pyrange


@dataclass
class PydanticGenerator(OOCodeGenerator):
    """
    Generates Pydantic-compliant classes from a schema

    This is an alternative to the dataclasses-based Pythongen
    """

    # ClassVar overrides
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["pydantic"]

    # ObjectVars
    template_file: str = None
    allow_extra: bool = field(default_factory=lambda: False)
    gen_mixin_inheritance: bool = field(default_factory=lambda: True)

    # ObjectVars (identical to pythongen)
    gen_classvars: bool = field(default_factory=lambda: True)
    gen_slots: bool = field(default_factory=lambda: True)
    genmeta: bool = field(default_factory=lambda: False)
    emit_metadata: bool = field(default_factory=lambda: True)


    def generate_enums(
        self, all_enums: Dict[EnumDefinitionName, EnumDefinition]
    ) -> Dict[str, dict]:
        # TODO: make an explicit class to represent how an enum is passed to the template
        enums = {}
        for enum_name, enum_orignal in all_enums.items():
            enum = {"name": camelcase(enum_name), "values": {}}

            for pv in enum_orignal.permissible_values.values():
                label = self.generate_enum_label(pv.text)
                enum["values"][label] = pv.text

            enums[enum_name] = enum

        return enums

    def sort_classes(self, clist: List[ClassDefinition]) -> List[ClassDefinition]:
        """
        sort classes such that if C is a child of P then C appears after P in the list

        Overridden method include mixin classes

        TODO: This should move to SchemaView
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
                raise ValueError(
                    f"could not find suitable element in {clist} that does not ref {slist}"
                )
        return slist

    def get_predefined_slot_values(self) -> Dict[str, Dict[str, str]]:
        """
        :return: Dictionary of dictionaries with predefined slot values for each class
        """
        sv = self.schemaview
        default_prefix = sv.schema.default_prefix
        slot_values = defaultdict(dict)
        for class_def in sv.all_classes().values():

            for slot_name in sv.class_slots(class_def.name):
                slot = sv.induced_slot(slot_name, class_def.name)
                if slot.designates_type:
                    slot_values[camelcase(class_def.name)][
                        slot.name
                    ] = f'"{default_prefix}:{camelcase(class_def.name)}"'
                    if slot.multivalued:
                        slot_values[camelcase(class_def.name)][slot.name] = (
                            "["
                            + slot_values[camelcase(class_def.name)][slot.name]
                            + "]"
                        )
                # Have a default factory of list for multivalued fields that don't
                # get any other sort of predefined value above this point
                elif slot.multivalued:
                    slot_values[camelcase(class_def.name)][
                        slot.name
                    ] = "default_factory=list"
        return slot_values

    def get_class_isa_plus_mixins(self) -> Dict[str, List[str]]:
        """
        Generate the inheritance list for each class from is_a plus mixins
        :return:
        """
        sv = self.schemaview
        parents = {}
        for class_def in sv.all_classes().values():
            class_parents = []
            if class_def.is_a:
                class_parents.append(camelcase(class_def.is_a))
            if self.gen_mixin_inheritance and class_def.mixins:
                class_parents.extend([camelcase(mixin) for mixin in class_def.mixins])
            if len(class_parents) > 0:
                # Use the sorted list of classes to order the parent classes, but reversed to match MRO needs
                class_parents.sort(key=lambda x: self.sorted_class_names.index(x))
                class_parents.reverse()
                parents[camelcase(class_def.name)] = class_parents
        return parents

    def get_mixin_identifier_range(self, mixin) -> str:
        sv = self.schemaview
        id_ranges = list(
            {
                _get_pyrange(sv.get_type(sv.get_identifier_slot(c).range), sv)
                for c in sv.class_descendants(mixin.name, mixins=True)
                if sv.get_identifier_slot(c) is not None
            }
        )
        if len(id_ranges) == 0:
            return None
        elif len(id_ranges) == 1:
            return id_ranges[0]
        else:
            return f"Union[{'.'.join(id_ranges)}]"

    def get_class_slot_range(self, slot):
        sv = self.schemaview
        range_cls = sv.get_class(slot.range)

        # Hardcoded handling for Any
        if range_cls.class_uri == "linkml:Any":
            return "Any"

        # Inline the class itself only if the class is defined as inline, or if the class has no
        # identifier slot and also isn't a mixin.
        if slot.inlined or (
            sv.get_identifier_slot(range_cls.name) is None
            and not sv.is_mixin(range_cls.name)
        ):
            return f"{camelcase(slot.range)}"

        # For the more difficult cases, set string as the default and attempt to improve it
        range_cls_identifier_slot_range = "str"

        # For mixins, try to use the identifier slot of descendant classes
        if (
            self.gen_mixin_inheritance
            and sv.is_mixin(range_cls.name)
            and sv.get_identifier_slot(range_cls.name)
        ):
            range_cls_identifier_slot_range = self.get_mixin_identifier_range(range_cls)

        # If the class itself has an identifier slot, it can be allowed to overwrite a value from mixin above
        if (
            sv.get_identifier_slot(range_cls.name) is not None
            and sv.get_identifier_slot(range_cls.name).range is not None
        ):
            range_cls_identifier_slot_range = _get_pyrange(
                sv.get_type(sv.get_identifier_slot(range_cls.name).range), sv
            )

        return range_cls_identifier_slot_range

    def serialize(self) -> str:
        sv = self.schemaview

        if self.template_file is not None:
            with open(self.template_file) as template_file:
                template_obj = Template(template_file.read())
        else:
            template_obj = Template(default_template)

        sv: SchemaView
        sv = self.schemaview
        schema = sv.schema
        # print(f'# SV c={sv.all_classes().keys()}')
        pyschema = SchemaDefinition(
            id=schema.id,
            name=schema.name,
            description=schema.description.replace('"', '\\"'),
        )
        enums = self.generate_enums(sv.all_enums())

        sorted_classes = self.sort_classes(list(sv.all_classes().values()))
        self.sorted_class_names = [camelcase(c.name) for c in sorted_classes]

        # Don't want to generate classes when class_uri is linkml:Any, will
        # just swap in typing.Any instead down below
        sorted_classes = [c for c in sorted_classes if c.class_uri != "linkml:Any"]

        for class_original in sorted_classes:
            class_def: ClassDefinition
            class_def = deepcopy(class_original)
            class_name = class_original.name
            class_def.name = camelcase(class_original.name)
            if class_def.is_a:
                class_def.is_a = camelcase(class_def.is_a)
            class_def.mixins = [camelcase(p) for p in class_def.mixins]
            if class_def.description:
                class_def.description = class_def.description.replace('"', '\\"')
            pyschema.classes[class_def.name] = class_def
            for attribute in list(class_def.attributes.keys()):
                del class_def.attributes[attribute]
            for sn in sv.class_slots(class_name):
                # TODO: fix runtime, copy should not be necessary
                s = deepcopy(sv.induced_slot(sn, class_name))
                # logging.error(f'Induced slot {class_name}.{sn} == {s.name} {s.range}')
                s.name = underscore(s.name)
                if s.description:
                    s.description = s.description.replace('"', '\\"')
                class_def.attributes[s.name] = s
                collection_key = None
                if s.range in sv.all_classes():
                    pyrange = self.get_class_slot_range(s)
                elif s.range in sv.all_enums():
                    pyrange = f"{camelcase(s.range)}"
                elif s.range in sv.all_types():
                    t = sv.get_type(s.range)
                    pyrange = _get_pyrange(t, sv)
                elif s.range is None:
                    pyrange = "str"
                else:
                    # TODO: default ranges in schemagen
                    # pyrange = 'str'
                    # logging.error(f'range: {s.range} is unknown')
                    raise Exception(f"range: {s.range}")
                if s.multivalued:
                    if collection_key is None:
                        pyrange = f"List[{pyrange}]"
                    else:
                        pyrange = f"Dict[{collection_key}, {pyrange}]"
                if not s.required:
                    pyrange = f"Optional[{pyrange}]"
                ann = Annotation("python_range", pyrange)
                s.annotations[ann.tag] = ann
        code = template_obj.render(
            schema=pyschema,
            underscore=underscore,
            enums=enums,
            predefined_slot_values=self.get_predefined_slot_values(),
            allow_extra=self.allow_extra,
            metamodel_version=self.schema.metamodel_version,
            version=self.schema.version,
            class_isa_plus_mixins=self.get_class_isa_plus_mixins(),
        )
        return code


@shared_arguments(PydanticGenerator)
@click.option(
    "--template_file", help="Optional jinja2 template to use for class generation"
)
@click.command()
def cli(
    yamlfile,
    template_file=None,
    head=True,
    emit_metadata=False,
    genmeta=False,
    classvars=True,
    slots=True,
    **args,
):
    """Generate pydantic classes to represent a LinkML model"""
    gen = PydanticGenerator(
        yamlfile,
        template_file=template_file,
        emit_metadata=head,
        genmeta=genmeta,
        gen_classvars=classvars,
        gen_slots=slots,
        **args,
    )
    print(gen.serialize())


if __name__ == "__main__":
    cli()
