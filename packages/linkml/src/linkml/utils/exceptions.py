"""
Custom exceptions
"""


class SchemaError(ValueError):
    """Base class for errors relating to schema specification, parsing, structure, etc."""


class SchemaValidationError(SchemaError):
    """Schema is invalid!"""
