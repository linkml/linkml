from linkml_runtime.linkml_model import ClassDefinition, EnumDefinitionName, SlotDefinition
from rdflib import Literal, URIRef

from linkml.generators.common.ifabsent_processor import IfAbsentProcessor
from linkml.generators.shacl.shacl_data_type import ShaclDataType


class ShaclIfAbsentProcessor(IfAbsentProcessor):

    def map_custom_default_values(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition) -> (bool, str):
        if default_value == "class_curie":
            class_uri = self.schema_view.get_uri(cls, expand=True)
            if class_uri:
                return True, URIRef(class_uri)
            return True, ""

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
        uri = URIRef(self.schema_view.expand_curie(default_value))
        return Literal(uri, datatype=ShaclDataType.URI.uri_ref)

    def map_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        return Literal(default_value, datatype=ShaclDataType.CURIE.uri_ref)

    def map_uri_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
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
