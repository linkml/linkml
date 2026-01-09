import logging
import os
from dataclasses import dataclass
from typing import Optional

import click
from jinja2 import Template

from linkml._version import __version__
from linkml.generators.common.subproperty import get_subproperty_values, is_uri_range
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    Element,
    SlotDefinition,
    SlotDefinitionName,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)


type_map = {
    "str": "string",
    "int": "number",
    "Bool": "boolean",
    "float": "number",
    "XSDDate": "date",
}

type_init_map = {
    "str": "''",
    "int": "0",
    "Bool": "false",
    "float": "0.0",
    "XSDDate": "new Date()",
}

default_template = """
{%- for c in view.all_classes().values() -%}
{%- set cref = gen.classref(c) -%}
{% if cref -%}
export type {{cref}} = string;
{% endif -%}
{%- endfor -%}

{% for e in enums.values() %}
{%- if e.description -%}
/**
* {{e.description}}
*/
{%- endif %}
export enum {{e.name}} {
    {% if not e.values -%}
    dummy = "dummy"
    {%- endif %}
    {%- for _, pv in e['values'].items() %}
    {% if pv.description -%}
    /** {{pv.description}} */
    {% endif -%}
    {{pv.label}} = "{{pv.value}}",
    {%- endfor %}
};
{% endfor %}

{% for c in view.all_classes().values() -%}
{%- if c.description -%}
/**
 * {{c.description}}
 */
{%- endif -%}
{% set parents = gen.parents(c) %}
export interface {{gen.name(c)}} {%- if parents %} extends {{parents|join(', ')}} {%- endif %} {
    {%- for sn in view.class_slots(c.name, direct=not(gen.include_induced_slots)) %}
    {% set s = view.induced_slot(sn, c.name) %}
    {%- if s.description -%}
    /** {{s.description}} */
    {% endif -%}
    {{gen.name(s)}}{%- if not s.required -%}?{%- endif -%}: {{gen.range(s)}},
    {%- endfor %}
}

{% if gen.gen_type_utils %}
export function is{{gen.name(c)}}(o: object): o is {{gen.name(c)}} {
    {%- set rcs = gen.required_slots(c) %}
    {%- set comp = "&&" if rcs else "||" %}
    {%- set cs = rcs if rcs else view.class_slots(c.name, direct=False) %}
    return (
        {%- for sn in cs %}
        '{{sn}}' in o {%- if not loop.last %} {{comp}}{% endif -%}
        {%- endfor %}
    )
}

export function to{{gen.name(c)}}(o: {{gen.name(c)}}): {{gen.name(c)}} {
    return {
        {%- for sn in view.class_slots(c.name, direct=False) %}
        {%- set s = view.induced_slot(sn, c.name) %}
        {{sn}}: o.{{sn}} ?? {{gen.init_range(s)}}{%- if not loop.last %},{%- endif -%}
        {%- endfor %}
    }
}
{% endif %}
{% endfor %}
"""


@dataclass
class TypescriptGenerator(OOCodeGenerator):
    """
    Generates typescript from a schema
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["text"]
    uses_schemaloader = False

    # ObjectVars
    gen_type_utils: bool = False
    include_induced_slots: bool = False
    expand_subproperty_of: bool = True
    """If True, expand subproperty_of to union types with slot descendants"""

    def serialize(self, output=None) -> str:
        """Serialize a schema to typescript string"""

        sv: SchemaView = self.schemaview
        enums = self.generate_enums(sv.all_enums())
        template_obj = Template(default_template)
        out_str = template_obj.render(
            gen=self,
            schema=self.schemaview.schema,
            view=self.schemaview,
            enums=enums,
        )
        if output is not None:
            with open(output, "w") as out:
                out.write(out_str)
        return out_str

    @staticmethod
    def name(element: Element) -> str:
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

    def get_identifier_or_key_slot(self, cn: ClassDefinitionName) -> Optional[SlotDefinition]:
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

        # Check for subproperty_of constraint first
        if self.expand_subproperty_of and slot.subproperty_of:
            subproperty_type = self._get_subproperty_union_type(slot)
            if subproperty_type:
                if slot.multivalued:
                    return f"({subproperty_type})[]"
                return subproperty_type

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
                tsrange = "string"
                if t.base and t.base in type_map:
                    tsrange = type_map[t.base]
                elif t.typeof and t.typeof in type_map:
                    tsrange = type_map[t.typeof]
                else:
                    logger.warning(f"Unknown type.base: {t.name}")
                if slot.multivalued:
                    tsrange = f"{tsrange}[]"
                return tsrange
            return "string"

    def init_range(self, slot: SlotDefinition) -> str:
        sv = self.schemaview
        r = slot.range
        if r in sv.all_classes():
            id_slot = self.get_identifier_or_key_slot(r)
            if slot.multivalued:
                if not id_slot or slot.inlined:
                    if slot.inlined_as_list or not id_slot:
                        return "[]"
                    else:
                        return "{}"
                else:
                    return "[]"
            else:
                if not id_slot or slot.inlined:
                    return "{}"
                else:
                    return "null"
        else:
            if r in sv.all_types():
                t = sv.get_type(r)
                if slot.multivalued:
                    return "[]"
                elif t.base and t.base in type_map:
                    return type_init_map[t.base]
                elif t.typeof and t.typeof in type_map:
                    return type_init_map[t.typeof]
                else:
                    logger.warning(f"Unknown type.base: {t.name}")
                return "null"
            return "null"

    @staticmethod
    def parents(cls: ClassDefinition) -> list[ClassDefinitionName]:
        if cls.is_a:
            parents = [cls.is_a]
        else:
            parents = []
        return [ClassDefinitionName(camelcase(p)) for p in parents + cls.mixins]

    def default_value_for_type(self, typ: str) -> str:
        pass

    def required_slots(self, cls: ClassDefinition) -> list[SlotDefinitionName]:
        return [s for s in self.schemaview.class_slots(cls.name) if self.schemaview.induced_slot(s, cls.name).required]

    def _get_subproperty_union_type(self, slot: SlotDefinition) -> Optional[str]:
        """
        Get TypeScript union type from slot hierarchy for subproperty_of constraint.

        Following metamodel semantics: "any ontological child (related to X via
        an is_a relationship), is a valid value for the slot"

        Values are formatted according to range type:
        - uri/uriorcurie: Uses CURIEs (e.g., "biolink:causes")
        - string: Uses snake_case slot names (e.g., "causes")

        :param slot: SlotDefinition with subproperty_of set
        :return: TypeScript union type string or None if no values
        """
        sv = self.schemaview

        # TypeScript uses CURIEs for URI-like ranges (not full URIs)
        # The shared utility handles formatting based on range type
        use_curie = is_uri_range(sv, slot.range)

        # Get formatted values - CURIEs for URI ranges, snake_case for strings
        values = get_subproperty_values(sv, slot, expand_uri=False if use_curie else None)

        if not values:
            return None

        # Format as TypeScript union type
        return " | ".join([f'"{v}"' for v in values])


@shared_arguments(TypescriptGenerator)
@click.version_option(__version__, "-V", "--version")
@click.option("--gen-type-utils/", "-u", help="Generate Type checking utils", is_flag=True)
@click.option("--include-induced-slots/", help="Generate slots induced through inheritance", is_flag=True)
@click.option("--output", type=click.Path(dir_okay=False))
@click.option(
    "--expand-subproperty-of/--no-expand-subproperty-of",
    default=True,
    show_default=True,
    help="If --expand-subproperty-of (default), slots with subproperty_of will generate union types "
    "containing all slot descendants. Use --no-expand-subproperty-of to disable this behavior.",
)
@click.command()
def cli(yamlfile, gen_type_utils=False, include_induced_slots=False, expand_subproperty_of=True, output=None, **args):
    """Generate typescript interfaces and types

    See https://github.com/linkml/linkml-runtime.js
    """
    gen = TypescriptGenerator(
        yamlfile,
        gen_type_utils=gen_type_utils,
        include_induced_slots=include_induced_slots,
        expand_subproperty_of=expand_subproperty_of,
        **args,
    )
    serialized = gen.serialize(output=output)
    if output is None:
        print(serialized)


if __name__ == "__main__":
    cli()
