"""
Lifestyle methods mixin
"""

from collections.abc import Iterable
from typing import TypeVar

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    EnumDefinition,
    SchemaDefinition,
    SlotDefinition,
    TypeDefinition,
)

from linkml.generators.common.build import ClassResult, EnumResult, RangeResult, SchemaResult, SlotResult, TypeResult
from linkml.generators.common.template import TemplateModel

TSchema = TypeVar("TSchema", bound=SchemaResult)
TClass = TypeVar("TClass", bound=ClassResult)
TSlot = TypeVar("TSlot", bound=SlotResult)
TRange = TypeVar("TRange", bound=RangeResult)
TType = TypeVar("TType", bound=TypeResult)
TEnum = TypeVar("TEnum", bound=EnumResult)
TTemplate = TypeVar("TTemplate", bound=TemplateModel)


class LifecycleMixin:
    """
    Mixin class for implementing lifecycle methods to modify the generation process
    without needing messy overrides and tiptoeing around parent generator classes.

    Not all classes that inherit from the mixin will be able to implement all of the lifecycle methods.
    The generator class should make it clear which methods are supported in its documentation -
    no programmatic checking for lifecycle method support is available on first implementation.

    Generators should **not** define any of the lifecycle methods themselves - the purpose is
    to allow downstream modification of the generation process with clear entrypoints and without
    needing to copy/paste code from the generator/call ``super()`` methods - if the Generator
    is also using the lifecycle method, the point of the mixin is lost.

    The order that these methods are called may vary in different generators, but in general, if
    slots are generated hierarchically within classes as in the pydantic generator...

    * :meth:`.before_generate_schema`
    * :meth:`.before_generate_classes`
    * :meth:`.before_generate_class`
    * :meth:`.before_generate_slots`
    * :meth:`.before_generate_slot`
    * :meth:`.after_generate_slot`
    * :meth:`.after_generate_slots`
    * :meth:`.after_generate_class`
    * :meth:`.after_generate_classes`
    * :meth:`.after_generate_schema`
    * :meth:`.before_render_template`
    * :meth:`.after_render_template`

    (Add other examples of ordering from other generators as implemented)

    Each method should receive a :class:`.SchemaView` to get perspective on the current schema
    being built. The ``before_`` methods should receive and return a single or list of ``Definitions``
    and the ``after_`` methods should receive and return a single or list of the appropriate :class:`.BuildResult`
    type.
    """

    def before_generate_schema(self, schema: SchemaDefinition, sv: SchemaView) -> SchemaDefinition:
        return schema

    def after_generate_schema(self, schema: TSchema, sv: SchemaView) -> TSchema:
        return schema

    def before_generate_class(self, cls: ClassDefinition, sv: SchemaView) -> ClassDefinition:
        return cls

    def after_generate_class(self, cls: TClass, sv: SchemaView) -> TClass:
        return cls

    def before_generate_classes(self, cls: Iterable[ClassDefinition], sv: SchemaView) -> Iterable[ClassDefinition]:
        return cls

    def after_generate_classes(self, cls: Iterable[TClass], sv: SchemaView) -> Iterable[TClass]:
        return cls

    def before_generate_slot(self, slot: SlotDefinition, sv: SchemaView) -> SlotDefinition:
        return slot

    def after_generate_slot(self, slot: TSlot, sv: SchemaView) -> TSlot:
        return slot

    def before_generate_slots(self, slot: Iterable[SlotDefinition], sv: SchemaView) -> Iterable[SlotDefinition]:
        return slot

    def after_generate_slots(self, slot: Iterable[TSlot], sv: SchemaView) -> Iterable[TSlot]:
        return slot

    def before_generate_class_slot(self, slot: SlotDefinition, cls: ClassDefinition, sv: SchemaView) -> SlotDefinition:
        return slot

    def after_generate_class_slot(self, slot: TSlot, cls: ClassDefinition, sv: SchemaView) -> TSlot:
        return slot

    def before_generate_class_slots(
        self, slot: Iterable[SlotDefinition], cls: ClassDefinition, sv: SchemaView
    ) -> Iterable[SlotDefinition]:
        return slot

    def after_generate_class_slots(
        self, slot: Iterable[TSlot], cls: ClassDefinition, sv: SchemaView
    ) -> Iterable[TSlot]:
        return slot

    def before_generate_type(self, typ: TypeDefinition, sv: SchemaView) -> TypeDefinition:
        return typ

    def after_generate_type(self, typ: TType, sv: SchemaView) -> TType:
        return typ

    def before_generate_types(self, typ: Iterable[TypeDefinition], sv: SchemaView) -> Iterable[TypeDefinition]:
        return typ

    def after_generate_types(self, typ: Iterable[TType], sv: SchemaView) -> Iterable[TType]:
        return typ

    def before_generate_enum(self, enum: EnumDefinition, sv: SchemaView) -> EnumDefinition:
        return enum

    def after_generate_enum(self, enum: TEnum, sv: SchemaView) -> TEnum:
        return enum

    def before_generate_enums(self, enum: Iterable[EnumDefinition], sv: SchemaView) -> Iterable[EnumDefinition]:
        return enum

    def after_generate_enums(self, enum: Iterable[TEnum], sv: SchemaView) -> Iterable[TEnum]:
        return enum

    def before_render_template(self, template: TTemplate, sv: SchemaView) -> TTemplate:
        return template

    def after_render_template(self, template: str, sv: SchemaView) -> str:
        return template
