# Auto generated from issue_44.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-10-15 20:00
# Schema: test44
#
# id: https://example.com/test44
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
RDFS = CurieNamespace('rdfs', 'http://example.org/UNKNOWN/rdfs/')
SHEX = CurieNamespace('shex', 'http://www.w3.org/ns/shex#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CurieNamespace('', 'https://example.com/test44/')


# Types
class IriType(Uriorcurie):
    """ An IRI """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "iri type"
    type_model_uri = URIRef("https://example.com/test44/IriType")


class String(str):
    """ A character string """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("https://example.com/test44/String")


class Integer(int):
    """ An integer """
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "integer"
    type_model_uri = URIRef("https://example.com/test44/Integer")


class Boolean(Bool):
    """ A binary (true or false) value """
    type_class_uri = XSD.boolean
    type_class_curie = "xsd:boolean"
    type_name = "boolean"
    type_model_uri = URIRef("https://example.com/test44/Boolean")


class Float(float):
    """ A real number that conforms to the xsd:float specification """
    type_class_uri = XSD.float
    type_class_curie = "xsd:float"
    type_name = "float"
    type_model_uri = URIRef("https://example.com/test44/Float")


class Double(float):
    """ A real number that conforms to the xsd:double specification """
    type_class_uri = XSD.double
    type_class_curie = "xsd:double"
    type_name = "double"
    type_model_uri = URIRef("https://example.com/test44/Double")


class Decimal(Decimal):
    """ A real number with arbitrary precision that conforms to the xsd:decimal specification """
    type_class_uri = XSD.decimal
    type_class_curie = "xsd:decimal"
    type_name = "decimal"
    type_model_uri = URIRef("https://example.com/test44/Decimal")


class Time(XSDTime):
    """ A time object represents a (local) time of day, independent of any particular day """
    type_class_uri = XSD.dateTime
    type_class_curie = "xsd:dateTime"
    type_name = "time"
    type_model_uri = URIRef("https://example.com/test44/Time")


class Date(XSDDate):
    """ a date (year, month and day) in an idealized calendar """
    type_class_uri = XSD.date
    type_class_curie = "xsd:date"
    type_name = "date"
    type_model_uri = URIRef("https://example.com/test44/Date")


class Datetime(XSDDateTime):
    """ The combination of a date and time """
    type_class_uri = XSD.dateTime
    type_class_curie = "xsd:dateTime"
    type_name = "datetime"
    type_model_uri = URIRef("https://example.com/test44/Datetime")


class Uriorcurie(URIorCURIE):
    """ a URI or a CURIE """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "uriorcurie"
    type_model_uri = URIRef("https://example.com/test44/Uriorcurie")


class Uri(URI):
    """ a complete URI """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "uri"
    type_model_uri = URIRef("https://example.com/test44/Uri")


class Ncname(NCName):
    """ Prefix part of CURIE """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "ncname"
    type_model_uri = URIRef("https://example.com/test44/Ncname")


class Objectidentifier(ElementIdentifier):
    """ A URI or CURIE that represents an object in the model. """
    type_class_uri = SHEX.iri
    type_class_curie = "shex:iri"
    type_name = "objectidentifier"
    type_model_uri = URIRef("https://example.com/test44/Objectidentifier")


class Nodeidentifier(NodeIdentifier):
    """ A URI, CURIE or BNODE that represents a node in a model. """
    type_class_uri = SHEX.nonLiteral
    type_class_curie = "shex:nonLiteral"
    type_name = "nodeidentifier"
    type_model_uri = URIRef("https://example.com/test44/Nodeidentifier")


# Class references



@dataclass
class NamedThing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.com/test44/NamedThing")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "named thing"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.com/test44/NamedThing")

    category: Union[Union[str, IriType], List[Union[str, IriType]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        if not isinstance(self.category, list):
            self.category = [self.category] if self.category is not None else []
        self.category = [v if isinstance(v, IriType) else IriType(v) for v in self.category]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.category = Slot(uri=RDFS.subClassOf, name="category", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.category, domain=NamedThing, range=Union[Union[str, IriType], List[Union[str, IriType]]])