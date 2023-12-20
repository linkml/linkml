from abc import ABC
from dataclasses import dataclass
from typing import Optional, List, Union

from pydantic import BaseModel

from linkml.transformers.model_transformer import ModelTransformer


NAME = str


class TargetLanguageProperties(BaseModel):
    """
    Properties for a target language
    """
    multiple_inheritance: Optional[bool] = None
    ranges_as_unions: Optional[bool] = None
    element_name_regex: Optional[str] = None
    reserved_words: Optional[List[str]] = None


class ProgramElement(BaseModel, ABC):
    """
    A base element in the object-oriented program model.

    Each element must have a name. This should uniquely
    identify within the context of the element type, and
    in the scope of a module
    """
    name: NAME
    doc: Optional[str] = None


class ProgramPackage(ProgramElement):
    pass


class ProgramModule(ProgramElement):
    pass


RANGE = Union["DisjunctiveRangeExpression", "AtomicRangeExpression"]

class RangeExpression(BaseModel, ABC):
    """
    A range expression
    """
    optional: Optional[bool] = None


class DisjunctiveRangeExpression(RangeExpression):
    """
    A disjunctive range expression
    """
    ranges: List[RANGE]


class AtomicRangeExpression(RangeExpression):
    """
    An atomic range expression
    """
    range: NAME
    package: Optional[NAME] = None


class ProgramField(ProgramElement):
    """
    A field (attribute, slot) in a class.
    """
    allowed_values: Optional[RANGE] = None
    default_expression: Optional[str] = None



class ProgramClass(ProgramElement):
    """
    A class in the object-oriented program model.
    """
    is_a: Optional[NAME] = None
    mixins: Optional[List[NAME]] = None
    class_attributes: Optional[List[ProgramField]] = None
    fields: Optional[List[ProgramField]] = None



class ProgramEnum(ProgramElement):
    pass


@dataclass
class ObjectOrientedModelTransformer(ModelTransformer):
    """
    Transforms the source schema into an object-oriented model
    """