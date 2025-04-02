import logging
import os
from dataclasses import dataclass
from typing import List, Optional

import click
from jinja2 import Template
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    Element,
    SlotDefinition,
    SlotDefinitionName,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments

logger = logging.getLogger(__name__)

# Mapping from LinkML base types to Zod validator expressions.
# Updated "XSDDate" to use the preprocessor "dateFromString"
zod_type_map = {
    "str": "z.string()",
    "int": "z.number()",
    "Bool": "z.boolean()",
    "float": "z.number()",
    "XSDDate": "dateFromString",
}

# Updated Jinja2 template to generate both Zod schemas and TypeScript types using z.infer.
# Added a definition for dateFromString to preprocess date strings.
zod_template = """
import { z } from "zod";

const dateFromString = z.preprocess((val) => {
    if (typeof val === "string" || val instanceof Date) return new Date(val);
}, z.date());

{% for e in view.all_enums().values() %}
{%- if e.description %}
/** {{ e.description }} */
{%- endif %}
export const {{ gen.name(e) }}Enum = z.enum([{{ gen.enum_values(e) }}]);
export type {{ gen.name(e) }} = z.infer<typeof {{ gen.name(e) }}Enum>;

{% endfor %}

{% for c in view.all_classes().values() %}
{%- if c.description %}
/** {{ c.description }} */
{%- endif %}
export const {{ gen.name(c) }}Schema = z.object({
{%- for sn in view.class_slots(c.name, direct=not(gen.include_induced_slots)) %}
    {%- set s = view.induced_slot(sn, c.name) %}
    {{ gen.name(s) }}: {{ gen.zod_type(s) }}{{ "," if not loop.last }}
{%- endfor %}
});
export type {{ gen.name(c) }} = z.infer<typeof {{ gen.name(c) }}Schema>;

{% endfor %}
"""


@dataclass
class ZodGenerator(OOCodeGenerator):
    """
    Generates Zod schemas and corresponding TypeScript types from a LinkML schema.
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["text"]
    uses_schemaloader = False

    # Whether to include slots inherited via mixins/inheritance
    include_induced_slots: bool = False

    def serialize(self, output: Optional[str] = None) -> str:
        """Serialize a LinkML schema to Zod types and TypeScript interfaces"""
        sv: SchemaView = self.schemaview
        template_obj = Template(zod_template)
        out_str = template_obj.render(
            gen=self,
            view=sv,
        )
        if output is not None:
            with open(output, "w") as out:
                out.write(out_str)
        return out_str

    @staticmethod
    def name(element: Element) -> str:
        """
        Returns the canonical name for an element.
        For slots, returns the underscored name; for classes and enums, returns the camelcased name.
        """
        alias = element.name
        if isinstance(element, SlotDefinition) and element.alias:
            alias = element.alias
        if type(element).class_name == "slot_definition":
            return underscore(alias)
        else:
            return camelcase(alias)

    def enum_values(self, enum_obj) -> str:
        """
        Returns a comma-separated list of enum values in double quotes,
        suitable for inclusion in a z.enum declaration.
        """
        values = list(enum_obj.permissible_values.keys())
        return ", ".join(f'"{v}"' for v in values)

    def zod_type(self, slot: SlotDefinition) -> str:
        """
        Returns a Zod type expression corresponding to a slot's range.
        For classes, it references the generated schema via z.lazy() to allow for circular references.
        For built-in types, it maps using zod_type_map.
        If a slot is multivalued, wraps the type in z.array(...).
        Appends .optional() if the slot is not required.
        """
        sv = self.schemaview
        r = slot.range
        if r in sv.all_classes():
            type_name = self.name(sv.get_class(r))
            base = f"z.lazy(() => {type_name}Schema)"
            if slot.multivalued:
                base = f"z.array({base})"
        elif r in sv.all_types():
            t = sv.get_type(r)
            if t.base and t.base in zod_type_map:
                base = zod_type_map[t.base]
            elif t.typeof and t.typeof in zod_type_map:
                base = zod_type_map[t.typeof]
            else:
                logger.warning(f"Unknown type for slot {slot.name}: {t.name}")
                base = "z.string()"
            if slot.multivalued:
                base = f"z.array({base})"
        else:
            base = "z.string()"
        if not slot.required:
            base = f"{base}.optional().nullable()"
        return base

    def required_slots(self, cls: ClassDefinition) -> List[SlotDefinitionName]:
        return [s for s in self.schemaview.class_slots(cls.name) if self.schemaview.induced_slot(s, cls.name).required]

    def default_value_for_type(self, typ: str) -> str:
        pass


@shared_arguments(ZodGenerator)
@click.version_option(__version__, "-V", "--version")
@click.option("--include-induced-slots/", help="Generate slots induced through inheritance", is_flag=True)
@click.option("--output", type=click.Path(dir_okay=False))
@click.command()
def cli(yamlfile, include_induced_slots=False, output=None, **args):
    """Generate Zod schemas and TypeScript interfaces from a LinkML model.

    This generator produces a set of Zod schemas and associated TypeScript types (using z.infer)
    for runtime validation in TypeScript.
    """
    gen = ZodGenerator(yamlfile, include_induced_slots=include_induced_slots, **args)
    serialized = gen.serialize(output=output)
    if output is None:
        print(serialized)


if __name__ == "__main__":
    cli()
