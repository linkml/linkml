from linkml.generators.common.ifabsent_processor import IfAbsentProcessor
from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinitionName,
    SlotDefinition,
)
from linkml_runtime.utils.namespaces import META_URI


class PythonIfAbsentProcessor(IfAbsentProcessor):
    # When generating meta.py from meta.yaml, these ifabsent directives must not be
    # baked in as dataclass-level defaults: instances of SlotDefinition/ClassDefinition
    # represent user-schema elements, so a static default would cross-contaminate every
    # user instance with the metamodel's own values (e.g. every user slot would carry
    # range="string" and slot_uri="linkml:slot_uri"). SchemaView.induced_slot() resolves
    # these at runtime. For non-metamodel schemas, baking remains correct because the
    # generated class corresponds 1:1 with a concrete user class.
    # TODO: replace with __post_init__ resolution per https://github.com/linkml/linkml/issues/2522.
    _METAMODEL_RUNTIME_COMPUTED_IFABSENT = (
        "default_range",
        "class_curie",
        "slot_curie",
        "class_uri",
        "slot_uri",
    )

    def map_custom_default_values(
        self, default_value: str, slot: SlotDefinition, cls: ClassDefinition
    ) -> tuple[bool, str | None]:
        if default_value in self.UNIMPLEMENTED_DEFAULT_VALUES:
            # default_ns depends on self.id at runtime, so no static default is possible.
            # The actual initialization is handled in __post_init__ by pythongen's gen_postinit().
            return True, None

        if default_value in self._METAMODEL_RUNTIME_COMPUTED_IFABSENT and self.schema_view.schema.id == META_URI:
            return True, None

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
        return f"datetime({int(year)}, {int(month)}, {int(day)}, {int(hour)}, {int(minutes)}, {int(seconds)})"

    def map_uri_or_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.URI_SPECIAL_CASES:
            return self._map_uri_special_case(default_value, slot, cls)
        elif default_value in self.CURIE_SPECIAL_CASES:
            return self._map_curie_special_case(default_value, slot, cls)
        else:
            return self._uri_for(default_value)

    def map_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.CURIE_SPECIAL_CASES:
            return self._map_curie_special_case(default_value, slot, cls)
        elif default_value in self.URI_SPECIAL_CASES:
            return None
        return self._uri_for(default_value)

    def map_uri_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.URI_SPECIAL_CASES:
            return self._map_uri_special_case(default_value, slot, cls)
        elif default_value in self.CURIE_SPECIAL_CASES:
            return None
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
