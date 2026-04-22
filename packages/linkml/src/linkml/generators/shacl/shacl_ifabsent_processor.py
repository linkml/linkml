from rdflib import Literal, URIRef

from linkml.generators.common.ifabsent_processor import IfAbsentProcessor
from linkml.generators.shacl.shacl_data_type import ShaclDataType
from linkml_runtime.linkml_model import ClassDefinition, EnumDefinitionName, SlotDefinition


class ShaclIfAbsentProcessor(IfAbsentProcessor):
    def map_custom_default_values(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition) -> (bool, str):
        return False, None

    def map_enum_default_value(
        self, enum_name: EnumDefinitionName, permissible_value_name: str, slot: SlotDefinition, cls: ClassDefinition
    ):
        return Literal(permissible_value_name)

    def map_string_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(default_value, datatype=ShaclDataType.STRING.uri_ref)

    def map_integer_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(default_value, datatype=ShaclDataType.INTEGER.uri_ref)

    def map_boolean_true_default_value(self, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(True, datatype=ShaclDataType.BOOLEAN.uri_ref)

    def map_boolean_false_default_value(self, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(False, datatype=ShaclDataType.BOOLEAN.uri_ref)

    def map_float_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(default_value, datatype=ShaclDataType.FLOAT.uri_ref)

    def map_double_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(default_value, datatype=ShaclDataType.DOUBLE.uri_ref)

    def map_decimal_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(default_value, datatype=ShaclDataType.DECIMAL.uri_ref)

    def map_time_default_value(self, hour: str, minutes: str, seconds: str, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(f"{hour}:{minutes}:{seconds}", datatype=ShaclDataType.TIME.uri_ref)

    def map_date_default_value(self, year: str, month: str, day: str, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(f"{year}-{month}-{day}", datatype=ShaclDataType.DATE.uri_ref)

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
        return Literal(f"{year}-{month}-{day}T{hour}:{minutes}:{seconds}", datatype=ShaclDataType.DATETIME.uri_ref)

    def map_uri_or_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.CURIE_SPECIAL_CASES:
            value = self._map_curie_special_case(default_value, slot, cls)
            return Literal(value, datatype=ShaclDataType.CURIE.uri_ref)
        elif default_value in self.URI_SPECIAL_CASES:
            value = self._map_uri_special_case(default_value, slot, cls)
            return Literal(value, datatype=ShaclDataType.URI.uri_ref)
        else:
            uri = URIRef(self.schema_view.expand_curie(default_value))
            return Literal(uri, datatype=ShaclDataType.URI.uri_ref)

    def map_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.CURIE_SPECIAL_CASES:
            default_value = self._map_curie_special_case(default_value, slot, cls)
        return Literal(default_value, datatype=ShaclDataType.CURIE.uri_ref)

    def map_uri_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        if default_value in self.URI_SPECIAL_CASES:
            default_value = self._map_uri_special_case(default_value, slot, cls)
        return Literal(default_value, datatype=ShaclDataType.URI.uri_ref)

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

    def _map_uri_special_case(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition) -> str:
        """Return raw (unquoted) URI values for use in RDF Literals."""
        if default_value == "class_uri":
            return str(self.schema_view.get_uri(cls, expand=True))
        elif default_value == "slot_uri":
            return str(self.schema_view.get_uri(slot, expand=True))
        raise ValueError(
            f"Default value must be one of the URI special cases: {self.URI_SPECIAL_CASES}. Got: {default_value}"
        )

    def _map_curie_special_case(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition) -> str:
        """Return raw (unquoted) CURIE values for use in RDF Literals."""
        if default_value == "class_curie":
            return str(self.schema_view.get_uri(cls, expand=False))
        elif default_value == "slot_curie":
            return str(self.schema_view.get_uri(slot, expand=False))
        raise ValueError(
            f"Default value must be one of the curie special cases: {self.CURIE_SPECIAL_CASES}. Got: {default_value}"
        )

    def _map_default_range_special_case(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        """Return default range as a string Literal."""
        default_range = self.schema_view.schema.default_range or "string"
        return Literal(default_range, datatype=ShaclDataType.STRING.uri_ref)
