from typing import Optional, Any

from pydantic import BaseModel


class BuildResult(BaseModel):
    """
    The result of any build phase for any linkML object

    BuildResults are merged in the serialization process, and are used
    to keep track of not only the particular representation
    of the thing in question, but any "side effects" that need to happen
    elsewhere in the generation process (like adding imports, injecting classes, etc.)
    """

    # FIXME: PLACEHOLDER TYPES PENDING MERGE OF OTHER PULL REQUESTS
    imports: Optional[dict[str, Any]] = None
    injected_classes: Optional[list[Any]] = None


class SlotResult(BuildResult):
    annotation: str
    """The type annotation used in the generated model"""
    field_extras: Optional[dict] = None
    """Additional metadata for this slot to be held in the Field object"""
