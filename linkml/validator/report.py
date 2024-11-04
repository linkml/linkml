import textwrap
from enum import Enum
from pprint import pformat
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from linkml.utils.exceptions import ValidationError


class Severity(str, Enum):
    """
    Enum to represent the severity of a validation message.
    """

    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"


class ValidationResult(BaseModel):
    """
    ValidationResult represents the results of validation
    by a plugin.
    An individual result arising from validation of a data instance using a particular rule
    """

    type: str
    severity: Severity
    message: str
    instance: Optional[Any] = None
    instance_index: Optional[int] = None
    instantiates: Optional[str] = None
    context: List[str] = []

    # The source object that caused this validation result
    source: Any = Field(None, description="The source of this validation result", exclude=True)

    def __str__(self) -> str:
        return pformat(self.model_dump(exclude_none=True, exclude_unset=True))


class ValidationReport(BaseModel):
    """
    ValidationReport represents the result of all types of
    validation for a given object.
    A report object.
    """

    results: List[ValidationResult]

    def raise_(self):
        """
        If any results, raise them as a :class:`.ValidationError`
        """
        if self.results:
            res = textwrap.indent("\n".join(str(res) for res in self.results), "  ")
            msg = f"Error(s) validating data: \n{res}"
            raise ValidationError(msg)
