"""Shared LinkML-to-TypeDB naming rules.

The TypeQL generator (:mod:`linkml.generators.typedbgen`) and any client that has to
address the types it defines, such as a data loader, must agree exactly on every label
it chooses. The decisions live here so both read them from one place:

- LinkML type to TypeDB value type (:data:`TYPEDB_PRIMITIVE`, :func:`resolve_typedb_value_type`)
- TypeDB reserved keywords and the suffixes that avoid them (:data:`TYPEDB_RESERVED`, :func:`typedb_name`)
- attribute and relation labels, deduplicated across type kinds (:func:`build_name_maps`)
- role labels, including specialization along ``is_a`` (:func:`build_role_names`, :func:`build_relationship_role_info`)
- sub-relations emitted for ``slot_usage`` range narrowing (:func:`build_class_range_narrowings`)

Nothing here emits TypeQL statements; it only decides what things are called.
"""

from dataclasses import dataclass

from linkml_runtime.utils.schemaview import SchemaView

# Maps LinkML / XSD type local-names to TypeDB primitive value types.
TYPEDB_PRIMITIVE: dict[str, str] = {
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
# Covers every word in the ``reserved`` rule of the TypeQL grammar
# (https://github.com/typedb/typeql/blob/master/rust/parser/typeql.pest), plus other keywords
# from the TypeQL keyword glossary (https://typedb.com/docs/typeql-reference/keywords/).
TYPEDB_RESERVED: frozenset[str] = frozenset(
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
        "given",
        "end",
        # Pattern logic
        "or",
        "not",
        "try",
        # Type statements
        "entity",
        "relation",
        "attribute",
        "role",
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
        "first",
        "last",
        "return",
        "of",
        "from",
        "in",
        "as",
        "type",
    }
)


def typeql_string(value: str) -> str:
    """Return ``value`` as an escaped, double-quoted TypeQL string literal.

    Newlines and tabs are escaped because TypeQL string literals are single-line.
    """
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n").replace("\t", "\\t")
    return f'"{escaped}"'


def typedb_name(name: str) -> str:
    """Convert a LinkML name to a TypeDB type label.

    Whitespace becomes underscores; everything else is kept verbatim. Reserved TypeDB
    keywords are suffixed with ``_attr`` to avoid parse errors.

    Examples:
        >>> typedb_name("GeneToDiseaseAssociation")
        'GeneToDiseaseAssociation'
        >>> typedb_name("gene to disease association")
        'gene_to_disease_association'
        >>> typedb_name("match")
        'match_attr'
    """
    result = "_".join(name.split())
    if result in TYPEDB_RESERVED:
        result = result + "_attr"
    return result


def resolve_typedb_value_type(sv: SchemaView, range_name: str | None) -> str | None:
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

    primitives = TYPEDB_PRIMITIVE

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


def check_class_name_collisions(sv: SchemaView) -> None:
    """Raise if two distinct LinkML class names map to the same TypeDB label.

    This happens when names differ only in whitespace vs underscores
    (``gene to disease`` and ``gene_to_disease``).

    :raises ValueError: if any TypeDB label is claimed by more than one class
    """
    by_label: dict[str, list[str]] = {}
    for class_name in sv.all_classes():
        by_label.setdefault(typedb_name(class_name), []).append(class_name)
    clashes = {label: names for label, names in by_label.items() if len(names) > 1}
    if clashes:
        detail = "; ".join(f"{label!r} <- {sorted(names)}" for label, names in sorted(clashes.items()))
        raise ValueError(
            f"Cannot generate TypeQL: distinct LinkML classes map to the same TypeDB label ({detail}). "
            "TypeDB labels must be unique; rename the conflicting classes in the source schema."
        )


def check_slot_name_collisions(sv: SchemaView, slot_ranges: dict[str, str | None]) -> None:
    """Raise if two distinct LinkML slot names map to the same TypeDB label of one kind.

    Same failure as :func:`check_class_name_collisions`, one level down: ``has name`` and
    ``has_name`` both become ``has_name``. Where the two land on different kinds the
    suffixing in :func:`build_name_maps` separates them, so only a collision within one
    kind is an error. Left unchecked the second slot's value type is silently dropped.

    :param slot_ranges: slot name -> range, from :func:`slot_ranges`
    :raises ValueError: if any kind's TypeDB label is claimed by more than one slot
    """
    all_class_names = set(sv.all_classes().keys())
    by_label: dict[tuple[str, str], set[str]] = {}

    def record(slot_name: str, slot_range: str | None) -> None:
        kind = "relation" if slot_range in all_class_names else "attribute"
        by_label.setdefault((kind, typedb_name(slot_name)), set()).add(slot_name)

    for slot_name, slot_range in slot_ranges.items():
        record(slot_name, slot_range)
    # Inline ``attributes:`` are not in ``all_slots()``, so walk the classes too.
    for class_name in sv.all_classes():
        for slot in sv.class_induced_slots(class_name):
            record(slot.name, slot.range)

    clashes = {key: names for key, names in by_label.items() if len(names) > 1}
    if clashes:
        detail = "; ".join(f"{kind} {label!r} <- {sorted(names)}" for (kind, label), names in sorted(clashes.items()))
        raise ValueError(
            f"Cannot generate TypeQL: distinct LinkML slots map to the same TypeDB label ({detail}). "
            "TypeDB labels must be unique; rename the conflicting slots in the source schema."
        )


def reserved_labels(sv: SchemaView, attr_names: dict[str, str], rel_names: dict[str, str]) -> set[str]:
    """Return every TypeDB label already claimed by an entity, attribute or relation.

    Generated names that are not derived from a LinkML name, such as the sub-relations
    emitted for range narrowing, are checked against this so they cannot collide with a
    label the schema already uses.
    """
    return {typedb_name(cn) for cn in sv.all_classes()} | set(attr_names.values()) | set(rel_names.values())


def uniquify_label(candidate: str, taken: set[str], suffix: str) -> str:
    """Return ``candidate``, or the first free ``candidate + suffix[n]`` if it is taken."""
    if candidate not in taken:
        return candidate
    attempt = candidate + suffix
    counter = 2
    while attempt in taken:
        attempt = f"{candidate}{suffix}{counter}"
        counter += 1
    return attempt


def find_label_case_collisions(
    sv: SchemaView,
    attr_names: dict[str, str],
    rel_names: dict[str, str],
) -> dict[str, list[str]]:
    """Group emitted TypeDB labels that differ only by case.

    TypeDB labels are case-sensitive, so ``Pathway`` the entity and ``pathway`` the
    relation coexist legally. They are also near-indistinguishable to a reader, and
    LinkML itself treats sharing a name between a class and a slot as bad practice.
    Exact clashes are already resolved by :func:`build_name_maps`, so what is left to
    report is the case-only kind.

    :param attr_names: slot name -> attribute label (from :func:`build_name_maps`)
    :param rel_names: slot name -> relation label (from :func:`build_name_maps`)
    :return: lowercased label -> sorted ``"<kind> <label>"`` descriptions, only for
        labels claimed by more than one kind
    """
    by_lower: dict[str, set[str]] = {}
    for class_name in sv.all_classes():
        label = typedb_name(class_name)
        by_lower.setdefault(label.lower(), set()).add(f"entity {label}")
    for label in attr_names.values():
        by_lower.setdefault(label.lower(), set()).add(f"attribute {label}")
    for label in rel_names.values():
        by_lower.setdefault(label.lower(), set()).add(f"relation {label}")
    return {
        lowered: sorted(kinds)
        for lowered, kinds in sorted(by_lower.items())
        if len({k.split(" ", 1)[1] for k in kinds}) > 1
    }


def slot_ranges(sv: SchemaView) -> dict[str, str | None]:
    """Return each slot's range, inherited through slot ``is_a`` when not set on the slot."""
    return {name: sv.induced_slot(name).range for name in sv.all_slots()}


def build_name_maps(sv: SchemaView, slot_ranges: dict[str, str | None]) -> tuple[dict[str, str], dict[str, str]]:
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
    entity_names = {typedb_name(cn) for cn in sv.all_classes()}

    # ── Attribute names ───────────────────────────────────────────────────────
    all_class_names = set(sv.all_classes().keys())
    attr_names: dict[str, str] = {}
    for class_name in sv.all_classes():
        for slot in sv.class_induced_slots(class_name):
            if slot.name in attr_names:
                continue
            if slot.range in all_class_names:
                continue  # object-ranged → relation, not attribute
            candidate = typedb_name(slot.name)
            if candidate in entity_names:
                candidate = candidate + "_attr"
            attr_names[slot.name] = candidate

    # Unattached scalar slots too, so whole slot is_a trees can be emitted.
    for slot_name, slot_range in slot_ranges.items():
        if slot_name in attr_names or slot_range in all_class_names:
            continue
        candidate = typedb_name(slot_name)
        if candidate in entity_names:
            candidate = candidate + "_attr"
        attr_names[slot_name] = candidate

    # ── Relation names ────────────────────────────────────────────────────────
    # Relations are derived from object-ranged slots only. ``class_induced_slots``
    # returns the union of inherited slots, top-level ``slots:`` references, and
    # inline ``attributes:`` declarations, so all three sources contribute.
    taken = entity_names | set(attr_names.values())
    rel_names: dict[str, str] = {}
    candidates = [
        slot.name
        for class_name in sv.all_classes()
        for slot in sv.class_induced_slots(class_name)
        if slot.range in all_class_names
    ] + [slot_name for slot_name, slot_range in slot_ranges.items() if slot_range in all_class_names]
    for slot_name in candidates:
        if slot_name in rel_names:
            continue
        candidate = typedb_name(slot_name)
        if candidate in taken:
            candidate = candidate + "_rel"
        rel_names[slot_name] = candidate
        taken.add(candidate)

    return attr_names, rel_names


def build_role_names(sv: SchemaView, rel_names: dict[str, str]) -> dict[str, tuple[str, str]]:
    """Build role-label pairs for each object-ranged slot's relation.

    The owning role is named after the slot and the played role after the range class,
    so reflexive slots (``parent`` on ``person``) still get two distinct roles. If the
    two names collide, the played role gets a ``_role`` suffix.

    :param rel_names: slot name → safe TypeDB relation name (from ``build_name_maps``)
    :return: slot name → ``(owning_role_name, played_role_name)``
    """
    result: dict[str, tuple[str, str]] = {}
    for slot_name in sv.all_slots():
        # Name the played role after the slot's own range, not a class's slot_usage narrowing of it.
        induced = sv.induced_slot(slot_name)
        if induced.range not in sv.all_classes():
            for class_name in sv.all_classes():
                declared = next((s for s in sv.class_induced_slots(class_name) if s.name == slot_name), None)
                if declared is not None:
                    induced = declared
                    break
        if induced.range not in sv.all_classes():
            continue
        owning_role = typedb_name(slot_name)
        played_role = typedb_name(induced.range)
        if played_role == owning_role:
            played_role = played_role + "_role"
        result[slot_name] = (owning_role, played_role)
    return result


def is_relationship_class(sv: SchemaView, class_name: str) -> bool:
    """Return True if ``class_name`` should be emitted as a TypeDB ``relation``.

    The nearest class in the ``is_a`` chain that sets ``represents_relationship``
    (true or false) decides. If none does, fall back to ``SchemaView.is_relationship()``,
    which detects RDF statement reification (``rdf:Statement`` / ``owl:Axiom``).

    The fallback additionally requires at least one class-ranged slot. A reified
    statement whose subject, predicate and object are all CURIE-valued has no roles to
    relate, and TypeDB rejects a non-abstract relation type that relates nothing
    (``[SVL41]``); as an entity it loads. An explicit ``represents_relationship: true``
    is honoured either way, since overriding a stated intent is worse than failing at
    load time.
    """
    current = class_name
    while current:
        class_def = sv.get_class(current)
        if class_def is None:
            break
        if class_def.represents_relationship is not None:
            return bool(class_def.represents_relationship)
        current = class_def.is_a
    if not sv.is_relationship(class_name):
        return False
    return has_class_ranged_slot(sv, class_name)


def has_class_ranged_slot(sv: SchemaView, class_name: str) -> bool:
    """Return True if any of ``class_name``'s induced slots has a class as its range."""
    all_class_names = sv.all_classes()
    return any(slot.range in all_class_names for slot in sv.class_induced_slots(class_name))


@dataclass
class RoleInfo:
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


def build_relationship_role_info(sv: SchemaView, relationship_classes: set[str]) -> dict[tuple[str, str], RoleInfo]:
    """Compute per-(class, slot) role specialization info for relationship classes.

    A specialized role ``<range>_<parent-role>`` is introduced only where the range
    actually changes along the ``is_a`` chain; restating an unchanged range reuses the
    ancestor's role, since redeclaring it violates TypeDB's ``[SVL7]``.

    :param relationship_classes: the set of class names being emitted as relations
    :return: ``(class_name, slot_name) -> RoleInfo`` for every object-ranged slot
        directly usable on a relationship class (including inherited ones)
    """
    result: dict[tuple[str, str], RoleInfo] = {}
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
                base_role = typedb_name(slot_name)
                prior_range = last_range.get(slot_name)
                prior_role = last_role.get(slot_name, base_role)

                if prior_range is None:
                    result[(cls, slot_name)] = RoleInfo(
                        role_name=base_role, specializes=None, introduced_here=True, declared_on=cls
                    )
                    last_range[slot_name] = induced.range
                    last_role[slot_name] = base_role
                    last_declared_on[slot_name] = cls
                elif induced.range == prior_range:
                    result[(cls, slot_name)] = RoleInfo(
                        role_name=prior_role,
                        specializes=None,
                        introduced_here=False,
                        declared_on=last_declared_on[slot_name],
                    )
                else:
                    specialized = f"{typedb_name(induced.range)}_{prior_role}"
                    result[(cls, slot_name)] = RoleInfo(
                        role_name=specialized, specializes=prior_role, introduced_here=True, declared_on=cls
                    )
                    last_range[slot_name] = induced.range
                    last_role[slot_name] = specialized
                    last_declared_on[slot_name] = cls

    return result


@dataclass
class ClassRangeNarrowing:
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


def build_class_range_narrowings(
    sv: SchemaView,
    relationship_classes: set[str],
    rel_names: dict[str, str],
    role_names: dict[str, tuple[str, str]],
    taken: set[str] | None = None,
) -> list[ClassRangeNarrowing]:
    """Find class-ranged slots that an ordinary (non-relationship) subclass narrows.

    Each narrowing becomes a sub-relation of the slot's base relation with a specialized
    played role (``relates <narrowed> as <base>``), so queries on the base role still
    match data inserted through the narrowed one. Only the first class in an ``is_a``
    chain to change the range counts; unchanged restatements are skipped.

    :param relationship_classes: class names emitted as ``relation`` (skipped)
    :param rel_names: slot name → safe TypeDB base relation name
    :param role_names: slot name → (owning_role_name, played_role_name)
    :param taken: labels already claimed elsewhere in the schema (see
        :func:`reserved_labels`). A sub-relation name that would collide is suffixed
        instead; without this, an unrelated slot named like the generated sub-relation
        would be merged into it by TypeDB and silently become its subtype.
    :return: one ``ClassRangeNarrowing`` per class that introduces a real narrowing
    """
    all_class_names = set(sv.all_classes().keys())
    result: list[ClassRangeNarrowing] = []
    claimed = set(taken) if taken else set()

    for slot_name in sv.all_slots():
        base_range = sv.induced_slot(slot_name).range
        if base_range not in all_class_names:
            continue  # not a class-ranged slot at all

        owning_role, base_played_role = role_names.get(slot_name, (typedb_name(slot_name), typedb_name(base_range)))
        base_relation = rel_names.get(slot_name, typedb_name(slot_name))

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

            sub_relation = uniquify_label(f"{base_relation}_{typedb_name(class_name)}", claimed, "_rel")
            claimed.add(sub_relation)
            narrowed_played_role = f"{typedb_name(induced.range)}_{base_played_role}"
            result.append(
                ClassRangeNarrowing(
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
