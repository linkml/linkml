"""
Custom exceptions
"""


class SchemaError(ValueError):
    """Base class for errors relating to schema specification, parsing, structure, etc."""


class DataError(ValueError):
    """Base class for errors relating to linkml instance data"""


class SchemaValidationError(SchemaError):
    """Schema is invalid!"""


class ValidationError(DataError, SchemaError):
    """Data is invalid relative to a schema"""
