"""Shared semantics of slot conditions in class-level boolean expressions.

The class-level operators ``any_of``, ``all_of``, ``exactly_one_of`` and
``none_of`` combine class expressions whose slot conditions constrain slots of
an instance.  The specification does not say what a condition means for an
absent slot.  Generators that translate class expressions read it the same
way, as an SQL CHECK constraint (ISO/IEC 9075) reads a condition on a null
value: a condition that doesn't state presence is *unknown* for an absent
slot, and an expression is violated only when it is definitely false.

Each expression therefore has two forms:

* its **"not false" form**, which the instance must satisfy, and in which a
  condition holds for an absent slot unless it states presence;
* its **"definitely true" form**, used under a negation, in which a condition
  that doesn't state presence also requires its slot.

``none_of`` takes its members in the opposite form, ``exactly_one_of`` counts
the members that are definitely true, and ``any_of`` / ``all_of`` keep the
form.

>>> from linkml_runtime.linkml_model.meta import SlotDefinition
>>> value_bounds(SlotDefinition("label", equals_string="A"), definite=False)
(0, None)
>>> value_bounds(SlotDefinition("label", equals_string="A"), definite=True)
(1, None)
>>> value_bounds(SlotDefinition("label", required=True, value_presence="ABSENT"), definite=True)
(0, 0)
>>> value_bounds(SlotDefinition("tags", minimum_cardinality=2, maximum_cardinality=3), definite=False)
(2, 3)
"""

from linkml_runtime.linkml_model.meta import PresenceEnum, SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView

_PRESENT = PresenceEnum(PresenceEnum.PRESENT)
_ABSENT = PresenceEnum(PresenceEnum.ABSENT)


def states_presence(condition: SlotDefinition) -> bool:
    """Whether *condition* decides whether its slot may be absent.

    Such a condition is definitely true or false for an absent slot:
    ``value_presence: PRESENT`` or ``ABSENT``; ``required: true``, unless
    ``value_presence`` overrides it; a minimum or exact cardinality of at least
    1, and ``has_member``, which asks for at least one value, all of which an
    absent slot fails; and a maximum or exact cardinality of 0, which it
    satisfies.  Other bounds, ``required: false`` and ``UNCOMMITTED`` leave
    absence open, so adding one never changes the verdict on an absent slot.

    >>> states_presence(SlotDefinition("label", equals_string="A"))
    False
    >>> states_presence(SlotDefinition("label", required=False, equals_string="A"))
    False
    >>> states_presence(SlotDefinition("tags", maximum_cardinality=5))
    False
    >>> states_presence(SlotDefinition("tags", maximum_cardinality=0))
    True
    >>> states_presence(SlotDefinition("tags", minimum_cardinality=1))
    True
    >>> states_presence(SlotDefinition("tags", has_member={"equals_string": "A"}))
    True
    """
    if condition.value_presence is not None:
        if condition.value_presence in (_PRESENT, _ABSENT):
            return True
    elif condition.required:
        return True
    if condition.has_member is not None:
        return True
    lower = (condition.minimum_cardinality, condition.exact_cardinality)
    upper = (condition.maximum_cardinality, condition.exact_cardinality)
    return any(bound is not None and bound >= 1 for bound in lower) or 0 in upper


def value_bounds(condition: SlotDefinition, definite: bool) -> tuple[int, int | None]:
    """The least and the greatest number of values *condition* allows its slot.

    ``value_presence`` takes precedence over ``required``, and ``has_member``
    asks for at least one value.  In the "definitely true" form (*definite*), a
    condition that doesn't state presence also requires the slot.  The greatest
    number is ``None`` when unbounded.

    >>> value_bounds(SlotDefinition("tags", has_member={"equals_string": "A"}), definite=False)
    (1, None)
    """
    lower, upper = [0], []
    if condition.value_presence is not None:
        if condition.value_presence == _PRESENT:
            lower.append(1)
        elif condition.value_presence == _ABSENT:
            upper.append(0)
    elif condition.required:
        lower.append(1)
    if condition.has_member is not None:
        lower.append(1)
    if definite and not states_presence(condition):
        lower.append(1)
    for bound, target in (
        (condition.minimum_cardinality, lower),
        (condition.exact_cardinality, lower),
        (condition.maximum_cardinality, upper),
        (condition.exact_cardinality, upper),
    ):
        if bound is not None:
            target.append(int(bound))
    return max(lower), min(upper) if upper else None


def class_membership(sv: SchemaView, cls_name: str, target: str) -> bool | None:
    """Whether an instance of the class *cls_name* is an instance of the class *target*.

    A LinkML instance belongs to its class and to that class's ancestors, by
    ``is_a`` and by ``mixins``.  So every instance of *cls_name* is one when
    *target* is *cls_name* or an ancestor (``True``); some may be when *target*
    is an ancestor of a descendant of *cls_name*, which the instance may belong
    to (``None``); and none is otherwise (``False``).

    A class carries the expressions of its ancestors, which may name any of
    these: a ``Person`` carries its parent's ``any_of: [{is_a: Person},
    {is_a: Organization}]``, whose first member it satisfies and whose second
    it cannot.  A value of ``linkml:Any`` may be an instance of any class, and
    every instance is one of ``linkml:Any``.

    >>> sv = SchemaView('''
    ... id: https://example.org/membership
    ... name: membership
    ... classes:
    ...   Any: {class_uri: linkml:Any}
    ...   Agent: {}
    ...   Person: {is_a: Agent}
    ...   Student: {is_a: Person}
    ...   Organization: {is_a: Agent}
    ... ''')
    >>> class_membership(sv, "Student", "Person")
    True
    >>> print(class_membership(sv, "Agent", "Person"))
    None
    >>> class_membership(sv, "Person", "Organization")
    False
    >>> print(class_membership(sv, "Any", "Person"))
    None
    >>> class_membership(sv, "Person", "Any")
    True
    """
    if target in sv.class_ancestors(cls_name) or _is_any(sv, target):
        return True
    if _is_any(sv, cls_name):
        return None
    if any(target in sv.class_ancestors(descendant) for descendant in sv.class_descendants(cls_name)):
        return None
    return False


def _is_any(sv: SchemaView, cls_name: str) -> bool:
    """Whether the class *cls_name* is ``linkml:Any``, the class of every value."""
    cls = sv.get_class(cls_name)
    if cls is None or not cls.class_uri:
        return False
    return cls.class_uri == "linkml:Any" or sv.expand_curie(cls.class_uri) == "https://w3id.org/linkml/Any"
