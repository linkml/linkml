import os
from typing import Any, Iterator, Optional

from jsonschema.exceptions import best_match

from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext


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
    """

    def __init__(
        self,
        *,
        closed: bool = False,
        include_range_class_descendants: bool = True,
        json_schema_path: Optional[os.PathLike] = None,
    ) -> None:
        self.closed = closed
        self.include_range_class_descendants = include_range_class_descendants
        self.json_schema_path = json_schema_path

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
            yield ValidationResult(
                type="jsonschema validation",
                severity=Severity.ERROR,
                instance=instance,
                instantiates=context.target_class,
                message=f"{best_error.message} in /{'/'.join(str(p) for p in best_error.absolute_path)}",
                context=error_context,
            )
