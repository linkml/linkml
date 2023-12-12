from __future__ import annotations

import re
import sys
from typing import List, Optional

from pydantic import BaseModel as BaseModel
from pydantic import Field, validator

if sys.version_info >= (3, 8):
    pass
else:
    pass


metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(
    WeakRefShimBaseModel,
    validate_assignment=True,
    validate_all=True,
    underscore_attrs_are_private=True,
    extra="forbid",
    arbitrary_types_allowed=True,
    use_enum_values=True,
):
    pass


class A(ConfiguredBaseModel):
    a: Optional[List[str]] = Field(default_factory=list)
    b: Optional[str] = Field(None)

    @validator("a", allow_reuse=True)
    def pattern_a(cls, v):
        pattern = re.compile(r"^A")
        if isinstance(v, list):
            # [raise ValueError(f"Invalid name format: {element}") for element in v if not pattern.match(element)]
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid a format: {element}")
        elif isinstance(v, str):
            if not pattern.match(v):
                raise ValueError(f"Invalid a format: {v}")
        return v

    @validator("b", allow_reuse=True)
    def pattern_b(cls, v):
        pattern = re.compile(r"^B")
        if isinstance(v, list):
            # [raise ValueError(f"Invalid name format: {element}") for element in v if not pattern.match(element)]
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid b format: {element}")
        elif isinstance(v, str):
            if not pattern.match(v):
                raise ValueError(f"Invalid b format: {v}")
        return v


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
A.update_forward_refs()
