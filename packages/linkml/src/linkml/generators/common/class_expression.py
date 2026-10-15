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

_PRESENT = PresenceEnum(PresenceEnum.PRESENT)
_ABSENT = PresenceEnum(PresenceEnum.ABSENT)


def states_presence(condition: SlotDefinition) -> bool:
    """Whether *condition* decides whether its slot may be absent.

    Such a condition is definitely true or false for an absent slot:
    ``value_presence: PRESENT`` or ``ABSENT``; ``required: true``, unless
    ``value_presence`` overrides it; a minimum or exact cardinality of at least
    1, which an absent slot fails; and a maximum or exact cardinality of 0,
    which it satisfies.  Other bounds, ``required: false`` and ``UNCOMMITTED``
    leave absence open, so adding one never changes the verdict on an absent
    slot.

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
    """
    if condition.value_presence is not None:
        if condition.value_presence in (_PRESENT, _ABSENT):
            return True
    elif condition.required:
        return True
    lower = (condition.minimum_cardinality, condition.exact_cardinality)
    upper = (condition.maximum_cardinality, condition.exact_cardinality)
    return any(bound is not None and bound >= 1 for bound in lower) or 0 in upper


def value_bounds(condition: SlotDefinition, definite: bool) -> tuple[int, int | None]:
    """The least and the greatest number of values *condition* allows its slot.

    ``value_presence`` takes precedence over ``required``.  In the "definitely
    true" form (*definite*), a condition that doesn't state presence also
    requires the slot.  The greatest number is ``None`` when unbounded.
    """
    lower, upper = [0], []
    if condition.value_presence is not None:
        if condition.value_presence == _PRESENT:
            lower.append(1)
        elif condition.value_presence == _ABSENT:
            upper.append(0)
    elif condition.required:
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
