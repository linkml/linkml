"""Standalone functions for evaluating LinkML slot and class expressions.

These functions are used by both the ReferenceValidator and the
RulesValidationPlugin to match instance data against slot conditions
and class expressions defined in schemas.
"""

import logging
import re
from typing import Any

from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    AnonymousSlotExpression,
    SlotDefinition,
)
from linkml_runtime.utils.eval_utils import eval_expr

logger = logging.getLogger(__name__)


def _is_numeric(value: Any) -> bool:
    """Check whether a value can be interpreted as a number."""
    if isinstance(value, int | float | complex):
        return True
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return False
        # Handle optional leading sign and decimal point
        stripped = stripped.lstrip("+-")
        return stripped.replace(".", "", 1).isdigit()
    return False


def matches_slot_expression(
    slot_value: Any,
    expr: SlotDefinition | AnonymousSlotExpression,
    input_object: dict | None = None,
) -> bool:
    """Evaluate whether a slot value matches a slot expression.

    Handles boolean combinators (``any_of``, ``all_of``, ``none_of``,
    ``exactly_one_of``), string/number equality, numeric range constraints,
    pattern matching, and required checks.

    :param slot_value: The value of the slot in the instance.
    :param expr: The slot expression to evaluate against.
    :param input_object: The full instance dict, used for ``equals_expression`` evaluation.
    :returns: True if the value satisfies the expression.
    """
    if input_object is None:
        input_object = {}

    # Boolean combinators
    for x in expr.none_of:
        if matches_slot_expression(slot_value, x, input_object):
            return False
    if expr.exactly_one_of:
        vals = [x for x in expr.exactly_one_of if matches_slot_expression(slot_value, x, input_object)]
        if len(vals) != 1:
            return False
    if expr.any_of:
        vals = [x for x in expr.any_of if matches_slot_expression(slot_value, x, input_object)]
        if not vals:
            return False
    for x in expr.all_of:
        if not matches_slot_expression(slot_value, x, input_object):
            return False

    # Expression evaluation
    if expr.equals_expression:
        if eval_expr(expr.equals_expression, **input_object) != slot_value:
            return False

    # String equality
    if expr.equals_string is not None:
        if slot_value is None or str(slot_value) != expr.equals_string:
            return False

    # Number equality
    if expr.equals_number is not None:
        if slot_value != expr.equals_number:
            return False

    # Required check
    if getattr(expr, "required", None) and slot_value is None:
        return False

    # Numeric range constraints
    if expr.minimum_value is not None:
        if slot_value is None or not _is_numeric(slot_value):
            return False
        if float(slot_value) < float(expr.minimum_value):
            return False

    if expr.maximum_value is not None:
        if slot_value is None or not _is_numeric(slot_value):
            return False
        if float(slot_value) > float(expr.maximum_value):
            return False

    # Pattern matching
    if getattr(expr, "pattern", None) is not None:
        if slot_value is None:
            return False
        if not re.search(expr.pattern, str(slot_value)):
            return False

    return True


def matches_class_expression(
    instance: dict,
    expr: AnonymousClassExpression,
) -> bool:
    """Evaluate whether an instance matches a class expression.

    Checks ``slot_conditions`` and boolean combinators (``any_of``,
    ``all_of``, ``none_of``, ``exactly_one_of``) at the class level.

    Note: the ``is_a`` field on class expressions requires a SchemaView
    for type hierarchy resolution and is not evaluated here. Use
    ``ReferenceValidator._matches_class_expression`` for ``is_a`` support.

    :param instance: The instance dict to evaluate.
    :param expr: The class expression to evaluate against.
    :returns: True if the instance satisfies the expression.
    """
    if not isinstance(instance, dict):
        return False

    # Slot conditions
    if expr.slot_conditions:
        for slot_name, slot_condition in expr.slot_conditions.items():
            value = instance.get(slot_name)
            if not matches_slot_expression(value, slot_condition, instance):
                return False

    # Boolean combinators at class level
    if expr.any_of:
        if not any(matches_class_expression(instance, x) for x in expr.any_of):
            return False
    if expr.all_of:
        if not all(matches_class_expression(instance, x) for x in expr.all_of):
            return False
    if expr.none_of:
        if any(matches_class_expression(instance, x) for x in expr.none_of):
            return False
    if expr.exactly_one_of:
        count = sum(1 for x in expr.exactly_one_of if matches_class_expression(instance, x))
        if count != 1:
            return False

    return True
