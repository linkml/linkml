from dataclasses import dataclass, field
from typing import Union, List, Dict

from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinition, SlotDefinition, Prefix


# TODO: move to linkml_runtime


@dataclass
class SchemaBuilder:
    """
    Builder class for SchemaDefinitions
    """
    schema: SchemaDefinition = field(default_factory=lambda: SchemaDefinition(id='http://example.org/test/',
                                                                              name='test-schema'))

    def add_class(self, cls: Union[ClassDefinition, str], slots: List[Union[str, SlotDefinition]] = None,
                  slot_usage: Dict[str, SlotDefinition] = None, **kwargs) -> "SchemaBuilder":
        """
        Adds a class to the schema

        :param cls:
        :param slots:
        :param slot_usage:
        :param kwargs:
        :return:
        """
        if not isinstance(cls, ClassDefinition):
            cls = ClassDefinition(cls)
        self.schema.classes[cls.name] = cls
        if slots is not None:
            for s in slots:
                self.add_slot(s, cls.name)
        if slot_usage:
            for k, v in slot_usage.items():
                cls.slot_usage[k] = v
        for k, v in kwargs.items():
            setattr(cls, k, v)
        return self

    def add_slot(self, slot: Union[SlotDefinition, Dict, str], class_name: str = None) -> "SchemaBuilder":
        """
        Adds the slot to the schema

        :param slot:
        :param class_name: if specified, this will become a valid slot for the class
        :return:
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
        :return:
        """
        slot = self.schema.slots[slot_name]
        for k, v in kwargs.items():
            setattr(slot, k, v)
        return self

    def add_prefix(self, prefix: str, url: str):
        """
        Adds a prefix for use with CURIEs

        :param prefix:
        :param url:
        :return:
        """
        obj = Prefix(prefix_prefix=prefix, prefix_reference=url)
        self.schema.prefixes[obj.prefix_prefix] = obj

    def add_defaults(self):
        """
        Sets defaults, including:

        - default_range
        - default imports to include linkml:types
        - default prefixes
        """
        self.schema.default_range = "string"
        self.schema.default_prefix = "ex"
        self.schema.imports.append("linkml:types")
        self.add_prefix("linkml", "https://w3id.org/linkml/")
        self.add_prefix("ex", "https://example.org/test/")
