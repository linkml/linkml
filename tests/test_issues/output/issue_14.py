# Auto generated from issue_14.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: test14
#
# id: https://example.com/test14
# description:
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
from linkml_runtime.utils.metamodelcore import Bool, Decimal, ElementIdentifier, NCName, NodeIdentifier, URI, URIorCURIE, XSDDate, XSDDateTime, XSDTime

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
META = CurieNamespace('meta', 'https://w3id.org/linkml/')
SHEX = CurieNamespace('shex', 'http://www.w3.org/ns/shex#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CurieNamespace('', 'https://example.com/test14/')


# Types
class String(str):
    """ A character string """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("https://example.com/test14/String")


class Integer(int):
    """ An integer """
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "integer"
    type_model_uri = URIRef("https://example.com/test14/Integer")


class Boolean(Bool):
    """ A binary (true or false) value """
    type_class_uri = XSD.boolean
    type_class_curie = "xsd:boolean"
    type_name = "boolean"
    type_model_uri = URIRef("https://example.com/test14/Boolean")


class Float(float):
    """ A real number that conforms to the xsd:float specification """
    type_class_uri = XSD.float
    type_class_curie = "xsd:float"
    type_name = "float"
    type_model_uri = URIRef("https://example.com/test14/Float")


class Double(float):
    """ A real number that conforms to the xsd:double specification """
    type_class_uri = XSD.double
    type_class_curie = "xsd:double"
    type_name = "double"
    type_model_uri = URIRef("https://example.com/test14/Double")


class Decimal(Decimal):
    """ A real number with arbitrary precision that conforms to the xsd:decimal specification """
    type_class_uri = XSD.decimal
    type_class_curie = "xsd:decimal"
    type_name = "decimal"
    type_model_uri = URIRef("https://example.com/test14/Decimal")


class Time(XSDTime):
    """ A time object represents a (local) time of day, independent of any particular day """
    type_class_uri = XSD.dateTime
    type_class_curie = "xsd:dateTime"
    type_name = "time"
    type_model_uri = URIRef("https://example.com/test14/Time")


class Date(XSDDate):
    """ a date (year, month and day) in an idealized calendar """
    type_class_uri = XSD.date
    type_class_curie = "xsd:date"
    type_name = "date"
    type_model_uri = URIRef("https://example.com/test14/Date")


class Datetime(XSDDateTime):
    """ The combination of a date and time """
    type_class_uri = XSD.dateTime
    type_class_curie = "xsd:dateTime"
    type_name = "datetime"
    type_model_uri = URIRef("https://example.com/test14/Datetime")


class Uriorcurie(URIorCURIE):
    """ a URI or a CURIE """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "uriorcurie"
    type_model_uri = URIRef("https://example.com/test14/Uriorcurie")


class Uri(URI):
    """ a complete URI """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "uri"
    type_model_uri = URIRef("https://example.com/test14/Uri")


class Ncname(NCName):
    """ Prefix part of CURIE """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "ncname"
    type_model_uri = URIRef("https://example.com/test14/Ncname")


class Objectidentifier(ElementIdentifier):
    """ A URI or CURIE that represents an object in the model. """
    type_class_uri = SHEX.iri
    type_class_curie = "shex:iri"
    type_name = "objectidentifier"
    type_model_uri = URIRef("https://example.com/test14/Objectidentifier")


class Nodeidentifier(NodeIdentifier):
    """ A URI, CURIE or BNODE that represents a node in a model. """
    type_class_uri = SHEX.nonLiteral
    type_class_curie = "shex:nonLiteral"
    type_name = "nodeidentifier"
    type_model_uri = URIRef("https://example.com/test14/Nodeidentifier")


# Class references
class NamedThingId(extended_str):
    pass


class MixinOwnerId(NamedThingId):
    pass


class SubjectRange1Id(NamedThingId):
    pass


class ObjectRange1Id(NamedThingId):
    pass


@dataclass
class NamedThing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/NamedThing")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "named thing"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/NamedThing")

    id: Union[str, NamedThingId] = None
    name: str = None
    subject: Union[str, NamedThingId] = None
    object: Union[str, NamedThingId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, NamedThingId):
            self.subject = NamedThingId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, NamedThingId):
            self.object = NamedThingId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class MixinOwner(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/MixinOwner")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "mixin_owner"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/MixinOwner")

    id: Union[str, MixinOwnerId] = None
    name: str = None
    object: Union[str, NamedThingId] = None
    subject: Union[str, SubjectRange1Id] = None
    sex_qualifier: Optional[Union[str, NamedThingId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MixinOwnerId):
            self.id = MixinOwnerId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, SubjectRange1Id):
            self.subject = SubjectRange1Id(self.subject)

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, NamedThingId):
            self.sex_qualifier = NamedThingId(self.sex_qualifier)

        super().__post_init__(**kwargs)


@dataclass
class SubjectRange1(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/SubjectRange1")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "subject_range_1"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/SubjectRange1")

    id: Union[str, SubjectRange1Id] = None
    name: str = None
    subject: Union[str, NamedThingId] = None
    object: Union[str, NamedThingId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SubjectRange1Id):
            self.id = SubjectRange1Id(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ObjectRange1(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/ObjectRange1")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "object_range_1"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/ObjectRange1")

    id: Union[str, ObjectRange1Id] = None
    name: str = None
    subject: Union[str, NamedThingId] = None
    object: Union[str, NamedThingId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObjectRange1Id):
            self.id = ObjectRange1Id(self.id)

        super().__post_init__(**kwargs)


@dataclass
class MixinClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/MixinClass")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "mixin_class"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.com/test14/MixinClass")

    object: Union[str, ObjectRange1Id] = None
    sex_qualifier: Optional[Union[str, NamedThingId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, ObjectRange1Id):
            self.object = ObjectRange1Id(self.object)

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, NamedThingId):
            self.sex_qualifier = NamedThingId(self.sex_qualifier)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.id, domain=NamedThing, range=Union[str, NamedThingId])

slots.name = Slot(uri=DEFAULT_.name, name="name", curie=DEFAULT_.curie('name'),
                   model_uri=DEFAULT_.name, domain=NamedThing, range=str)

slots.subject = Slot(uri=DEFAULT_.subject, name="subject", curie=DEFAULT_.curie('subject'),
                   model_uri=DEFAULT_.subject, domain=None, range=Union[str, NamedThingId])

slots.object = Slot(uri=DEFAULT_.object, name="object", curie=DEFAULT_.curie('object'),
                   model_uri=DEFAULT_.object, domain=None, range=Union[str, NamedThingId])

slots.sex_qualifier = Slot(uri=DEFAULT_.sex_qualifier, name="sex qualifier", curie=DEFAULT_.curie('sex_qualifier'),
                   model_uri=DEFAULT_.sex_qualifier, domain=None, range=Optional[Union[str, NamedThingId]])

slots.mixin_owner_subject = Slot(uri=DEFAULT_.subject, name="mixin_owner_subject", curie=DEFAULT_.curie('subject'),
                   model_uri=DEFAULT_.mixin_owner_subject, domain=MixinOwner, range=Union[str, SubjectRange1Id])

slots.mixin_class_object = Slot(uri=DEFAULT_.object, name="mixin_class_object", curie=DEFAULT_.curie('object'),
                   model_uri=DEFAULT_.mixin_class_object, domain=MixinClass, range=Union[str, ObjectRange1Id])