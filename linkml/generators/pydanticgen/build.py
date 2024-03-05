from typing import List, Optional, Type, Union

from pydantic import BaseModel

from linkml.generators.pydanticgen.template import Import, Imports


class BuildResult(BaseModel):
    """
    The result of any build phase for any linkML object

    BuildResults are merged in the serialization process, and are used
    to keep track of not only the particular representation
    of the thing in question, but any "side effects" that need to happen
    elsewhere in the generation process (like adding imports, injecting classes, etc.)
    """

    # FIXME: PLACEHOLDER TYPES PENDING MERGE OF OTHER PULL REQUESTS
    imports: Optional[Union[List[Import], Imports]] = None
    injected_classes: Optional[List[Union[str, Type]]] = None

    def __add__(self, other: "BuildResult"):
        self_copy = self.copy()
        if other.imports:
            if self.imports is not None:
                self_copy.imports += other.imports
            else:
                self_copy.imports = other.imports
        if other.injected_classes:
            self_copy.injected_classes = self_copy.injected_classes.extend(other.injected_classes)
        return self_copy


class SlotResult(BuildResult):
    annotation: str
    """The type annotation used in the generated model"""
    field_extras: Optional[dict] = None
    """Additional metadata for this slot to be held in the Field object"""

    def __add__(self, other: "SlotResult"):
        res = super(SlotResult, self).__add__(other)
        # Replace with other's annotation
        res.annotation = other.annotation
        return res
