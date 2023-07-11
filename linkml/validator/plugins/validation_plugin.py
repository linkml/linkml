from abc import ABC, abstractmethod
from typing import Iterable

from linkml.validator.report import ValidationResult
from linkml.validator.validation_context import ValidationContext


class ValidationPlugin(ABC):
    """Abstract base class for validation plugins.

    Subclasses must implement a `process` method.
    """

    @abstractmethod
    def process(self, instance: dict, context: ValidationContext) -> Iterable[ValidationResult]:
        """Lazily yield validation results for an instance according to
        the validation context.

        :param instance: The instance to validate
        :param context: A `ValidationContext` instance which provides
            access to the schema, target class, and artifacts generated
            from the schema
        :return: Iterator over validation results
        :rtype: Iterable[ValidationResult]
        """
        pass
