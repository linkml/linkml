"""
.. deprecated::
    Import SchemaBuilder from ``linkml_runtime.utils.schema_builder`` instead.
"""

from linkml.utils.deprecation import deprecation_warning

deprecation_warning("schema-builder-import-location")

from linkml_runtime.utils.schema_builder import SchemaBuilder  # noqa: E402

__all__ = ["SchemaBuilder"]
