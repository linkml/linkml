import logging
import os
import logging
from collections import defaultdict
from copy import deepcopy
from dataclasses import field, dataclass
from types import ModuleType
from typing import Dict, List, TextIO, Union, Optional, Set

from linkml_runtime.utils.compile_python import compile_python

from linkml.utils.ifabsent_functions import ifabsent_value_declaration

import click
from jinja2 import Template
# from linkml.generators import pydantic_GEN_VERSION
from linkml_runtime.linkml_model.meta import (Annotation,
                                              AnonymousSlotExpression,
                                              ClassDefinition, EnumDefinition,
                                              EnumDefinitionName,
                                              SchemaDefinition, SlotDefinition,
                                              TypeDefinition)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.generators.common.type_designators import (
    get_accepted_type_designator_values, get_type_designator_value)
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments
from linkml.utils.ifabsent_functions import ifabsent_value_declaration

default_template = """
{#-

  Jinja2 Template for a pydantic classes
-#}
from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel as BaseModel, Field
from linkml_runtime.linkml_model import Decimal
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


metamodel_version = "{{metamodel_version}}"
version = "{{version if version else None}}"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True,
                validate_all = True,
                underscore_attrs_are_private = True,
                extra = {% if allow_extra %}'allow'{% else %}'forbid'{% endif %},
                arbitrary_types_allowed = True,
                use_enum_values = True):
    pass

{% for e in enums.values() %}
class {{ e.name }}(str, Enum):
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
    {%- elif attr.required -%}
        ...
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
    pyrange = t.repr if t is not None else None
    if pyrange is None:
        pyrange = t.base
    if t.base == "XSDDateTime":
        pyrange = "datetime "
    if t.base == "XSDDate":
        pyrange = "date"
    if pyrange is None and t.typeof is not None:
        pyrange = _get_pyrange(sv.get_type(t.typeof), sv)
    if pyrange is None:
        raise Exception(f"No python type for range: {t.name} // {t}")
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

    def compile_module(self, **kwargs) -> ModuleType:
        """
        Compiles generated python code to a module
        :return:
        """
        pycode = self.serialize(**kwargs)
        try:
            return compile_python(pycode)
        except NameError as e:
            logging.error(f"Code:\n{pycode}")
            logging.error(f"Error compiling generated python code: {e}")
            raise e

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
        slot_values = defaultdict(dict)
        for class_def in sv.all_classes().values():
            for slot_name in sv.class_slots(class_def.name):
                slot = sv.induced_slot(slot_name, class_def.name)
                if slot.designates_type:
                    target_value = get_type_designator_value(sv, slot, class_def)
                    slot_values[camelcase(class_def.name)][
                        slot.name
                    ] = f'"{target_value}"'
                    if slot.multivalued:
                        slot_values[camelcase(class_def.name)][slot.name] = (
                            "["
                            + slot_values[camelcase(class_def.name)][slot.name]
                            + "]"
                        )
                    slot_values[camelcase(class_def.name)][slot.name] = slot_values[
                        camelcase(class_def.name)
                    ][slot.name]
                elif slot.ifabsent is not None:
                    value = ifabsent_value_declaration(
                        slot.ifabsent, sv, class_def, slot
                    )
                    slot_values[camelcase(class_def.name)][slot.name] = value
                # Multivalued slots that are either not inlined (just an identifier) or are
                # inlined as lists should get default_factory list, if they're inlined but
                # not as a list, that means a dictionary
                elif slot.multivalued:
                    has_identifier_slot = self.range_class_has_identifier_slot(slot)

                    if (
                        slot.inlined
                        and not slot.inlined_as_list
                        and has_identifier_slot
                    ):
                        slot_values[camelcase(class_def.name)][
                            slot.name
                        ] = "default_factory=dict"
                    else:
                        slot_values[camelcase(class_def.name)][
                            slot.name
                        ] = "default_factory=list"

        return slot_values

    def range_class_has_identifier_slot(self, slot):
        """
        Check if the range class of a slot has an identifier slot, via both slot.any_of and slot.range
        Should return False if the range is not a class, and also if the range is a class but has no
        identifier slot

        :param slot: SlotDefinition
        :return: bool
        """
        sv = self.schemaview
        has_identifier_slot = False
        if slot.any_of:
            for slot_range in slot.any_of:
                any_of_range = slot_range.range
                if (
                    any_of_range in sv.all_classes()
                    and sv.get_identifier_slot(any_of_range, use_key=True) is not None
                ):
                    has_identifier_slot = True
        if (
            slot.range in sv.all_classes()
            and sv.get_identifier_slot(slot.range, use_key=True) is not None
        ):
            has_identifier_slot = True
        return has_identifier_slot

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

    def get_class_slot_range(
        self, slot_range: str, inlined: bool, inlined_as_list: bool
    ) -> str:
        sv = self.schemaview
        range_cls = sv.get_class(slot_range)

        # Hardcoded handling for Any
        if range_cls.class_uri == "linkml:Any":
            return "Any"

        # Inline the class itself only if the class is defined as inline, or if the class has no
        # identifier slot and also isn't a mixin.
        if (
            inlined
            or inlined_as_list
            or (
                sv.get_identifier_slot(range_cls.name, use_key=True) is None
                and not sv.is_mixin(range_cls.name)
            )
        ):
            if (
                len(
                    [x for x in sv.class_induced_slots(slot_range) if x.designates_type]
                )
                > 0
                and len(sv.class_descendants(slot_range)) > 1
            ):
                return (
                    f"Union["
                    + ",".join([camelcase(c) for c in sv.class_descendants(slot_range)])
                    + "]"
                )
            else:
                return f"{camelcase(slot_range)}"

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

    def generate_python_range(
        self, slot_range, slot_def: SlotDefinition, class_def: ClassDefinition
    ) -> str:
        """
        Generate the python range for a slot range value
        """
        sv = self.schemaview

        if slot_def.designates_type:
            pyrange = (
                "Literal["
                + ",".join(
                    [
                        '"' + x + '"'
                        for x in get_accepted_type_designator_values(
                            sv, slot_def, class_def
                        )
                    ]
                )
                + "]"
            )
        elif slot_range in sv.all_classes():
            pyrange = self.get_class_slot_range(
                slot_range,
                inlined=slot_def.inlined,
                inlined_as_list=slot_def.inlined_as_list,
            )
        elif slot_range in sv.all_enums():
            pyrange = f"{camelcase(slot_range)}"
        elif slot_range in sv.all_types():
            t = sv.get_type(slot_range)
            pyrange = _get_pyrange(t, sv)
        elif slot_range is None:
            pyrange = "str"
        else:
            # TODO: default ranges in schemagen
            # pyrange = 'str'
            # logging.error(f'range: {s.range} is unknown')
            raise Exception(f"range: {slot_range}")
        return pyrange

    def generate_collection_key(
        self,
        slot_ranges: List[str],
        slot_def: SlotDefinition,
        class_def: ClassDefinition,
    ) -> Optional[str]:
        """
        Find the python range value (str, int, etc) for the identifier slot
        of a class used as a slot range.

        If a pyrange value matches a class name, the range of the identifier slot
        will be returned. If more than one match is found and they don't match,
        an exception will be raised.

        :param slot_ranges: list of python range values
        """

        collection_keys: Set[str] = set()

        if slot_ranges is None:
            return None

        for slot_range in slot_ranges:
            if slot_range is None or slot_range not in self.schemaview.all_classes():
                continue  # ignore non-class ranges

            identifier_slot = self.schemaview.get_identifier_slot(slot_range, use_key=True)
            if identifier_slot is not None:
                collection_keys.add(
                    self.generate_python_range(
                        identifier_slot.range, slot_def, class_def
                    )
                )
        if len(collection_keys) > 1:
            raise Exception(
                f"Slot with any_of range has multiple identifier slot range types: {collection_keys}"
            )
        if len(collection_keys) == 1:
            return list(collection_keys)[0]
        return None

    def serialize(self) -> str:
        if self.template_file is not None:
            with open(self.template_file) as template_file:
                template_obj = Template(template_file.read())
        else:
            template_obj = Template(default_template)

        sv: SchemaView
        sv = self.schemaview
        schema = sv.schema
        pyschema = SchemaDefinition(
            id=schema.id,
            name=schema.name,
            description=schema.description.replace('"', '\\"')
            if schema.description
            else None,
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

                slot_ranges: List[str] = []

                # Confirm that the original slot range (ignoring the default that comes in from
                # induced_slot) isn't in addition to setting any_of
                if len(s.any_of) > 0 and sv.get_slot(sn).range is not None:
                    raise ValueError("Slot cannot have both range and any_of defined")

                if s.any_of is not None and len(s.any_of) > 0:
                    # list comprehension here is pulling ranges from within AnonymousSlotExpression
                    slot_ranges.extend([r.range for r in s.any_of])
                else:
                    slot_ranges.append(s.range)

                pyranges = [
                    self.generate_python_range(slot_range, s, class_def)
                    for slot_range in slot_ranges
                ]

                pyranges = list(set(pyranges))  # remove duplicates
                pyranges.sort()

                if len(pyranges) == 1:
                    pyrange = pyranges[0]
                elif len(pyranges) > 1:
                    pyrange = f"Union[{', '.join(pyranges)}]"
                else:
                    raise Exception(
                        f"Could not generate python range for {class_name}.{s.name}"
                    )

                if s.multivalued:
                    if s.inlined or s.inlined_as_list:
                        collection_key = self.generate_collection_key(
                            slot_ranges, s, class_def
                        )
                    else:
                        collection_key = None
                    if (
                        s.inlined == False
                        or collection_key is None
                        or s.inlined_as_list == True
                    ):
                        pyrange = f"List[{pyrange}]"
                    else:
                        pyrange = f"Dict[{collection_key}, {pyrange}]"
                if not s.required and not s.designates_type:
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

    def default_value_for_type(self, typ: str) -> str:
        return "None"


@shared_arguments(PydanticGenerator)
@click.option(
    "--template_file", help="Optional jinja2 template to use for class generation"
)
@click.version_option(__version__, "-V", "--version")
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
