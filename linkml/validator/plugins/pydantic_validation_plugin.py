from typing import Any, Iterator

from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext


class PydanticValidationPlugin(ValidationPlugin):
    """A validation plugin which validates instances using a Pydantic validator.

    Note that this plugin provides less complete validation than
    :class:`JsonschemaValidationPlugin`.
    Also, due to the nature of Pydantic, it will fail fast on errors and only report the first
    error found.

    For general use cases, JsonschemaValidationPlugin is recommended. However, this plugin
    may be useful in some scenarios:

    - You are using in a pipeline to ensure objects will be valid for loading into Pydantic.
    - You are exploring relative capabilities of Pydantic and JSON Schema validation.
    - Pydantic is faster for your use case (to be tested).

    :param closed: If ``True``, additional properties are not allowed on instances.
        Defaults to ``False``.
    """

    def __init__(self, closed: bool = False) -> None:
        self.closed = closed

    def process(self, instance: Any, context: ValidationContext) -> Iterator[ValidationResult]:
        """Perform Pydantic validation on the provided instance

        :param instance: The instance to validate
        :param context: The validation context which provides a Pydantic artifact
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        pydantic_model = context.pydantic_model(closed=self.closed)
        try:
            instance = pydantic_model.parse_obj(instance)
        except Exception as e:
            yield ValidationResult(
                type="Pydantic validation",
                severity=Severity.ERROR,
                instance=instance,
                instantiates=context.target_class,
                message=f"{e}",
            )
