"""
Models for intermediate build results

(see PydanticGenerator for example implementation and use)
"""

import dataclasses
from typing import Annotated, Any, TypeVar

from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinition,
    SchemaDefinition,
    SlotDefinition,
    TypeDefinition,
)
from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler
from pydantic_core import core_schema

T = TypeVar("T", bound="BuildResult", covariant=True)


@dataclasses.dataclass()
class SkipValidation:
    """
    A version of :class:`pydantic.SkipValidation` that actually skips generating the
    schema for the field entirely - useful for including types that don't need to be validated
    like the metamodel dataclasses
    """

    def __class_getitem__(cls, item: Any) -> Any:
        return Annotated[item, SkipValidation()]

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.any_schema()

    __hash__ = object.__hash__


class BuildResult(BaseModel):
    """
    The result of any build phase for any linkML object

    BuildResults are merged in the serialization process, and are used
    to keep track of not only the particular representation
    of the thing in question, but any "side effects" that need to happen
    elsewhere in the generation process (like adding imports, injecting classes, etc.)
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def merge(self, other: T) -> T:
        """
        Build results should have some means of merging results of a like kind
        """
        raise NotImplementedError("This build result doesn't know how to merge!")


class SchemaResult(BuildResult):
    """Abstract results container for built schemas"""

    source: SkipValidation[SchemaDefinition]

    def merge(self, other: T) -> T:
        """
        SchemaResults are special and don't need a merge method, since generating
        multiple schemas at once is not common or expected behavior for a generator.
        """
        raise NotImplementedError("SchemaResult doesn't need a merge method, and none has been defined")


class ClassResult(BuildResult):
    """Abstract results container for built classes"""

    source: SkipValidation[ClassDefinition]


class SlotResult(BuildResult):
    """Abstract results container for built slots"""

    source: SkipValidation[SlotDefinition]


class TypeResult(BuildResult):
    """Abstract results container for built types"""

    source: SkipValidation[TypeDefinition]


class EnumResult(BuildResult):
    """Abstract results container for built enums"""

    source: SkipValidation[EnumDefinition]


class RangeResult(BuildResult):
    """Abstract results container for just the range part of a slot"""
