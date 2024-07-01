"""
Custom exceptions
"""


class SchemaError(ValueError):
    """Base class for errors relating to schema specification, parsing, structure, etc."""


class ValidationError(SchemaError):
    """Schema is invalid!"""
