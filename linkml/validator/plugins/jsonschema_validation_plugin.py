import os
from typing import Any, Iterator, Optional

import jsonschema
from jsonschema.exceptions import best_match

from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext


class JsonschemaValidationPlugin(ValidationPlugin):
    """A validation plugin which validates instances using a JSON Schema validator."""

    def __init__(
        self,
        closed: bool = False,
        strict: bool = False,
        json_schema_path: Optional[os.PathLike] = None,
    ) -> None:
        """Constructor method

        :param closed: If True, additional properties are not allowed on instances.
            Defaults to False.
        :param strict: If true, stop validating after the first validation problem
            is found. Defaults to False.
        :param json_schema_path: If provided, JSON Schema will not be generated from the schema,
            instead it will be read from this path. In this case the value of the `closed` argument
            is disregarded and the open- or closed-ness of the existing JSON Schema is taken as-is.
        """
        self.closed = closed
        self.strict = strict
        self.json_schema_path = json_schema_path

    def process(self, instance: Any, context: ValidationContext) -> Iterator[ValidationResult]:
        """Perform JSON Schema validation on the provided instance

        :param instance: The instance to validate
        :param context: The validation context which provides a JSON Schema artifact
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        json_schema = context.json_schema(closed=self.closed, path_override=self.json_schema_path)
        validator = jsonschema.Draft7Validator(json_schema, format_checker=jsonschema.Draft7Validator.FORMAT_CHECKER)
        for error in validator.iter_errors(instance):
            best_error = best_match([error])
            yield ValidationResult(
                type="jsonschema validation",
                severity=Severity.ERROR,
                instance=instance,
                instantiates=context.target_class,
                message=f"{best_error.message} in /{'/'.join(str(p) for p in best_error.absolute_path)}",
            )
            if self.strict:
                return
