"""Generator for TypeDB 3.x TypeQL schema definitions.

Converts a LinkML schema into a TypeQL ``define`` block that can be loaded
directly into a TypeDB 3.x database.

Mapping summary:
- LinkML class → TypeDB ``entity`` type
- Scalar slot → TypeDB ``attribute`` type + ``owns`` declaration
- Object-ranged slot → TypeDB ``relation`` type + ``plays`` declarations
- Enum → ``attribute value string`` with permitted-values comment
- ``is_a`` inheritance → TypeDB ``sub`` keyword
- ``abstract: true`` → ``@abstract`` annotation
- ``identifier: true`` → ``@key`` annotation
- ``required: true`` (singular) → ``@card(1..1)``
- ``multivalued: true`` → ``@card(0..)``
"""

import os
from dataclasses import dataclass

import click

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.utils.schemaview import SchemaView

# Maps LinkML / XSD type local-names to TypeDB primitive value types.
_TYPEDB_PRIMITIVE: dict[str, str] = {
    # string-like
    "string": "string",
    "str": "string",
    "anyuri": "string",
    "uri": "string",
    "uriorcurie": "string",
    "curie": "string",
    "ncname": "string",
    "nodeid": "string",
    "jsonpointer": "string",
    "jsonschemanoturi": "string",
    # integer-like
    "integer": "integer",
    "int": "integer",
    "long": "integer",
    "short": "integer",
    "byte": "integer",
    "nonpositiveinteger": "integer",
    "negativeinteger": "integer",
    "nonnegativeinteger": "integer",
    "positiveinteger": "integer",
    "unsignedlong": "integer",
    "unsignedint": "integer",
    "unsignedshort": "integer",
    "unsignedbyte": "integer",
    # double-like
    "float": "double",
    "double": "double",
    "decimal": "double",
    # boolean
    "boolean": "boolean",
    "bool": "boolean",
    # datetime-like
    "date": "datetime",
    "datetime": "datetime",
    "datetimestamp": "datetime",
    "time": "datetime",
    "duration": "string",  # no native duration in TypeDB 3
}


# TypeDB 3.x reserved keywords that cannot be used as user-defined type names.
# When a slot or class name collides with one of these, we append a suffix.
_TYPEDB_RESERVED: frozenset[str] = frozenset({
    # Kind keywords
    "entity", "relation", "attribute", "role",
    # Schema keywords
    "sub", "owns", "plays", "relates", "abstract", "value", "type",
    "define", "redefine", "undefine", "fun",
    # Query keywords
    "match", "insert", "delete", "update", "put", "fetch",
    "reduce", "distinct", "select", "sort", "limit", "offset",
    "not", "or", "and", "is", "has", "isa", "links",
    "let", "as", "from", "groupby", "key", "label", "iid",
    "like", "contains", "true", "false",
    # Aggregation
    "count", "sum", "max", "min", "mean", "std",
    # Primitive value types
    "integer", "double", "string", "boolean", "datetime", "duration",
})


def _typedb_name(name: str) -> str:
    """Convert a LinkML name to TypeDB hyphen-case convention.

    Reserved TypeDB keywords are suffixed with ``-attr`` to avoid parse errors.

    Examples:
        >>> _typedb_name("my_slot")
        'my-slot'
        >>> _typedb_name("FirstName")
        'firstname'
        >>> _typedb_name("age in years")
        'age-in-years'
        >>> _typedb_name("role")
        'role-attr'
        >>> _typedb_name("type")
        'type-attr'
    """
    result = name.replace("_", "-").replace(" ", "-").lower()
    if result in _TYPEDB_RESERVED:
        result = result + "-attr"
    return result


def _resolve_typedb_value_type(sv: SchemaView, range_name: str | None) -> str | None:
    """Return the TypeDB value type for a scalar range, or None if range is a class/enum.

    Walks the LinkML type hierarchy to find the XSD URI, then maps to a TypeDB primitive.
    Returns None if the range refers to a class or enum (i.e. not a scalar type).
    """
    if range_name is None:
        return "string"

    all_classes = sv.all_classes()
    all_enums = sv.all_enums()

    if range_name in all_classes:
        return None  # object reference, not scalar
    if range_name in all_enums:
        return "string"  # enums become string attributes

    # Walk type aliases until we find an XSD URI
    type_def = sv.get_type(range_name)
    while type_def is not None:
        uri = str(type_def.uri) if type_def.uri else ""
        # Extract the local name from a full URI (e.g. http://...#dateTime) or a CURIE (xsd:dateTime)
        local = uri.split("#")[-1].split("/")[-1].split(":")[-1].lower()
        if local in _TYPEDB_PRIMITIVE:
            return _TYPEDB_PRIMITIVE[local]
        # Try the base type name
        base_lower = (type_def.base or "").lower()
        if base_lower in _TYPEDB_PRIMITIVE:
            return _TYPEDB_PRIMITIVE[base_lower]
        # Walk up
        type_def = sv.get_type(type_def.from_schema) if type_def.from_schema else None
        break  # avoid infinite loop; fall through to name-based lookup

    # Last resort: match the range name directly
    return _TYPEDB_PRIMITIVE.get(range_name.lower(), "string")


def _build_name_maps(sv: SchemaView) -> tuple[dict[str, str], dict[str, str]]:
    """Build safe TypeDB name mappings for attributes and relations.

    TypeDB requires globally unique labels across all type kinds (entity, attribute,
    relation). This function detects and resolves:

    - Attribute name colliding with an entity name → append ``-attr``
    - Relation name colliding with an entity or attribute name → append ``-rel``

    :return: ``(attr_names, rel_names)`` where each maps original slot name → safe TypeDB name
    """
    entity_names = {_typedb_name(cn) for cn in sv.all_classes()}

    # ── Attribute names ───────────────────────────────────────────────────────
    all_class_names = set(sv.all_classes().keys())
    attr_names: dict[str, str] = {}
    for class_name in sv.all_classes():
        for slot in sv.class_induced_slots(class_name):
            if slot.name in attr_names:
                continue
            if slot.range in all_class_names:
                continue  # object-ranged → relation, not attribute
            candidate = _typedb_name(slot.name)
            if candidate in entity_names:
                candidate = candidate + "-attr"
            attr_names[slot.name] = candidate

    # ── Relation names ────────────────────────────────────────────────────────
    # Relations are derived from object-ranged slots only.
    taken = entity_names | set(attr_names.values())
    rel_names: dict[str, str] = {}
    for class_name in sv.all_classes():
        for slot_name in (sv.get_class(class_name).slots or []):
            if slot_name in rel_names:
                continue
            induced = sv.induced_slot(slot_name, class_name)
            if induced.range not in sv.all_classes():
                continue
            candidate = _typedb_name(slot_name)
            if candidate in taken:
                candidate = candidate + "-rel"
            rel_names[slot_name] = candidate
            taken.add(candidate)

    return attr_names, rel_names


@dataclass
class TypeDBGenerator(Generator):
    """Generates TypeDB 3.x TypeQL schema definitions from a LinkML schema.

    Output is a single ``define`` block containing attribute types, entity types,
    and relation types derived from the LinkML schema.
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["typeql"]
    uses_schemaloader = False

    def serialize(self) -> str:  # type: ignore[override]
        """Generate a TypeQL define block from the LinkML schema.

        :return: TypeQL schema as a string
        """
        sv = self.schemaview
        # Pre-compute safe names; resolves collisions across entity/attribute/relation labels.
        attr_names, rel_names = _build_name_maps(sv)
        lines: list[str] = []

        # Header comment
        lines.append(f"# Generated by linkml-typedb-generator v{self.generatorversion}")
        lines.append(f"# Schema: {sv.schema.name}")
        lines.append("# https://linkml.io")
        lines.append("")
        lines.append("define")
        lines.append("")

        # ── Attribute types ──────────────────────────────────────────────────
        attr_defs = self._collect_attribute_defs(sv, attr_names)
        if attr_defs:
            lines.append("  # Attribute types")
            for attr_line in attr_defs:
                lines.append(f"  {attr_line}")
            lines.append("")

        # ── Entity types ─────────────────────────────────────────────────────
        entity_lines = self._collect_entity_defs(sv, attr_names, rel_names)
        if entity_lines:
            lines.append("  # Entity types")
            for el in entity_lines:
                lines.append(f"  {el}")
            lines.append("")

        # ── Relation types ───────────────────────────────────────────────────
        relation_lines = self._collect_relation_defs(sv, rel_names)
        if relation_lines:
            lines.append("  # Relations (from object-ranged slots)")
            for rl in relation_lines:
                lines.append(f"  {rl}")
            lines.append("")

        return "\n".join(lines)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _collect_attribute_defs(self, sv: SchemaView, attr_names: dict[str, str]) -> list[str]:
        """Return deduplicated ``attribute <name>, value <type>;`` declarations.

        Also generates enum-attribute declarations with a comment listing permitted values.
        Slot names that reference classes (object ranges) are skipped.

        :param attr_names: pre-computed mapping from slot name → safe TypeDB attribute name
        """
        seen: dict[str, str] = {}  # safe_attr_name → typeql_line

        for class_name in sv.all_classes():
            for induced_slot in sv.class_induced_slots(class_name):
                slot_name = attr_names.get(induced_slot.name, _typedb_name(induced_slot.name))
                if slot_name in seen:
                    continue
                value_type = _resolve_typedb_value_type(sv, induced_slot.range)
                if value_type is None:
                    continue  # object range → relation, not attribute
                seen[slot_name] = f"attribute {slot_name}, value {value_type};"

        # Enums used in slot ranges also need attribute declarations with comments
        enum_attr_lines: list[str] = []
        enum_slots_seen: set[str] = set()
        for class_name in sv.all_classes():
            for induced_slot in sv.class_induced_slots(class_name):
                slot_name = attr_names.get(induced_slot.name, _typedb_name(induced_slot.name))
                if induced_slot.range in sv.all_enums() and slot_name not in enum_slots_seen:
                    enum_slots_seen.add(slot_name)
                    enum_def = sv.get_enum(induced_slot.range)
                    permitted = list(enum_def.permissible_values.keys()) if enum_def else []
                    comment = f"# Enum: {_typedb_name(induced_slot.range)} (permitted values: {', '.join(permitted)})"
                    enum_attr_lines.append(comment)
                    seen.pop(slot_name, None)
                    enum_attr_lines.append(f"attribute {slot_name}, value string;")

        result = list(seen.values()) + enum_attr_lines
        return result

    def _collect_entity_defs(
        self, sv: SchemaView, attr_names: dict[str, str], rel_names: dict[str, str]
    ) -> list[str]:
        """Return entity type definition lines including owns and plays.

        Only directly-declared slots are emitted as ``owns`` and ``plays``
        on each entity — TypeDB 3.x inherits capabilities from supertypes and
        raises an error if a subtype redeclares an already-inherited capability.

        :param attr_names: slot name → safe TypeDB attribute name
        :param rel_names: slot name → safe TypeDB relation name
        """
        plays_map: dict[str, list[str]] = {cn: [] for cn in sv.all_classes()}
        for class_name in sv.all_classes():
            ancestor_slots: set[str] = set()
            for ancestor in sv.class_ancestors(class_name)[1:]:
                ancestor_cls = sv.get_class(ancestor)
                if ancestor_cls and ancestor_cls.slots:
                    ancestor_slots.update(ancestor_cls.slots)
            direct_slot_names = {
                s for s in (sv.get_class(class_name).slots or [])
                if s not in ancestor_slots
            }
            for slot_name in direct_slot_names:
                induced = sv.induced_slot(slot_name, class_name)
                if induced.range not in sv.all_classes():
                    continue
                slot_tname = rel_names.get(slot_name, _typedb_name(slot_name))
                domain_role = _typedb_name(class_name)
                range_role = _typedb_name(induced.range)
                plays_map[class_name].append(f"plays {slot_tname}:{domain_role}")
                range_class = induced.range
                if range_class in plays_map:
                    plays_map[range_class].append(f"plays {slot_tname}:{range_role}")

        lines: list[str] = []
        for class_name, class_def in sv.all_classes().items():
            tname = _typedb_name(class_name)

            parts: list[str] = []
            if class_def.abstract:
                parts.append(f"entity {tname} @abstract")
            else:
                parts.append(f"entity {tname}")
            if class_def.is_a:
                parts[0] += f", sub {_typedb_name(class_def.is_a)}"

            # Slots that appear on ANY ancestor are already inherited in TypeDB —
            # re-declaring them causes [SVL42]. Filter them out here.
            ancestor_slots: set[str] = set()
            for ancestor in sv.class_ancestors(class_name)[1:]:  # skip self
                ancestor_cls = sv.get_class(ancestor)
                if ancestor_cls and ancestor_cls.slots:
                    ancestor_slots.update(ancestor_cls.slots)

            direct_slot_names = [
                s for s in (sv.get_class(class_name).slots or [])
                if s not in ancestor_slots
            ]
            for slot_name in direct_slot_names:
                induced = sv.induced_slot(slot_name, class_name)
                value_type = _resolve_typedb_value_type(sv, induced.range)
                if value_type is None:
                    continue  # object range → relation
                slot_tname = attr_names.get(slot_name, _typedb_name(slot_name))
                owns = f"owns {slot_tname}"
                if induced.identifier:
                    owns += " @key"
                elif induced.required and not induced.multivalued:
                    owns += " @card(1..1)"
                elif induced.multivalued:
                    owns += " @card(0..)"
                parts.append(owns)

            for plays_stmt in dict.fromkeys(plays_map.get(class_name, [])):
                parts.append(plays_stmt)

            if len(parts) == 1:
                lines.append(f"{parts[0]};")
            else:
                lines.append(f"{parts[0]},")
                for p in parts[1:-1]:
                    lines.append(f"    {p},")
                lines.append(f"    {parts[-1]};")
            lines.append("")

        return lines

    def _collect_relation_defs(self, sv: SchemaView, rel_names: dict[str, str]) -> list[str]:
        """Return relation type definition lines for all object-ranged slots.

        One relation type per unique slot name. A slot may appear on multiple classes,
        so all domain classes and range classes are included as ``relates`` role types.

        :param rel_names: slot name → safe TypeDB relation name
        """
        # First pass: collect all (domain_class, range_class) pairs per slot.
        slot_pairs: dict[str, list[tuple[str, str]]] = {}
        for class_name in sv.all_classes():
            for slot_name in (sv.get_class(class_name).slots or []):
                induced = sv.induced_slot(slot_name, class_name)
                if induced.range not in sv.all_classes():
                    continue
                slot_pairs.setdefault(slot_name, []).append((class_name, induced.range))

        lines: list[str] = []
        for slot_name, pairs in slot_pairs.items():
            slot_tname = rel_names.get(slot_name, _typedb_name(slot_name))
            # Collect unique role names in declaration order
            roles: list[str] = []
            seen_roles: set[str] = set()
            for domain_class, range_class in pairs:
                for role in (_typedb_name(domain_class), _typedb_name(range_class)):
                    if role not in seen_roles:
                        roles.append(role)
                        seen_roles.add(role)
            lines.append(f"relation {slot_tname},")
            for i, role in enumerate(roles):
                suffix = "," if i < len(roles) - 1 else ";"
                lines.append(f"    relates {role}{suffix}")
            lines.append("")
        return lines


@shared_arguments(TypeDBGenerator)
@click.version_option(__version__, "-V", "--version")
@click.command(name="typedb")
def cli(yamlfile, **args):
    """Generate TypeDB TypeQL schema definitions from a LinkML model."""
    print(TypeDBGenerator(yamlfile, **args).serialize())


if __name__ == "__main__":
    cli()
