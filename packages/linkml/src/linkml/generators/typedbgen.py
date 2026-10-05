"""Generator for TypeDB 3.x TypeQL schema definitions.

Converts a LinkML schema into a TypeQL ``define`` block that can be loaded
directly into a TypeDB 3.x database.

Mapping summary:
- class → ``entity`` type; or with ``represents_relationship`` or ``SchemaView.is_relationship()`` → ``relation`` type with ``relates`` roles
- ``is_a`` → ``sub`` (classes and slots)
- ``abstract: true`` → ``@abstract`` (dropped with a warning if any ancestor is concrete)
- Scalar slot → ``attribute`` type + ``owns``; slot ``is_a`` → attribute subtype, but only if value types match
- Class-ranged slot → binary ``relation`` named after the slot with "owning" role named after the slot, "played" role after the range class, both ``@card(1)``
- Class-ranged slot ``is_a`` → sub-relation specializing the owning role; players of a slot's owning role also play those below it
- Non-abstract slot with a ``domain`` that no class declares → owned or played by the domain class
- ``slot_usage`` range narrowing → specialized ``relates ... as ...`` (on a sub-relation for entity-like classes)
- Mixin → not emitted; its slots are inlined, and a mixin range or domain resolves to its most general concrete classes
- Enum → ``attribute value string @values(...)``; an enum set by ``slot_usage`` → ``@values`` on that ``owns``
- ``identifier: true`` → ``@key``
- ``required`` / ``multivalued`` / ``*_cardinality`` → ``@card``, on ``owns`` for scalar slots and on the owner's ``plays`` for class-ranged ones
- ``minimum_value`` / ``maximum_value`` → ``@range(...)``; ``pattern`` → ``@regex(...)``, on ``owns``
- ``description`` → ``@doc(...)``
"""

import os
from dataclasses import dataclass

import click

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import SlotDefinition
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
    # boolean
    "boolean": "boolean",
    "bool": "boolean",
    # datetime-like
    "datetime": "datetime",
    "datetimestamp": "datetime",
    "time": "datetime",
    "date": "date",
    "decimal": "decimal",
    "duration": "duration",
}


# TypeDB 3.x reserved keywords that cannot be used as user-defined type names.
# When a slot or class name collides with one of these, we append a suffix.
# Sourced from the official TypeQL keyword glossary (https://typedb.com/docs/typeql-reference/keywords/).
_TYPEDB_RESERVED: frozenset[str] = frozenset(
    {
        # Schema queries
        "define",
        "undefine",
        "redefine",
        # Pipeline stages
        "match",
        "fetch",
        "insert",
        "delete",
        "update",
        "put",
        "select",
        "require",
        "distinct",
        "sort",
        "limit",
        "offset",
        "reduce",
        "with",
        "end",
        # Pattern logic
        "or",
        "not",
        "try",
        # Type statements
        "entity",
        "relation",
        "attribute",
        "struct",
        "fun",
        # Constraint statements
        "sub",
        "sub!",
        "relates",
        "plays",
        "value",
        "owns",
        "alias",
        # Instance statements
        "isa",
        "isa!",
        "links",
        "has",
        "is",
        "let",
        "contains",
        "like",
        # Identity
        "label",
        "iid",
        # Reductions
        "count",
        "max",
        "min",
        "mean",
        "median",
        "std",
        "sum",
        "list",
        # Value types
        "boolean",
        "integer",
        "double",
        "decimal",
        "datetime-tz",
        "datetime",
        "date",
        "duration",
        "string",
        # Built-ins
        "round",
        "ceil",
        "floor",
        "abs",
        "len",
        # Misc
        "true",
        "false",
        "asc",
        "desc",
        "return",
        "of",
        "from",
        "in",
        "as",
        "type",
    }
)


def _typeql_string(value: str) -> str:
    """Return ``value`` as an escaped, double-quoted TypeQL string literal.

    Newlines and tabs are escaped because TypeQL string literals are single-line.
    """
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n").replace("\t", "\\t")
    return f'"{escaped}"'


def _typedb_name(name: str) -> str:
    """Convert a LinkML name to a TypeDB type label.

    Whitespace becomes underscores; everything else is kept verbatim. Reserved TypeDB
    keywords are suffixed with ``_attr`` to avoid parse errors.

    Examples:
        >>> _typedb_name("GeneToDiseaseAssociation")
        'GeneToDiseaseAssociation'
        >>> _typedb_name("gene to disease association")
        'gene_to_disease_association'
        >>> _typedb_name("match")
        'match_attr'
    """
    result = "_".join(name.split())
    if result in _TYPEDB_RESERVED:
        result = result + "_attr"
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

    primitives = _TYPEDB_PRIMITIVE

    # Walk type aliases until we find an XSD URI
    type_def = sv.get_type(range_name)
    while type_def is not None:
        uri = str(type_def.uri) if type_def.uri else ""
        # Extract the local name from a full URI (e.g. http://...#dateTime) or a CURIE (xsd:dateTime)
        local = uri.split("#")[-1].split("/")[-1].split(":")[-1].lower()
        if local in primitives:
            return primitives[local]
        # Try the base type name
        base_lower = (type_def.base or "").lower()
        if base_lower in primitives:
            return primitives[base_lower]
        # Walk up
        type_def = sv.get_type(type_def.typeof) if type_def.typeof else None

    # Last resort: match the range name directly
    return primitives.get(range_name.lower(), "string")


def _card(lo: object, hi: object) -> str:
    """Return a ``@card`` annotation, using the ``@card(n)`` shorthand for an exact count."""
    return f"@card({lo})" if str(lo) == str(hi) else f"@card({lo}..{hi})"


def _build_range_annotation(induced: SlotDefinition) -> str | None:
    """Return a ``@range(min..max)`` annotation string, or ``None`` if no range constraints are set.

    Reads ``minimum_value`` and ``maximum_value`` from the induced slot definition.
    Supports open-ended ranges (``@range(N..)`` or ``@range(..M)``).

    :param induced: the induced SlotDefinition carrying value range metadata
    :return: annotation string like ``@range(0..150)`` or ``None``
    """
    lo = induced.minimum_value
    hi = induced.maximum_value
    if lo is None and hi is None:
        return None
    lo_str = str(lo) if lo is not None else ""
    hi_str = str(hi) if hi is not None else ""
    return f"@range({lo_str}..{hi_str})"


def _build_regex_annotation(induced: SlotDefinition) -> str | None:
    """Return a ``@regex(...)`` annotation string from ``pattern``, or ``None`` if unset.

    :param induced: the induced SlotDefinition carrying the ``pattern`` constraint
    :return: annotation string like ``@regex("^[A-Z]+$")`` or ``None``
    """
    if not induced.pattern:
        return None
    return f"@regex({_typeql_string(induced.pattern)})"


def _build_doc_annotation(description: str | None) -> str | None:
    """Return a ``@doc(...)`` annotation string, or ``None`` if unset.

    :param description: the LinkML ``description`` text
    :return: annotation string like ``@doc("...")`` or ``None``
    """
    if not description:
        return None
    return f"@doc({_typeql_string(description)})"


def _check_class_name_collisions(sv: SchemaView) -> None:
    """Raise if two distinct LinkML class names map to the same TypeDB label.

    This happens when names differ only in whitespace vs underscores
    (``gene to disease`` and ``gene_to_disease``).

    :raises ValueError: if any TypeDB label is claimed by more than one class
    """
    by_label: dict[str, list[str]] = {}
    for class_name in sv.all_classes():
        by_label.setdefault(_typedb_name(class_name), []).append(class_name)
    clashes = {label: names for label, names in by_label.items() if len(names) > 1}
    if clashes:
        detail = "; ".join(f"{label!r} <- {sorted(names)}" for label, names in sorted(clashes.items()))
        raise ValueError(
            f"Cannot generate TypeQL: distinct LinkML classes map to the same TypeDB label ({detail}). "
            "TypeDB labels must be unique; rename the conflicting classes in the source schema."
        )


def _slot_ranges(sv: SchemaView) -> dict[str, str | None]:
    """Return each slot's range, inherited through slot ``is_a`` when not set on the slot."""
    return {name: sv.induced_slot(name).range for name in sv.all_slots()}


def _build_name_maps(sv: SchemaView, slot_ranges: dict[str, str | None]) -> tuple[dict[str, str], dict[str, str]]:
    """Build safe TypeDB name mappings for attributes and relations.

    TypeDB requires globally unique labels across all type kinds (entity, attribute,
    relation). This function detects and resolves:

    - Attribute name colliding with an entity name → append ``-attr``
    - Relation name colliding with an entity or attribute name → append ``-rel``

    Relations arise from two sources: object-ranged slots on regular classes, and
    classes with ``represents_relationship: true`` (which become TypeDB ``relation``
    types directly rather than generating standalone relation types per slot).

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
                candidate = candidate + "_attr"
            attr_names[slot.name] = candidate

    # Unattached scalar slots too, so whole slot is_a trees can be emitted.
    for slot_name, slot_range in slot_ranges.items():
        if slot_name in attr_names or slot_range in all_class_names:
            continue
        candidate = _typedb_name(slot_name)
        if candidate in entity_names:
            candidate = candidate + "_attr"
        attr_names[slot_name] = candidate

    # ── Relation names ────────────────────────────────────────────────────────
    # Relations are derived from object-ranged slots only.
    taken = entity_names | set(attr_names.values())
    rel_names: dict[str, str] = {}
    candidates = [
        slot_name
        for class_name in sv.all_classes()
        for slot_name in sv.get_class(class_name).slots or []
        if sv.induced_slot(slot_name, class_name).range in all_class_names
    ] + [slot_name for slot_name, slot_range in slot_ranges.items() if slot_range in all_class_names]
    for slot_name in candidates:
        if slot_name in rel_names:
            continue
        candidate = _typedb_name(slot_name)
        if candidate in taken:
            candidate = candidate + "_rel"
        rel_names[slot_name] = candidate
        taken.add(candidate)

    return attr_names, rel_names


def _build_role_names(sv: SchemaView, rel_names: dict[str, str]) -> dict[str, tuple[str, str]]:
    """Build role-label pairs for each object-ranged slot's relation.

    The owning role is named after the slot and the played role after the range class,
    so reflexive slots (``parent`` on ``person``) still get two distinct roles. If the
    two names collide, the played role gets a ``_role`` suffix.

    :param rel_names: slot name → safe TypeDB relation name (from ``_build_name_maps``)
    :return: slot name → ``(owning_role_name, played_role_name)``
    """
    result: dict[str, tuple[str, str]] = {}
    for slot_name in sv.all_slots():
        # Name the played role after the slot's own range, not a class's slot_usage narrowing of it.
        induced = sv.induced_slot(slot_name)
        if induced.range not in sv.all_classes():
            for class_name in sv.all_classes():
                if slot_name in (sv.get_class(class_name).slots or []):
                    induced = sv.induced_slot(slot_name, class_name)
                    break
        if induced.range not in sv.all_classes():
            continue
        owning_role = _typedb_name(slot_name)
        played_role = _typedb_name(induced.range)
        if played_role == owning_role:
            played_role = played_role + "_role"
        result[slot_name] = (owning_role, played_role)
    return result


def _is_relationship_class(sv: SchemaView, class_name: str) -> bool:
    """Return True if ``class_name`` should be emitted as a TypeDB ``relation``.

    The nearest class in the ``is_a`` chain that sets ``represents_relationship``
    (true or false) decides. If none does, fall back to ``SchemaView.is_relationship()``,
    which detects RDF statement reification (``rdf:Statement`` / ``owl:Axiom``).
    """
    current = class_name
    while current:
        class_def = sv.get_class(current)
        if class_def is None:
            break
        if class_def.represents_relationship is not None:
            return bool(class_def.represents_relationship)
        current = class_def.is_a
    return sv.is_relationship(class_name)


@dataclass
class _RoleInfo:
    """Resolved TypeDB role info for one object-ranged slot on one relationship class.

    :ivar role_name: the role this class's players use (base or specialized)
    :ivar specializes: the parent role this one specializes, or None if not new here
    :ivar introduced_here: True if this class must emit the ``relates`` declaration
    :ivar declared_on: the relation type that declares ``role_name``; ``plays`` must be
        scoped to it, since inherited roles are only declared on their introducing class
    """

    role_name: str
    specializes: str | None
    introduced_here: bool
    declared_on: str


def _build_relationship_role_info(
    sv: SchemaView, relationship_classes: set[str]
) -> dict[tuple[str, str], _RoleInfo]:
    """Compute per-(class, slot) role specialization info for relationship classes.

    A specialized role ``<range>_<parent-role>`` is introduced only where the range
    actually changes along the ``is_a`` chain; restating an unchanged range reuses the
    ancestor's role, since redeclaring it violates TypeDB's ``[SVL7]``.

    :param relationship_classes: the set of class names being emitted as relations
    :return: ``(class_name, slot_name) -> _RoleInfo`` for every object-ranged slot
        directly usable on a relationship class (including inherited ones)
    """
    result: dict[tuple[str, str], _RoleInfo] = {}
    all_class_names = set(sv.all_classes().keys())

    for class_name in relationship_classes:
        # Root-first chain of this class's own relationship-class ancestry.
        chain = [class_name]
        cur = sv.get_class(class_name)
        while cur and cur.is_a and cur.is_a in relationship_classes:
            chain.append(cur.is_a)
            cur = sv.get_class(cur.is_a)
        chain.reverse()

        # Per slot: range, role and declaring class from the nearest ancestor.
        last_range: dict[str, str] = {}
        last_role: dict[str, str] = {}
        last_declared_on: dict[str, str] = {}

        for cls in chain:
            for induced in sv.class_induced_slots(cls):
                if induced.range not in all_class_names:
                    continue
                slot_name = induced.name
                base_role = _typedb_name(slot_name)
                prior_range = last_range.get(slot_name)
                prior_role = last_role.get(slot_name, base_role)

                if prior_range is None:
                    result[(cls, slot_name)] = _RoleInfo(
                        role_name=base_role, specializes=None, introduced_here=True, declared_on=cls
                    )
                    last_range[slot_name] = induced.range
                    last_role[slot_name] = base_role
                    last_declared_on[slot_name] = cls
                elif induced.range == prior_range:
                    result[(cls, slot_name)] = _RoleInfo(
                        role_name=prior_role,
                        specializes=None,
                        introduced_here=False,
                        declared_on=last_declared_on[slot_name],
                    )
                else:
                    specialized = f"{_typedb_name(induced.range)}_{prior_role}"
                    result[(cls, slot_name)] = _RoleInfo(
                        role_name=specialized, specializes=prior_role, introduced_here=True, declared_on=cls
                    )
                    last_range[slot_name] = induced.range
                    last_role[slot_name] = specialized
                    last_declared_on[slot_name] = cls

    return result


@dataclass
class _ClassRangeNarrowing:
    """A single class-ranged slot narrowing on an ordinary (non-relationship) class.

    :ivar slot_name: the LinkML slot being narrowed
    :ivar narrowing_class: the class whose ``slot_usage`` narrows the range
    :ivar base_relation: the slot's base relation
    :ivar sub_relation: the sub-relation emitted for this narrowing
    :ivar owning_role: the owning role, inherited from the base relation
    :ivar base_played_role: the played role being specialized
    :ivar narrowed_played_role: the specialized played role
    :ivar narrowed_range: the narrowed LinkML range class
    """

    slot_name: str
    narrowing_class: str
    base_relation: str
    sub_relation: str
    owning_role: str
    base_played_role: str
    narrowed_played_role: str
    narrowed_range: str


@dataclass
class _SlotRelation:
    """A class-ranged slot emitted as a standalone ``relation``.

    :ivar induced: the slot definition cardinality and range are read from
    :ivar relation: the safe TypeDB relation name
    :ivar parent: the parent slot's name if its relation is this one's supertype
    :ivar owning_role: the role played by the declaring class
    :ivar played_role: the role played by the range class
    :ivar played_declared_on: the relation that declares ``played_role``
    :ivar played_specializes: the parent's played role, if this relation narrows it
    :ivar declared: whether some class declares the slot; if not, its ``domain`` plays it
    """

    induced: SlotDefinition
    relation: str
    parent: str | None
    owning_role: str
    played_role: str
    played_declared_on: str
    played_specializes: str | None
    declared: bool = True


def _build_class_range_narrowings(
    sv: SchemaView,
    relationship_classes: set[str],
    rel_names: dict[str, str],
    role_names: dict[str, tuple[str, str]],
) -> list[_ClassRangeNarrowing]:
    """Find class-ranged slots that an ordinary (non-relationship) subclass narrows.

    Each narrowing becomes a sub-relation of the slot's base relation with a specialized
    played role (``relates <narrowed> as <base>``), so queries on the base role still
    match data inserted through the narrowed one. Only the first class in an ``is_a``
    chain to change the range counts; unchanged restatements are skipped.

    :param relationship_classes: class names emitted as ``relation`` (skipped)
    :param rel_names: slot name → safe TypeDB base relation name
    :param role_names: slot name → (owning_role_name, played_role_name)
    :return: one ``_ClassRangeNarrowing`` per class that introduces a real narrowing
    """
    all_class_names = set(sv.all_classes().keys())
    result: list[_ClassRangeNarrowing] = []

    for slot_name in sv.all_slots():
        base_range = sv.induced_slot(slot_name).range
        if base_range not in all_class_names:
            continue  # not a class-ranged slot at all

        owning_role, base_played_role = role_names.get(
            slot_name, (_typedb_name(slot_name), _typedb_name(base_range))
        )
        base_relation = rel_names.get(slot_name, _typedb_name(slot_name))

        for class_name in sv.all_classes():
            class_def = sv.get_class(class_name)
            if class_def.mixin or class_name in relationship_classes:
                continue
            if slot_name not in (class_def.slots or []) and slot_name not in (class_def.slot_usage or {}):
                continue
            induced = sv.induced_slot(slot_name, class_name)
            if induced.range not in all_class_names or induced.range == base_range:
                continue  # unranged, or same as the base range

            # Skip if the parent already has this range (a restatement, not a narrowing).
            parent = class_def.is_a
            parent_range = sv.induced_slot(slot_name, parent).range if parent else base_range
            if induced.range == parent_range:
                continue

            sub_relation = f"{base_relation}_{_typedb_name(class_name)}"
            narrowed_played_role = f"{_typedb_name(induced.range)}_{base_played_role}"
            result.append(
                _ClassRangeNarrowing(
                    slot_name=slot_name,
                    narrowing_class=class_name,
                    base_relation=base_relation,
                    sub_relation=sub_relation,
                    owning_role=owning_role,
                    base_played_role=base_played_role,
                    narrowed_played_role=narrowed_played_role,
                    narrowed_range=induced.range,
                )
            )

    return result


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
    file_extension = "tql"

    def serialize(self, **kwargs) -> str:
        """Generate a TypeQL define block from the LinkML schema.

        :return: TypeQL schema as a string
        """
        sv = self.schemaview
        _check_class_name_collisions(sv)
        # Pre-compute safe names; resolves collisions across entity/attribute/relation labels.
        attr_names, rel_names = _build_name_maps(sv, _slot_ranges(sv))
        role_names = _build_role_names(sv, rel_names)
        relationship_classes = {cn for cn in sv.all_classes() if _is_relationship_class(sv, cn)}
        relationship_role_info = _build_relationship_role_info(sv, relationship_classes)
        slot_relations = self._build_slot_relations(sv, relationship_classes, rel_names, role_names)
        for slot_name, sr in slot_relations.items():
            role_names[slot_name] = (sr.owning_role, sr.played_role)
        class_range_narrowings = _build_class_range_narrowings(sv, relationship_classes, rel_names, role_names)
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
        entity_lines = self._collect_entity_defs(
            sv,
            attr_names,
            rel_names,
            role_names,
            relationship_classes,
            relationship_role_info,
            class_range_narrowings,
            slot_relations,
        )
        if entity_lines:
            lines.append("  # Entity types")
            for el in entity_lines:
                lines.append(f"  {el}")
            lines.append("")

        # ── Relation types ───────────────────────────────────────────────────
        relation_lines = self._collect_relation_defs(sv, slot_relations, class_range_narrowings)
        if relation_lines:
            lines.append("  # Relations (from object-ranged slots)")
            for rl in relation_lines:
                lines.append(f"  {rl}")
            lines.append("")

        return "\n".join(lines)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _build_slot_relations(
        self,
        sv: SchemaView,
        relationship_classes: set[str],
        rel_names: dict[str, str],
        role_names: dict[str, tuple[str, str]],
    ) -> dict[str, _SlotRelation]:
        """Return the class-ranged slots emitted as standalone relations, parents first.

        That is every class-ranged slot except those used only as roles of relationship
        classes. A slot whose ``is_a`` parent is also emitted becomes a sub-relation that
        specializes the parent's owning role, and its played role too if the range narrows.

        :param relationship_classes: class names emitted as ``relation``
        :param rel_names: slot name → safe TypeDB relation name
        :param role_names: slot name → (owning_role_name, played_role_name)
        """
        all_class_names = set(sv.all_classes().keys())
        defs: dict[str, SlotDefinition] = {}
        used_on_relationship: set[str] = set()
        for class_name, class_def in sv.all_classes().items():
            if class_def.mixin:
                continue
            if class_name in relationship_classes:
                used_on_relationship.update(s.name for s in sv.class_induced_slots(class_name))
                continue
            ancestor_slot_names = self._ancestor_slot_names(sv, class_name)
            for induced in sv.class_induced_slots(class_name):
                if induced.name not in ancestor_slot_names and induced.range in all_class_names:
                    # If the declaring class narrows the range, the base relation keeps the
                    # slot's own range and the narrowing becomes a sub-relation.
                    base = sv.induced_slot(induced.name)
                    if base.range in all_class_names and base.range != induced.range:
                        induced = base
                    defs.setdefault(induced.name, induced)
        declared = set(defs)
        for slot_name in sv.all_slots():
            if slot_name in defs or slot_name in used_on_relationship:
                continue
            induced = sv.induced_slot(slot_name)
            if induced.range in all_class_names:
                defs[slot_name] = induced

        def depth(slot_name: str) -> int:
            parent = sv.get_slot(slot_name).is_a
            return 1 + depth(parent) if parent in defs else 0

        result: dict[str, _SlotRelation] = {}
        for slot_name in sorted(defs, key=depth):
            induced = defs[slot_name]
            relation = rel_names.get(slot_name, _typedb_name(slot_name))
            owning_role, played_role = role_names.get(
                slot_name, (_typedb_name(slot_name), _typedb_name(induced.range))
            )
            parent = sv.get_slot(slot_name).is_a
            if parent not in result:
                result[slot_name] = _SlotRelation(induced, relation, None, owning_role, played_role, relation, None)
                continue
            p = result[parent]
            if induced.range == p.induced.range:
                result[slot_name] = _SlotRelation(
                    induced, relation, parent, owning_role, p.played_role, p.played_declared_on, None
                )
                continue
            ancestor_roles: set[str] = set()
            cur: str | None = parent
            while cur:
                ancestor_roles.update((result[cur].owning_role, result[cur].played_role))
                cur = result[cur].parent
            if played_role in ancestor_roles:
                played_role = f"{_typedb_name(induced.range)}_{p.played_role}"
            result[slot_name] = _SlotRelation(
                induced, relation, parent, owning_role, played_role, relation, p.played_role
            )
        for slot_name, sr in result.items():
            sr.declared = slot_name in declared
        return result

    def _slot_relation_descendants(self, slot_relations: dict[str, _SlotRelation], slot_name: str) -> list[str]:
        """Return every slot whose relation is a (transitive) subtype of ``slot_name``'s."""
        children: dict[str, list[str]] = {}
        for name, sr in slot_relations.items():
            if sr.parent:
                children.setdefault(sr.parent, []).append(name)
        result: list[str] = []
        stack = list(children.get(slot_name, []))
        while stack:
            name = stack.pop()
            result.append(name)
            stack.extend(children.get(name, []))
        return result

    def _abstract_ok(self, sv: SchemaView, class_name: str, _cache: dict[str, bool] | None = None) -> bool:
        """Return True if ``class_name`` may legally be declared ``@abstract`` in TypeDB.

        TypeDB requires an abstract type's supertype to be abstract too (``[SVL14]``), so
        this holds only if every ``is_a`` ancestor up to the root is abstract. Otherwise
        ``@abstract`` is dropped from the class.
        """
        cache = {} if _cache is None else _cache
        if class_name in cache:
            return cache[class_name]
        class_def = sv.get_class(class_name)
        parent_def = sv.get_class(class_def.is_a) if class_def.is_a else None
        if not class_def.is_a or (parent_def and parent_def.mixin):
            result = True  # no TypeDB supertype is emitted
        elif not class_def.abstract:
            result = True  # legality is moot for a concrete class; treat as "ok"
        else:
            result = bool(parent_def and parent_def.abstract and self._abstract_ok(sv, class_def.is_a, cache))
        cache[class_name] = result
        return result

    def _collect_attribute_defs(self, sv: SchemaView, attr_names: dict[str, str]) -> list[str]:
        """Return deduplicated ``attribute <name>, value <type>;`` declarations.

        Also generates enum-attribute declarations with a comment listing permitted values.
        Slot names that reference classes (object ranges) are skipped. Per-class range and
        pattern constraints go on ``owns``, not here.

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
                doc_ann = _build_doc_annotation(induced_slot.description)
                if doc_ann:
                    seen[slot_name] = f"attribute {slot_name} {doc_ann}, value {value_type};"
                else:
                    seen[slot_name] = f"attribute {slot_name}, value {value_type};"

        # Slots not attached to any class, so their is_a trees can be subtyped below.
        all_slots_for_base = sv.all_slots()
        for slot_name_orig, safe_name in attr_names.items():
            if safe_name in seen:
                continue
            slot_def = all_slots_for_base.get(slot_name_orig)
            slot_range = sv.induced_slot(slot_name_orig).range if slot_def else None
            value_type = _resolve_typedb_value_type(sv, slot_range)
            if value_type is None:
                continue  # object range → relation, not attribute
            doc_ann = _build_doc_annotation(slot_def.description if slot_def else None)
            if doc_ann:
                seen[safe_name] = f"attribute {safe_name} {doc_ann}, value {value_type};"
            else:
                seen[safe_name] = f"attribute {safe_name}, value {value_type};"

        # A slot whose own range is an enum gets @values(...) on the attribute. An enum set by
        # one class's slot_usage goes on that class's owns instead (see _values_annotation).
        enum_attr_lines: list[str] = []
        for slot_name_orig, slot_name in attr_names.items():
            enum_name = sv.induced_slot(slot_name_orig).range
            if enum_name not in sv.all_enums() or slot_name not in seen:
                continue
            values_ann = self._enum_values(enum_name)
            if values_ann is None:
                continue  # no static values: stays a plain string attribute
            enum_attr_lines.append(f"# Enum: {_typedb_name(enum_name)}")
            seen.pop(slot_name)
            enum_attr_lines.append(f"attribute {slot_name}, value string {values_ann};")

        # Attribute subtyping: slot is_a becomes sub (slot mixins are dropped). Iterated to a
        # fixed point so multi-level chains resolve regardless of dict order.
        all_slots = sv.all_slots()
        changed = True
        # A subtype inherits its parent's value type, so a child with a different one stays separate.
        value_type_of = {name: line.rsplit("value ", 1)[1].rstrip(";") for name, line in seen.items()}
        while changed:
            changed = False
            for slot_name_orig, safe_name in attr_names.items():
                if safe_name not in seen or seen[safe_name].startswith(f"attribute {safe_name}, sub "):
                    continue
                slot_def = all_slots.get(slot_name_orig)
                if slot_def and slot_def.is_a:
                    parent_safe = attr_names.get(slot_def.is_a)
                    if parent_safe and parent_safe in seen and value_type_of[parent_safe] == value_type_of[safe_name]:
                        seen[safe_name] = f"attribute {safe_name}, sub {parent_safe};"
                        changed = True

        result = list(seen.values()) + enum_attr_lines
        return result

    def _ancestor_slot_names(self, sv: SchemaView, class_name: str) -> set[str]:
        """Return the set of slot names inherited from non-mixin ancestors (excluding self).

        Mixin ancestors are skipped because TypeDB has single ``sub`` inheritance
        only — there is no mixin/trait mechanism.  Mixin-contributed slots must be
        redeclared on each consuming class as ``owns`` / ``plays``.
        """
        result: set[str] = set()
        for ancestor in sv.class_ancestors(class_name)[1:]:  # skip self
            ancestor_def = sv.get_class(ancestor)
            if ancestor_def and ancestor_def.mixin:
                continue  # mixin slots must be redeclared; TypeDB has no mixin inheritance
            for slot in sv.class_induced_slots(ancestor):
                result.add(slot.name)
        return result

    def _narrowed_inherited_slots(self, sv: SchemaView, class_name: str) -> list[SlotDefinition]:
        """Return inherited slots whose constraints this class tightens via ``slot_usage``.

        Range, pattern and enum values are compared. TypeDB accepts a redeclared ``owns``
        that adds a constraint, but rejects a plain repeat (``[SVL42]``).

        :return: induced slots on ``class_name`` that constrain an inherited slot further
        """
        parent = sv.get_class(class_name).is_a
        if not parent:
            return []
        parent_slot_names = {s.name for s in sv.class_induced_slots(parent)}
        narrowed: list[SlotDefinition] = []
        for induced in sv.class_induced_slots(class_name):
            if induced.name not in parent_slot_names:
                continue
            if _resolve_typedb_value_type(sv, induced.range) is None:
                continue  # object-ranged slots are roles, handled elsewhere
            inherited = sv.induced_slot(induced.name, parent)
            if (
                _build_range_annotation(induced) != _build_range_annotation(inherited)
                or _build_regex_annotation(induced) != _build_regex_annotation(inherited)
                or self._values_annotation(induced) != self._values_annotation(inherited)
            ):
                narrowed.append(induced)
        return narrowed

    def _enum_values(self, enum_name: str) -> str | None:
        """Return a ``@values(...)`` annotation listing an enum's permissible values.

        Returns ``None`` for an enum with no static values (e.g. a dynamic ``reachable_from``
        enum), which is then a plain ``string``.
        """
        enum_def = self.schemaview.get_enum(enum_name)
        permitted = list(enum_def.permissible_values.keys()) if enum_def else []
        if not permitted:
            return None
        return f"@values({', '.join(_typeql_string(v) for v in permitted)})"

    def _values_annotation(self, induced: SlotDefinition) -> str | None:
        """Return ``@values(...)`` for an owns whose enum range differs from the slot's own range."""
        sv = self.schemaview
        if induced.range not in sv.all_enums() or sv.induced_slot(induced.name).range == induced.range:
            return None
        return self._enum_values(induced.range)

    def _build_owns_narrowing_stmt(self, slot_tname: str, induced: SlotDefinition) -> str:
        """Return an ``owns`` statement with only the narrowing range/regex annotations.

        Cardinality and ``@key`` are inherited unchanged, so they are omitted.
        """
        owns = f"owns {slot_tname}"
        for ann in (
            _build_range_annotation(induced),
            _build_regex_annotation(induced),
            self._values_annotation(induced),
        ):
            if ann:
                owns += f" {ann}"
        return owns

    def _build_owns_stmt(self, slot_tname: str, induced: SlotDefinition) -> str:
        """Return a TypeQL ``owns`` statement with cardinality/range/regex/doc annotations.

        Uses ``minimum_cardinality`` / ``maximum_cardinality`` / ``exact_cardinality``
        when set, falling back to the boolean flags (``required``, ``multivalued``,
        ``identifier``) for backwards compatibility.

        :param slot_tname: the safe TypeDB attribute name for the slot
        :param induced: the induced SlotDefinition carrying cardinality/constraint metadata
        :return: a TypeQL ``owns`` clause string (without trailing punctuation)
        """
        owns = f"owns {slot_tname}"
        if induced.identifier:
            owns += " @key"
        elif induced.exact_cardinality is not None:
            owns += f" {_card(induced.exact_cardinality, induced.exact_cardinality)}"
        elif induced.minimum_cardinality is not None or induced.maximum_cardinality is not None:
            lo = induced.minimum_cardinality if induced.minimum_cardinality is not None else 0
            hi = str(induced.maximum_cardinality) if induced.maximum_cardinality is not None else ""
            owns += f" {_card(lo, hi)}"
        elif induced.required and not induced.multivalued:
            owns += " @card(1)"
        elif induced.multivalued:
            owns += " @card(0..)"

        range_ann = _build_range_annotation(induced)
        if range_ann:
            owns += f" {range_ann}"
        regex_ann = _build_regex_annotation(induced)
        if regex_ann:
            owns += f" {regex_ann}"
        values_ann = self._values_annotation(induced)
        if values_ann:
            owns += f" {values_ann}"
        return owns

    def _build_relates_stmt(self, role_name: str, induced: SlotDefinition) -> str:
        """Return a TypeQL ``relates`` statement with a cardinality annotation.

        Uses the same cardinality rules as ``_build_owns_stmt``.

        :param role_name: the safe TypeDB role name
        :param induced: the induced SlotDefinition carrying cardinality metadata
        :return: a TypeQL ``relates`` clause string (without trailing punctuation)
        """
        relates = f"relates {role_name}"
        if induced.exact_cardinality is not None:
            relates += f" {_card(induced.exact_cardinality, induced.exact_cardinality)}"
        elif induced.minimum_cardinality is not None or induced.maximum_cardinality is not None:
            lo = induced.minimum_cardinality if induced.minimum_cardinality is not None else 0
            hi = str(induced.maximum_cardinality) if induced.maximum_cardinality is not None else ""
            relates += f" {_card(lo, hi)}"
        elif induced.required and not induced.multivalued:
            relates += " @card(1)"
        elif induced.multivalued:
            relates += " @card(0..)"
        return relates

    def _build_plays_stmt(self, rel_tname: str, role_name: str, induced: SlotDefinition | None = None) -> str:
        """Return a TypeQL ``plays`` statement, with the slot's cardinality if given.

        Slot relations hold one link per value, so a slot's cardinality counts the links
        its owner takes part in, which is ``@card`` on the owner's ``plays``.

        :param rel_tname: the safe TypeDB relation type name
        :param role_name: the safe TypeDB role name being played
        :param induced: the slot whose cardinality applies; omit for the range side
        :return: a TypeQL ``plays`` clause string (without trailing punctuation)
        """
        plays = f"plays {rel_tname}:{role_name}"
        if induced is None:
            return plays
        if induced.exact_cardinality is not None:
            lo = hi = str(induced.exact_cardinality)
        elif induced.minimum_cardinality is not None or induced.maximum_cardinality is not None:
            lo = str(induced.minimum_cardinality or 0)
            hi = str(induced.maximum_cardinality) if induced.maximum_cardinality is not None else ""
        else:
            lo = "1" if induced.required else "0"
            hi = "" if induced.multivalued else "1"
        return f"{plays} {_card(lo, hi)}"

    def _player_classes_for_range(self, sv: SchemaView, range_name: str) -> list[str]:
        """Return the concrete classes that may play a role whose LinkML range is ``range_name``.

        Mixins are not emitted as TypeDB types, so a mixin range resolves to the concrete
        classes that include it. Only the topmost of those are returned, since TypeDB
        rejects redeclaring an inherited ``plays`` (``[SVL42]``).

        :param range_name: the LinkML class name a slot's range points at
        :return: concrete class names that should receive the ``plays`` declaration
        """
        range_def = sv.get_class(range_name)
        if range_def is None or not range_def.mixin:
            return [range_name]
        implementers = {
            cn for cn, cd in sv.all_classes().items() if not cd.mixin and range_name in sv.class_ancestors(cn)
        }
        # Drop implementers that inherit the capability from another implementer via
        # `is_a` (the only edge TypeDB's `sub` chain follows), keeping the topmost.
        result = []
        for cn in implementers:
            ancestor = sv.get_class(cn).is_a
            covered = False
            while ancestor:
                if ancestor in implementers:
                    covered = True
                    break
                ancestor = sv.get_class(ancestor).is_a if sv.get_class(ancestor) else None
            if not covered:
                result.append(cn)
        return result

    def _collect_entity_defs(
        self,
        sv: SchemaView,
        attr_names: dict[str, str],
        rel_names: dict[str, str],
        role_names: dict[str, tuple[str, str]],
        relationship_classes: set[str],
        relationship_role_info: dict[tuple[str, str], "_RoleInfo"],
        class_range_narrowings: list["_ClassRangeNarrowing"],
        slot_relations: dict[str, "_SlotRelation"],
    ) -> list[str]:
        """Return entity and relation-class type definition lines including owns, relates, and plays.

        Only directly-declared slots are emitted as ``owns``, ``relates``, and ``plays``
        on each type — TypeDB 3.x inherits capabilities from supertypes and
        raises an error if a subtype redeclares an already-inherited capability.

        Relationship classes are emitted as TypeDB ``relation`` types: their object-ranged
        slots become ``relates`` role declarations and their range classes receive
        ``plays`` declarations; scalar slots become ``owns``.

        :param attr_names: slot name → safe TypeDB attribute name
        :param rel_names: slot name → safe TypeDB relation name
        :param role_names: slot name → (owning_role_name, played_role_name)
        :param relationship_classes: class names to emit as ``relation``
        :param relationship_role_info: (class_name, slot_name) → resolved role info
        :param class_range_narrowings: output of ``_build_class_range_narrowings``
        :param slot_relations: output of ``_build_slot_relations``
        """
        # Pre-compute ancestor slot names and direct induced slots for all classes.
        # ``_ancestor_slot_names`` already skips mixin ancestors, so mixin-contributed
        # slots appear as "direct" on the consuming class.
        ancestor_slot_names_cache: dict[str, set[str]] = {
            cn: self._ancestor_slot_names(sv, cn) for cn in sv.all_classes()
        }
        narrowing_by_class_slot: dict[tuple[str, str], _ClassRangeNarrowing] = {
            (n.narrowing_class, n.slot_name): n for n in class_range_narrowings
        }
        direct_slots_cache: dict[str, list[SlotDefinition]] = {
            cn: [
                s
                for s in sv.class_induced_slots(cn)
                # Inherited slots are skipped, unless this class narrows their range.
                if s.name not in ancestor_slot_names_cache[cn] or (cn, s.name) in narrowing_by_class_slot
            ]
            for cn in sv.all_classes()
        }
        all_class_names = set(sv.all_classes().keys())

        # A scalar slot no class declares is owned by its domain class (abstract slots excepted).
        declared_slot_names = {s.name for cn in sv.all_classes() for s in sv.class_induced_slots(cn)}
        domain_owned: dict[str, list[SlotDefinition]] = {cn: [] for cn in sv.all_classes()}
        for slot_name, slot_def in sv.all_slots().items():
            if slot_name in declared_slot_names or slot_def.abstract:
                continue
            induced = sv.induced_slot(slot_name)
            if not induced.domain or _resolve_typedb_value_type(sv, induced.range) is None:
                continue
            for owner in self._player_classes_for_range(sv, induced.domain):
                if owner in domain_owned:
                    domain_owned[owner].append(induced)

        # class_name -> list of (typeql_plays_statement)
        plays_map: dict[str, list[str]] = {cn: [] for cn in sv.all_classes()}

        # Relationship classes: every object-ranged slot, inherited or direct.
        for class_name in relationship_classes:
            class_def = sv.get_class(class_name)
            if class_def.mixin:
                continue
            for induced in sv.class_induced_slots(class_name):
                if induced.range not in all_class_names:
                    continue
                info = relationship_role_info.get((class_name, induced.name))
                if info is None:
                    continue
                rel_tname = _typedb_name(info.declared_on)
                plays_stmt = self._build_plays_stmt(rel_tname, info.role_name)
                for player in self._player_classes_for_range(sv, induced.range):
                    if player in plays_map:
                        plays_map[player].append(plays_stmt)

        # Entity classes: the declaring class plays the owning role, the range the played role.
        for class_name in sv.all_classes():
            class_def = sv.get_class(class_name)
            if class_def.mixin or class_name in relationship_classes:
                continue  # handled above or skipped
            for induced in direct_slots_cache[class_name]:
                if induced.range not in all_class_names:
                    continue
                narrowing = narrowing_by_class_slot.get((class_name, induced.name))
                if narrowing is not None:
                    narrowed_stmt = self._build_plays_stmt(narrowing.sub_relation, narrowing.narrowed_played_role)
                    for player in self._player_classes_for_range(sv, narrowing.narrowed_range):
                        if player in plays_map:
                            plays_map[player].append(narrowed_stmt)
                    if induced.name in ancestor_slot_names_cache[class_name]:
                        continue  # the owning role's plays is inherited

                sr = slot_relations[induced.name]
                plays_map[class_name].append(self._build_plays_stmt(sr.relation, sr.owning_role, induced))
                if narrowing is None:
                    played_stmt = self._build_plays_stmt(sr.played_declared_on, sr.played_role)
                    for player in self._player_classes_for_range(sv, induced.range):
                        if player in plays_map:
                            plays_map[player].append(played_stmt)

                # Players of a slot's owning role also play every role below it in the hierarchy.
                for descendant in self._slot_relation_descendants(slot_relations, induced.name):
                    d = slot_relations[descendant]
                    plays_map[class_name].append(self._build_plays_stmt(d.relation, d.owning_role, d.induced))
                    if d.played_specializes:
                        d_stmt = self._build_plays_stmt(d.relation, d.played_role)
                        for player in self._player_classes_for_range(sv, d.induced.range):
                            if player in plays_map:
                                plays_map[player].append(d_stmt)

        # A slot no class declares is played by its domain class, and its range class plays the
        # other end. Each level uses its own (possibly inherited) domain; nothing propagates down.
        for slot_name, sr in slot_relations.items():
            if sr.declared or not sr.induced.domain or sv.get_slot(slot_name).abstract:
                continue
            owning_stmt = self._build_plays_stmt(sr.relation, sr.owning_role, sr.induced)
            for player in self._player_classes_for_range(sv, sr.induced.domain):
                if player in plays_map:
                    plays_map[player].append(owning_stmt)
            played_stmt = self._build_plays_stmt(sr.played_declared_on, sr.played_role)
            for player in self._player_classes_for_range(sv, sr.induced.range):
                if player in plays_map:
                    plays_map[player].append(played_stmt)

        # Drop plays a class already inherits through sub, which TypeDB rejects ([SVL42]).
        def sub_ancestors(class_name: str) -> list[str]:
            result, cur = [], sv.get_class(class_name)
            while cur.is_a and (cur.is_a in relationship_classes) == (class_name in relationship_classes):
                parent = sv.get_class(cur.is_a)
                if parent is None or parent.mixin:
                    break
                result.append(cur.is_a)
                cur = parent
            return result

        plays_map = {
            cn: [
                stmt
                for stmt in dict.fromkeys(stmts)
                if not any(stmt in plays_map.get(a, []) for a in sub_ancestors(cn))
            ]
            for cn, stmts in plays_map.items()
        }

        lines: list[str] = []
        for class_name, class_def in sv.all_classes().items():
            if class_def.mixin:
                continue  # mixins are not emitted as TypeDB types
            tname = _typedb_name(class_name)
            is_rel_class = class_name in relationship_classes
            is_abstract = bool(class_def.abstract) and self._abstract_ok(sv, class_name)

            parts: list[str] = []
            warnings: list[str] = []
            if class_def.abstract and not is_abstract:
                warnings.append(
                    f"  # WARNING: '{tname}' is abstract in LinkML but its supertype "
                    f"'{_typedb_name(class_def.is_a)}' is not; TypeDB requires an abstract "
                    "type's direct supertype to also be abstract [SVL14]. @abstract dropped "
                    "here rather than propagated to the (likely intentionally concrete) "
                    "supertype — review whether the supertype should be abstract instead."
                )

            doc_ann = _build_doc_annotation(class_def.description)

            is_a_parent = sv.get_class(class_def.is_a) if class_def.is_a else None
            # No `sub` when is_a points at a mixin, or a relation's parent is not a relation.
            is_a_is_mixin = bool(is_a_parent and is_a_parent.mixin)
            is_a_not_relationship = bool(class_def.is_a) and class_def.is_a not in relationship_classes

            if is_rel_class:
                # Emit as TypeDB relation type, not entity
                label = f"relation {tname}"
                if doc_ann:
                    label += f" {doc_ann}"
                if is_abstract:
                    label += " @abstract"
                parts.append(label)
                has_relation_supertype = bool(class_def.is_a) and not is_a_is_mixin and not is_a_not_relationship
                if has_relation_supertype:
                    parts[0] += f", sub {_typedb_name(class_def.is_a)}"

                # All induced slots, since a range can be narrowed anywhere in the chain.
                for induced in sv.class_induced_slots(class_name):
                    if induced.range not in all_class_names:
                        continue
                    info = relationship_role_info.get((class_name, induced.name))
                    if info is None or not info.introduced_here:
                        continue  # inherited unchanged from an ancestor; nothing to emit
                    if info.specializes:
                        parts.append(f"relates {info.role_name} as {info.specializes}")
                    else:
                        parts.append(self._build_relates_stmt(info.role_name, induced))

                # Scalar slots: direct ones only, since inherited ones can't be redeclared. A root
                # relation inherits nothing, so it also declares slots from non-relation ancestors.
                scalar_slots = direct_slots_cache[class_name] if has_relation_supertype else sv.class_induced_slots(class_name)
                for induced in scalar_slots:
                    value_type = _resolve_typedb_value_type(sv, induced.range)
                    if value_type is not None:
                        slot_tname = attr_names.get(induced.name, _typedb_name(induced.name))
                        parts.append(self._build_owns_stmt(slot_tname, induced))
                if has_relation_supertype:
                    for induced in self._narrowed_inherited_slots(sv, class_name):
                        slot_tname = attr_names.get(induced.name, _typedb_name(induced.name))
                        parts.append(self._build_owns_narrowing_stmt(slot_tname, induced))
                domain_sources = [class_name]
                if not has_relation_supertype:
                    domain_sources += [
                        a for a in sv.class_ancestors(class_name)[1:] if not sv.get_class(a).mixin
                    ]
                for source in domain_sources:
                    for induced in domain_owned.get(source, []):
                        slot_tname = attr_names.get(induced.name, _typedb_name(induced.name))
                        parts.append(self._build_owns_stmt(slot_tname, induced))
            else:
                # Emit as TypeDB entity type
                label = f"entity {tname}"
                if doc_ann:
                    label += f" {doc_ann}"
                if is_abstract:
                    label += " @abstract"
                parts.append(label)
                if class_def.is_a and not is_a_is_mixin:
                    parts[0] += f", sub {_typedb_name(class_def.is_a)}"

                # Slots that appear on ANY non-mixin ancestor are already inherited
                # in TypeDB — redeclaring them causes [SVL42].
                for induced in direct_slots_cache[class_name]:
                    value_type = _resolve_typedb_value_type(sv, induced.range)
                    if value_type is None:
                        continue  # object range → relation
                    slot_tname = attr_names.get(induced.name, _typedb_name(induced.name))
                    parts.append(self._build_owns_stmt(slot_tname, induced))
                for induced in domain_owned[class_name]:
                    slot_tname = attr_names.get(induced.name, _typedb_name(induced.name))
                    parts.append(self._build_owns_stmt(slot_tname, induced))

                # An inherited slot the class narrows via slot_usage is redeclared with
                # just the tightened constraints, which TypeDB accepts as a narrowing.
                for induced in self._narrowed_inherited_slots(sv, class_name):
                    slot_tname = attr_names.get(induced.name, _typedb_name(induced.name))
                    parts.append(self._build_owns_narrowing_stmt(slot_tname, induced))

                for plays_stmt in dict.fromkeys(plays_map.get(class_name, [])):
                    parts.append(plays_stmt)

            # For relation classes, also append plays from plays_map (if any)
            if is_rel_class:
                for plays_stmt in dict.fromkeys(plays_map.get(class_name, [])):
                    parts.append(plays_stmt)

            lines.extend(warnings)
            if len(parts) == 1:
                lines.append(f"{parts[0]};")
            else:
                lines.append(f"{parts[0]},")
                for p in parts[1:-1]:
                    lines.append(f"    {p},")
                lines.append(f"    {parts[-1]};")
            lines.append("")

        return lines

    def _collect_relation_defs(
        self,
        sv: SchemaView,
        slot_relations: dict[str, "_SlotRelation"],
        class_range_narrowings: list["_ClassRangeNarrowing"],
    ) -> list[str]:
        """Return relation type definition lines for all object-ranged slots.

        One relation type per class-ranged slot, as a sub-relation of its ``is_a`` parent's
        relation where there is one, plus a sub-relation for each range narrowing on an
        ordinary subclass.

        :param slot_relations: output of ``_build_slot_relations``
        :param class_range_narrowings: output of ``_build_class_range_narrowings``
        """
        narrowings_by_slot: dict[str, list[_ClassRangeNarrowing]] = {}
        for n in class_range_narrowings:
            narrowings_by_slot.setdefault(n.slot_name, []).append(n)

        all_slots = sv.all_slots()
        lines: list[str] = []
        for slot_name, sr in slot_relations.items():
            parts = [f"relation {sr.relation}"]
            doc_ann = _build_doc_annotation(all_slots[slot_name].description)
            if doc_ann:
                parts[0] += f" {doc_ann}"
            # One link per value: every link has exactly one owner and one target.
            if sr.parent:
                parent = slot_relations[sr.parent]
                parts.append(f"sub {parent.relation}")
                parts.append(f"relates {sr.owning_role} as {parent.owning_role} @card(1)")
                if sr.played_specializes:
                    parts.append(f"relates {sr.played_role} as {sr.played_specializes} @card(1)")
            else:
                parts.append(f"relates {sr.owning_role} @card(1)")
                parts.append(f"relates {sr.played_role} @card(1)")
            lines.append(f"{parts[0]},")
            lines.extend(f"    {p}," for p in parts[1:-1])
            lines.append(f"    {parts[-1]};")
            lines.append("")

            for n in narrowings_by_slot.get(slot_name, []):
                lines.append(f"relation {n.sub_relation} sub {n.base_relation},")
                lines.append(f"    relates {n.narrowed_played_role} as {n.base_played_role} @card(1);")
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
