from typing import Any, Iterator

from linkml.generators import PydanticGenerator
from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext


class PydanticValidationPlugin(ValidationPlugin):
    """A validation plugin which validates instances using a Pydantic validator.

    Note that this plugin provides less complete validation than JsonschemaValidationPlugin.
    Also, due to the nature of pydantic, it will fail fast on errors and only report the first
    error found.

    For general use cases, JsonschemaValidationPlugin is recommended. However, this plugin
    may be useful in some scenarios:

    - You are using in a pipeline to ensure objects will be valid for loading into Pydantic.
    - You are exploring relative capabilities of Pydantic and JSON Schema validation.
    - Pydantic is faster for your use case (to be tested).
    """

    def __init__(self, closed: bool = False, strict: bool = False) -> None:
        """Constructor method

        :param strict: If true, stop validating after the first validation problem
            is found. Defaults to False.
        """
        self.strict = strict

    def process(self, instance: Any, context: ValidationContext) -> Iterator[ValidationResult]:
        """Perform Pydantic validation on the provided instance

        :param instance: The instance to validate
        :param context: The validation context which provides a Pydantic artifact
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        if "pydantic_module" not in context.cached_artefacts:
            context.cached_artefacts["pydantic_module"] = PydanticGenerator(
                context.schema
            ).compile_module()
        pydantic_module = context.cached_artefacts["pydantic_module"]
        target_class = pydantic_module.__dict__[context.target_class]
        try:
            instance = target_class.parse_obj(instance)
        except Exception as e:
            yield ValidationResult(
                type="Pydantic validation",
                severity=Severity.ERROR,
                instance=instance,
                instantiates=context.target_class,
                message=f"{e}",
            )
        return
