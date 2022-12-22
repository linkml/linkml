from dataclasses import dataclass

from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinitionName


@dataclass
class DataValidator:
    """
    Base class for all validators
    """

    schema: SchemaDefinition = None

    def validate_dict(
            self, data: dict, target_class: ClassDefinitionName = None, closed: bool = True
    ) -> None:
        raise NotImplementedError
