import os
from copy import deepcopy
from typing import Union, TextIO, Dict

import click
from jinja2 import Template
# from linkml.generators import pydantic_GEN_VERSION
from linkml_runtime.linkml_model.meta import SchemaDefinition, TypeDefinition, ClassDefinition, Annotation, \
    EnumDefinitionName, EnumDefinition
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
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

metamodel_version = {{metamodel_version}}
version = {{version if version else None}}

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
{% endfor %}

{% for c in schema.classes.values() %}
class {{ c.name }}( 
                   {%- if c.is_a %}{{c.is_a}}{% else %}BaseModel{% endif -%}
                   {#- {%- for p in c.mixins %}, "{{p}}" {% endfor -%} -#} 
                  ):
    {% if c.description -%}
    \"\"\"
    {{ c.description }}
    \"\"\"
    {%- endif %}
    {% for attr in c.attributes.values() -%}
    {{attr.name}}: {{ attr.annotations['python_range'].value }} = Field(None
    {%- if attr.title != None %}, title="{{attr.title}}"{% endif -%}
    {%- if attr.description %}, description=\"\"\"{{attr.description}}\"\"\"{% endif -%}
    {%- if attr.minimum_value != None %}, ge={{attr.minimum_value}}{% endif -%}
    {%- if attr.maximum_value != None %}, le={{attr.maximum_value}}{% endif -%}
    )
    {% endfor %}
    {% if not c.attributes %}
    None
    {% endif %}
{% endfor %}

{% for c in schema.classes.values() %}
{{ c.name }}.update_forward_refs()
{% endfor %}
"""

def _get_pyrange(t: TypeDefinition, sv: SchemaView) -> str:
    pyrange = t.repr
    if pyrange is None:
        pyrange = t.base
    if t.base == 'XSDDateTime':
        pyrange = 'datetime '
    if t.base == 'XSDDate':
        pyrange = 'date'
    if pyrange is None and t.typeof is not None:
        pyrange = _get_pyrange(sv.get_type(t.typeof), sv)
    if pyrange is None:
        raise Exception(f'No python type for range: {s.range} // {t}')
    return pyrange


class PydanticGenerator(OOCodeGenerator):
    generatorname = os.path.basename(__file__)
    generatorversion = '0.0.1'
    valid_formats = ['pydantic']
    visit_all_class_slots = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition],
                 template_file: str = None,
                 format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.template_file = template_file

    def map_type(self, t: TypeDefinition) -> str:
        return TYPEMAP.get(t.base, t.base)

    def generate_enums(self, all_enums: Dict[EnumDefinitionName, EnumDefinition]) -> Dict[str, dict]:
        # TODO: make an explicit class to represent how an enum is passed to the template
        enums = {}
        for enum_name, enum_orignal in all_enums.items():
            enum = {}
            enum['name'] = camelcase(enum_name)

            enum['values'] = {}
            for pv in enum_orignal.permissible_values.values():
                label = self.generate_enum_label(pv.text)
                enum['values'][label] = pv.text

            enums[enum_name] = enum

        return enums

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
        #print(f'# SV c={sv.all_classes().keys()}')
        pyschema = SchemaDefinition(id=schema.id, name=schema.name, description=schema.description)

        enums = self.generate_enums(sv.all_enums())

        for class_name, class_original in sv.all_classes().items():
            class_def: ClassDefinition
            class_def = deepcopy(class_original)
            class_def.name = camelcase(class_original.name)
            if class_def.is_a:
                class_def.is_a = camelcase(class_def.is_a)
            class_def.mixins = [camelcase(p) for p in class_def.mixins]
            pyschema.classes[class_def.name] = class_def
            for attribute in list(class_def.attributes.keys()):
                del class_def.attributes[attribute]
            for sn in sv.class_slots(class_name):
                # TODO: fix runtime, copy should not be necessary
                s = deepcopy(sv.induced_slot(sn, class_name))
                # logging.error(f'Induced slot {class_name}.{sn} == {s.name} {s.range}')
                s.name = underscore(s.name)
                class_def.attributes[s.name] = s
                collection_key = None
                if s.range in sv.all_classes():
                    range_cls = sv.get_class(s.range)
                    #pyrange = f'"{camelcase(s.range)}"'
                    if s.inlined or sv.get_identifier_slot(range_cls.name) is None:
                        pyrange = f'{camelcase(s.range)}'
                        if sv.get_identifier_slot(range_cls.name) is not None and not s.inlined_as_list:
                            #collection_type = sv.get_identifier_slot(range_cls.name).range
                            collection_type = 'str'
                    else:
                        pyrange = 'str'
                elif s.range in sv.all_enums():
                    pyrange = f'{camelcase(s.range)}'
                elif s.range in sv.all_types():
                    t = sv.get_type(s.range)
                    pyrange = _get_pyrange(t, sv)
                elif s.range is None:
                    pyrange = 'str'
                else:
                    # TODO: default ranges in schemagen
                    #pyrange = 'str'
                    #logging.error(f'range: {s.range} is unknown')
                    raise Exception(f'range: {s.range}')
                if s.multivalued:
                    if collection_key is None:
                        pyrange = f'List[{pyrange}]'
                    else:
                        pyrange = f'Dict[{collection_key}, {pyrange}]'
                if not s.required:
                    pyrange = f'Optional[{pyrange}]'
                ann = Annotation('python_range', pyrange)
                s.annotations[ann.tag] = ann
        code = template_obj.render(schema=pyschema, underscore=underscore, enums=enums, metamodel_version=self.schema.metamodel_version, version=self.schema.version)
        return code


@shared_arguments(PydanticGenerator)
@click.option("--template_file", help="Optional jinja2 template to use for class generation")
@click.command()
def cli(yamlfile, template_file=None, head=True, emit_metadata=False, genmeta=False, classvars=True, slots=True, **args):
    """Generate pydantic classes to represent a LinkML model"""
    gen = PydanticGenerator(yamlfile, template_file=template_file, emit_metadata=head, genmeta=genmeta, gen_classvars=classvars, gen_slots=slots,  **args)
    print(gen.serialize())


if __name__ == '__main__':
    cli()
