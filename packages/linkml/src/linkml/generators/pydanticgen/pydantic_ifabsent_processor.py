from linkml.generators.python.python_ifabsent_processor import PythonIfAbsentProcessor
from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinitionName,
    SlotDefinition,
)


class PydanticIfAbsentProcessor(PythonIfAbsentProcessor):
    def map_enum_default_value(
        self, enum_name: EnumDefinitionName, permissible_value_name: str, slot: SlotDefinition, cls: ClassDefinition
    ):
        return f"{enum_name}.{permissible_value_name}"
