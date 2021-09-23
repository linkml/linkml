from dataclasses import dataclass

from linkml_runtime.linkml_model import SchemaDefinition


@dataclass
class DataValidator:
    """
    Base class for all validators
    """

    schema: SchemaDefinition = None
