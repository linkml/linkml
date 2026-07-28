"""ifabsent default-value processor for the Zod generator.

Maps LinkML ``ifabsent`` directives to Zod-compatible JavaScript/TypeScript
literal expressions that can be passed to ``.default(...)``.
"""

from linkml.generators.common.ifabsent_processor import IfAbsentProcessor
from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinitionName,
    SlotDefinition,
)


class ZodIfAbsentProcessor(IfAbsentProcessor):
    """Render LinkML ``ifabsent`` values as Zod ``.default(...)`` literal expressions."""

    def map_custom_default_values(
        self, default_value: str, slot: SlotDefinition, cls: ClassDefinition
    ) -> tuple[bool, str | None]:
        if default_value in self.UNIMPLEMENTED_DEFAULT_VALUES:
            # e.g. ``bnode`` / ``default_ns`` cannot be resolved to a static literal.
            return True, None
        return False, None

    def map_string_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._strval(default_value)

    def map_boolean_true_default_value(self, slot: SlotDefinition, cls: ClassDefinition):
        return "true"

    def map_boolean_false_default_value(self, slot: SlotDefinition, cls: ClassDefinition):
        return "false"

    def map_integer_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return default_value

    def map_float_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return default_value

    def map_double_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return default_value

    def map_decimal_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return default_value

    def map_time_default_value(self, hour: str, minutes: str, seconds: str, slot: SlotDefinition, cls: ClassDefinition):
        # ``time`` ranges are represented as ``z.string()``.
        return f'"{hour}:{minutes}:{seconds}"'

    def map_date_default_value(self, year: str, month: str, day: str, slot: SlotDefinition, cls: ClassDefinition):
        # ``date`` ranges are represented as ``z.date()`` via the dateFromString preprocessor,
        # or as an ISO string (``z.iso.date()``) when ``iso_dates`` is set.
        if getattr(self, "iso_dates", False):
            return f'"{year}-{month}-{day}"'
        return f'new Date("{year}-{month}-{day}")'

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
        if getattr(self, "iso_dates", False):
            return f'"{year}-{month}-{day}T{hour}:{minutes}:{seconds}"'
        return f'new Date("{year}-{month}-{day}T{hour}:{minutes}:{seconds}")'

    def map_uri_or_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.URI_SPECIAL_CASES:
            return self._map_uri_special_case(default_value, slot, cls)
        elif default_value in self.CURIE_SPECIAL_CASES:
            return self._map_curie_special_case(default_value, slot, cls)
        return self._strval(default_value)

    def map_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.CURIE_SPECIAL_CASES:
            return self._map_curie_special_case(default_value, slot, cls)
        return self._strval(default_value)

    def map_uri_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.URI_SPECIAL_CASES:
            return self._map_uri_special_case(default_value, slot, cls)
        return self._strval(default_value)

    def map_nc_name_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._strval(default_value)

    def map_object_identifier_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._strval(default_value)

    def map_node_identifier_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._strval(default_value)

    def map_json_pointer_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._strval(default_value)

    def map_json_path_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._strval(default_value)

    def map_sparql_path_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return self._strval(default_value)

    def map_enum_default_value(
        self, enum_name: EnumDefinitionName, permissible_value_name: str, slot: SlotDefinition, cls: ClassDefinition
    ):
        return self._strval(permissible_value_name)
