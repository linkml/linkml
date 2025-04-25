from pathlib import Path
from typing import Optional, TypeVar, Union

from linkml.generators.common.build import (
    BuildResult,
    SchemaResult,
)
from linkml.generators.common.build import (
    ClassResult as ClassResult_,
)
from linkml.generators.common.build import (
    RangeResult as RangeResult_,
)
from linkml.generators.common.build import (
    SlotResult as SlotResult_,
)
from linkml.generators.pydanticgen.template import Import, Imports, PydanticAttribute, PydanticClass

T = TypeVar("T", bound="PydanticBuildResult", covariant=True)


class PydanticBuildResult(BuildResult):
    """
    BuildResult parent class for pydantic generator
    """

    imports: Optional[Union[list[Import], Imports]] = None
    injected_classes: Optional[list[Union[str, type]]] = None

    def merge(self, other: T) -> T:
        """
        Merge a build result with another.

        - Merges imports with :meth:`.Imports.__add__`
        - Extends (with simple deduplication) injected classes

        The top-level `merge` method is intended to just merge the "extra" parts of a result
        - ie. propagating the imports and injected classes up from 'lower' level results.
        It should *not* be used as a general "merge" method to eg. merge the results of two
        slot ranges into a Union of those ranges, etc. Either override this method (preserving
        the base behavior) or put that kind of merging logic into the generator.

        .. note::

            This returns a (shallow) copy of ``self``, so subclasses don't need to make additional copies.

        Args:
            other (:class:`.PydanticBuildResult`): A subclass of PydanticBuildResult,
            generic over whatever we have passed.

        Returns:
            :class:`.PydanticBuildResult`
        """
        self_copy = self.model_copy()
        if other.imports:
            if self.imports is not None:
                self_copy.imports += other.imports
            else:
                self_copy.imports = other.imports
        if other.injected_classes:
            if self_copy.injected_classes is not None:
                # only combine and dedupe when injected_classes don't match
                if self_copy.injected_classes != other.injected_classes:
                    self_copy.injected_classes.extend(other.injected_classes)
                    self_copy.injected_classes = list(dict.fromkeys(self_copy.injected_classes))
            else:
                self_copy.injected_classes = other.injected_classes
        return self_copy


class RangeResult(PydanticBuildResult, RangeResult_):
    """
    The result of building just the range part of a slot
    """

    range: str
    """The type annotation used in the generated model"""
    field_extras: Optional[dict] = None
    """Additional metadata for this slot to be held in the Field object"""

    def merge(self, other: "RangeResult") -> "RangeResult":
        """
        Merge two SlotResults...

        - calling :meth:`.PydanticBuildResult.merge`
        - replacing the existing annotation with that given by ``other`` .
        - updating any ``field_extras`` with the other

        Args:
            other (:class:`.SlotResult`): The other slot result to merge!

        Returns:
            :class:`.SlotResult`
        """
        res = super().merge(other)
        # Replace with other's annotation
        res.range = other.range
        if other.field_extras is not None:
            if res.field_extras is None:
                res.field_extras = {}
            res.field_extras.update(other.field_extras)
        return res


class SlotResult(PydanticBuildResult, SlotResult_):
    attribute: PydanticAttribute


class ClassResult(PydanticBuildResult, ClassResult_):
    cls: PydanticClass
    """Constructed Template Model for class, including attributes/slots"""


class SplitResult(SchemaResult):
    """Build result when generating with :func:`.generate_split`"""

    main: bool = False
    path: Path
    serialized_module: str
    module_import: Optional[str] = None
