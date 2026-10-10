"""Prune a schema to one of its declared subsets and to the elements that the subset's members need.

The base :class:`~linkml.utils.generator.Generator` applies this when its ``subset`` option is set,
so that every generator can emit one declared slice of a large schema instead of all of it
(linkml/linkml#1497 and linkml/linkml#2579). :func:`subset_closure` decides what to keep, and
:func:`prune_to_subset` builds the pruned :class:`~linkml_runtime.linkml_model.meta.SchemaDefinition`
that the generator then loads in place of the full one.
"""

from __future__ import annotations

import logging
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    AnonymousEnumExpression,
    AnonymousSlotExpression,
    ClassDefinition,
    ClassDefinitionName,
    EnumDefinition,
    EnumDefinitionName,
    SchemaDefinition,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
    TypeDefinitionName,
)

logger = logging.getLogger(__name__)

METAMODEL_IMPORT_PREFIXES = ("linkml:", "https://w3id.org/linkml/")
"""How an import of one of the LinkML metamodel's own schemas (``linkml:types`` and its siblings) is
written. Those imports stay imports in the pruned schema, just as the SchemaLoader keeps their
elements apart when it merges every other import (see :func:`linkml.utils.mergeutils.merge_dicts`)."""

KEPT_SLOT_FLAGS = ("identifier", "key", "designates_type")
"""Flags that keep a slot on a kept class even when the subset names other slots. A reference to the
class is written as the value of its identifier or key, and a polymorphic range is resolved through
its type designator, so a class without them would be serialized differently."""


@dataclass
class SubsetClosure:
    """The elements that one subset keeps, by kind.

    ``classes`` maps each kept class to the names of the slots it keeps: the slots it declares,
    inherits or refines with ``slot_usage`` that stay in the pruned schema. The pruning filters the
    class's ``slots``, ``attributes`` and ``slot_usage`` with that set. ``slots``, ``enums`` and
    ``types`` hold the names of the kept schema-level slots, enums and types.
    """

    subset_name: str
    classes: dict[ClassDefinitionName, set[SlotDefinitionName]] = field(default_factory=dict)
    slots: set[SlotDefinitionName] = field(default_factory=set)
    enums: set[EnumDefinitionName] = field(default_factory=set)
    types: set[TypeDefinitionName] = field(default_factory=set)


def subset_closure(schemaview: SchemaView, subset_name: str) -> SubsetClosure:
    """Return the elements of the schema to keep for one declared subset.

    The members of the subset are the elements whose ``in_subset`` names it, as
    :meth:`~linkml_runtime.utils.schemaview.SchemaView.get_elements_by_subset` returns them. The
    subset names slots when one of its members is a slot or an attribute, or when a class's
    ``slot_usage`` puts a slot in it. The closure keeps, over the whole imports closure:

    - the members themselves;
    - every ancestor of a kept class, through ``is_a`` and ``mixins``, so that inheritance still
      resolves; a mixin that a kept class uses is therefore kept, and so is a class that applies
      itself to a kept class through ``apply_to``, which the SchemaLoader turns into a mixin;
    - for every kept class, its induced slots. When the subset names no slot, every induced slot
      stays. When it names any, a class keeps the induced slots that are members for that class,
      which ``slot_usage`` and attributes can make class-specific, together with its identifier, key
      and type designator (see :data:`KEPT_SLOT_FLAGS`). A class of a LinkML metamodel schema keeps
      every induced slot, because those schemas stay imported in full;
    - for every slot that a class keeps, each declaration and ``slot_usage`` of it on the class's
      ancestors, so that the induced slot is the same as in the full schema. A slot that stays
      declared on an ancestor is inherited, so every kept class below that ancestor keeps it too;
    - every ancestor of a kept schema-level slot, and the slots that a kept slot names in
      ``subproperty_of``, ``slot_group``, ``transitive_form_of``, ``reflexive_transitive_form_of``
      and ``union_of``;
    - every class, enum and type that a kept slot refers to: its range, the ranges in its boolean
      expressions (``any_of``, ``exactly_one_of``, ``all_of``, ``none_of``) and in ``has_member``
      and ``all_members``, the enums that its ``enum_range`` inherits from, the classes in its
      ``range_expression``, and its ``domain``; likewise a kept class's ``union_of`` members and
      ``extra_slots`` range, a kept enum's ancestors and the enums it ``inherits`` from, a kept
      type's ``typeof`` chain and ``union_of`` members, and the schema's ``default_range``.

    The rules are applied together until nothing new is reached, so that no kept element refers to
    a dropped one; that is the reference closure. Everything else is dropped. Subset definitions are
    not part of the closure; :func:`prune_to_subset` keeps all of them so that ``in_subset`` values
    still resolve.

    :param schemaview: view of the schema, imports included
    :param subset_name: name of a subset that the schema declares
    :return: the kept elements by kind
    :raises ValueError: if the schema declares no subset of that name; the message lists the
        subsets that it does declare
    """
    sv = schemaview
    declared = sv.all_subsets()
    if subset_name not in declared:
        names = ", ".join(sorted(declared)) if declared else "none"
        msg = f'No such subset "{subset_name}"; the schema declares: {names}'
        raise ValueError(msg)

    metamodel_ids = {str(schema.id) for schema in _metamodel_schemas(sv).values()}
    all_classes = sv.all_classes()
    all_enums = sv.all_enums()
    all_types = sv.all_types()
    schema_slots = sv.all_slots(attributes=False)
    members = sv.get_elements_by_subset(subset_name)
    if not members:
        logger.warning(f"Subset {subset_name} has no members; the pruned schema will hold no classes")
    narrow = any(isinstance(element, SlotDefinition) for element in members) or any(
        subset_name in usage.in_subset for cls in all_classes.values() for usage in cls.slot_usage.values()
    )

    applied_to: dict[ClassDefinitionName, list[ClassDefinitionName]] = {}
    for cls in all_classes.values():
        for target in cls.apply_to:
            applied_to.setdefault(target, []).append(cls.name)

    closure = SubsetClosure(subset_name)
    class_queue: deque[ClassDefinitionName] = deque()
    class_slot_queue: deque[tuple[ClassDefinitionName, SlotDefinitionName]] = deque()
    slot_queue: deque[SlotDefinitionName] = deque()

    def add_class(name: str) -> None:
        for ancestor in sv.class_ancestors(name):
            if ancestor not in closure.classes:
                closure.classes[ancestor] = set()
                class_queue.append(ancestor)
                for applied in applied_to.get(ancestor, []):
                    add_class(applied)

    def add_slot(name: str | None) -> None:
        if name not in schema_slots:
            return
        for ancestor in sv.slot_ancestors(name):
            if ancestor in schema_slots and ancestor not in closure.slots:
                closure.slots.add(ancestor)
                slot_queue.append(ancestor)

    def add_enum(name: str) -> None:
        for ancestor in sv.enum_ancestors(name):
            if ancestor in all_enums and ancestor not in closure.enums:
                closure.enums.add(ancestor)
                for inherited in _enum_expression_references(all_enums[ancestor]):
                    add_reference(inherited)

    def add_type(name: str) -> None:
        for ancestor in sv.type_ancestors(name):
            if ancestor in all_types and ancestor not in closure.types:
                closure.types.add(ancestor)
                for member in all_types[ancestor].union_of:
                    add_reference(member)

    def add_reference(name: str | None) -> None:
        """Keep the class, enum or type of this name, if the schema has one."""
        if name in all_classes:
            add_class(name)
        elif name in all_enums:
            add_enum(name)
        elif name in all_types:
            add_type(name)

    def follow(expression: SlotDefinition | AnonymousSlotExpression | None) -> None:
        """Keep every element that a slot definition, or a slot expression, refers to."""
        if expression is None:
            return
        for name in _slot_expression_references(expression):
            add_reference(name)
        if isinstance(expression, SlotDefinition):
            add_reference(expression.domain)
            for name in (
                expression.is_a,
                *expression.mixins,
                expression.subproperty_of,
                expression.slot_group,
                expression.transitive_form_of,
                expression.reflexive_transitive_form_of,
                *expression.union_of,
            ):
                add_slot(name)

    def keep_slot(class_name: ClassDefinitionName, slot_name: SlotDefinitionName) -> None:
        if slot_name not in closure.classes[class_name]:
            closure.classes[class_name].add(slot_name)
            class_slot_queue.append((class_name, slot_name))

    def expand_class(class_name: ClassDefinitionName) -> None:
        cls = all_classes[class_name]
        for name in cls.union_of:
            add_reference(name)
        if cls.extra_slots is not None:
            follow(cls.extra_slots.range_expression)
        keeps_all = not narrow or str(cls.from_schema) in metamodel_ids
        for slot_name in sv.class_slots(class_name):
            slot = sv.induced_slot(slot_name, class_name)
            if keeps_all or subset_name in slot.in_subset or any(getattr(slot, flag) for flag in KEPT_SLOT_FLAGS):
                keep_slot(class_name, slot_name)
        # what a kept ancestor already declares is inherited
        for ancestor in sv.class_ancestors(class_name, reflexive=False):
            for slot_name in [s for s in closure.classes[ancestor] if _declares(all_classes[ancestor], s)]:
                keep_slot(class_name, slot_name)

    def expand_class_slot(class_name: ClassDefinitionName, slot_name: SlotDefinitionName) -> None:
        cls = all_classes[class_name]
        # the induced slot is built from every declaration and slot_usage of it among the ancestors
        for ancestor in sv.class_ancestors(class_name, reflexive=False):
            if _declares(all_classes[ancestor], slot_name) or slot_name in all_classes[ancestor].slot_usage:
                keep_slot(ancestor, slot_name)
        # and a declaration that stays is inherited by every kept class below it
        if _declares(cls, slot_name):
            for descendant in sv.class_descendants(class_name, reflexive=False):
                if descendant in closure.classes:
                    keep_slot(descendant, slot_name)
        if slot_name in cls.slots:
            add_slot(slot_name)
        if slot_name in sv.class_slots(class_name):
            follow(sv.induced_slot(slot_name, class_name))
        follow(cls.attributes.get(slot_name))
        follow(cls.slot_usage.get(slot_name))

    for element in members:
        if isinstance(element, ClassDefinition):
            add_class(element.name)
        elif isinstance(element, SlotDefinition):
            # a member attribute is not a schema-level slot; it stays with its class if that is kept
            add_slot(element.name)
        elif isinstance(element, EnumDefinition):
            add_enum(element.name)
        elif isinstance(element, TypeDefinition):
            add_type(element.name)
    add_reference(sv.schema.default_range)

    while class_queue or class_slot_queue or slot_queue:
        if class_queue:
            expand_class(class_queue.popleft())
        elif class_slot_queue:
            expand_class_slot(*class_slot_queue.popleft())
        else:
            follow(schema_slots[slot_queue.popleft()])
    return closure


def prune_to_subset(schemaview: SchemaView, subset_name: str) -> SchemaDefinition:
    """Return a copy of the schema that holds only what :func:`subset_closure` keeps.

    The copy is self-contained. Every imported schema is merged into it, apart from the LinkML
    metamodel's own (``linkml:types`` and its siblings, see :data:`METAMODEL_IMPORT_PREFIXES`), which
    stay imports because generators treat their elements as a standard library. So an imported model
    contributes only the elements that the subset reaches. The prefixes and settings of the merged
    schemas are added where the root schema does not define them, every subset definition is kept so
    that ``in_subset`` values still resolve, and the root schema's own metadata is unchanged. A class,
    slot, attribute or enum merged from an import would take the root schema's namespace, so the URI
    it has in the full schema is written out as its ``class_uri``, ``slot_uri`` or ``enum_uri``,
    unless it declares one.

    A kept class keeps the slots, attributes and slot usages that the closure keeps for it. A
    constraint that refers to a dropped slot, class, enum or type is dropped whole, which can only
    loosen validation: a unique key, the list of defining slots, a rule, a classification rule, one
    of the boolean expression lists ``any_of``, ``all_of``, ``exactly_one_of`` and ``none_of``, or a
    slot condition. A kept class keeps only the ``disjoint_with`` and ``apply_to`` classes that are
    kept, and a kept slot keeps only the ``disjoint_with`` slots and the ``inverse`` that are kept.
    Every slot definition, attribute and slot usage lists in ``domain_of`` only the classes that still
    have the slot.

    :param schemaview: view of the schema, imports included
    :param subset_name: name of a subset that the schema declares
    :return: the pruned schema
    :raises ValueError: if the schema declares no subset of that name
    """
    sv = schemaview
    closure = subset_closure(sv, subset_name)
    root = sv.schema
    metamodel = _metamodel_schemas(sv)
    metamodel_imports = [name for name in root.imports if name in metamodel]
    metamodel_imports += [name for name in metamodel if name not in metamodel_imports]
    metamodel_ids = {str(schema.id) for schema in metamodel.values()}

    # Dict-valued fields are edited in place throughout: assigning a new dict to a field of a
    # metamodel object would wrap it as a JsonObj, which the generators do not expect.
    pruned = deepcopy(root)
    pruned.imports = metamodel_imports
    for merged in sv.all_schema():
        if merged is root or str(merged.id) in metamodel_ids:
            continue
        for target, source in ((pruned.prefixes, merged.prefixes), (pruned.settings, merged.settings)):
            for name, value in source.items():
                if name not in target:
                    target[name] = deepcopy(value)
    _keep(pruned.subsets, sv.all_subsets(), set(sv.all_subsets()), metamodel_ids)
    _keep(pruned.classes, sv.all_classes(), set(closure.classes), metamodel_ids)
    _keep(pruned.slots, sv.all_slots(attributes=False), closure.slots, metamodel_ids)
    _keep(pruned.enums, sv.all_enums(), closure.enums, metamodel_ids)
    _keep(pruned.types, sv.all_types(), closure.types, metamodel_ids)
    for cls in pruned.classes.values():
        if str(cls.from_schema) != str(root.id):
            _pin_uri(cls, "class_uri", sv)
            for attribute in cls.attributes.values():
                _pin_uri(attribute, "slot_uri", sv)
    for slot in pruned.slots.values():
        if str(slot.from_schema) != str(root.id):
            _pin_uri(slot, "slot_uri", sv)
    for enum in pruned.enums.values():
        if str(enum.from_schema) != str(root.id):
            _pin_uri(enum, "enum_uri", sv)

    # the elements a constraint may refer to: those kept, and those the metamodel imports provide
    available = set(closure.classes) | closure.enums | closure.types
    available |= {name for name, element in sv.all_elements().items() if str(element.from_schema) in metamodel_ids}
    for class_name, cls in pruned.classes.items():
        kept = closure.classes[class_name]
        cls.slots = [name for name in cls.slots if name in kept]
        _delete_except(cls.attributes, kept)
        _delete_except(cls.slot_usage, kept)
        for name in list(cls.slot_conditions):
            if name not in kept or not _slot_expression_references(cls.slot_conditions[name]) <= available:
                del cls.slot_conditions[name]
        if not set(cls.defining_slots) <= kept:
            cls.defining_slots = []
        for name in list(cls.unique_keys):
            if not set(cls.unique_keys[name].unique_key_slots) <= kept:
                del cls.unique_keys[name]
        cls.rules = [
            rule
            for rule in cls.rules
            if all(
                _refers_only_to(condition, kept, available)
                for condition in (rule.preconditions, rule.postconditions, rule.elseconditions)
            )
        ]
        cls.classification_rules = [
            expression for expression in cls.classification_rules if _refers_only_to(expression, kept, available)
        ]
        for name in ("any_of", "all_of", "exactly_one_of", "none_of"):
            if not all(_refers_only_to(expression, kept, available) for expression in getattr(cls, name)):
                setattr(cls, name, [])
        cls.disjoint_with = [name for name in cls.disjoint_with if name in closure.classes]
        cls.apply_to = [name for name in cls.apply_to if name in closure.classes]
        for definition in (*cls.attributes.values(), *cls.slot_usage.values()):
            _trim_domain_of(definition, closure)
    for slot in pruned.slots.values():
        slot.disjoint_with = [name for name in slot.disjoint_with if name in closure.slots]
        if slot.inverse is not None and slot.inverse not in closure.slots:
            slot.inverse = None
        _trim_domain_of(slot, closure)
    return pruned


def _metamodel_schemas(schemaview: SchemaView) -> dict[str, SchemaDefinition]:
    """Return the LinkML metamodel schemas in the imports closure, keyed by the import that names them."""
    root = schemaview.schema
    schemaview.all_schema()  # resolves the imports closure, which fills schema_map and from_schema
    return {
        name: schema
        for name, schema in schemaview.schema_map.items()
        if schema is not root and name.startswith(METAMODEL_IMPORT_PREFIXES)
    }


def _declares(cls: ClassDefinition, slot_name: str) -> bool:
    """Return whether a class declares a slot, in its ``slots`` or as an attribute."""
    return slot_name in cls.slots or slot_name in cls.attributes


def _keep(target: dict, view: dict, keep: set[str], metamodel_ids: set[str]) -> None:
    """Reduce one kind of element in the pruned schema to the kept names, in place.

    ``target`` starts as the root schema's own elements and ends with those of them that are kept,
    in their order, followed by the kept elements that the merged imports add. ``view`` is the merged
    dictionary that the SchemaView gives, in which the root's definition of a name wins over an
    imported one. Elements of a metamodel schema are left out, since that schema stays imported.
    """
    _delete_except(target, keep)
    for name, element in view.items():
        if name in keep and name not in target and str(element.from_schema) not in metamodel_ids:
            target[name] = deepcopy(element)


def _trim_domain_of(slot: SlotDefinition, closure: SubsetClosure) -> None:
    """Keep only the classes in a slot's ``domain_of`` that still have the slot.

    ``domain_of`` is derived, and SchemaView adds to it in place whenever it induces a slot, so a copied
    definition can list classes that the pruning dropped.
    """
    slot.domain_of = [name for name in slot.domain_of if slot.name in closure.classes.get(name, ())]


def _pin_uri(element: ClassDefinition | SlotDefinition | EnumDefinition, uri_slot: str, schemaview: SchemaView) -> None:
    """Write out the URI that an element has in the full schema, unless the element declares one.

    A type is never passed here: its ``uri`` is its datatype, not its own URI.
    """
    if getattr(element, uri_slot) is None:
        setattr(element, uri_slot, schemaview.get_uri(element))


def _delete_except(target: dict, keep: set[str]) -> None:
    """Delete every entry of ``target`` whose key is not in ``keep``, in place."""
    for name in list(target):
        if name not in keep:
            del target[name]


def _slot_expression_references(expression: SlotDefinition | AnonymousSlotExpression) -> set[str]:
    """Return the names of the classes, enums and types that a slot expression refers to.

    These are its range, the ranges of the boolean expressions and of ``has_member`` and
    ``all_members`` nested in it, the enums that its ``enum_range`` inherits from, and the classes
    that its ``range_expression`` names.
    """
    names = {expression.range} if expression.range else set()
    for nested in (
        *expression.any_of,
        *expression.exactly_one_of,
        *expression.all_of,
        *expression.none_of,
        expression.has_member,
        expression.all_members,
    ):
        if nested is not None:
            names |= _slot_expression_references(nested)
    if expression.enum_range is not None:
        names |= _enum_expression_references(expression.enum_range)
    names |= _class_expression_references(expression.range_expression)[1]
    return names


def _enum_expression_references(expression: EnumDefinition | AnonymousEnumExpression) -> set[str]:
    """Return the names of the enums that an enum expression inherits from, in ``include`` and ``minus`` too."""
    names = set(expression.inherits)
    for nested in (*expression.include, *expression.minus):
        names |= _enum_expression_references(nested)
    return names


def _class_expression_references(expression: AnonymousClassExpression | None) -> tuple[set[str], set[str]]:
    """Return the slot names, and the class, enum and type names, that a class expression refers to.

    Nested boolean expressions are included, and a slot condition contributes both its slot and what
    its slot expression refers to.
    """
    slots: set[str] = set()
    elements: set[str] = set()
    if expression is None:
        return slots, elements
    if expression.is_a:
        elements.add(expression.is_a)
    for name, condition in expression.slot_conditions.items():
        slots.add(name)
        elements |= _slot_expression_references(condition)
    for nested in (*expression.any_of, *expression.all_of, *expression.exactly_one_of, *expression.none_of):
        nested_slots, nested_elements = _class_expression_references(nested)
        slots |= nested_slots
        elements |= nested_elements
    return slots, elements


def _refers_only_to(expression: AnonymousClassExpression | None, slots: set[str], elements: set[str]) -> bool:
    """Return whether a class expression refers to no slot outside ``slots`` and no element outside ``elements``."""
    expression_slots, expression_elements = _class_expression_references(expression)
    return expression_slots <= slots and expression_elements <= elements
