from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinitionName,
    SlotDefinition,
)

from linkml.generators.common.ifabsent_processor import IfAbsentProcessor


class PythonIfAbsentProcessor(IfAbsentProcessor):
    UNIMPLEMENTED_DEFAULT_VALUES = ["class_curie", "class_uri", "slot_uri", "slot_curie", "default_range", "default_ns"]

    def map_custom_default_values(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition) -> (bool, str):
        if default_value in self.UNIMPLEMENTED_DEFAULT_VALUES:
            return True, None

        if default_value == "bnode":
            return True, "bnode()"

        return False, None

    def map_string_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._strval(default_value)

    def map_boolean_true_default_value(self, slot: SlotDefinition, cls: ClassDefinition):
        return "True"

    def map_boolean_false_default_value(self, slot: SlotDefinition, cls: ClassDefinition):
        return "False"

    def map_integer_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return default_value

    def map_float_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return default_value

    def map_double_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return default_value

    def map_decimal_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return default_value

    def map_time_default_value(self, hour: str, minutes: str, seconds: str, slot: SlotDefinition, cls: ClassDefinition):
        return f"time({int(hour)}, {int(minutes)}, {int(seconds)})"

    def map_date_default_value(self, year: str, month: str, day: str, slot: SlotDefinition, cls: ClassDefinition):
        return f"date({int(year)}, {int(month)}, {int(day)})"

    def map_datetime_default_value(
        self,
        year: str,
        month: str,
        day: str,
        hour: str,
        minutes: str,
        seconds: str,
        slot: SlotDefinition,
        cls: ClassDefinition,
    ):
        return f"datetime({int(year)}, {int(month)}, {int(day)}, " f"{int(hour)}, {int(minutes)}, {int(seconds)})"

    def map_uri_or_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._uri_for(default_value)

    def map_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._uri_for(default_value)

    def map_uri_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._uri_for(default_value)

    def map_enum_default_value(
        self, enum_name: EnumDefinitionName, permissible_value_name: str, slot: SlotDefinition, cls: ClassDefinition
    ):
        return f"'{permissible_value_name}'"

    def map_nc_name_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    def map_object_identifier_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    def map_node_identifier_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    def map_json_pointer_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    def map_json_path_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    def map_sparql_path_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()
