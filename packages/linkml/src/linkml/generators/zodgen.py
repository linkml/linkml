import logging
import os
import re
from dataclasses import dataclass

import click
from jinja2 import Template

from linkml._version import __version__
from linkml.generators.common.type_designators import get_type_designator_value
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.generators.zod_ifabsent_processor import ZodIfAbsentProcessor
from linkml.utils.generator import shared_arguments
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    Element,
    EnumDefinition,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)

# Mapping from LinkML base types (TypeDefinition.base) to Zod validator expressions.
# Any base not listed here falls back to ``z.string()``.
# ``XSDDate`` / ``XSDDateTime`` use the ``dateFromString`` preprocessor defined in the
# generated preamble so that ISO date strings are coerced to JavaScript ``Date`` objects.
zod_type_map = {
    "str": "z.string()",
    "int": "z.number().int()",
    "Bool": "z.boolean()",
    "float": "z.number()",
    "Decimal": "z.number()",
    "XSDDate": "dateFromString",
    "XSDDateTime": "dateFromString",
    "XSDTime": "z.string()",
    "URI": "z.url()",
    "NCName": "z.string()",
}

# Base -> a Zod check token (applied via the active dialect) validating a lexical format.
_FORMAT_CHECKS = {
    "NCName": "regex(/^[A-Za-z_][A-Za-z0-9._-]*$/)",
}

# Named ``zod_format`` annotation values -> the top-level Zod format validator they emit.
# All are dialect-agnostic (available in both regular Zod and zod/mini).
_ZOD_FORMATS = {
    "email": "z.email()",
    "uuid": "z.uuid()",
    "url": "z.url()",
    "httpUrl": "z.httpUrl()",
    "ipv4": "z.ipv4()",
    "ipv6": "z.ipv6()",
    "e164": "z.e164()",
    "jwt": "z.jwt()",
    "emoji": "z.emoji()",
    "base64": "z.base64()",
    "base64url": "z.base64url()",
    "nanoid": "z.nanoid()",
    "cuid": "z.cuid()",
    "cuid2": "z.cuid2()",
    "ulid": "z.ulid()",
    "date": "z.iso.date()",
    "time": "z.iso.time()",
    "datetime": "z.iso.datetime()",
}

# Base -> Zod ISO string validator, used instead of the ``dateFromString`` Date coercion
# when ``--iso-dates`` (or ``--zod-mini``) is set: values are validated as ISO strings.
_ISO_DATE_MAP = {
    "XSDDate": "z.iso.date()",
    "XSDDateTime": "z.iso.datetime()",
    "XSDTime": "z.iso.time()",
}

# Zod expressions that represent a numeric value; used to decide whether numeric
# range constraints (minimum_value / maximum_value) are applicable.
_NUMERIC_BASES = {"z.number()", "z.number().int()", "z.coerce.number()", "z.coerce.number().int()", "z.int()"}

# Zod expressions that represent a string value; used to decide whether a ``pattern``
# constraint (rendered as ``.regex``) is applicable. Includes ``z.url()`` and the named
# ``zod_format`` validators, which are all string schemas that accept a further ``.regex``.
_STRING_BASES = {"z.string()", "z.coerce.string()", "z.url()"} | set(_ZOD_FORMATS.values())

# Canonical scalar expression -> coercing variant, applied when ``--coerce`` is set.
_COERCE_MAP = {
    "z.string()": "z.coerce.string()",
    "z.number()": "z.coerce.number()",
    "z.number().int()": "z.coerce.number().int()",
    "z.boolean()": "z.coerce.boolean()",
}

# A valid ECMAScript identifier (usable as an unquoted object key).
_JS_IDENTIFIER = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")

# TypeScript metadata interface for the optional custom registry (--registry).
_REGISTRY_INTERFACE = """export interface LinkmlMeta {
    uri?: string;
    definition_uri?: string;
    exact_mappings?: string[];
    close_mappings?: string[];
    related_mappings?: string[];
    narrow_mappings?: string[];
    broad_mappings?: string[];
    in_subset?: string[];
    rank?: number;
    source?: string;
}
"""

# Jinja2 template producing Zod schemas plus the inferred TypeScript types (via z.infer).
# ``dateFromString`` coerces incoming date strings/Date objects into Date values.
zod_template = """
{{ gen.import_stmt() }}
{% if gen.emit_date_preprocessor() %}
const dateFromString = z.preprocess((val) => {
    if (typeof val === "string" || val instanceof Date) return new Date(val);
}, z.date());
{% endif %}
{{ gen.registry_preamble() }}
{% for e in view.all_enums().values() %}
{%- if e.description %}
/** {{ gen.jsdoc(e.description) }} */
{%- endif %}
export const {{ gen.enum_const_name(e) }} = {{ gen.enum_expr(e) }}{{ gen.meta_expr(e, gen.enum_value_meta(e)) }};
export type {{ gen.name(e) }} = z.infer<typeof {{ gen.enum_const_name(e) }}>;
{{ gen.register_call(e, gen.enum_const_name(e)) }}
{% endfor %}

{% for c in view.all_classes().values() %}
{%- if c.description %}
/** {{ gen.jsdoc(c.description) }} */
{%- endif %}
{%- if c.union_of %}
export const {{ gen.class_schema_name(c) }} = {{ gen.union_of_expr(c) }}{{ gen.meta_expr(c) }};
{%- elif gen.is_any_class(c.name) %}
export const {{ gen.class_schema_name(c) }} = z.any(){{ gen.meta_expr(c) }};
{%- else %}
export const {{ gen.class_schema_name(c) }} = {{ gen.object_kw() }}({
{%- for sn in view.class_slots(c.name, direct=False) %}
    {%- set s = view.induced_slot(sn, c.name) %}
    {{ gen.slot_member(s, c, loop.last) }}
{%- endfor %}
}){{ gen.rules_expr(c) }}{{ gen.brand_expr(c) }}{{ gen.meta_expr(c) }};
{%- endif %}
export type {{ gen.name(c) }} = z.infer<typeof {{ gen.class_schema_name(c) }}>;
{{ gen.register_call(c, gen.class_schema_name(c)) }}
{% endfor %}
"""


@dataclass
class ZodGenerator(OOCodeGenerator):
    """
    Generates Zod schemas and corresponding TypeScript types from a LinkML schema.

    Each class becomes a self-contained ``z.object`` schema that includes every slot
    induced through ``is_a`` inheritance and ``mixins``, and an inferred TypeScript type
    exported via ``z.infer``. Enums become ``z.enum`` schemas.
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "0.12.0"
    valid_formats = ["text"]
    uses_schemaloader = False

    # Deprecated / retained for CLI backwards-compatibility. Generated schemas always
    # include slots induced through inheritance and mixins, so this flag has no effect.
    include_induced_slots: bool = False

    # Behavior flags are tri-state: ``None`` defers to the schema's ``zodgen`` annotation
    # block (then to ``False``); an explicit ``True`` / ``False`` always wins.

    # Emit ``z.strictObject`` (reject unknown keys) instead of ``z.object`` (strip them).
    strict: bool | None = None

    # Wrap scalar validators in ``z.coerce.*`` so inputs are converted before validation.
    coerce: bool | None = None

    # Validate date/time values as ISO strings (``z.iso.*``) rather than coercing to Date.
    iso_dates: bool | None = None

    # Nominally brand class schemas that have an identifier (``.brand("ClassName")``).
    brand: bool | None = None

    # Target ``zod/mini`` (functional, tree-shakable API). Implies ISO-string dates.
    zod_mini: bool = False

    # Emit a ``z.registry<LinkmlMeta>()`` of this name collecting every schema with its
    # LinkML semantic metadata (URIs, mappings, subsets, rank, source). Disabled when None.
    registry: str | None = None

    def serialize(self, output: str | None = None) -> str:
        """Serialize a LinkML schema to Zod schemas and TypeScript types."""
        self._resolve_option_annotations()
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

    def _resolve_option_annotations(self) -> None:
        """Resolve tri-state behavior flags from schema-level ``zod_*`` annotations.

        An explicit constructor/CLI value (``True``/``False``) always wins; ``None`` defers
        to the annotation, then to ``False``.
        """
        schema = self.schemaview.schema
        for field in ("strict", "coerce", "iso_dates", "brand"):
            if getattr(self, field) is None:
                value = self._annotation_value(schema, f"zod_{field}")
                setattr(self, field, self._as_bool(value) if value is not None else False)

    @staticmethod
    def _as_bool(value) -> bool:
        """Coerce an annotation value (bool or string) to a boolean."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("true", "1", "yes", "on")
        return bool(value)

    def _annotation_value(self, expr, tag: str):
        """
        Return the value of an annotation ``tag`` on an element, or ``None``.

        Handles both container shapes LinkML uses: a dict-like ``Annotations`` (``.get``)
        and a ``JsonObj`` (attribute access), as returned by ``induced_slot``.
        """
        anns = getattr(expr, "annotations", None)
        if not anns:
            return None
        ann = anns.get(tag) if hasattr(anns, "get") else getattr(anns, tag, None)
        return getattr(ann, "value", None) if ann is not None else None

    @staticmethod
    def name(element: Element) -> str:
        """
        Return the canonical TypeScript name for an element.

        Slots are rendered as underscored names (object keys / property names);
        classes and enums are rendered in CamelCase.
        """
        alias = element.name
        if isinstance(element, SlotDefinition) and element.alias:
            alias = element.alias
        if type(element).class_name == "slot_definition":
            return underscore(alias)
        else:
            return camelcase(alias)

    def class_schema_name(self, cls: ClassDefinition) -> str:
        """Return the exported Zod schema constant name for a class (``<Name>Schema``)."""
        return f"{self.name(cls)}Schema"

    def enum_const_name(self, enum_obj: EnumDefinition) -> str:
        """
        Return the exported Zod schema constant name for an enum.

        Uses an ``Enum`` suffix but avoids producing a doubled ``EnumEnum`` suffix when
        the enum is already named e.g. ``LifeStatusEnum``.
        """
        base = self.name(enum_obj)
        return base if base.endswith("Enum") else f"{base}Enum"

    @staticmethod
    def jsdoc(text: str) -> str:
        """Escape a description so it can be embedded safely inside a ``/** ... */`` block."""
        return text.replace("*/", "*\\/")

    @staticmethod
    def _js_string(value: str) -> str:
        """Render a Python string as a double-quoted, escaped JavaScript string literal."""
        escaped = str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'

    def meta_expr(self, element: Element, extra: list[str] | None = None) -> str:
        """
        Return a ``.meta({...})`` suffix carrying LinkML metadata, or an empty string.

        Metadata attached this way survives conversion to JSON Schema / OpenAPI (via
        ``z.toJSONSchema()``), unlike JSDoc comments. ``extra`` supplies pre-rendered
        object fields (e.g. per-enum-value metadata).
        """
        fields: list[str] = []
        if isinstance(element, ClassDefinition | EnumDefinition):
            name = self.name(element)
            # ``id`` names the ``$defs`` entry produced by ``z.toJSONSchema``; only emit it
            # when the name is unique so the global registry cannot throw on a duplicate.
            if name in self._unique_element_names():
                fields.append(f"id: {self._js_string(name)}")
        title = getattr(element, "title", None)
        if title:
            fields.append(f"title: {self._js_string(title)}")
        description = getattr(element, "description", None)
        if description:
            fields.append(f"description: {self._js_string(description)}")
        unit = getattr(element, "unit", None)
        if unit is not None and getattr(unit, "ucum_code", None):
            fields.append(f"unit: {self._js_string(unit.ucum_code)}")
        examples = getattr(element, "examples", None)
        if examples:
            vals = [self._js_string(e.value) for e in examples if getattr(e, "value", None) is not None]
            if vals:
                fields.append("examples: [" + ", ".join(vals) + "]")
        aliases = getattr(element, "aliases", None)
        if aliases:
            fields.append("aliases: [" + ", ".join(self._js_string(a) for a in aliases) + "]")
        see_also = getattr(element, "see_also", None)
        if see_also:
            fields.append("see_also: [" + ", ".join(self._js_string(s) for s in see_also) + "]")
        deprecated = getattr(element, "deprecated", None)
        if deprecated:
            # Zod's GlobalMeta types ``deprecated`` as boolean; keep the reason separately.
            fields.append("deprecated: true")
            fields.append(f"deprecatedReason: {self._js_string(deprecated)}")
        if extra:
            fields.extend(extra)
        if not fields:
            return ""
        obj = "{ " + ", ".join(fields) + " }"
        return f".check(z.meta({obj}))" if self.zod_mini else f".meta({obj})"

    def enum_value_meta(self, enum_obj: EnumDefinition) -> list[str]:
        """Render a ``values`` metadata field mapping permissible values to their metadata."""
        entries = []
        for text, pv in enum_obj.permissible_values.items():
            parts = []
            if getattr(pv, "description", None):
                parts.append(f"description: {self._js_string(pv.description)}")
            if getattr(pv, "meaning", None):
                parts.append(f"meaning: {self._js_string(pv.meaning)}")
            if parts:
                entries.append(f"{self._js_string(text)}: {{ {', '.join(parts)} }}")
        if not entries:
            return []
        return ["values: { " + ", ".join(entries) + " }"]

    def object_kw(self) -> str:
        """Return the Zod object constructor: ``z.strictObject`` when ``strict`` else ``z.object``."""
        return "z.strictObject" if self.strict else "z.object"

    def brand_expr(self, cls: ClassDefinition) -> str:
        """Return a ``.brand(...)`` suffix for identifier-bearing classes when ``brand`` is set."""
        if not self.brand:
            return ""
        if self.schemaview.get_identifier_slot(cls.name, use_key=True) is None:
            return ""
        return f".brand({self._js_string(self.name(cls))})"

    def registry_preamble(self) -> str:
        """Return the ``LinkmlMeta`` interface and registry declaration, or empty string."""
        if not self.registry:
            return ""
        return f"\n{_REGISTRY_INTERFACE}\nexport const {self.registry} = z.registry<LinkmlMeta>();\n"

    def register_call(self, element: Element, const_name: str) -> str:
        """Return a ``<registry>.add(<Schema>, {...})`` statement, or empty string."""
        if not self.registry:
            return ""
        return f"{self.registry}.add({const_name}, {self._semantic_meta(element)});"

    def _semantic_meta(self, element: Element) -> str:
        """Render an element's LinkML semantic metadata as a JS object literal."""
        fields: list[str] = []
        uri = self.schemaview.get_uri(element)
        if uri:
            fields.append(f"uri: {self._js_string(uri)}")
        definition_uri = getattr(element, "definition_uri", None)
        if definition_uri:
            fields.append(f"definition_uri: {self._js_string(definition_uri)}")
        for key in ("exact_mappings", "close_mappings", "related_mappings", "narrow_mappings", "broad_mappings"):
            vals = getattr(element, key, None)
            if vals:
                fields.append(f"{key}: [" + ", ".join(self._js_string(v) for v in vals) + "]")
        in_subset = getattr(element, "in_subset", None)
        if in_subset:
            fields.append("in_subset: [" + ", ".join(self._js_string(v) for v in in_subset) + "]")
        rank = getattr(element, "rank", None)
        if rank is not None:
            fields.append(f"rank: {rank}")
        source = getattr(element, "source", None)
        if source:
            fields.append(f"source: {self._js_string(source)}")
        return "{ " + ", ".join(fields) + " }" if fields else "{}"

    # -- output dialect (regular Zod vs. tree-shakable zod/mini) --------------------

    @property
    def _use_iso(self) -> bool:
        """ISO-string dates are used when requested or when targeting zod/mini (no preprocess)."""
        return self.iso_dates or self.zod_mini

    def import_stmt(self) -> str:
        """Return the import line for the active dialect."""
        return 'import * as z from "zod/mini";' if self.zod_mini else 'import { z } from "zod";'

    def emit_date_preprocessor(self) -> bool:
        """The ``dateFromString`` preprocessor is only needed for Date-coercing regular Zod."""
        return not self._use_iso

    def getter_annotation(self, slot: SlotDefinition, cls: ClassDefinition) -> str:
        """
        Annotate a reference getter's return type only when it is part of a reference cycle.

        zod/mini's functional wrappers cannot infer self-referential types, so recursive
        getters need an explicit (broad) annotation; non-recursive getters keep their precise
        inferred types. Regular Zod needs no annotation.
        """
        if not self.zod_mini:
            return ""
        return ": z.ZodMiniType" if self._getter_is_recursive(slot, cls) else ""

    def _getter_is_recursive(self, slot: SlotDefinition, cls: ClassDefinition) -> bool:
        """Return whether a reference slot's schema can transitively reach its own class."""
        targets = self._slot_reference_targets(slot)
        if cls.name in targets:
            return True
        visited = set(targets)
        stack = list(targets)
        while stack:
            for tgt in self._class_reference_targets(stack.pop()):
                if tgt == cls.name:
                    return True
                if tgt not in visited:
                    visited.add(tgt)
                    stack.append(tgt)
        return False

    def _referenced_classes(self, expr) -> list[str]:
        """Return inlined class ranges referenced by a slot/sub-expression (recursively)."""
        out: list[str] = []
        for attr in ("any_of", "all_of", "exactly_one_of", "none_of"):
            members = getattr(expr, attr, None)
            if members:
                for member in members:
                    out.extend(self._referenced_classes(member))
        r = getattr(expr, "range", None)
        if r in self.schemaview.all_classes() and not self.is_any_class(r) and self._is_inlined(expr):
            out.append(r)
        return out

    def _slot_reference_targets(self, slot) -> set[str]:
        """Return the concrete classes a slot's schema eagerly references."""
        targets: set[str] = set()
        for class_name in self._referenced_classes(slot):
            targets.update(self._polymorphic_alternatives(class_name))
        return targets

    def _class_reference_targets(self, class_name: str) -> set[str]:
        """Return concrete classes referenced by a class's slots and ``union_of`` members."""
        cache = getattr(self, "_cls_ref_cache", None)
        if cache is None:
            cache = {}
            self._cls_ref_cache = cache
        if class_name not in cache:
            sv = self.schemaview
            targets: set[str] = set()
            for sn in sv.class_slots(class_name):
                targets |= self._slot_reference_targets(sv.induced_slot(sn, class_name))
            cls = sv.get_class(class_name)
            for member in getattr(cls, "union_of", None) or []:
                targets.update(self._polymorphic_alternatives(member))
            cache[class_name] = targets
        return cache[class_name]

    def _apply_checks(self, base: str, checks: list[str]) -> str:
        """
        Apply a list of check tokens (e.g. ``"regex(/re/)"``, ``"gte(0)"``) to a schema.

        Regular Zod chains them as methods; zod/mini collects them in a single ``.check(...)``.
        Duplicate tokens (e.g. the same bound declared on a type and its slot) are collapsed.
        """
        checks = self._dedupe(checks)
        if not checks:
            return base
        if self.zod_mini:
            return f"{base}.check(" + ", ".join(f"z.{c}" for c in checks) + ")"
        return base + "".join(f".{c}" for c in checks)

    def _length_check(self, kind: str, value) -> str:
        """Return a collection-length check token (``min``/``max``/``exact``) for the dialect."""
        if kind == "exact":
            return f"length({value})"
        name = {"min": "minLength", "max": "maxLength"}[kind] if self.zod_mini else kind
        return f"{name}({value})"

    def slot_member(self, slot: SlotDefinition, cls: ClassDefinition, is_last: bool) -> str:
        """Render one object member: a lazy getter for reference slots, else ``key: expr``."""
        sep = "" if is_last else ","
        expr = self.zod_type(slot, cls)
        if self.is_reference_slot(slot):
            return f"get {self.slot_key(slot)}(){self.getter_annotation(slot, cls)} {{ return {expr}; }}{sep}"
        return f"{self.slot_key(slot)}: {expr}{sep}"

    def _optional_nullable(self, base: str) -> str:
        """Mark a schema optional and nullable in the active dialect."""
        if self.zod_mini:
            return f"z.nullable(z.optional({base}))"
        return f"{base}.optional().nullable()"

    def _with_default(self, base: str, value: str) -> str:
        """Attach a default value in the active dialect."""
        if self.zod_mini:
            return f"z._default({base}, {value})"
        return f"{base}.default({value})"

    def _readonly(self, base: str) -> str:
        """Mark a schema read-only in the active dialect."""
        return f"z.readonly({base})" if self.zod_mini else f"{base}.readonly()"

    def _intersection(self, members: list[str]) -> str:
        """Intersect member schemas in the active dialect."""
        result = members[0]
        for member in members[1:]:
            result = f"z.intersection({result}, {member})" if self.zod_mini else f"{result}.and({member})"
        return result

    def _refine(self, base: str, inner: str) -> str:
        """Attach a ``refine`` predicate in the active dialect."""
        return f"{base}.check(z.refine({inner}))" if self.zod_mini else f"{base}.refine({inner})"

    def _unique_element_names(self) -> set[str]:
        """Return TypeScript names used by exactly one class or enum (safe as a registry id)."""
        cache = getattr(self, "_unique_names_cache", None)
        if cache is None:
            counts: dict[str, int] = {}
            for c in self.schemaview.all_classes().values():
                counts[self.name(c)] = counts.get(self.name(c), 0) + 1
            for e in self.schemaview.all_enums().values():
                counts[self.name(e)] = counts.get(self.name(e), 0) + 1
            cache = {n for n, k in counts.items() if k == 1}
            self._unique_names_cache = cache
        return cache

    def union_of_expr(self, cls: ClassDefinition) -> str:
        """Render a class-level ``union_of`` as a lazily-evaluated ``z.union`` of member schemas."""
        members = ", ".join(self.class_schema_name(self.schemaview.get_class(m)) for m in cls.union_of)
        return f"z.lazy(() => z.union([{members}]))"

    def _polymorphic_alternatives(self, class_name: str) -> list[str]:
        """Return the concrete classes a class range may resolve to (itself + is_a descendants)."""
        sv = self.schemaview
        result = []
        for descendant in sv.class_descendants(class_name, mixins=False):
            cls = sv.get_class(descendant)
            if not cls.abstract and not cls.mixin:
                result.append(descendant)
        return result

    def _inlined_class_expr(self, class_name: str) -> str:
        """
        Return the schema expression for an inlined class range.

        A class with concrete ``is_a`` descendants expands to a union over every concrete
        alternative so that polymorphic payloads validate. When the range class carries a
        type-designator slot, a ``z.discriminatedUnion`` is emitted for efficient dispatch;
        otherwise a plain ``z.union``.
        """
        sv = self.schemaview
        alternatives = self._polymorphic_alternatives(class_name)
        if len(alternatives) <= 1:
            return self.class_schema_name(sv.get_class(class_name))
        schemas = ", ".join(self.class_schema_name(sv.get_class(a)) for a in alternatives)
        designator = sv.get_type_designator_slot(class_name)
        if designator is not None:
            return f"z.discriminatedUnion({self._js_string(self.name(designator))}, [{schemas}])"
        return f"z.union([{schemas}])"

    def slot_key(self, slot: SlotDefinition) -> str:
        """Return the object key for a slot, quoting it when it is not a valid JS identifier."""
        key = self.name(slot)
        if _JS_IDENTIFIER.match(key):
            return key
        return '"' + key.replace("\\", "\\\\").replace('"', '\\"') + '"'

    def enum_values(self, enum_obj: EnumDefinition) -> str:
        """
        Return the permissible values of an enum as a comma-separated list of
        double-quoted, escaped string literals suitable for ``z.enum([...])``.
        """
        values = list(enum_obj.permissible_values.keys())
        return ", ".join('"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"' for v in values)

    def enum_expr(self, enum_obj: EnumDefinition) -> str:
        """
        Return the base schema expression for an enum.

        Enums with no static permissible values (e.g. dynamic ``reachable_from`` enums that
        have not been materialized) fall back to ``z.string()``; ``z.enum([])`` would infer
        the ``never`` type and reject all data.
        """
        values = self.enum_values(enum_obj)
        if not values:
            return "z.string()"
        return f"z.enum([{values}])"

    def _base_zod_type(self, type_def: TypeDefinition) -> str | None:
        """
        Resolve a LinkML type to a base Zod expression by walking the ``typeof`` chain.

        Returns ``None`` if no mapping can be found.
        """
        sv = self.schemaview
        seen = set()
        current: TypeDefinition | None = type_def
        while current is not None and current.name not in seen:
            seen.add(current.name)
            if current.base and current.base in zod_type_map:
                if self._use_iso and current.base in _ISO_DATE_MAP:
                    return _ISO_DATE_MAP[current.base]
                if current.base == "int" and self.zod_mini:
                    # zod/mini has no ``.int()`` method; use the top-level integer schema.
                    return "z.coerce.number()" if self.coerce else "z.int()"
                return self._coerce(zod_type_map[current.base])
            if current.typeof:
                current = sv.get_type(current.typeof)
            else:
                current = None
        return None

    def _coerce(self, expr: str) -> str:
        """Rewrite a canonical scalar expression to its coercing variant when ``coerce`` is set."""
        if self.coerce and expr in _COERCE_MAP:
            return _COERCE_MAP[expr]
        return expr

    def _leaf_base(self, type_def: TypeDefinition) -> str | None:
        """Return the ``base`` at the end of a type's ``typeof`` chain."""
        sv = self.schemaview
        seen = set()
        current: TypeDefinition | None = type_def
        while current is not None and current.name not in seen:
            seen.add(current.name)
            if current.base:
                return current.base
            current = sv.get_type(current.typeof) if current.typeof else None
        return None

    def is_reference_slot(self, slot: SlotDefinition) -> bool:
        """
        Return whether a slot's generated expression eagerly references another class
        schema (``<Name>Schema``) and therefore must be rendered as a lazy getter to
        support forward and recursive references.
        """
        return self._references_schema(slot)

    def _references_schema(self, expr) -> bool:
        """Recursively determine whether a slot (or sub-expression) references a class schema."""
        for attr in ("any_of", "all_of", "exactly_one_of", "none_of"):
            members = getattr(expr, attr, None)
            if members:
                return any(self._references_schema(m) for m in members)
        r = getattr(expr, "range", None)
        return r in self.schemaview.all_classes() and not self.is_any_class(r) and self._is_inlined(expr)

    def is_any_class(self, class_name: str) -> bool:
        """Return whether a class represents an unconstrained object (``class_uri: linkml:Any``)."""
        cls = self.schemaview.get_class(class_name)
        return cls is not None and cls.class_uri == "linkml:Any"

    def _is_inlined(self, expr) -> bool:
        """
        Return whether a class-ranged (sub-)expression is inlined (embedded object) rather
        than a reference by identifier. Mirrors ``SchemaView.is_inlined``.
        """
        sv = self.schemaview
        r = getattr(expr, "range", None)
        if r not in sv.all_classes():
            return False
        if getattr(expr, "inlined", None) or getattr(expr, "inlined_as_list", None):
            return True
        return sv.get_identifier_slot(r) is None

    def zod_type(self, slot: SlotDefinition, cls: ClassDefinition | None = None) -> str:
        """
        Return the full Zod expression for a slot.

        Composes, in order: the range or boolean slot expression (``any_of`` / ``all_of`` /
        ``exactly_one_of`` / ``none_of``), scalar constraints (``pattern``,
        ``minimum_value`` / ``maximum_value``), multivalued wrapping (``z.array`` or, for
        inlined-as-dict slots, ``z.record``), and finally optionality — either an
        ``ifabsent`` ``.default(...)`` or ``.optional().nullable()``.
        """
        element = self._element_expr(slot)

        if cls is not None and getattr(slot, "designates_type", False):
            # A type designator is a fixed discriminator literal for its containing class.
            value = get_type_designator_value(self.schemaview, slot, cls)
            return f"z.literal({self._js_string(value)})" + self.meta_expr(slot)

        array = getattr(slot, "array", None)
        if array is not None:
            result = self._array_expr(element, array)
            if not slot.required:
                result = self._optional_nullable(result)
        elif slot.multivalued:
            result = self._wrap_multivalued(element, slot)
            if not slot.required:
                result = self._optional_nullable(result)
        elif slot.required:
            result = element
        else:
            default = self._default_expr(slot, cls) if cls is not None else None
            if default is not None:
                result = self._with_default(element, default)
            else:
                result = self._optional_nullable(element)
        if getattr(slot, "readonly", None):
            result = self._readonly(result)
        return result + self.meta_expr(slot)

    def _array_expr(self, element: str, array) -> str:
        """
        Wrap an element expression in nested ``z.array`` layers per a LinkML ``array`` spec.

        Explicit ``dimensions`` carry per-axis cardinality (``.length`` / ``.min`` / ``.max``);
        otherwise the dimension count comes from ``exact_number_dimensions``,
        ``minimum_number_dimensions``, or defaults to one.
        """
        dimensions = getattr(array, "dimensions", None)
        if dimensions:
            expr = element
            for dim in reversed(dimensions):
                expr = self._wrap_dim_array(expr, dim)
            return expr
        count = (
            getattr(array, "exact_number_dimensions", None) or getattr(array, "minimum_number_dimensions", None) or 1
        )
        expr = element
        for _ in range(count):
            expr = f"z.array({expr})"
        return expr

    def _wrap_dim_array(self, element: str, dim) -> str:
        """Wrap one array dimension, applying its cardinality bounds."""
        checks: list[str] = []
        if getattr(dim, "exact_cardinality", None) is not None:
            checks.append(self._length_check("exact", dim.exact_cardinality))
        else:
            if getattr(dim, "minimum_cardinality", None) is not None:
                checks.append(self._length_check("min", dim.minimum_cardinality))
            if getattr(dim, "maximum_cardinality", None) is not None:
                checks.append(self._length_check("max", dim.maximum_cardinality))
        return self._apply_checks(f"z.array({element})", checks)

    def rules_expr(self, cls: ClassDefinition) -> str:
        """
        Render class-level ``rules`` as chained cross-field ``refine`` checks.

        Each rule enforces: when all precondition slot_conditions hold, every postcondition
        slot_condition must hold (rendered as ``pre implies post``). Only ``slot_conditions``
        are translated.
        """
        if not cls.rules:
            return ""
        parts = []
        for rule in cls.rules:
            post = self._condition_pairs(getattr(rule, "postconditions", None), cls)
            if not post:
                continue
            pre = self._condition_pairs(getattr(rule, "preconditions", None), cls)
            pre_js = "[" + ", ".join(f"[{k}, {s}]" for k, s in pre) + "] as [string, any][]"
            post_js = "[" + ", ".join(f"[{k}, {s}]" for k, s in post) + "] as [string, any][]"
            fn = (
                "(val) => { "
                f"const pre = {pre_js}; const post = {post_js}; "
                "return !pre.every(([k, s]) => s.safeParse((val as any)[k]).success) "
                "|| post.every(([k, s]) => s.safeParse((val as any)[k]).success); }"
            )
            inner = f'{fn}, {{ message: "rule violation", path: [{post[0][0]}] }}'
            parts.append(self._refine("", inner))
        return "".join(parts)

    def _condition_pairs(self, class_expr, cls: ClassDefinition) -> list[tuple[str, str]]:
        """Return ``(js_key_literal, schema_expr)`` pairs for a rule's slot_conditions."""
        if class_expr is None:
            return []
        conditions = getattr(class_expr, "slot_conditions", None)
        if not conditions:
            return []
        pairs = []
        for slot_name, cond in conditions.items():
            induced = self.schemaview.induced_slot(slot_name, cls.name)
            schema = self._member_expr(cond, induced)
            pairs.append((self._js_string(self.name(induced)), schema))
        return pairs

    def _element_expr(self, slot: SlotDefinition) -> str:
        """Return the single-value Zod expression for a slot's range or boolean expression."""
        equals = self._equals_expr(slot)
        if equals is not None:
            return equals
        if slot.any_of:
            return self._union_expr(slot.any_of, slot)
        if slot.exactly_one_of:
            return self._xor_expr(slot.exactly_one_of, slot)
        if slot.all_of:
            return self._intersection_expr(slot.all_of, slot)
        if slot.none_of:
            return self._none_of_expr(slot.none_of, slot)

        base, is_scalar = self._single_range(slot)
        if is_scalar:
            base = self._apply_checks(base, self._scalar_check_tokens(slot, slot, base))
        return base

    def _single_range(self, expr) -> tuple[str, bool]:
        """
        Return ``(expression, is_scalar)`` for a single (non-boolean) range.

        Class ranges resolve to their inlined schema (when embedded) or to the scalar type
        of the target's identifier (when referenced). ``is_scalar`` is ``True`` only for
        scalar/type ranges, so that scalar constraints may be applied to them.

        A ``zod_type`` annotation overrides the expression verbatim (no auto-constraints);
        a ``zod_format`` annotation supplies a named format base (constraints still apply).
        """
        override = self._annotation_value(expr, "zod_type")
        if override:
            return str(override), False
        fmt = self._annotation_value(expr, "zod_format")
        if fmt is not None:
            if fmt in _ZOD_FORMATS:
                return _ZOD_FORMATS[fmt], True
            logger.warning(f"Unknown zod_format `{fmt}`; ignoring (see docs for supported formats)")
        sv = self.schemaview
        r = getattr(expr, "range", None)
        if r in sv.all_classes():
            if self.is_any_class(r):
                return "z.any()", False
            if self._is_inlined(expr):
                return self._inlined_class_expr(r), False
            # Non-inlined class range: the value is the identifier of the referenced instance.
            id_slot = sv.get_identifier_slot(r, use_key=True)
            if id_slot is not None and id_slot.range in sv.all_types():
                return self._base_zod_type(sv.get_type(id_slot.range)) or "z.string()", False
            return "z.string()", False
        if r in sv.all_enums():
            return self.enum_const_name(sv.get_enum(r)), False
        if r in sv.all_types():
            type_def = sv.get_type(r)
            resolved = self._base_zod_type(type_def)
            if resolved is None:
                logger.warning(f"Unknown type range `{r}`; defaulting to z.string()")
                resolved = "z.string()"
            # Format and type-level constraints are applied by the caller (single ``.check``).
            return resolved, True
        logger.warning(f"Unrecognized range `{r}`; defaulting to z.string()")
        return "z.string()", True

    def _member_expr(self, member, parent: SlotDefinition) -> str:
        """Return the Zod expression for a single member of a boolean slot expression."""
        equals = self._equals_expr(member)
        if equals is not None:
            return equals
        if member.any_of:
            return self._union_expr(member.any_of, parent)
        if member.all_of:
            return self._intersection_expr(member.all_of, parent)
        source = member if member.range else parent
        base, is_scalar = self._single_range(source)
        if is_scalar:
            base = self._apply_checks(base, self._scalar_check_tokens(source, member, base))
        return base

    def _equals_expr(self, expr) -> str | None:
        """Return a Zod literal/enum for an ``equals_string`` / ``equals_number`` /
        ``equals_string_in`` constraint, or ``None`` when none is present."""
        if getattr(expr, "equals_string", None) is not None:
            return f"z.literal({self._js_string(expr.equals_string)})"
        if getattr(expr, "equals_number", None) is not None:
            return f"z.literal({expr.equals_number})"
        equals_string_in = getattr(expr, "equals_string_in", None)
        if equals_string_in:
            return "z.enum([" + ", ".join(self._js_string(v) for v in equals_string_in) + "])"
        return None

    def _union_expr(self, members, parent: SlotDefinition) -> str:
        exprs = self._dedupe([self._member_expr(m, parent) for m in members])
        if len(exprs) == 1:
            return exprs[0]
        return "z.union([" + ", ".join(exprs) + "])"

    def _xor_expr(self, members, parent: SlotDefinition) -> str:
        """Render ``exactly_one_of`` as Zod's exclusive union (``z.xor``): exactly one matches."""
        exprs = self._dedupe([self._member_expr(m, parent) for m in members])
        if len(exprs) == 1:
            return exprs[0]
        return "z.xor([" + ", ".join(exprs) + "])"

    def _intersection_expr(self, members, parent: SlotDefinition) -> str:
        exprs = self._dedupe([self._member_expr(m, parent) for m in members])
        return self._intersection(exprs)

    def _none_of_expr(self, members, parent: SlotDefinition) -> str:
        outer, is_scalar = self._single_range(parent)
        if is_scalar:
            outer = self._apply_checks(outer, self._scalar_check_tokens(parent, parent, outer))
        exprs = self._dedupe([self._member_expr(m, parent) for m in members])
        schemas = "[" + ", ".join(exprs) + "]"
        return self._refine(
            outer,
            f"(val) => !{schemas}.some((s) => s.safeParse(val).success), "
            '{ message: "must not match any of the none_of schemas" }',
        )

    @staticmethod
    def _dedupe(items: list[str]) -> list[str]:
        """Return the list with duplicates removed, preserving order."""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    def _wrap_multivalued(self, element: str, slot: SlotDefinition) -> str:
        """
        Wrap a single-value expression for a multivalued slot.

        Multivalued, inlined, identifier-keyed slots (LinkML's inlined-as-dict form) become
        ``z.record``; everything else becomes a bounded ``z.array``.
        """
        sv = self.schemaview
        r = slot.range
        if r in sv.all_classes() and self._is_inlined(slot) and not slot.inlined_as_list:
            id_slot = sv.get_identifier_slot(r, use_key=True)
            if id_slot is not None:
                key_type = "z.string()"
                if id_slot.range in sv.all_types():
                    key_type = self._base_zod_type(sv.get_type(id_slot.range)) or "z.string()"
                return f"z.record({key_type}, {element})"
        base = f"z.array({element})"
        checks: list[str] = []
        if slot.minimum_cardinality is not None:
            checks.append(self._length_check("min", slot.minimum_cardinality))
        if slot.maximum_cardinality is not None:
            checks.append(self._length_check("max", slot.maximum_cardinality))
        if slot.exact_cardinality is not None:
            checks.append(self._length_check("exact", slot.exact_cardinality))
        base = self._apply_checks(base, checks)
        if getattr(slot, "all_members", None) is not None:
            member = self._member_expr(slot.all_members, slot)
            base = self._refine(
                base,
                f"(arr) => arr.every((x) => ({member}).safeParse(x).success), "
                '{ message: "all_members constraint failed" }',
            )
        if getattr(slot, "has_member", None) is not None:
            member = self._member_expr(slot.has_member, slot)
            base = self._refine(
                base,
                f"(arr) => arr.some((x) => ({member}).safeParse(x).success), "
                '{ message: "has_member constraint failed" }',
            )
        return base

    def _default_expr(self, slot: SlotDefinition, cls: ClassDefinition) -> str | None:
        """Return a Zod ``.default(...)`` literal for a slot's ``ifabsent``, or ``None``."""
        if not slot.ifabsent:
            return None
        processor = getattr(self, "_ifabsent_proc", None)
        if processor is None:
            processor = ZodIfAbsentProcessor(self.schemaview)
            processor.iso_dates = self._use_iso
            self._ifabsent_proc = processor
        try:
            return processor.process_slot(slot, cls)
        except (ValueError, NotImplementedError) as e:
            logger.warning(f"Could not map ifabsent for slot `{slot.name}`: {e}")
            return None

    def _constraint_tokens(self, base: str, holder) -> list[str]:
        """Return ``pattern`` / numeric-range check tokens declared on ``holder``."""
        tokens: list[str] = []
        if getattr(holder, "pattern", None) and base in _STRING_BASES:
            escaped_pattern = holder.pattern.replace("/", "\\/")
            tokens.append(f"regex(/{escaped_pattern}/)")
        if base in _NUMERIC_BASES:
            if getattr(holder, "minimum_value", None) is not None:
                tokens.append(f"gte({holder.minimum_value})")
            if getattr(holder, "maximum_value", None) is not None:
                tokens.append(f"lte({holder.maximum_value})")
        return tokens

    def _scalar_check_tokens(self, range_holder, constraint_holder, base: str) -> list[str]:
        """
        Collect every scalar check for a value: lexical format and type-level constraints
        (from ``range_holder``'s range type) plus the ``constraint_holder``'s own constraints,
        so they can be emitted in a single ``.check(...)``.
        """
        tokens: list[str] = []
        r = getattr(range_holder, "range", None)
        if r in self.schemaview.all_types():
            type_def = self.schemaview.get_type(r)
            leaf = self._leaf_base(type_def)
            if leaf in _FORMAT_CHECKS:
                tokens.append(_FORMAT_CHECKS[leaf])
            # A coerced integer in zod/mini needs an explicit ``z.int()`` check.
            if leaf == "int" and self.zod_mini and self.coerce:
                tokens.append("int()")
            tokens += self._constraint_tokens(base, type_def)
        tokens += self._constraint_tokens(base, constraint_holder)
        return tokens

    def required_slots(self, cls: ClassDefinition) -> list[SlotDefinitionName]:
        """Return the names of the required slots induced on a class."""
        return [s for s in self.schemaview.class_slots(cls.name) if self.schemaview.induced_slot(s, cls.name).required]

    def default_value_for_type(self, typ: str) -> str:
        pass


@shared_arguments(ZodGenerator)
@click.version_option(__version__, "-V", "--version")
@click.option(
    "--include-induced-slots/--no-include-induced-slots",
    default=False,
    help="Deprecated: generated schemas always include inherited and mixin slots.",
)
@click.option(
    "--strict/--no-strict",
    default=None,
    help="Emit z.strictObject instead of z.object. Overrides the schema's zod_strict annotation.",
)
@click.option(
    "--coerce/--no-coerce",
    default=None,
    help="Wrap scalar validators in z.coerce.*. Overrides the schema's zod_coerce annotation.",
)
@click.option(
    "--iso-dates/--no-iso-dates",
    default=None,
    help="Validate date/time values as ISO strings (z.iso.*). Overrides the schema's zod_iso_dates annotation.",
)
@click.option(
    "--brand/--no-brand",
    default=None,
    help="Brand identifier-bearing class schemas (.brand). Overrides the schema's zod_brand annotation.",
)
@click.option(
    "--zod-mini/--no-zod-mini",
    default=False,
    help="Target zod/mini (functional, tree-shakable API). Implies ISO-string dates.",
)
@click.option(
    "--registry",
    default=None,
    help="Emit a z.registry<LinkmlMeta>() of this name collecting every schema with its semantic metadata.",
)
@click.option("--output", type=click.Path(dir_okay=False))
@click.command()
def cli(
    yamlfile,
    include_induced_slots=False,
    strict=None,
    coerce=None,
    iso_dates=None,
    brand=None,
    zod_mini=False,
    registry=None,
    output=None,
    **args,
):
    """Generate Zod schemas and TypeScript types from a LinkML model.

    This generator produces a set of Zod schemas and associated TypeScript types
    (via ``z.infer``) for runtime validation in TypeScript.
    """
    gen = ZodGenerator(
        yamlfile,
        include_induced_slots=include_induced_slots,
        strict=strict,
        coerce=coerce,
        iso_dates=iso_dates,
        brand=brand,
        zod_mini=zod_mini,
        registry=registry,
        **args,
    )
    serialized = gen.serialize(output=output)
    if output is None:
        print(serialized)


if __name__ == "__main__":
    cli()
