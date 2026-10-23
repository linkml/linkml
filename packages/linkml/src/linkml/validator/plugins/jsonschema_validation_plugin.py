import logging
import os
from collections.abc import Iterator
from typing import Any

from jsonschema.exceptions import best_match

from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext

logger = logging.getLogger(__name__)


class JsonschemaValidationPlugin(ValidationPlugin):
    """A validation plugin which validates instances using a JSON Schema validator.

    :param closed: If ``True``, additional properties are not allowed on instances.
        Defaults to ``False``.
    :param include_range_class_descendants: If True, use an open world assumption and allow the
        range of a slot to be any descendant of the declared range. Note that if the range of a
        slot has a type designator, descendants will always be included.
    :param json_schema_path: If provided, JSON Schema will not be generated from the schema,
        instead it will be read from this path. In this case the value of the ``closed`` argument
        is disregarded and the open- or closed-ness of the existing JSON Schema is taken as-is.
    :param allow_null_for_optional_enums: If ``True``, downgrade enum validation errors
        to warnings when the value is null/empty and the slot is not required. Prevents
        spurious ``None is not one of [...]`` and ``'' is not one of [...]`` errors for
        nullable enum columns. Defaults to ``False``.
    """

    def __init__(
        self,
        *,
        closed: bool = False,
        include_range_class_descendants: bool = True,
        json_schema_path: os.PathLike | None = None,
        allow_null_for_optional_enums: bool = False,
    ) -> None:
        self.closed = closed
        self.include_range_class_descendants = include_range_class_descendants
        self.json_schema_path = json_schema_path
        self.allow_null_for_optional_enums = allow_null_for_optional_enums

    def _is_null_enum_error(self, value: Any, path: list, context: ValidationContext) -> bool:
        """
        Returns True if the error is a null/empty value on an optional enum slot.

        Uses the jsonschema error's absolute_path and instance value directly —
        no regex parsing of error message strings needed.

        :param value: The actual invalid value (e.g. '' or None)
        :param path: The absolute_path from the jsonschema error as a list
        :param context: The validation context providing schema_view
        """
        # Only handle null/empty values
        if value is not None and value != "":
            return False

        # Need at least one path element to identify the slot
        if not path:
            return False

        # The last element of the path is the slot name
        slot_name = str(path[-1])

        try:
            sv = context.schema_view
            induced = sv.induced_slot(slot_name, context.target_class)
            # Downgrade only if slot is not required AND has an enum range
            if not induced.required:
                if induced.range and induced.range in sv.all_enums():
                    return True
        except Exception as e:
            logger.debug("Could not induce slot %s for null enum check: %s", slot_name, e)

        return False

    def process(self, instance: Any, context: ValidationContext) -> Iterator[ValidationResult]:
        """Perform JSON Schema validation on the provided instance

        :param instance: The instance to validate
        :param context: The validation context which provides a JSON Schema artifact
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        validator = context.json_schema_validator(
            closed=self.closed,
            include_range_class_descendants=self.include_range_class_descendants,
            path_override=self.json_schema_path,
        )
        for error in validator.iter_errors(instance):
            error_context = [ctx.message for ctx in error.context]
            best_error = best_match([error])
            message = f"{best_error.message} in /{'/'.join(str(p) for p in best_error.absolute_path)}"

            severity = Severity.ERROR
            if self.allow_null_for_optional_enums:
                # Use absolute_path and instance value directly — no regex needed
                path = list(best_error.absolute_path)
                value = best_error.instance
                if self._is_null_enum_error(value, path, context):
                    severity = Severity.WARN

            yield ValidationResult(
                type="jsonschema validation",
                severity=severity,
                instance=instance,
                instantiates=context.target_class,
                message=message,
                context=error_context,
                source=best_error,
            )
