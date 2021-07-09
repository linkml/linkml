# Auto generated from python_complex_ranges.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: complex_ranges
#
# id: http://examples.org/linkml/test/complex_ranges
# description: sample complex ranges
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Date, Double, Integer, String
from linkml_runtime.utils.metamodelcore import XSDDate

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
COMPLEX_RANGES = CurieNamespace('complex_ranges', 'http://examples.org/linkml/test/complex_ranges')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = COMPLEX_RANGES


# Types

# Class references
class KeyedOneElementClassName(extended_str):
    pass


class KeyedTwoElementClassName(extended_str):
    pass


class KeyedThreeElementClassName(extended_str):
    pass


class IdentifiedOneElementClassName(extended_str):
    pass


class IdentifiedTwoElementClassName(extended_str):
    pass


class IdentifiedThreeElementClassName(extended_str):
    pass


@dataclass
class OneElementClass(YAMLRoot):
    """
    A class with a single non-key integer as a value
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.OneElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:OneElementClass"
    class_name: ClassVar[str] = "OneElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.OneElementClass

    value: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        super().__post_init__(**kwargs)


@dataclass
class TwoElementClass(YAMLRoot):
    """
    A class with a two non-key strings as a values
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.TwoElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:TwoElementClass"
    class_name: ClassVar[str] = "TwoElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.TwoElementClass

    value1: Optional[str] = None
    value2: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value1 is not None and not isinstance(self.value1, str):
            self.value1 = str(self.value1)

        if self.value2 is not None and not isinstance(self.value2, str):
            self.value2 = str(self.value2)

        super().__post_init__(**kwargs)


@dataclass
class ThreeElementClass(YAMLRoot):
    """
    A class with three non-key doubles as values
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.ThreeElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:ThreeElementClass"
    class_name: ClassVar[str] = "ThreeElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.ThreeElementClass

    value1: Optional[float] = None
    value2: Optional[float] = None
    value3: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value1 is not None and not isinstance(self.value1, float):
            self.value1 = float(self.value1)

        if self.value2 is not None and not isinstance(self.value2, float):
            self.value2 = float(self.value2)

        if self.value3 is not None and not isinstance(self.value3, float):
            self.value3 = float(self.value3)

        super().__post_init__(**kwargs)


@dataclass
class KeyedOneElementClass(YAMLRoot):
    """
    A keyed class with one element
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.KeyedOneElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:KeyedOneElementClass"
    class_name: ClassVar[str] = "KeyedOneElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.KeyedOneElementClass

    name: Union[str, KeyedOneElementClassName] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, KeyedOneElementClassName):
            self.name = KeyedOneElementClassName(self.name)

        super().__post_init__(**kwargs)


@dataclass
class KeyedTwoElementClass(YAMLRoot):
    """
    A keyed class with an additional integer
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.KeyedTwoElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:KeyedTwoElementClass"
    class_name: ClassVar[str] = "KeyedTwoElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.KeyedTwoElementClass

    name: Union[str, KeyedTwoElementClassName] = None
    value: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, KeyedTwoElementClassName):
            self.name = KeyedTwoElementClassName(self.name)

        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        super().__post_init__(**kwargs)


@dataclass
class KeyedThreeElementClass(YAMLRoot):
    """
    A keyed class with an additional integer and date
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.KeyedThreeElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:KeyedThreeElementClass"
    class_name: ClassVar[str] = "KeyedThreeElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.KeyedThreeElementClass

    name: Union[str, KeyedThreeElementClassName] = None
    value: Optional[int] = None
    modifier: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, KeyedThreeElementClassName):
            self.name = KeyedThreeElementClassName(self.name)

        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        if self.modifier is not None and not isinstance(self.modifier, XSDDate):
            self.modifier = XSDDate(self.modifier)

        super().__post_init__(**kwargs)


@dataclass
class IdentifiedOneElementClass(YAMLRoot):
    """
    A identified class with one element
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.IdentifiedOneElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:IdentifiedOneElementClass"
    class_name: ClassVar[str] = "IdentifiedOneElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.IdentifiedOneElementClass

    name: Union[str, IdentifiedOneElementClassName] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, IdentifiedOneElementClassName):
            self.name = IdentifiedOneElementClassName(self.name)

        super().__post_init__(**kwargs)


@dataclass
class IdentifiedTwoElementClass(YAMLRoot):
    """
    A identified class with an additional integer
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.IdentifiedTwoElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:IdentifiedTwoElementClass"
    class_name: ClassVar[str] = "IdentifiedTwoElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.IdentifiedTwoElementClass

    name: Union[str, IdentifiedTwoElementClassName] = None
    value: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, IdentifiedTwoElementClassName):
            self.name = IdentifiedTwoElementClassName(self.name)

        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        super().__post_init__(**kwargs)


@dataclass
class IdentifiedThreeElementClass(YAMLRoot):
    """
    A identified class with an additional integer and date
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = COMPLEX_RANGES.IdentifiedThreeElementClass
    class_class_curie: ClassVar[str] = "complex_ranges:IdentifiedThreeElementClass"
    class_name: ClassVar[str] = "IdentifiedThreeElementClass"
    class_model_uri: ClassVar[URIRef] = COMPLEX_RANGES.IdentifiedThreeElementClass

    name: Union[str, IdentifiedThreeElementClassName] = None
    value: Optional[int] = None
    modifier: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, IdentifiedThreeElementClassName):
            self.name = IdentifiedThreeElementClassName(self.name)

        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        if self.modifier is not None and not isinstance(self.modifier, XSDDate):
            self.modifier = XSDDate(self.modifier)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.oneElementClass__value = Slot(uri=COMPLEX_RANGES.value, name="oneElementClass__value", curie=COMPLEX_RANGES.curie('value'),
                   model_uri=COMPLEX_RANGES.oneElementClass__value, domain=None, range=Optional[int])

slots.twoElementClass__value1 = Slot(uri=COMPLEX_RANGES.value1, name="twoElementClass__value1", curie=COMPLEX_RANGES.curie('value1'),
                   model_uri=COMPLEX_RANGES.twoElementClass__value1, domain=None, range=Optional[str])

slots.twoElementClass__value2 = Slot(uri=COMPLEX_RANGES.value2, name="twoElementClass__value2", curie=COMPLEX_RANGES.curie('value2'),
                   model_uri=COMPLEX_RANGES.twoElementClass__value2, domain=None, range=Optional[str])

slots.threeElementClass__value1 = Slot(uri=COMPLEX_RANGES.value1, name="threeElementClass__value1", curie=COMPLEX_RANGES.curie('value1'),
                   model_uri=COMPLEX_RANGES.threeElementClass__value1, domain=None, range=Optional[float])

slots.threeElementClass__value2 = Slot(uri=COMPLEX_RANGES.value2, name="threeElementClass__value2", curie=COMPLEX_RANGES.curie('value2'),
                   model_uri=COMPLEX_RANGES.threeElementClass__value2, domain=None, range=Optional[float])

slots.threeElementClass__value3 = Slot(uri=COMPLEX_RANGES.value3, name="threeElementClass__value3", curie=COMPLEX_RANGES.curie('value3'),
                   model_uri=COMPLEX_RANGES.threeElementClass__value3, domain=None, range=Optional[float])

slots.keyedOneElementClass__name = Slot(uri=COMPLEX_RANGES.name, name="keyedOneElementClass__name", curie=COMPLEX_RANGES.curie('name'),
                   model_uri=COMPLEX_RANGES.keyedOneElementClass__name, domain=None, range=URIRef)

slots.keyedTwoElementClass__name = Slot(uri=COMPLEX_RANGES.name, name="keyedTwoElementClass__name", curie=COMPLEX_RANGES.curie('name'),
                   model_uri=COMPLEX_RANGES.keyedTwoElementClass__name, domain=None, range=URIRef)

slots.keyedTwoElementClass__value = Slot(uri=COMPLEX_RANGES.value, name="keyedTwoElementClass__value", curie=COMPLEX_RANGES.curie('value'),
                   model_uri=COMPLEX_RANGES.keyedTwoElementClass__value, domain=None, range=Optional[int])

slots.keyedThreeElementClass__name = Slot(uri=COMPLEX_RANGES.name, name="keyedThreeElementClass__name", curie=COMPLEX_RANGES.curie('name'),
                   model_uri=COMPLEX_RANGES.keyedThreeElementClass__name, domain=None, range=URIRef)

slots.keyedThreeElementClass__value = Slot(uri=COMPLEX_RANGES.value, name="keyedThreeElementClass__value", curie=COMPLEX_RANGES.curie('value'),
                   model_uri=COMPLEX_RANGES.keyedThreeElementClass__value, domain=None, range=Optional[int])

slots.keyedThreeElementClass__modifier = Slot(uri=COMPLEX_RANGES.modifier, name="keyedThreeElementClass__modifier", curie=COMPLEX_RANGES.curie('modifier'),
                   model_uri=COMPLEX_RANGES.keyedThreeElementClass__modifier, domain=None, range=Optional[Union[str, XSDDate]])

slots.identifiedOneElementClass__name = Slot(uri=COMPLEX_RANGES.name, name="identifiedOneElementClass__name", curie=COMPLEX_RANGES.curie('name'),
                   model_uri=COMPLEX_RANGES.identifiedOneElementClass__name, domain=None, range=URIRef)

slots.identifiedTwoElementClass__name = Slot(uri=COMPLEX_RANGES.name, name="identifiedTwoElementClass__name", curie=COMPLEX_RANGES.curie('name'),
                   model_uri=COMPLEX_RANGES.identifiedTwoElementClass__name, domain=None, range=URIRef)

slots.identifiedTwoElementClass__value = Slot(uri=COMPLEX_RANGES.value, name="identifiedTwoElementClass__value", curie=COMPLEX_RANGES.curie('value'),
                   model_uri=COMPLEX_RANGES.identifiedTwoElementClass__value, domain=None, range=Optional[int])

slots.identifiedThreeElementClass__name = Slot(uri=COMPLEX_RANGES.name, name="identifiedThreeElementClass__name", curie=COMPLEX_RANGES.curie('name'),
                   model_uri=COMPLEX_RANGES.identifiedThreeElementClass__name, domain=None, range=URIRef)

slots.identifiedThreeElementClass__value = Slot(uri=COMPLEX_RANGES.value, name="identifiedThreeElementClass__value", curie=COMPLEX_RANGES.curie('value'),
                   model_uri=COMPLEX_RANGES.identifiedThreeElementClass__value, domain=None, range=Optional[int])

slots.identifiedThreeElementClass__modifier = Slot(uri=COMPLEX_RANGES.modifier, name="identifiedThreeElementClass__modifier", curie=COMPLEX_RANGES.curie('modifier'),
                   model_uri=COMPLEX_RANGES.identifiedThreeElementClass__modifier, domain=None, range=Optional[Union[str, XSDDate]])