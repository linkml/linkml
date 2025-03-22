import abc
import re
import sys
from abc import ABC
from typing import Any, Optional, Union

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias

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
    types,
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

TYPES_TYPE: TypeAlias = Union[
    type[Boolean],
    type[Curie],
    type[Date],
    type[DateOrDatetime],
    type[Datetime],
    type[Decimal],
    type[Double],
    type[Float],
    type[Integer],
    type[Jsonpath],
    type[Jsonpointer],
    type[Ncname],
    type[Nodeidentifier],
    type[Objectidentifier],
    type[Sparqlpath],
    type[String],
    type[Time],
    type[Uri],
    type[Uriorcurie],
]

TYPES = [
    t
    for t in types.__dict__.values()
    if isinstance(t, type) and t.__module__ == types.__name__ and hasattr(t, "type_name")
]


class IfAbsentProcessor(ABC):
    """
    Processes value of ifabsent slot.

    See `<https://w3id.org/linkml/ifabsent>`_.
    """

    ifabsent_regex = re.compile(r"""(?:(?P<type>\w+)\()?[\"\']?(?P<default_value>[^\(\)\"\')]*)[\"\']?\)?""")

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

        base_type = self._base_type(slot.range)

        if base_type is String:
            return self.map_string_default_value(ifabsent_default_value, slot, cls)

        if base_type is Boolean:
            if re.match(r"^[Tt]rue$", ifabsent_default_value):
                return self.map_boolean_true_default_value(slot, cls)
            elif re.match(r"^[Ff]alse$", ifabsent_default_value):
                return self.map_boolean_false_default_value(slot, cls)
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid boolean "
                    f"value"
                )

        if base_type is Integer:
            return self.map_integer_default_value(ifabsent_default_value, slot, cls)

        if base_type is Float:
            return self.map_float_default_value(ifabsent_default_value, slot, cls)

        if base_type is Double:
            return self.map_double_default_value(ifabsent_default_value, slot, cls)

        if base_type is Decimal:
            return self.map_decimal_default_value(ifabsent_default_value, slot, cls)

        if base_type is Time:
            match = re.match(r"^(\d{2}):(\d{2}):(\d{2}).*$", ifabsent_default_value)
            if match:
                return self.map_time_default_value(match[1], match[2], match[3], slot, cls)
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid time value"
                )

        # TODO manage timezones and offsets
        if base_type is Date:
            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", ifabsent_default_value)
            if match:
                return self.map_date_default_value(match[1], match[2], match[3], slot, cls)
            else:
                raise ValueError(
                    f"The ifabsent value `{slot.ifabsent}` of the `{slot.name}` slot does not match a valid date value"
                )

        # TODO manage timezones and offsets
        if base_type is Datetime:
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
        if base_type is DateOrDatetime:
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

        if base_type is Uri:
            return self.map_uri_default_value(ifabsent_default_value, slot, cls)

        if base_type is Curie:
            return self.map_curie_default_value(ifabsent_default_value, slot, cls)

        if base_type is Uriorcurie:
            return self.map_uri_or_curie_default_value(ifabsent_default_value, slot, cls)

        if base_type is Ncname:
            return self.map_nc_name_default_value(ifabsent_default_value, slot, cls)

        if base_type is Objectidentifier:
            return self.map_object_identifier_default_value(ifabsent_default_value, slot, cls)

        if base_type is Nodeidentifier:
            return self.map_node_identifier_default_value(ifabsent_default_value, slot, cls)

        if base_type is Jsonpointer:
            return self.map_json_pointer_default_value(ifabsent_default_value, slot, cls)

        if base_type is Jsonpath:
            return self.map_json_path_default_value(ifabsent_default_value, slot, cls)

        if base_type is Sparqlpath:
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

    def _base_type(self, range_: str) -> Optional[TYPES_TYPE]:
        """
        Find the linkml base type that corresponds to either a matching type_name or custom type

        First check for an explicit match of the range == TypeDefinition.type_name
        Then check for explicit inheritance via typeof
        Finally check for implicit matching via matching base

        Don't raise here, just return None in case another method of resolution like enums are
        available
        """
        # first check for matching type using type_name - ie. range is already a base type

        for typ in TYPES:
            if range_ == typ.type_name:
                return typ

        # if we're not a type, return None to indicate that, e.g. if an enum's permissible_value
        if range_ not in self.schema_view.all_types(imports=True):
            return

        # then check explicit descendents of types
        # base types do not inherit from one another, so the last ancestor is always a base type
        # if it is inheriting from a base type
        ancestor = self.schema_view.type_ancestors(range_)[-1]
        for typ in TYPES:
            if ancestor == typ.type_name:
                return typ

        # finally check if we have a matching base
        induced_typ = self.schema_view.induced_type(range_)
        if induced_typ.repr is None and induced_typ.base is None:
            return None
        for typ in TYPES:
            # types always inherit from a single type, and that type is their base
            # our range can match it with repr or base
            typ_base = typ.__mro__[1].__name__
            if typ_base == induced_typ.base:
                return typ

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
