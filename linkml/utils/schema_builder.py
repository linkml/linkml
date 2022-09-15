from dataclasses import dataclass, field
from typing import Dict, List, Union

from linkml_runtime.linkml_model import (ClassDefinition, EnumDefinition,
                                         PermissibleValue, Prefix,
                                         SchemaDefinition, SlotDefinition,
                                         TypeDefinition)
from linkml_runtime.utils.formatutils import camelcase, underscore


@dataclass
class SchemaBuilder:
    """
    Builder class for SchemaDefinitions
    """

    name: str = None
    schema: SchemaDefinition = None

    def __post_init__(self):
        name = self.name
        if name is None:
            name = "test-schema"
        self.schema = SchemaDefinition(id=f"http://example.org/{name}", name=name)

    def add_class(
        self,
        cls: Union[ClassDefinition, str],
        slots: List[Union[str, SlotDefinition]] = None,
        slot_usage: Dict[str, SlotDefinition] = None,
        use_attributes=False,
        **kwargs,
    ) -> "SchemaBuilder":
        """
        Adds a class to the schema

        :param cls:
        :param slots:
        :param slot_usage:
        :param kwargs:
        :return: builder
        """
        if not isinstance(cls, ClassDefinition):
            cls = ClassDefinition(cls)
        self.schema.classes[cls.name] = cls
        if use_attributes:
            for s in slots:
                if isinstance(s, SlotDefinition):
                    cls.attributes[s.name] = s
                else:
                    raise ValueError(
                        f"If use_attributes=True then slots must be SlotDefinitions"
                    )
        else:
            if slots is not None:
                for s in slots:
                    self.add_slot(s, cls.name)
            if slot_usage:
                for k, v in slot_usage.items():
                    cls.slot_usage[k] = v
        for k, v in kwargs.items():
            setattr(cls, k, v)
        return self

    def add_slot(
        self, slot: Union[SlotDefinition, Dict, str], class_name: str = None
    ) -> "SchemaBuilder":
        """
        Adds the slot to the schema

        :param slot:
        :param class_name: if specified, this will become a valid slot for the class
        :return: builder
        """
        if isinstance(slot, str):
            slot = SlotDefinition(slot)
        elif isinstance(slot, dict):
            slot = SlotDefinition(**slot)
        self.schema.slots[slot.name] = slot
        if class_name is not None:
            self.schema.classes[class_name].slots.append(slot.name)
        return self

    def set_slot(self, slot_name: str, **kwargs) -> "SchemaBuilder":
        """
        Set details of the slot

        :param slot_name:
        :param kwargs:
        :return: builder
        """
        slot = self.schema.slots[slot_name]
        for k, v in kwargs.items():
            setattr(slot, k, v)
        return self

    def add_enum(
        self,
        enum_def: Union[EnumDefinition, str],
        permissible_values: List[Union[str, PermissibleValue]] = None,
    ) -> "SchemaBuilder":
        """
        Adds an enum to the schema

        :param enum_def:
        :param permissible_values:
        :return: builder
        """
        if not isinstance(enum_def, EnumDefinition):
            enum_def = EnumDefinition(enum_def)
        self.schema.enums[enum_def.name] = enum_def
        if permissible_values is not None:
            for pv in permissible_values:
                if isinstance(pv, str):
                    pv = PermissibleValue(text=pv)
                    enum_def.permissible_values[pv.text] = pv
        return self

    def add_prefix(self, prefix: str, url: str) -> "SchemaBuilder":
        """
        Adds a prefix for use with CURIEs

        :param prefix:
        :param url:
        :return: builder
        """
        obj = Prefix(prefix_prefix=prefix, prefix_reference=url)
        self.schema.prefixes[obj.prefix_prefix] = obj
        return self

    def add_defaults(self) -> "SchemaBuilder":
        """
        Sets defaults, including:

        - default_range
        - default imports to include linkml:types
        - default prefixes

        :return: builder
        """
        name = underscore(self.schema.name)
        uri = self.schema.id
        self.schema.default_range = "string"
        self.schema.default_prefix = name
        self.schema.imports.append("linkml:types")
        self.add_prefix("linkml", "https://w3id.org/linkml/")
        self.add_prefix(name, f"{uri}/")
        return self

    def add_type(self, type: Union[TypeDefinition, Dict, str]) -> "SchemaBuilder":
        """
        Adds the type to the schema

        :param type:
        :return: builder
        """
        if isinstance(type, str):
            type = TypeDefinition(type)
        elif isinstance(type, dict):
            type = TypeDefinition(**type)
        self.schema.types[type.name] = type
        return self
