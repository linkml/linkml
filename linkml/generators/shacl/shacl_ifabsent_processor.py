from typing import Any, Optional

from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition
from rdflib import Literal, URIRef

from linkml.generators.common.ifabsent_processor import IfAbsentProcessor
from linkml.generators.shacl.shacl_data_type import ShaclDataType


class ShaclIfAbsentProcessor(IfAbsentProcessor):

    def _map_to_default_value(
        self,
        slot: SlotDefinition,
        ifabsent_default_value: Any,
        cls: ClassDefinition,
    ) -> Optional[str]:
        for datatype in list(ShaclDataType):
            if datatype.linkml_type == slot.range:
                return Literal(ifabsent_default_value, datatype=datatype.uri_ref)

        for enum_name, enum in self.schema_view.all_enums().items():
            if enum_name == slot.range:
                for permissible_value_name, permissible_value in enum.permissible_values.items():
                    if permissible_value_name == ifabsent_default_value:
                        return Literal(ifabsent_default_value)

        if ifabsent_default_value == "class_curie":
            class_uri = self.schema_view.get_uri(cls, expand=True)
            if class_uri:
                return URIRef(class_uri)
            return None

        raise ValueError(f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot could not be processed")
