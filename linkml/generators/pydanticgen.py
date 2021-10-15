import os
import logging
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set
from copy import copy, deepcopy

import click
from jinja2 import Template

from linkml_runtime.utils.schemaview import SchemaView

#from linkml.generators import pydantic_GEN_VERSION
from linkml_runtime.linkml_model.meta import SchemaDefinition, TypeDefinition, ClassDefinition, Annotation
from linkml_runtime.utils.formatutils import camelcase, underscore

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

{% for e in schema.enums.values() %}
class {{ e.name }}(str, Enum):
    {% if e.description -%}
    \"\"\"
    {{ e.description }}
    \"\"\"
    {%- endif %}
    {% for pv in e.permissible_values.values() -%}
    {{underscore(pv.text)}} = "{{pv.text}}"
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
    {%- if attr.description %}, description="{{attr.description}}"{% endif -%}
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
                 package: str = None,
                 template_file: str = None,
                 format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.package = package
        self.template_file = template_file

    def map_type(self, t: TypeDefinition) -> str:
        return TYPEMAP.get(t.base, t.base)

    def serialize(self, directory: str = None) -> None:
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
        for en, e in sv.all_enums().items():
            e2: ClassDefinition
            e2 = deepcopy(e)
            e2.name = camelcase(e.name)
            pyschema.enums[e2.name] = e2

        for cn, c in sv.all_classes().items():
            c2: ClassDefinition
            c2 = deepcopy(c)
            c2.name = camelcase(c.name)
            if c2.is_a:
                c2.is_a = camelcase(c2.is_a)
            c2.mixins = [camelcase(p) for p in c2.mixins]
            pyschema.classes[c2.name] = c2
            for a in list(c2.attributes.keys()):
                del c2.attributes[a]
            for sn in sv.class_slots(cn):
                s = sv.induced_slot(sn, cn)
                s.name = underscore(s.name)
                c2.attributes[s.name] = s
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
        code = template_obj.render(schema=pyschema, underscore=underscore)
        return code


@shared_arguments(PydanticGenerator)
@click.option("--output_directory", default="output", help="Output directory for individually generated class files")
@click.option("--package", help="Package name where relevant for generated class files")
@click.option("--template_file", help="Optional jinja2 template to use for class generation")
@click.command()
def cli(yamlfile, output_directory=None, package=None, template_file=None, head=True, emit_metadata=False, genmeta=False, classvars=True, slots=True, **args):
    """Generate pydantic classes to represent a LinkML model"""
    gen = PydanticGenerator(yamlfile, package=package, template_file=template_file, emit_metadata=head, genmeta=genmeta, gen_classvars=classvars, gen_slots=slots,  **args)
    print(gen.serialize(output_directory))


if __name__ == '__main__':
    cli()
