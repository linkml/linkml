import logging
import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import (Callable, Dict, Iterator, List, Optional, Set, TextIO,
                    Tuple, Union)

import click
import pkg_resources
from jinja2 import Environment, FileSystemLoader, Template
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model.meta import (Annotation, ClassDefinition,
                                              ClassDefinitionName, Definition,
                                              DefinitionName, Element,
                                              EnumDefinition, SchemaDefinition,
                                              SlotDefinition,
                                              SlotDefinitionName,
                                              TypeDefinition)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

type_map = {
    "str": "string",
    "int": "number",
    "Bool": "boolean",
    "float": "number",
    "XSDDate": "date",
}

default_template = """
{%- for c in view.all_classes().values() -%}
{%- set cref = gen.classref(c) -%}
{% if cref -%}
export type {{cref}} = string
{% endif -%}
{%- endfor -%}

{% for c in view.all_classes().values() -%}
{%- if c.description -%}
/**
 * {{c.description}}
 */
{%- endif -%} 
{% set parents = gen.parents(c) %}
export interface {{gen.name(c)}} {% if parents %} extends {{parents|join(', ')}} {% endif %} {
    {%- for sn in view.class_slots(c.name, direct=False) %}
    {% set s = view.induced_slot(sn, c.name) %}
    {%- if s.description -%}
    /**
     * {{s.description}}
     */
     {%- endif -%}
    {{gen.name(s)}}?: {{gen.range(s)}},
    {%- endfor %}
}
{% endfor %}
"""


@dataclass
class TypescriptGenerator(Generator):
    """
    Generates typescript from a schema
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["text"]
    uses_schemaloader = False

    def serialize(self) -> str:
        """
        Serialize a schema to typescript string
        :return:
        """
        template_obj = Template(default_template)
        out_str = template_obj.render(
            gen=self, schema=self.schemaview.schema, view=self.schemaview
        )
        return out_str

    def name(self, element: Element) -> str:
        """
        Returns the name of the element in its canonical form

        :param element:
        :return:
        """
        alias = element.name
        if isinstance(element, SlotDefinition) and element.alias:
            alias = element.alias
        if type(element).class_name == "slot_definition":
            return underscore(alias)
        else:
            return camelcase(alias)

    def classref(self, cls: ClassDefinition) -> Optional[str]:
        """
        Returns the class name for the class that holds a reference (foreign key) to members of this class

        E.g. if a class Person has an identifier field called unique_id, then this will
        return PersonUniqueId

        :param cls:
        :return: ref name, None if no identifier
        """
        id_slot = self.get_identifier_or_key_slot(cls.name)
        if id_slot:
            return f"{self.name(cls)}{camelcase(id_slot.name)}"
        else:
            return None

    def get_identifier_or_key_slot(
        self, cn: ClassDefinitionName
    ) -> Optional[SlotDefinition]:
        sv = self.schemaview
        id_slot = sv.get_identifier_slot(cn)
        if id_slot:
            return id_slot
        else:
            for s in sv.class_induced_slots(cn):
                if s.key:
                    return s
            return None

    def range(self, slot: SlotDefinition) -> str:
        sv = self.schemaview
        r = slot.range
        if r in sv.all_classes():
            rc = sv.get_class(r)
            rc_ref = self.classref(rc)
            rc_name = self.name(rc)
            id_slot = self.get_identifier_or_key_slot(r)
            if slot.multivalued:
                if not id_slot or slot.inlined:
                    if slot.inlined_as_list or not id_slot:
                        return f"{rc_name}[]"
                    else:
                        return f"{{[index: {rc_ref}]: {rc_name} }}"
                else:
                    return f"{rc_ref}[]"
            else:
                if not id_slot or slot.inlined:
                    return rc_name
                else:
                    return f"{rc_ref}"
        else:
            if r in sv.all_types():
                t = sv.get_type(r)
                if t.base and t.base in type_map:
                    return type_map[t.base]
                else:
                    logging.warning(f"Unknown type.base: {t.name}")
            return "string"

    def parents(self, cls: ClassDefinition) -> List[ClassDefinitionName]:
        if cls.is_a:
            parents = [cls.is_a]
        else:
            parents = []
        return [ClassDefinitionName(camelcase(p)) for p in parents + cls.mixins]


@shared_arguments(TypescriptGenerator)
@click.version_option(__version__, "-V", "--version")
@click.command()
def cli(yamlfile, **args):
    """Generate typescript interfaces and types

    See https://linkml.io/linkml-runtime.js
    """
    gen = TypescriptGenerator(yamlfile, **args)
    print(gen.serialize())


if __name__ == "__main__":
    cli()
