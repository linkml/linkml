from typing import Optional
from pydantic import Field, computed_field
from linkml.generators.common.template import TemplateModel


class RustTemplateModel(TemplateModel):
    """
    Parent class for rust template models :)
    """

    pyo3: bool = True
    """
    Whether pyO3 annotations should be added to generated items :)
    """


class RustProperty(RustTemplateModel):
    """
    A property within a rust struct
    """

    name: str
    type_: str
    required: bool


class RustStruct(RustTemplateModel):
    """
    A struct!
    """

    name: str
    bases: Optional[list[str]] = None
    """
    Base classes to inherit from - must have entire MRO, just just immediate ancestor
    """
    properties: list[RustProperty] = Field(default_factory=list)


class RustFile(RustTemplateModel):
    """
    A whole rust file!
    """

    name: str
    structs: list[RustStruct] = Field(default_factory=list)

    @computed_field
    def struct_names(self) -> list[str]:
        """Names of all the structs we have!"""
        return [c.name for c in self.structs]
