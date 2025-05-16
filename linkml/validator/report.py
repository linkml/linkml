from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


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
    context: list[str] = []

    # The source object that caused this validation result
    source: Any = Field(None, description="The source of this validation result", exclude=True)


class ValidationReport(BaseModel):
    """
    ValidationReport represents the result of all types of
    validation for a given object.
    A report object.
    """

    results: list[ValidationResult]
