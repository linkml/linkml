# Auto generated from issue_134.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: example1
#
# id: http://example.org/sample/example1
# description:
# license:

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


metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
XSD = CurieNamespace('xsd', 'http://example.org/UNKNOWN/xsd/')
DEFAULT_ = CurieNamespace('', 'http://example.org/sample/example1/')


# Types
class String(str):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("http://example.org/sample/example1/String")


# Class references
class AId(extended_str):
    pass


class BId(AId):
    pass


class CId(BId):
    pass


class D1Id(CId):
    pass


class D2Id(CId):
    pass


class EId(D1Id):
    pass


@dataclass
class A(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/A")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "a"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/A")

    id: Union[str, AId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AId):
            self.id = AId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class B(A):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/B")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "b"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/B")

    id: Union[str, BId] = None
    has_a: Optional[Union[str, AId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BId):
            self.id = BId(self.id)

        if self.has_a is not None and not isinstance(self.has_a, AId):
            self.has_a = AId(self.has_a)

        super().__post_init__(**kwargs)


@dataclass
class C(B):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/C")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "c"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/C")

    id: Union[str, CId] = None
    has_b: Optional[Union[str, BId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CId):
            self.id = CId(self.id)

        if self.has_b is not None and not isinstance(self.has_b, BId):
            self.has_b = BId(self.has_b)

        super().__post_init__(**kwargs)


@dataclass
class D1(C):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/D1")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "d1"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/D1")

    id: Union[str, D1Id] = None
    has_c: Optional[Union[str, CId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, D1Id):
            self.id = D1Id(self.id)

        if self.has_c is not None and not isinstance(self.has_c, CId):
            self.has_c = CId(self.has_c)

        super().__post_init__(**kwargs)


@dataclass
class D2(C):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/D2")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "d2"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/D2")

    id: Union[str, D2Id] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, D2Id):
            self.id = D2Id(self.id)

        super().__post_init__(**kwargs)


@dataclass
class E(D1):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/E")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "e"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/example1/E")

    id: Union[str, EId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EId):
            self.id = EId(self.id)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.has_a = Slot(uri=DEFAULT_.has_a, name="has a", curie=DEFAULT_.curie('has_a'),
                   model_uri=DEFAULT_.has_a, domain=None, range=Optional[Union[str, AId]])

slots.has_b = Slot(uri=DEFAULT_.has_b, name="has b", curie=DEFAULT_.curie('has_b'),
                   model_uri=DEFAULT_.has_b, domain=None, range=Optional[Union[str, BId]])

slots.has_c = Slot(uri=DEFAULT_.has_c, name="has c", curie=DEFAULT_.curie('has_c'),
                   model_uri=DEFAULT_.has_c, domain=None, range=Optional[Union[str, CId]])