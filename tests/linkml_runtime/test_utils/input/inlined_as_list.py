# Auto generated from inlined_as_dict.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-05-02 14:54
# Schema: inlined_as_dict
#
# id: https://example.org/inlined_as_dict
# description: Test schema for inlined_as_dict
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.metamodelcore import empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace


metamodel_version = "1.7.0"

# Namespaces
EX = CurieNamespace('ex', 'https://example.org/inlined_as_dict#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = EX


# Types
class String(str):
    """ A character string """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = EX.String


class Integer(int):
    """ An integer """
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "integer"
    type_model_uri = EX.Integer


# Class references
class EInstS1(extended_str):
    pass


@dataclass
class EInst(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.EInst
    class_class_curie: ClassVar[str] = "ex:EInst"
    class_name: ClassVar[str] = "EInst"
    class_model_uri: ClassVar[URIRef] = EX.EInst

    s1: Union[str, EInstS1] = None
    s2: Optional[str] = None
    s3: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.s1 is None:
            raise ValueError("s1 must be supplied")
        if not isinstance(self.s1, EInstS1):
            self.s1 = EInstS1(self.s1)

        if self.s2 is not None and not isinstance(self.s2, str):
            self.s2 = str(self.s2)

        if self.s3 is not None and not isinstance(self.s3, str):
            self.s3 = str(self.s3)

        super().__post_init__(**kwargs)


@dataclass
class E(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.E
    class_class_curie: ClassVar[str] = "ex:E"
    class_name: ClassVar[str] = "E"
    class_model_uri: ClassVar[URIRef] = EX.E

    ev: Optional[Union[dict[Union[str, EInstS1], Union[dict, EInst]], list[Union[dict, EInst]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="ev", slot_type=EInst, key_name="s1", keyed=True)
        super().__post_init__(**kwargs)


# Enumerations


# Slots

