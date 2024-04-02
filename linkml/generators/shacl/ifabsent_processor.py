import re
from typing import Any, Callable, Optional

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SlotDefinition
from rdflib import SH, Literal, URIRef
from rdflib.term import Identifier

from linkml.generators.shacl.shacl_data_type import ShaclDataType


class IfAbsentProcessor:
    """
    Processes value of ifabsent slot.

    See `<https://w3id.org/linkml/ifabsent>`_.

    TODO: unify this with ifabsent_functions
    """

    ifabsent_regex = re.compile("""(?:(?P<type>\w+)\()?[\"\']?(?P<default_value>[^\(\)\"\')]*)[\"\']?\)?""")

    def __init__(self, schema_view: SchemaView):
        self.schema_view = schema_view

    def process_slot(
        self, add_prop: Callable[[URIRef, Identifier], None], slot: SlotDefinition, class_uri: Optional[URIRef] = None
    ) -> None:
        if slot.ifabsent:
            ifabsent_match = self.ifabsent_regex.search(slot.ifabsent)
            ifabsent_default_value = ifabsent_match.group("default_value")

            self._map_to_default_value(slot, add_prop, ifabsent_default_value, class_uri)

    def _map_to_default_value(
        self,
        slot: SlotDefinition,
        add_prop: Callable[[URIRef, Identifier], None],
        ifabsent_default_value: Any,
        class_uri: Optional[URIRef] = None,
    ) -> None:
        for datatype in list(ShaclDataType):
            if datatype.linkml_type == slot.range:
                add_prop(SH.defaultValue, Literal(ifabsent_default_value, datatype=datatype.uri_ref))
                return

        for enum_name, enum in self.schema_view.all_enums().items():
            if enum_name == slot.range:
                for permissible_value_name, permissible_value in enum.permissible_values.items():
                    if permissible_value_name == ifabsent_default_value:
                        add_prop(SH.defaultValue, Literal(ifabsent_default_value))
                        return

        if ifabsent_default_value == "class_curie":
            if class_uri:
                add_prop(SH.defaultValue, class_uri)
            return

        raise ValueError(f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot could not be processed")
