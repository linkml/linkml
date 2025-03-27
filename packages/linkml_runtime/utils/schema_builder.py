from dataclasses import dataclass, fields
from typing import Union, Optional

from linkml_runtime.linkml_model import (ClassDefinition, EnumDefinition,
                                         PermissibleValue, Prefix,
                                         SchemaDefinition, SlotDefinition,
                                         TypeDefinition)
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schema_as_dict import schema_as_dict


@dataclass
class SchemaBuilder:
    """
    Builder class for SchemaDefinitions.

    Example:

        >>> from linkml_runtime.utils.schema_builder import SchemaBuilder
        >>> sb = SchemaBuilder('test-schema')
        >>> sb.add_class('Person', slots=['name', 'age'])
        >>> sb.add_class('Organization', slots=['name', 'employees'])
        >>> sb.add_slot('name',description='Name of the person or organization')
        >>> sb.add_slot('age',description='Age of the person', range='integer')
        >>> schema = sb.schema
        >>> print()

    Most builder methods accepts either a string, an instance of a metamodel element,
    or a dictionary.  If a string is provided, then a new element is created with this
    as the name.

    This follows the standard Builder pattern, so the results of a build operation
    are a builder, allowing chaining. For example:

        >>> sb = SchemaBuilder('test-schema').add_class('Person', slots=['name', 'age'])

    """

    name: Optional[str] = None
    """Initialized name for the schema."""

    id: Optional[str] = None
    """Initialized id for the schema."""

    schema: SchemaDefinition = None
    """generated SchemaDefinition object."""

    def __post_init__(self):
        name = self.name
        if name is None:
            name = "test-schema"
        id = self.id if self.id else f"http://example.org/{name}"
        self.schema = SchemaDefinition(id=id, name=name)

    def add_class(
        self,
        cls: Union[ClassDefinition, dict, str],
        slots: list[Union[str, SlotDefinition]] = None,
        slot_usage: dict[str, SlotDefinition] = None,
        replace_if_present: bool = False,
        use_attributes: bool = False,
        **kwargs,
    ) -> "SchemaBuilder":
        """
        Adds a class to the schema.

        :param cls: name, dict object, or ClassDefinition object to add
        :param slots: list of slot names or slot objects. This must be a list of
            `SlotDefinition` objects if `use_attributes=True`
        :param slot_usage: slots keyed by slot name (ignored if `use_attributes=True`)
        :param replace_if_present: if True, replace existing class if present
        :param use_attributes: Whether to specify the given slots as an inline
            definition of slots, attributes, in the class definition
        :param kwargs: additional ClassDefinition properties
        :return: builder
        :raises ValueError: if class already exists and replace_if_present=False
        """
        if slots is None:
            slots = []
        if slot_usage is None:
            slot_usage = {}

        if isinstance(cls, str):
            cls = ClassDefinition(cls, **kwargs)
        elif isinstance(cls, dict):
            cls = ClassDefinition(**{**cls, **kwargs})
        else:
            # Ensure that `cls` is a `ClassDefinition` object
            if not isinstance(cls, ClassDefinition):
                msg = (
                    f"cls must be a string, dict, or ClassDefinition, "
                    f"not {type(cls)!r}"
                )
                raise TypeError(msg)

            cls_as_dict = {f.name: getattr(cls, f.name) for f in fields(cls)}

            cls = ClassDefinition(**{**cls_as_dict, **kwargs})

        if cls.name in self.schema.classes and not replace_if_present:
            raise ValueError(f"Class {cls.name} already exists")
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
            for s in slots:
                cls.slots.append(s.name if isinstance(s, SlotDefinition) else s)
                if isinstance(s, str) and s in self.schema.slots:
                    # top-level slot already exists
                    continue
                self.add_slot(s, replace_if_present=replace_if_present)
            for k, v in slot_usage.items():
                cls.slot_usage[k] = v
        return self

    def add_slot(
        self, slot: Union[SlotDefinition, dict, str], class_name: str = None, replace_if_present=False, **kwargs
    ) -> "SchemaBuilder":
        """
        Adds the slot to the schema.

        :param slot: name, dict object, or SlotDefinition object to add
        :param class_name: if specified, this will become a valid slot for this class
        :param replace_if_present: if True, replace existing slot if present
        :param kwargs: additional properties
        :return: builder
        :raises ValueError: if slot already exists and replace_if_present=False
        """
        if isinstance(slot, str):
            slot = SlotDefinition(slot, **kwargs)
        elif isinstance(slot, dict):
            slot = SlotDefinition(**{**slot, **kwargs})
        if not replace_if_present and slot.name in self.schema.slots:
            raise ValueError(f"Slot {slot.name} already exists")
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
        enum_def: Union[EnumDefinition, dict, str],
        permissible_values: list[Union[str, PermissibleValue]] = None,
        replace_if_present=False,
        **kwargs,
    ) -> "SchemaBuilder":
        """
        Adds an enum to the schema

        :param enum_def: The base specification of the enum to be added
        :param permissible_values: Additional, or overriding, permissible values
            of the enum to be added
        :param replace_if_present: Whether to replace the enum if it already exists in
            the schema by name
        :param kwargs: Additional `EnumDefinition` properties to be set as part of the
            enum to be added
        :return: builder
        :raises ValueError: if enum already exists and replace_if_present=False
        """
        if permissible_values is None:
            permissible_values = []

        if isinstance(enum_def, str):
            enum_def = EnumDefinition(enum_def, **kwargs)
        elif isinstance(enum_def, dict):
            enum_def = EnumDefinition(**{**enum_def, **kwargs})
        else:
            # Ensure that `enum_def` is a `EnumDefinition` object
            if not isinstance(enum_def, EnumDefinition):
                msg = (
                    f"enum_def must be a `str`, `dict`, or `EnumDefinition`, "
                    f"not {type(enum_def)!r}"
                )
                raise TypeError(msg)

        if enum_def.name in self.schema.enums and not replace_if_present:
            raise ValueError(f"Enum {enum_def.name} already exists")

        # Attach the enum definition to the schema
        self.schema.enums[enum_def.name] = enum_def

        for pv in permissible_values:
            if isinstance(pv, str):
                pv = PermissibleValue(text=pv)
            elif not isinstance(pv, PermissibleValue):
                msg = (
                    f"A permissible value must be a `str` or "
                    f"a `PermissibleValue` object, not {type(pv)}"
                )
                raise TypeError(msg)

            enum_def.permissible_values[pv.text] = pv

        return self

    def add_prefix(self, prefix: str, url: str, replace_if_present = False) -> "SchemaBuilder":
        """
        Adds a prefix for use with CURIEs

        :param prefix:
        :param url:
        :return: builder
        :raises ValueError: if prefix already exists and replace_if_present=False
        """
        obj = Prefix(prefix_prefix=prefix, prefix_reference=url)
        if prefix in self.schema.prefixes and not replace_if_present:
            raise ValueError(f"Prefix {prefix} already exists")
        self.schema.prefixes[obj.prefix_prefix] = obj
        return self

    def add_imports(self, *imports) -> "SchemaBuilder":
        """
        Adds imports to the schema

        :param imports: list of imports
        :return: builder
        """
        self.schema.imports.extend(imports)
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

    def add_type(
            self,
            type: Union[TypeDefinition, dict, str],
            typeof: str = None,
            uri: str = None,
            replace_if_present=False,
            **kwargs
    ) -> "SchemaBuilder":
        """
        Adds the type to the schema

        :param type:
        :param typeof: if specified, the parent type
        :param uri: if specified, the URI or curie of the type
        :param replace_if_present:
        :param kwargs:
        :return: builder
        :raises ValueError: if type already exists and replace_if_present=False
        """
        if isinstance(type, str):
            type = TypeDefinition(type)
        elif isinstance(type, dict):
            type = TypeDefinition(**type)
        if typeof:
            type.typeof = typeof
        if not replace_if_present and type.name in self.schema.types:
            raise ValueError(f"Type {type.name} already exists")
        self.schema.types[type.name] = type
        for k, v in kwargs.items():
            setattr(type, k, v)
        return self

    def as_dict(self) -> dict:
        """
        Returns the schema as a dictionary.

        Compaction is performed to eliminate redundant keys

        :return: dictionary representation
        """
        return schema_as_dict(self.schema)
