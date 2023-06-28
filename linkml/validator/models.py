from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel


# Shadow models derived from linkml_runtime.linkml_model.validation
# This was created to have something quick and easy in pydantic
# This will be replaced by the proper model classes from linkml-model
# Currently there is a bug in the linkml_runtime.linkml_model.validation


class SeverityOptions(str, Enum):
    """
    Enum to represent the severity of a validation message.
    """
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"


class ProblemType(str, Enum):
    undeclared_slot = "undeclared_slot"
    inapplicable_slot = "inapplicable_slot"
    missing_slot_value = "missing_slot_value"
    slot_range_violation = "slot_range_violation"
    max_count_violation = "max_count_violation"
    parsing_error = "parsing_error"


class ValidationResult(BaseModel):
    """
    ValidationResult represents the results of validation
    by a plugin.

    An individual result arising from validation of a data instance using a particular rule
    """
    type: Optional[str]
    severity: SeverityOptions
    subject: Optional[Any]
    instantiates: Optional[str]
    predicate: Optional[str]
    object: Optional[str]
    object_str: Optional[str]
    node_source: Optional[str]
    info: Optional[str]


class ValidationReport(BaseModel):
    """
    ValidationReport represents the result of all types of
    validation for a given object.

    A report object.
    """
    results: List[ValidationResult]

