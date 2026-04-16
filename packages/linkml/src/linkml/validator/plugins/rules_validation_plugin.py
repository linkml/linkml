"""Validation plugin that evaluates ClassRule preconditions and postconditions.

A ClassRule has the form: if preconditions match, then postconditions must hold.
When preconditions match an instance but postconditions do not, a validation
error is reported.
"""

from collections.abc import Iterator

from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    ClassRule,
    SlotDefinition,
)
from linkml_runtime.utils.expression_utils import matches_class_expression, matches_slot_expression


class RulesValidationPlugin(ValidationPlugin):
    """A validation plugin that evaluates ClassRule rules on class instances.

    For each rule defined on the target class, this plugin checks whether the
    preconditions match the instance. If they do, it verifies that the
    postconditions also hold. A violation is reported when preconditions match
    but postconditions do not.
    """

    def process(self, instance: dict, context: ValidationContext) -> Iterator[ValidationResult]:
        yield from self._process_instance(instance, context.target_class, context)

    def _process_instance(
        self,
        instance: dict,
        class_name: str,
        context: ValidationContext,
        location: list[str] | None = None,
    ) -> Iterator[ValidationResult]:
        """Evaluate rules on an instance and recurse into nested objects."""
        if not isinstance(instance, dict):
            return
        if location is None:
            location = []

        class_def = context.schema_view.get_class(class_name)
        if class_def is None:
            return

        for rule in class_def.rules:
            yield from self._evaluate_rule(instance, rule, class_name, location)

        # Recurse into nested objects
        for slot_def in context.schema_view.class_induced_slots(class_name):
            slot_value = instance.get(slot_def.name)
            if slot_value is None:
                continue
            slot_range_class = context.schema_view.get_class(slot_def.range)
            if slot_range_class is None:
                continue
            child_location = [*location, slot_def.name]
            if slot_def.multivalued:
                if isinstance(slot_value, list):
                    for i, item in enumerate(slot_value):
                        yield from self._process_instance(
                            item, slot_range_class.name, context, [*child_location, str(i)]
                        )
                elif isinstance(slot_value, dict):
                    for key, item in slot_value.items():
                        yield from self._process_instance(item, slot_range_class.name, context, [*child_location, key])
            else:
                yield from self._process_instance(slot_value, slot_range_class.name, context, child_location)

    def _evaluate_rule(
        self,
        instance: dict,
        rule: ClassRule,
        class_name: str,
        location: list[str],
    ) -> Iterator[ValidationResult]:
        """Evaluate a single ClassRule against an instance.

        If preconditions match but postconditions do not, yield a violation.
        """
        if rule.deactivated:
            return

        # Check preconditions — if they don't match, rule doesn't apply
        if rule.preconditions is not None:
            if not matches_class_expression(instance, rule.preconditions):
                return

        # Preconditions matched (or absent) — postconditions must hold
        if rule.postconditions is not None:
            violated_slots = self._find_violations(instance, rule.postconditions)
            for slot_name, reason in violated_slots:
                loc = "/".join(location)
                description = f" ({rule.description})" if rule.description else ""
                yield ValidationResult(
                    type="class_rule",
                    severity=Severity.ERROR,
                    instance=instance,
                    instantiates=class_name,
                    message=(
                        f"Rule violation{description} on class '{class_name}' in /{loc}: slot '{slot_name}' {reason}"
                    ),
                )

    def _find_violations(self, instance: dict, expression: AnonymousClassExpression) -> list[tuple[str, str]]:
        """Find postcondition violations, returning (slot_name, reason) pairs.

        Uses the shared ``matches_slot_expression`` for matching, then generates
        human-readable reasons for any violations found.
        """
        violations = []
        if expression.slot_conditions:
            for slot_name, slot_condition in expression.slot_conditions.items():
                value = instance.get(slot_name)
                if not matches_slot_expression(value, slot_condition, instance):
                    reason = _describe_violation(value, slot_condition)
                    violations.append((slot_name, reason))
        return violations


def _describe_violation(value, condition: SlotDefinition) -> str:
    """Generate a human-readable description of why a slot value violates a condition."""
    if getattr(condition, "required", None) and value is None:
        return "is required but missing"

    if condition.equals_string is not None:
        if value is None:
            return f"is required to equal '{condition.equals_string}' but is absent"
        return f"must equal '{condition.equals_string}' but is '{value}'"

    if condition.minimum_value is not None:
        if value is None:
            return f"must be >= {condition.minimum_value} but is absent"
        try:
            if float(value) < float(condition.minimum_value):
                return f"must be >= {condition.minimum_value} but is {value}"
        except (ValueError, TypeError):
            return f"must be >= {condition.minimum_value} but '{value}' is not numeric"

    if condition.maximum_value is not None:
        if value is None:
            return f"must be <= {condition.maximum_value} but is absent"
        try:
            if float(value) > float(condition.maximum_value):
                return f"must be <= {condition.maximum_value} but is {value}"
        except (ValueError, TypeError):
            return f"must be <= {condition.maximum_value} but '{value}' is not numeric"

    if getattr(condition, "pattern", None) is not None:
        if value is None:
            return f"must match pattern '{condition.pattern}' but is absent"
        return f"must match pattern '{condition.pattern}' but is '{value}'"

    return "does not satisfy postcondition"
