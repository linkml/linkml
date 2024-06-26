import re
from typing import Any, Optional

from linkml_runtime.linkml_model import (
    Boolean,
    Date,
    Datetime,
    Decimal,
    Double,
    Float,
    Integer,
    SlotDefinition,
    String,
    Time,
    Uri,
    Uriorcurie,
)
from linkml_runtime.linkml_model.types import Curie

from linkml.generators.common.ifabsent_processor import IfAbsentProcessor


class PythonIfAbsentProcessor(IfAbsentProcessor):
    UNIMPLEMENTED_DEFAULT_VALUES = ["class_curie", "class_uri", "slot_uri", "slot_curie", "default_range", "default_ns"]

    def _map_to_default_value(
        self,
        slot: SlotDefinition,
        ifabsent_default_value: Any,
        class_uri: Optional[str] = None,
    ) -> Optional[str]:

        # ---------------------------------
        #   Unimplemented default values
        # ---------------------------------

        if ifabsent_default_value in self.UNIMPLEMENTED_DEFAULT_VALUES:
            return None

        # -----------------------
        #    Basic slot ranges
        # -----------------------
        if slot.range == String.type_name:
            return self.__strval(ifabsent_default_value)

        if slot.range == Boolean.type_name:
            if re.match(r"^[Tt]rue$", ifabsent_default_value):
                return "True"
            elif re.match(r"^[Ff]alse$", ifabsent_default_value):
                return "False"
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid boolean "
                    f"value"
                )

        if slot.range in [Integer.type_name, Float.type_name, Double.type_name, Decimal.type_name]:
            return ifabsent_default_value

        if slot.range == Time.type_name:
            match = re.match(r"^(\d{2}):(\d{2}):(\d{2}).*$", ifabsent_default_value)
            if match:
                return f"time({int(match[1])}, {int(match[2])}, {int(match[3])})"
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid time value"
                )

        if slot.range == Date.type_name:
            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", ifabsent_default_value)
            if match:
                return f"date({int(match[1])}, {int(match[2])}, {int(match[3])})"
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid date value"
                )

        if slot.range == Datetime.type_name:
            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).*$", ifabsent_default_value)
            if match:
                return (
                    f"datetime({int(match[1])}, {int(match[2])}, {int(match[3])}, "
                    f"{int(match[4])}, {int(match[5])}, {int(match[6])})"
                )
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid datetime "
                    f"value"
                )

        if slot.range in [Uri.type_name, Curie.type_name, Uriorcurie.type_name]:
            return self.__uri_for(ifabsent_default_value)

        # -------------------------
        #   Custom default values
        # -------------------------

        if ifabsent_default_value == "bnode":
            return "bnode()"

        # -----------------------
        #    Enum slot ranges
        # -----------------------

        for enum_name, enum in self.schema_view.all_enums().items():
            if enum_name == slot.range:
                for permissible_value_name, permissible_value in enum.permissible_values.items():
                    if permissible_value_name == ifabsent_default_value:
                        return f"{enum_name}.{ifabsent_default_value}"

        raise ValueError(f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot could not be processed")

    def __uri_for(self, s: str) -> str:
        uri = str(self.schema_view.namespaces().uri_for(s))
        return self.schema_view.namespaces().curie_for(uri, True, True) or self.__strval(uri)

    def __strval(self, txt: str) -> str:
        txt = str(txt).replace('"', '\\"')
        return f'"{txt}"'
