from linkml.generators.python.python_ifabsent_processor import PythonIfAbsentProcessor
from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinitionName,
    SlotDefinition,
)


class FactoryDefault(str):
    """Marker for ifabsent values that should use ``default_factory`` instead of ``default``."""


class PydanticIfAbsentProcessor(PythonIfAbsentProcessor):
    """Ifabsent processor for pydantic code generation.

    Extends PythonIfAbsentProcessor with pydantic-specific handling,
    including :class:`FactoryDefault` support for values like ``bnode``
    that must be unique per instance.
    """

    def map_custom_default_values(
        self, default_value: str, slot: SlotDefinition, cls: ClassDefinition
    ) -> tuple[bool, str | None]:
        if default_value == "bnode":
            return True, FactoryDefault('lambda: "_:" + uuid.uuid4().hex')
        return super().map_custom_default_values(default_value, slot, cls)

    def map_enum_default_value(
        self, enum_name: EnumDefinitionName, permissible_value_name: str, slot: SlotDefinition, cls: ClassDefinition
    ):
        return f"{enum_name}.{permissible_value_name}"
