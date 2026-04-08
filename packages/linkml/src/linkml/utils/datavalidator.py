from dataclasses import dataclass

from linkml_runtime.linkml_model import ClassDefinitionName, SchemaDefinition


@dataclass
class DataValidator:
    """
    Base class for all validators
    """

    schema: str | SchemaDefinition = None
    """
    LinkML Schema to validate against
    """

    def validate_dict(self, data: dict, target_class: ClassDefinitionName = None, closed: bool = True) -> None:
        raise NotImplementedError
