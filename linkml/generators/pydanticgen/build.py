from typing import List, Optional, Type, TypeVar, Union

from pydantic import BaseModel

from linkml.generators.pydanticgen.template import Import, Imports, PydanticAttribute, PydanticClass

T = TypeVar("T", bound="BuildResult", covariant=True)


class BuildResult(BaseModel):
    """
    The result of any build phase for any linkML object

    BuildResults are merged in the serialization process, and are used
    to keep track of not only the particular representation
    of the thing in question, but any "side effects" that need to happen
    elsewhere in the generation process (like adding imports, injecting classes, etc.)
    """

    imports: Optional[Union[List[Import], Imports]] = None
    injected_classes: Optional[List[Union[str, Type]]] = None

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
            other (:class:`.BuildResult`): A subclass of BuildResult, generic over whatever we have passed.

        Returns:
            :class:`.BuildResult`
        """
        self_copy = self.model_copy()
        if other.imports:
            if self.imports is not None:
                self_copy.imports += other.imports
            else:
                self_copy.imports = other.imports
        if other.injected_classes:
            if self_copy.injected_classes is not None:
                self_copy.injected_classes.extend(other.injected_classes)
                self_copy.injected_classes = list(dict.fromkeys(self_copy.injected_classes))
            else:
                self_copy.injected_classes = other.injected_classes
        return self_copy


class RangeResult(BuildResult):
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

        - calling :meth:`.BuildResult.merge`
        - replacing the existing annotation with that given by ``other`` .
        - updating any ``field_extras`` with the other

        Args:
            other (:class:`.SlotResult`): The other slot result to merge!

        Returns:
            :class:`.SlotResult`
        """
        res = super(RangeResult, self).merge(other)
        # Replace with other's annotation
        res.range = other.range
        if other.field_extras is not None:
            if res.field_extras is None:
                res.field_extras = {}
            res.field_extras.update(other.field_extras)
        return res


class SlotResult(BuildResult):
    attribute: PydanticAttribute


class ClassResult(BuildResult):
    cls: PydanticClass
    """Constructed Template Model for class, including attributes/slots"""
