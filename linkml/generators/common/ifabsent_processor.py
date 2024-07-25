import abc
import re
from abc import ABC
from typing import Any, Optional

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import (
    Boolean,
    ClassDefinition,
    Date,
    Datetime,
    Decimal,
    Double,
    EnumDefinitionName,
    Float,
    Integer,
    SlotDefinition,
    String,
    Time,
    Uri,
)
from linkml_runtime.linkml_model.types import (
    Curie,
    DateOrDatetime,
    Jsonpath,
    Jsonpointer,
    Ncname,
    Nodeidentifier,
    Objectidentifier,
    Sparqlpath,
    Uriorcurie,
)


class IfAbsentProcessor(ABC):
    """
    Processes value of ifabsent slot.

    See `<https://w3id.org/linkml/ifabsent>`_.
    """

    ifabsent_regex = re.compile("""(?:(?P<type>\w+)\()?[\"\']?(?P<default_value>[^\(\)\"\')]*)[\"\']?\)?""")

    def __init__(self, schema_view: SchemaView):
        self.schema_view = schema_view

    def process_slot(self, slot: SlotDefinition, cls: ClassDefinition) -> Optional[str]:
        if slot.ifabsent:
            ifabsent_match = self.ifabsent_regex.search(slot.ifabsent)
            ifabsent_default_value = ifabsent_match.group("default_value")

            return self._map_to_default_value(slot, ifabsent_default_value, cls)

        return None

    def _map_to_default_value(
        self, slot: SlotDefinition, ifabsent_default_value: Any, cls: ClassDefinition
    ) -> Optional[str]:
        # Used to manage specific cases that aren't generic
        mapped, custom_default_value = self.map_custom_default_values(ifabsent_default_value, slot, cls)
        if mapped:
            return custom_default_value

        if slot.range == String.type_name:
            return self.map_string_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Boolean.type_name:
            if re.match(r"^[Tt]rue$", ifabsent_default_value):
                return self.map_boolean_true_default_value(slot, cls)
            elif re.match(r"^[Ff]alse$", ifabsent_default_value):
                return self.map_boolean_false_default_value(slot, cls)
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid boolean "
                    f"value"
                )

        if slot.range == Integer.type_name:
            return self.map_integer_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Float.type_name:
            return self.map_float_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Double.type_name:
            return self.map_double_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Decimal.type_name:
            return self.map_decimal_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Time.type_name:
            match = re.match(r"^(\d{2}):(\d{2}):(\d{2}).*$", ifabsent_default_value)
            if match:
                return self.map_time_default_value(match[1], match[2], match[3], slot, cls)
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid time value"
                )

        # TODO manage timezones and offsets
        if slot.range == Date.type_name:
            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", ifabsent_default_value)
            if match:
                return self.map_date_default_value(match[1], match[2], match[3], slot, cls)
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid date value"
                )

        # TODO manage timezones and offsets
        if slot.range == Datetime.type_name:
            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).*$", ifabsent_default_value)
            if match:
                return self.map_datetime_default_value(
                    match[1], match[2], match[3], match[4], match[5], match[6], slot, cls
                )
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid datetime "
                    f"value"
                )

        # TODO manage timezones and offsets
        if slot.range == DateOrDatetime.type_name:
            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2}):(\d{2}))?.*$", ifabsent_default_value)
            if match and (match[4] is None or match[5] is None or match[6] is None):
                return self.map_date_default_value(match[1], match[2], match[3], slot, cls)
            elif match:
                return self.map_datetime_default_value(
                    match[1], match[2], match[3], match[4], match[5], match[6], slot, cls
                )
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid date or "
                    f"datetime value"
                )

        if slot.range == Uri.type_name:
            return self.map_uri_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Curie.type_name:
            return self.map_curie_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Uriorcurie.type_name:
            return self.map_uri_or_curie_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Ncname.type_name:
            return self.map_nc_name_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Objectidentifier.type_name:
            return self.map_object_identifier_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Nodeidentifier.type_name:
            return self.map_node_identifier_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Jsonpointer.type_name:
            return self.map_json_pointer_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Jsonpath.type_name:
            return self.map_json_path_default_value(ifabsent_default_value, slot, cls)

        if slot.range == Sparqlpath.type_name:
            return self.map_sparql_path_default_value(ifabsent_default_value, slot, cls)

        # -----------------------
        #    Enum slot ranges
        # -----------------------

        for enum_name, enum in self.schema_view.all_enums().items():
            if enum_name == slot.range:
                for permissible_value_name, permissible_value in enum.permissible_values.items():
                    if permissible_value_name == ifabsent_default_value:
                        return self.map_enum_default_value(enum_name, permissible_value_name, slot, cls)

        raise ValueError(f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot could not be processed")

    @abc.abstractmethod
    def map_custom_default_values(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition) -> (bool, str):
        """
        Maps custom default values that aren't generic behaviours.

        @param default_value: the default value extracted from the ifabsent attribute
        @param slot: the definition of the slot
        @param cls: the definition of the class
        @return: a boolean that indicates if the value has been mapped followed by the mapped value
        """
        return False, None

    @abc.abstractmethod
    def map_string_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_integer_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_boolean_true_default_value(self, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_boolean_false_default_value(self, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_float_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_double_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_decimal_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_time_default_value(self, hour: str, minutes: str, seconds: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_date_default_value(self, year: str, month: str, day: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
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
        raise NotImplementedError()

    @abc.abstractmethod
    def map_uri_or_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_curie_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_uri_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_nc_name_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_object_identifier_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_node_identifier_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_json_pointer_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_json_path_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_sparql_path_default_value(self, default_value: str, slot: SlotDefinition, cls: ClassDefinition):
        raise NotImplementedError()

    @abc.abstractmethod
    def map_enum_default_value(
        self, enum_name: EnumDefinitionName, permissible_value_name: str, slot: SlotDefinition, cls: ClassDefinition
    ):
        raise NotImplementedError()

    def _uri_for(self, s: str) -> str:
        uri = str(self.schema_view.namespaces().uri_for(s))
        return self.schema_view.namespaces().curie_for(uri, True, True) or self._strval(uri)

    def _strval(self, txt: str) -> str:
        txt = str(txt).replace('"', '\\"')
        return f'"{txt}"'
