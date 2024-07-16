"""
Models for intermediate build results

(see PydanticGenerator for example implementation and use)
"""

from abc import abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound="BuildResult", covariant=True)


class BuildResult(BaseModel):
    """
    The result of any build phase for any linkML object

    BuildResults are merged in the serialization process, and are used
    to keep track of not only the particular representation
    of the thing in question, but any "side effects" that need to happen
    elsewhere in the generation process (like adding imports, injecting classes, etc.)
    """

    @abstractmethod
    def merge(self, other: T) -> T:
        """
        Build results should have some means of merging results of a like kind
        """


class SchemaResult(BuildResult):
    """Abstract results container for built schemas"""


class ClassResult(BuildResult):
    """Abstract results container for built classes"""


class SlotResult(BuildResult):
    """Abstract results container for built slots"""


class TypeResult(BuildResult):
    """Abstract results container for built types"""


class EnumResult(BuildResult):
    """Abstract results container for built enums"""


class RangeResult(BuildResult):
    """Abstract results container for just the range part of a slot"""
