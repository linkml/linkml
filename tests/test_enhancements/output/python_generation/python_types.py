# Auto generated from python_types.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: ptypes
#
# id: http://examples.org/linkml/test/ptypes
# description: Test of python types generation
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
from linkml_runtime.linkml_model.types import Boolean, Date, Datetime, Double, Float, Integer, Ncname, Nodeidentifier, Objectidentifier, String, Time, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, ElementIdentifier, NCName, NodeIdentifier, URI, URIorCURIE, XSDDate, XSDDateTime, XSDTime

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PTYPES = CurieNamespace('ptypes', 'http://examples.org/linkml/ptypes')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = PTYPES


# Types
class InheritedType(Integer):
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "InheritedType"
    type_model_uri = PTYPES.InheritedType


class InheritedType2(Uriorcurie):
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "InheritedType2"
    type_model_uri = PTYPES.InheritedType2


class InheritedType3(InheritedType2):
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "InheritedType3"
    type_model_uri = PTYPES.InheritedType3


# Class references
class KeyedElementName(extended_str):
    pass


class IdentifiedElementId(URIorCURIE):
    pass


@dataclass
class Strings(YAMLRoot):
    """
    various permutations of the string type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.Strings
    class_class_curie: ClassVar[str] = "ptypes:Strings"
    class_name: ClassVar[str] = "Strings"
    class_model_uri: ClassVar[URIRef] = PTYPES.Strings

    mand_string: str = None
    mand_multi_string: Union[str, List[str]] = None
    opt_string: Optional[str] = None
    opt_multi_string: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_string):
            self.MissingRequiredField("mand_string")
        if not isinstance(self.mand_string, str):
            self.mand_string = str(self.mand_string)

        if self._is_empty(self.mand_multi_string):
            self.MissingRequiredField("mand_multi_string")
        if not isinstance(self.mand_multi_string, list):
            self.mand_multi_string = [self.mand_multi_string] if self.mand_multi_string is not None else []
        self.mand_multi_string = [v if isinstance(v, str) else str(v) for v in self.mand_multi_string]

        if self.opt_string is not None and not isinstance(self.opt_string, str):
            self.opt_string = str(self.opt_string)

        if not isinstance(self.opt_multi_string, list):
            self.opt_multi_string = [self.opt_multi_string] if self.opt_multi_string is not None else []
        self.opt_multi_string = [v if isinstance(v, str) else str(v) for v in self.opt_multi_string]

        super().__post_init__(**kwargs)


@dataclass
class InheritedStrings1(Strings):
    """
    Inherited class with no changes from base
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.InheritedStrings1
    class_class_curie: ClassVar[str] = "ptypes:InheritedStrings1"
    class_name: ClassVar[str] = "InheritedStrings1"
    class_model_uri: ClassVar[URIRef] = PTYPES.InheritedStrings1

    mand_string: str = None
    mand_multi_string: Union[str, List[str]] = None

@dataclass
class InheritedStrings2(Strings):
    """
    Inherited class with base change
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.InheritedStrings2
    class_class_curie: ClassVar[str] = "ptypes:InheritedStrings2"
    class_name: ClassVar[str] = "InheritedStrings2"
    class_model_uri: ClassVar[URIRef] = PTYPES.InheritedStrings2

    mand_string: str = None
    mand_multi_string: Union[str, List[str]] = None
    req_second_string: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.req_second_string is not None and not isinstance(self.req_second_string, str):
            self.req_second_string = str(self.req_second_string)

        super().__post_init__(**kwargs)


@dataclass
class Integers(YAMLRoot):
    """
    various permutations of the integer type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.Integers
    class_class_curie: ClassVar[str] = "ptypes:Integers"
    class_name: ClassVar[str] = "Integers"
    class_model_uri: ClassVar[URIRef] = PTYPES.Integers

    mand_integer: int = None
    mand_multi_integer: Union[int, List[int]] = None
    opt_integer: Optional[int] = None
    opt_multi_integer: Optional[Union[int, List[int]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_integer):
            self.MissingRequiredField("mand_integer")
        if not isinstance(self.mand_integer, int):
            self.mand_integer = int(self.mand_integer)

        if self._is_empty(self.mand_multi_integer):
            self.MissingRequiredField("mand_multi_integer")
        if not isinstance(self.mand_multi_integer, list):
            self.mand_multi_integer = [self.mand_multi_integer] if self.mand_multi_integer is not None else []
        self.mand_multi_integer = [v if isinstance(v, int) else int(v) for v in self.mand_multi_integer]

        if self.opt_integer is not None and not isinstance(self.opt_integer, int):
            self.opt_integer = int(self.opt_integer)

        if not isinstance(self.opt_multi_integer, list):
            self.opt_multi_integer = [self.opt_multi_integer] if self.opt_multi_integer is not None else []
        self.opt_multi_integer = [v if isinstance(v, int) else int(v) for v in self.opt_multi_integer]

        super().__post_init__(**kwargs)


@dataclass
class Booleans(YAMLRoot):
    """
    various permutations of the boolean type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.Booleans
    class_class_curie: ClassVar[str] = "ptypes:Booleans"
    class_name: ClassVar[str] = "Booleans"
    class_model_uri: ClassVar[URIRef] = PTYPES.Booleans

    mand_boolean: Union[bool, Bool] = None
    mand_multi_boolean: Union[Union[bool, Bool], List[Union[bool, Bool]]] = None
    opt_boolean: Optional[Union[bool, Bool]] = None
    opt_multi_boolean: Optional[Union[Union[bool, Bool], List[Union[bool, Bool]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_boolean):
            self.MissingRequiredField("mand_boolean")
        if not isinstance(self.mand_boolean, Bool):
            self.mand_boolean = Bool(self.mand_boolean)

        if self._is_empty(self.mand_multi_boolean):
            self.MissingRequiredField("mand_multi_boolean")
        if not isinstance(self.mand_multi_boolean, list):
            self.mand_multi_boolean = [self.mand_multi_boolean] if self.mand_multi_boolean is not None else []
        self.mand_multi_boolean = [v if isinstance(v, Bool) else Bool(v) for v in self.mand_multi_boolean]

        if self.opt_boolean is not None and not isinstance(self.opt_boolean, Bool):
            self.opt_boolean = Bool(self.opt_boolean)

        if not isinstance(self.opt_multi_boolean, list):
            self.opt_multi_boolean = [self.opt_multi_boolean] if self.opt_multi_boolean is not None else []
        self.opt_multi_boolean = [v if isinstance(v, Bool) else Bool(v) for v in self.opt_multi_boolean]

        super().__post_init__(**kwargs)


@dataclass
class Floats(YAMLRoot):
    """
    various permutations of the float type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.Floats
    class_class_curie: ClassVar[str] = "ptypes:Floats"
    class_name: ClassVar[str] = "Floats"
    class_model_uri: ClassVar[URIRef] = PTYPES.Floats

    mand_float: float = None
    mand_multi_float: Union[float, List[float]] = None
    opt_float: Optional[float] = None
    opt_multi_float: Optional[Union[float, List[float]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_float):
            self.MissingRequiredField("mand_float")
        if not isinstance(self.mand_float, float):
            self.mand_float = float(self.mand_float)

        if self._is_empty(self.mand_multi_float):
            self.MissingRequiredField("mand_multi_float")
        if not isinstance(self.mand_multi_float, list):
            self.mand_multi_float = [self.mand_multi_float] if self.mand_multi_float is not None else []
        self.mand_multi_float = [v if isinstance(v, float) else float(v) for v in self.mand_multi_float]

        if self.opt_float is not None and not isinstance(self.opt_float, float):
            self.opt_float = float(self.opt_float)

        if not isinstance(self.opt_multi_float, list):
            self.opt_multi_float = [self.opt_multi_float] if self.opt_multi_float is not None else []
        self.opt_multi_float = [v if isinstance(v, float) else float(v) for v in self.opt_multi_float]

        super().__post_init__(**kwargs)


@dataclass
class Doubles(YAMLRoot):
    """
    various permutations of the double type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.Doubles
    class_class_curie: ClassVar[str] = "ptypes:Doubles"
    class_name: ClassVar[str] = "Doubles"
    class_model_uri: ClassVar[URIRef] = PTYPES.Doubles

    mand_double: float = None
    mand_multi_double: Union[float, List[float]] = None
    opt_double: Optional[float] = None
    opt_multi_double: Optional[Union[float, List[float]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_double):
            self.MissingRequiredField("mand_double")
        if not isinstance(self.mand_double, float):
            self.mand_double = float(self.mand_double)

        if self._is_empty(self.mand_multi_double):
            self.MissingRequiredField("mand_multi_double")
        if not isinstance(self.mand_multi_double, list):
            self.mand_multi_double = [self.mand_multi_double] if self.mand_multi_double is not None else []
        self.mand_multi_double = [v if isinstance(v, float) else float(v) for v in self.mand_multi_double]

        if self.opt_double is not None and not isinstance(self.opt_double, float):
            self.opt_double = float(self.opt_double)

        if not isinstance(self.opt_multi_double, list):
            self.opt_multi_double = [self.opt_multi_double] if self.opt_multi_double is not None else []
        self.opt_multi_double = [v if isinstance(v, float) else float(v) for v in self.opt_multi_double]

        super().__post_init__(**kwargs)


@dataclass
class Times(YAMLRoot):
    """
    various permutations of the time type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.Times
    class_class_curie: ClassVar[str] = "ptypes:Times"
    class_name: ClassVar[str] = "Times"
    class_model_uri: ClassVar[URIRef] = PTYPES.Times

    mand_time: Union[str, XSDTime] = None
    mand_multi_time: Union[Union[str, XSDTime], List[Union[str, XSDTime]]] = None
    opt_time: Optional[Union[str, XSDTime]] = None
    opt_multi_time: Optional[Union[Union[str, XSDTime], List[Union[str, XSDTime]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_time):
            self.MissingRequiredField("mand_time")
        if not isinstance(self.mand_time, XSDTime):
            self.mand_time = XSDTime(self.mand_time)

        if self._is_empty(self.mand_multi_time):
            self.MissingRequiredField("mand_multi_time")
        if not isinstance(self.mand_multi_time, list):
            self.mand_multi_time = [self.mand_multi_time] if self.mand_multi_time is not None else []
        self.mand_multi_time = [v if isinstance(v, XSDTime) else XSDTime(v) for v in self.mand_multi_time]

        if self.opt_time is not None and not isinstance(self.opt_time, XSDTime):
            self.opt_time = XSDTime(self.opt_time)

        if not isinstance(self.opt_multi_time, list):
            self.opt_multi_time = [self.opt_multi_time] if self.opt_multi_time is not None else []
        self.opt_multi_time = [v if isinstance(v, XSDTime) else XSDTime(v) for v in self.opt_multi_time]

        super().__post_init__(**kwargs)


@dataclass
class Dates(YAMLRoot):
    """
    various permutations of the date type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.Dates
    class_class_curie: ClassVar[str] = "ptypes:Dates"
    class_name: ClassVar[str] = "Dates"
    class_model_uri: ClassVar[URIRef] = PTYPES.Dates

    mand_date: Union[str, XSDDate] = None
    mand_multi_date: Union[Union[str, XSDDate], List[Union[str, XSDDate]]] = None
    opt_date: Optional[Union[str, XSDDate]] = None
    opt_multi_date: Optional[Union[Union[str, XSDDate], List[Union[str, XSDDate]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_date):
            self.MissingRequiredField("mand_date")
        if not isinstance(self.mand_date, XSDDate):
            self.mand_date = XSDDate(self.mand_date)

        if self._is_empty(self.mand_multi_date):
            self.MissingRequiredField("mand_multi_date")
        if not isinstance(self.mand_multi_date, list):
            self.mand_multi_date = [self.mand_multi_date] if self.mand_multi_date is not None else []
        self.mand_multi_date = [v if isinstance(v, XSDDate) else XSDDate(v) for v in self.mand_multi_date]

        if self.opt_date is not None and not isinstance(self.opt_date, XSDDate):
            self.opt_date = XSDDate(self.opt_date)

        if not isinstance(self.opt_multi_date, list):
            self.opt_multi_date = [self.opt_multi_date] if self.opt_multi_date is not None else []
        self.opt_multi_date = [v if isinstance(v, XSDDate) else XSDDate(v) for v in self.opt_multi_date]

        super().__post_init__(**kwargs)


@dataclass
class DateTimes(YAMLRoot):
    """
    various permutations of the datetime type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.DateTimes
    class_class_curie: ClassVar[str] = "ptypes:DateTimes"
    class_name: ClassVar[str] = "DateTimes"
    class_model_uri: ClassVar[URIRef] = PTYPES.DateTimes

    mand_datetime: Union[str, XSDDateTime] = None
    mand_multi_datetime: Union[Union[str, XSDDateTime], List[Union[str, XSDDateTime]]] = None
    opt_datetime: Optional[Union[str, XSDDateTime]] = None
    opt_multi_datetime: Optional[Union[Union[str, XSDDateTime], List[Union[str, XSDDateTime]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_datetime):
            self.MissingRequiredField("mand_datetime")
        if not isinstance(self.mand_datetime, XSDDateTime):
            self.mand_datetime = XSDDateTime(self.mand_datetime)

        if self._is_empty(self.mand_multi_datetime):
            self.MissingRequiredField("mand_multi_datetime")
        if not isinstance(self.mand_multi_datetime, list):
            self.mand_multi_datetime = [self.mand_multi_datetime] if self.mand_multi_datetime is not None else []
        self.mand_multi_datetime = [v if isinstance(v, XSDDateTime) else XSDDateTime(v) for v in self.mand_multi_datetime]

        if self.opt_datetime is not None and not isinstance(self.opt_datetime, XSDDateTime):
            self.opt_datetime = XSDDateTime(self.opt_datetime)

        if not isinstance(self.opt_multi_datetime, list):
            self.opt_multi_datetime = [self.opt_multi_datetime] if self.opt_multi_datetime is not None else []
        self.opt_multi_datetime = [v if isinstance(v, XSDDateTime) else XSDDateTime(v) for v in self.opt_multi_datetime]

        super().__post_init__(**kwargs)


@dataclass
class URIorCURIEs(YAMLRoot):
    """
    various permutations of the uriorcurie type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.URIorCURIEs
    class_class_curie: ClassVar[str] = "ptypes:URIorCURIEs"
    class_name: ClassVar[str] = "URIorCURIEs"
    class_model_uri: ClassVar[URIRef] = PTYPES.URIorCURIEs

    mand_uriorcurie: Union[str, URIorCURIE] = None
    mand_multi_uriorcurie: Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]] = None
    opt_uriorcurie: Optional[Union[str, URIorCURIE]] = None
    opt_multi_uriorcurie: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_uriorcurie):
            self.MissingRequiredField("mand_uriorcurie")
        if not isinstance(self.mand_uriorcurie, URIorCURIE):
            self.mand_uriorcurie = URIorCURIE(self.mand_uriorcurie)

        if self._is_empty(self.mand_multi_uriorcurie):
            self.MissingRequiredField("mand_multi_uriorcurie")
        if not isinstance(self.mand_multi_uriorcurie, list):
            self.mand_multi_uriorcurie = [self.mand_multi_uriorcurie] if self.mand_multi_uriorcurie is not None else []
        self.mand_multi_uriorcurie = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.mand_multi_uriorcurie]

        if self.opt_uriorcurie is not None and not isinstance(self.opt_uriorcurie, URIorCURIE):
            self.opt_uriorcurie = URIorCURIE(self.opt_uriorcurie)

        if not isinstance(self.opt_multi_uriorcurie, list):
            self.opt_multi_uriorcurie = [self.opt_multi_uriorcurie] if self.opt_multi_uriorcurie is not None else []
        self.opt_multi_uriorcurie = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.opt_multi_uriorcurie]

        super().__post_init__(**kwargs)


@dataclass
class URIs(YAMLRoot):
    """
    various permutations of the uri type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.URIs
    class_class_curie: ClassVar[str] = "ptypes:URIs"
    class_name: ClassVar[str] = "URIs"
    class_model_uri: ClassVar[URIRef] = PTYPES.URIs

    mand_uri: Union[str, URI] = None
    mand_multi_uri: Union[Union[str, URI], List[Union[str, URI]]] = None
    opt_uri: Optional[Union[str, URI]] = None
    opt_multi_uri: Optional[Union[Union[str, URI], List[Union[str, URI]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_uri):
            self.MissingRequiredField("mand_uri")
        if not isinstance(self.mand_uri, URI):
            self.mand_uri = URI(self.mand_uri)

        if self._is_empty(self.mand_multi_uri):
            self.MissingRequiredField("mand_multi_uri")
        if not isinstance(self.mand_multi_uri, list):
            self.mand_multi_uri = [self.mand_multi_uri] if self.mand_multi_uri is not None else []
        self.mand_multi_uri = [v if isinstance(v, URI) else URI(v) for v in self.mand_multi_uri]

        if self.opt_uri is not None and not isinstance(self.opt_uri, URI):
            self.opt_uri = URI(self.opt_uri)

        if not isinstance(self.opt_multi_uri, list):
            self.opt_multi_uri = [self.opt_multi_uri] if self.opt_multi_uri is not None else []
        self.opt_multi_uri = [v if isinstance(v, URI) else URI(v) for v in self.opt_multi_uri]

        super().__post_init__(**kwargs)


@dataclass
class NCNames(YAMLRoot):
    """
    various permutations of the ncname type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.NCNames
    class_class_curie: ClassVar[str] = "ptypes:NCNames"
    class_name: ClassVar[str] = "NCNames"
    class_model_uri: ClassVar[URIRef] = PTYPES.NCNames

    mand_ncname: Union[str, NCName] = None
    mand_multi_ncname: Union[Union[str, NCName], List[Union[str, NCName]]] = None
    opt_ncname: Optional[Union[str, NCName]] = None
    opt_multi_ncname: Optional[Union[Union[str, NCName], List[Union[str, NCName]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_ncname):
            self.MissingRequiredField("mand_ncname")
        if not isinstance(self.mand_ncname, NCName):
            self.mand_ncname = NCName(self.mand_ncname)

        if self._is_empty(self.mand_multi_ncname):
            self.MissingRequiredField("mand_multi_ncname")
        if not isinstance(self.mand_multi_ncname, list):
            self.mand_multi_ncname = [self.mand_multi_ncname] if self.mand_multi_ncname is not None else []
        self.mand_multi_ncname = [v if isinstance(v, NCName) else NCName(v) for v in self.mand_multi_ncname]

        if self.opt_ncname is not None and not isinstance(self.opt_ncname, NCName):
            self.opt_ncname = NCName(self.opt_ncname)

        if not isinstance(self.opt_multi_ncname, list):
            self.opt_multi_ncname = [self.opt_multi_ncname] if self.opt_multi_ncname is not None else []
        self.opt_multi_ncname = [v if isinstance(v, NCName) else NCName(v) for v in self.opt_multi_ncname]

        super().__post_init__(**kwargs)


@dataclass
class ObjectIdentifiers(YAMLRoot):
    """
    various permutations of the objectidentifier type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.ObjectIdentifiers
    class_class_curie: ClassVar[str] = "ptypes:ObjectIdentifiers"
    class_name: ClassVar[str] = "ObjectIdentifiers"
    class_model_uri: ClassVar[URIRef] = PTYPES.ObjectIdentifiers

    mand_objectidentifier: Union[str, ElementIdentifier] = None
    mand_multi_objectidentifier: Union[Union[str, ElementIdentifier], List[Union[str, ElementIdentifier]]] = None
    opt_objectidentifier: Optional[Union[str, ElementIdentifier]] = None
    opt_multi_objectidentifier: Optional[Union[Union[str, ElementIdentifier], List[Union[str, ElementIdentifier]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_objectidentifier):
            self.MissingRequiredField("mand_objectidentifier")
        if not isinstance(self.mand_objectidentifier, ElementIdentifier):
            self.mand_objectidentifier = ElementIdentifier(self.mand_objectidentifier)

        if self._is_empty(self.mand_multi_objectidentifier):
            self.MissingRequiredField("mand_multi_objectidentifier")
        if not isinstance(self.mand_multi_objectidentifier, list):
            self.mand_multi_objectidentifier = [self.mand_multi_objectidentifier] if self.mand_multi_objectidentifier is not None else []
        self.mand_multi_objectidentifier = [v if isinstance(v, ElementIdentifier) else ElementIdentifier(v) for v in self.mand_multi_objectidentifier]

        if self.opt_objectidentifier is not None and not isinstance(self.opt_objectidentifier, ElementIdentifier):
            self.opt_objectidentifier = ElementIdentifier(self.opt_objectidentifier)

        if not isinstance(self.opt_multi_objectidentifier, list):
            self.opt_multi_objectidentifier = [self.opt_multi_objectidentifier] if self.opt_multi_objectidentifier is not None else []
        self.opt_multi_objectidentifier = [v if isinstance(v, ElementIdentifier) else ElementIdentifier(v) for v in self.opt_multi_objectidentifier]

        super().__post_init__(**kwargs)


@dataclass
class NodeIdentifiers(YAMLRoot):
    """
    various permutations of the nodeidentifier type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.NodeIdentifiers
    class_class_curie: ClassVar[str] = "ptypes:NodeIdentifiers"
    class_name: ClassVar[str] = "NodeIdentifiers"
    class_model_uri: ClassVar[URIRef] = PTYPES.NodeIdentifiers

    mand_nodeidentifier: Union[str, NodeIdentifier] = None
    mand_multi_nodeidentifier: Union[Union[str, NodeIdentifier], List[Union[str, NodeIdentifier]]] = None
    opt_nodeidentifier: Optional[Union[str, NodeIdentifier]] = None
    opt_multi_nodeidentifier: Optional[Union[Union[str, NodeIdentifier], List[Union[str, NodeIdentifier]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_nodeidentifier):
            self.MissingRequiredField("mand_nodeidentifier")
        if not isinstance(self.mand_nodeidentifier, NodeIdentifier):
            self.mand_nodeidentifier = NodeIdentifier(self.mand_nodeidentifier)

        if self._is_empty(self.mand_multi_nodeidentifier):
            self.MissingRequiredField("mand_multi_nodeidentifier")
        if not isinstance(self.mand_multi_nodeidentifier, list):
            self.mand_multi_nodeidentifier = [self.mand_multi_nodeidentifier] if self.mand_multi_nodeidentifier is not None else []
        self.mand_multi_nodeidentifier = [v if isinstance(v, NodeIdentifier) else NodeIdentifier(v) for v in self.mand_multi_nodeidentifier]

        if self.opt_nodeidentifier is not None and not isinstance(self.opt_nodeidentifier, NodeIdentifier):
            self.opt_nodeidentifier = NodeIdentifier(self.opt_nodeidentifier)

        if not isinstance(self.opt_multi_nodeidentifier, list):
            self.opt_multi_nodeidentifier = [self.opt_multi_nodeidentifier] if self.opt_multi_nodeidentifier is not None else []
        self.opt_multi_nodeidentifier = [v if isinstance(v, NodeIdentifier) else NodeIdentifier(v) for v in self.opt_multi_nodeidentifier]

        super().__post_init__(**kwargs)


@dataclass
class InheritedTypes(YAMLRoot):
    """
    various permutations of a typeof referencing a builtin
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.InheritedTypes
    class_class_curie: ClassVar[str] = "ptypes:InheritedTypes"
    class_name: ClassVar[str] = "InheritedTypes"
    class_model_uri: ClassVar[URIRef] = PTYPES.InheritedTypes

    mand_InheritedType: Union[int, InheritedType] = None
    mand_multi_InheritedType: Union[Union[int, InheritedType], List[Union[int, InheritedType]]] = None
    opt_InheritedType: Optional[Union[int, InheritedType]] = None
    opt_multi_InheritedType: Optional[Union[Union[int, InheritedType], List[Union[int, InheritedType]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_InheritedType):
            self.MissingRequiredField("mand_InheritedType")
        if not isinstance(self.mand_InheritedType, InheritedType):
            self.mand_InheritedType = InheritedType(self.mand_InheritedType)

        if self._is_empty(self.mand_multi_InheritedType):
            self.MissingRequiredField("mand_multi_InheritedType")
        if not isinstance(self.mand_multi_InheritedType, list):
            self.mand_multi_InheritedType = [self.mand_multi_InheritedType] if self.mand_multi_InheritedType is not None else []
        self.mand_multi_InheritedType = [v if isinstance(v, InheritedType) else InheritedType(v) for v in self.mand_multi_InheritedType]

        if self.opt_InheritedType is not None and not isinstance(self.opt_InheritedType, InheritedType):
            self.opt_InheritedType = InheritedType(self.opt_InheritedType)

        if not isinstance(self.opt_multi_InheritedType, list):
            self.opt_multi_InheritedType = [self.opt_multi_InheritedType] if self.opt_multi_InheritedType is not None else []
        self.opt_multi_InheritedType = [v if isinstance(v, InheritedType) else InheritedType(v) for v in self.opt_multi_InheritedType]

        super().__post_init__(**kwargs)


@dataclass
class InheritedType2s(YAMLRoot):
    """
    various permutations of a typeof referencing a metamodelcore type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.InheritedType2s
    class_class_curie: ClassVar[str] = "ptypes:InheritedType2s"
    class_name: ClassVar[str] = "InheritedType2s"
    class_model_uri: ClassVar[URIRef] = PTYPES.InheritedType2s

    mand_InheritedType2: Union[str, InheritedType2] = None
    mand_multi_InheritedType2: Union[Union[str, InheritedType2], List[Union[str, InheritedType2]]] = None
    opt_InheritedType2: Optional[Union[str, InheritedType2]] = None
    opt_multi_InheritedType2: Optional[Union[Union[str, InheritedType2], List[Union[str, InheritedType2]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_InheritedType2):
            self.MissingRequiredField("mand_InheritedType2")
        if not isinstance(self.mand_InheritedType2, InheritedType2):
            self.mand_InheritedType2 = InheritedType2(self.mand_InheritedType2)

        if self._is_empty(self.mand_multi_InheritedType2):
            self.MissingRequiredField("mand_multi_InheritedType2")
        if not isinstance(self.mand_multi_InheritedType2, list):
            self.mand_multi_InheritedType2 = [self.mand_multi_InheritedType2] if self.mand_multi_InheritedType2 is not None else []
        self.mand_multi_InheritedType2 = [v if isinstance(v, InheritedType2) else InheritedType2(v) for v in self.mand_multi_InheritedType2]

        if self.opt_InheritedType2 is not None and not isinstance(self.opt_InheritedType2, InheritedType2):
            self.opt_InheritedType2 = InheritedType2(self.opt_InheritedType2)

        if not isinstance(self.opt_multi_InheritedType2, list):
            self.opt_multi_InheritedType2 = [self.opt_multi_InheritedType2] if self.opt_multi_InheritedType2 is not None else []
        self.opt_multi_InheritedType2 = [v if isinstance(v, InheritedType2) else InheritedType2(v) for v in self.opt_multi_InheritedType2]

        super().__post_init__(**kwargs)


@dataclass
class InheritedType3s(YAMLRoot):
    """
    various permutations of a typeof referencing another defined type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.InheritedType3s
    class_class_curie: ClassVar[str] = "ptypes:InheritedType3s"
    class_name: ClassVar[str] = "InheritedType3s"
    class_model_uri: ClassVar[URIRef] = PTYPES.InheritedType3s

    mand_InheritedType3: Union[str, InheritedType3] = None
    mand_multi_InheritedType3: Union[Union[str, InheritedType3], List[Union[str, InheritedType3]]] = None
    opt_InheritedType3: Optional[Union[str, InheritedType3]] = None
    opt_multi_InheritedType3: Optional[Union[Union[str, InheritedType3], List[Union[str, InheritedType3]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.mand_InheritedType3):
            self.MissingRequiredField("mand_InheritedType3")
        if not isinstance(self.mand_InheritedType3, InheritedType3):
            self.mand_InheritedType3 = InheritedType3(self.mand_InheritedType3)

        if self._is_empty(self.mand_multi_InheritedType3):
            self.MissingRequiredField("mand_multi_InheritedType3")
        if not isinstance(self.mand_multi_InheritedType3, list):
            self.mand_multi_InheritedType3 = [self.mand_multi_InheritedType3] if self.mand_multi_InheritedType3 is not None else []
        self.mand_multi_InheritedType3 = [v if isinstance(v, InheritedType3) else InheritedType3(v) for v in self.mand_multi_InheritedType3]

        if self.opt_InheritedType3 is not None and not isinstance(self.opt_InheritedType3, InheritedType3):
            self.opt_InheritedType3 = InheritedType3(self.opt_InheritedType3)

        if not isinstance(self.opt_multi_InheritedType3, list):
            self.opt_multi_InheritedType3 = [self.opt_multi_InheritedType3] if self.opt_multi_InheritedType3 is not None else []
        self.opt_multi_InheritedType3 = [v if isinstance(v, InheritedType3) else InheritedType3(v) for v in self.opt_multi_InheritedType3]

        super().__post_init__(**kwargs)


@dataclass
class KeyedElement(YAMLRoot):
    """
    keyed  example
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.KeyedElement
    class_class_curie: ClassVar[str] = "ptypes:KeyedElement"
    class_name: ClassVar[str] = "KeyedElement"
    class_model_uri: ClassVar[URIRef] = PTYPES.KeyedElement

    name: Union[str, KeyedElementName] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, KeyedElementName):
            self.name = KeyedElementName(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass
class IdentifiedElement(YAMLRoot):
    """
    identifier example
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PTYPES.IdentifiedElement
    class_class_curie: ClassVar[str] = "ptypes:IdentifiedElement"
    class_name: ClassVar[str] = "IdentifiedElement"
    class_model_uri: ClassVar[URIRef] = PTYPES.IdentifiedElement

    id: Union[str, IdentifiedElementId] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IdentifiedElementId):
            self.id = IdentifiedElementId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.strings__opt_string = Slot(uri=PTYPES.opt_string, name="strings__opt_string", curie=PTYPES.curie('opt_string'),
                   model_uri=PTYPES.strings__opt_string, domain=None, range=Optional[str])

slots.strings__mand_string = Slot(uri=PTYPES.mand_string, name="strings__mand_string", curie=PTYPES.curie('mand_string'),
                   model_uri=PTYPES.strings__mand_string, domain=None, range=str)

slots.strings__opt_multi_string = Slot(uri=PTYPES.opt_multi_string, name="strings__opt_multi_string", curie=PTYPES.curie('opt_multi_string'),
                   model_uri=PTYPES.strings__opt_multi_string, domain=None, range=Optional[Union[str, List[str]]])

slots.strings__mand_multi_string = Slot(uri=PTYPES.mand_multi_string, name="strings__mand_multi_string", curie=PTYPES.curie('mand_multi_string'),
                   model_uri=PTYPES.strings__mand_multi_string, domain=None, range=Union[str, List[str]])

slots.inheritedStrings2__req_second_string = Slot(uri=PTYPES.req_second_string, name="inheritedStrings2__req_second_string", curie=PTYPES.curie('req_second_string'),
                   model_uri=PTYPES.inheritedStrings2__req_second_string, domain=None, range=Optional[str])

slots.integers__opt_integer = Slot(uri=PTYPES.opt_integer, name="integers__opt_integer", curie=PTYPES.curie('opt_integer'),
                   model_uri=PTYPES.integers__opt_integer, domain=None, range=Optional[int])

slots.integers__mand_integer = Slot(uri=PTYPES.mand_integer, name="integers__mand_integer", curie=PTYPES.curie('mand_integer'),
                   model_uri=PTYPES.integers__mand_integer, domain=None, range=int)

slots.integers__opt_multi_integer = Slot(uri=PTYPES.opt_multi_integer, name="integers__opt_multi_integer", curie=PTYPES.curie('opt_multi_integer'),
                   model_uri=PTYPES.integers__opt_multi_integer, domain=None, range=Optional[Union[int, List[int]]])

slots.integers__mand_multi_integer = Slot(uri=PTYPES.mand_multi_integer, name="integers__mand_multi_integer", curie=PTYPES.curie('mand_multi_integer'),
                   model_uri=PTYPES.integers__mand_multi_integer, domain=None, range=Union[int, List[int]])

slots.booleans__opt_boolean = Slot(uri=PTYPES.opt_boolean, name="booleans__opt_boolean", curie=PTYPES.curie('opt_boolean'),
                   model_uri=PTYPES.booleans__opt_boolean, domain=None, range=Optional[Union[bool, Bool]])

slots.booleans__mand_boolean = Slot(uri=PTYPES.mand_boolean, name="booleans__mand_boolean", curie=PTYPES.curie('mand_boolean'),
                   model_uri=PTYPES.booleans__mand_boolean, domain=None, range=Union[bool, Bool])

slots.booleans__opt_multi_boolean = Slot(uri=PTYPES.opt_multi_boolean, name="booleans__opt_multi_boolean", curie=PTYPES.curie('opt_multi_boolean'),
                   model_uri=PTYPES.booleans__opt_multi_boolean, domain=None, range=Optional[Union[Union[bool, Bool], List[Union[bool, Bool]]]])

slots.booleans__mand_multi_boolean = Slot(uri=PTYPES.mand_multi_boolean, name="booleans__mand_multi_boolean", curie=PTYPES.curie('mand_multi_boolean'),
                   model_uri=PTYPES.booleans__mand_multi_boolean, domain=None, range=Union[Union[bool, Bool], List[Union[bool, Bool]]])

slots.floats__opt_float = Slot(uri=PTYPES.opt_float, name="floats__opt_float", curie=PTYPES.curie('opt_float'),
                   model_uri=PTYPES.floats__opt_float, domain=None, range=Optional[float])

slots.floats__mand_float = Slot(uri=PTYPES.mand_float, name="floats__mand_float", curie=PTYPES.curie('mand_float'),
                   model_uri=PTYPES.floats__mand_float, domain=None, range=float)

slots.floats__opt_multi_float = Slot(uri=PTYPES.opt_multi_float, name="floats__opt_multi_float", curie=PTYPES.curie('opt_multi_float'),
                   model_uri=PTYPES.floats__opt_multi_float, domain=None, range=Optional[Union[float, List[float]]])

slots.floats__mand_multi_float = Slot(uri=PTYPES.mand_multi_float, name="floats__mand_multi_float", curie=PTYPES.curie('mand_multi_float'),
                   model_uri=PTYPES.floats__mand_multi_float, domain=None, range=Union[float, List[float]])

slots.doubles__opt_double = Slot(uri=PTYPES.opt_double, name="doubles__opt_double", curie=PTYPES.curie('opt_double'),
                   model_uri=PTYPES.doubles__opt_double, domain=None, range=Optional[float])

slots.doubles__mand_double = Slot(uri=PTYPES.mand_double, name="doubles__mand_double", curie=PTYPES.curie('mand_double'),
                   model_uri=PTYPES.doubles__mand_double, domain=None, range=float)

slots.doubles__opt_multi_double = Slot(uri=PTYPES.opt_multi_double, name="doubles__opt_multi_double", curie=PTYPES.curie('opt_multi_double'),
                   model_uri=PTYPES.doubles__opt_multi_double, domain=None, range=Optional[Union[float, List[float]]])

slots.doubles__mand_multi_double = Slot(uri=PTYPES.mand_multi_double, name="doubles__mand_multi_double", curie=PTYPES.curie('mand_multi_double'),
                   model_uri=PTYPES.doubles__mand_multi_double, domain=None, range=Union[float, List[float]])

slots.times__opt_time = Slot(uri=PTYPES.opt_time, name="times__opt_time", curie=PTYPES.curie('opt_time'),
                   model_uri=PTYPES.times__opt_time, domain=None, range=Optional[Union[str, XSDTime]])

slots.times__mand_time = Slot(uri=PTYPES.mand_time, name="times__mand_time", curie=PTYPES.curie('mand_time'),
                   model_uri=PTYPES.times__mand_time, domain=None, range=Union[str, XSDTime])

slots.times__opt_multi_time = Slot(uri=PTYPES.opt_multi_time, name="times__opt_multi_time", curie=PTYPES.curie('opt_multi_time'),
                   model_uri=PTYPES.times__opt_multi_time, domain=None, range=Optional[Union[Union[str, XSDTime], List[Union[str, XSDTime]]]])

slots.times__mand_multi_time = Slot(uri=PTYPES.mand_multi_time, name="times__mand_multi_time", curie=PTYPES.curie('mand_multi_time'),
                   model_uri=PTYPES.times__mand_multi_time, domain=None, range=Union[Union[str, XSDTime], List[Union[str, XSDTime]]])

slots.dates__opt_date = Slot(uri=PTYPES.opt_date, name="dates__opt_date", curie=PTYPES.curie('opt_date'),
                   model_uri=PTYPES.dates__opt_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.dates__mand_date = Slot(uri=PTYPES.mand_date, name="dates__mand_date", curie=PTYPES.curie('mand_date'),
                   model_uri=PTYPES.dates__mand_date, domain=None, range=Union[str, XSDDate])

slots.dates__opt_multi_date = Slot(uri=PTYPES.opt_multi_date, name="dates__opt_multi_date", curie=PTYPES.curie('opt_multi_date'),
                   model_uri=PTYPES.dates__opt_multi_date, domain=None, range=Optional[Union[Union[str, XSDDate], List[Union[str, XSDDate]]]])

slots.dates__mand_multi_date = Slot(uri=PTYPES.mand_multi_date, name="dates__mand_multi_date", curie=PTYPES.curie('mand_multi_date'),
                   model_uri=PTYPES.dates__mand_multi_date, domain=None, range=Union[Union[str, XSDDate], List[Union[str, XSDDate]]])

slots.dateTimes__opt_datetime = Slot(uri=PTYPES.opt_datetime, name="dateTimes__opt_datetime", curie=PTYPES.curie('opt_datetime'),
                   model_uri=PTYPES.dateTimes__opt_datetime, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.dateTimes__mand_datetime = Slot(uri=PTYPES.mand_datetime, name="dateTimes__mand_datetime", curie=PTYPES.curie('mand_datetime'),
                   model_uri=PTYPES.dateTimes__mand_datetime, domain=None, range=Union[str, XSDDateTime])

slots.dateTimes__opt_multi_datetime = Slot(uri=PTYPES.opt_multi_datetime, name="dateTimes__opt_multi_datetime", curie=PTYPES.curie('opt_multi_datetime'),
                   model_uri=PTYPES.dateTimes__opt_multi_datetime, domain=None, range=Optional[Union[Union[str, XSDDateTime], List[Union[str, XSDDateTime]]]])

slots.dateTimes__mand_multi_datetime = Slot(uri=PTYPES.mand_multi_datetime, name="dateTimes__mand_multi_datetime", curie=PTYPES.curie('mand_multi_datetime'),
                   model_uri=PTYPES.dateTimes__mand_multi_datetime, domain=None, range=Union[Union[str, XSDDateTime], List[Union[str, XSDDateTime]]])

slots.uRIorCURIEs__opt_uriorcurie = Slot(uri=PTYPES.opt_uriorcurie, name="uRIorCURIEs__opt_uriorcurie", curie=PTYPES.curie('opt_uriorcurie'),
                   model_uri=PTYPES.uRIorCURIEs__opt_uriorcurie, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.uRIorCURIEs__mand_uriorcurie = Slot(uri=PTYPES.mand_uriorcurie, name="uRIorCURIEs__mand_uriorcurie", curie=PTYPES.curie('mand_uriorcurie'),
                   model_uri=PTYPES.uRIorCURIEs__mand_uriorcurie, domain=None, range=Union[str, URIorCURIE])

slots.uRIorCURIEs__opt_multi_uriorcurie = Slot(uri=PTYPES.opt_multi_uriorcurie, name="uRIorCURIEs__opt_multi_uriorcurie", curie=PTYPES.curie('opt_multi_uriorcurie'),
                   model_uri=PTYPES.uRIorCURIEs__opt_multi_uriorcurie, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.uRIorCURIEs__mand_multi_uriorcurie = Slot(uri=PTYPES.mand_multi_uriorcurie, name="uRIorCURIEs__mand_multi_uriorcurie", curie=PTYPES.curie('mand_multi_uriorcurie'),
                   model_uri=PTYPES.uRIorCURIEs__mand_multi_uriorcurie, domain=None, range=Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]])

slots.uRIs__opt_uri = Slot(uri=PTYPES.opt_uri, name="uRIs__opt_uri", curie=PTYPES.curie('opt_uri'),
                   model_uri=PTYPES.uRIs__opt_uri, domain=None, range=Optional[Union[str, URI]])

slots.uRIs__mand_uri = Slot(uri=PTYPES.mand_uri, name="uRIs__mand_uri", curie=PTYPES.curie('mand_uri'),
                   model_uri=PTYPES.uRIs__mand_uri, domain=None, range=Union[str, URI])

slots.uRIs__opt_multi_uri = Slot(uri=PTYPES.opt_multi_uri, name="uRIs__opt_multi_uri", curie=PTYPES.curie('opt_multi_uri'),
                   model_uri=PTYPES.uRIs__opt_multi_uri, domain=None, range=Optional[Union[Union[str, URI], List[Union[str, URI]]]])

slots.uRIs__mand_multi_uri = Slot(uri=PTYPES.mand_multi_uri, name="uRIs__mand_multi_uri", curie=PTYPES.curie('mand_multi_uri'),
                   model_uri=PTYPES.uRIs__mand_multi_uri, domain=None, range=Union[Union[str, URI], List[Union[str, URI]]])

slots.nCNames__opt_ncname = Slot(uri=PTYPES.opt_ncname, name="nCNames__opt_ncname", curie=PTYPES.curie('opt_ncname'),
                   model_uri=PTYPES.nCNames__opt_ncname, domain=None, range=Optional[Union[str, NCName]])

slots.nCNames__mand_ncname = Slot(uri=PTYPES.mand_ncname, name="nCNames__mand_ncname", curie=PTYPES.curie('mand_ncname'),
                   model_uri=PTYPES.nCNames__mand_ncname, domain=None, range=Union[str, NCName])

slots.nCNames__opt_multi_ncname = Slot(uri=PTYPES.opt_multi_ncname, name="nCNames__opt_multi_ncname", curie=PTYPES.curie('opt_multi_ncname'),
                   model_uri=PTYPES.nCNames__opt_multi_ncname, domain=None, range=Optional[Union[Union[str, NCName], List[Union[str, NCName]]]])

slots.nCNames__mand_multi_ncname = Slot(uri=PTYPES.mand_multi_ncname, name="nCNames__mand_multi_ncname", curie=PTYPES.curie('mand_multi_ncname'),
                   model_uri=PTYPES.nCNames__mand_multi_ncname, domain=None, range=Union[Union[str, NCName], List[Union[str, NCName]]])

slots.objectIdentifiers__opt_objectidentifier = Slot(uri=PTYPES.opt_objectidentifier, name="objectIdentifiers__opt_objectidentifier", curie=PTYPES.curie('opt_objectidentifier'),
                   model_uri=PTYPES.objectIdentifiers__opt_objectidentifier, domain=None, range=Optional[Union[str, ElementIdentifier]])

slots.objectIdentifiers__mand_objectidentifier = Slot(uri=PTYPES.mand_objectidentifier, name="objectIdentifiers__mand_objectidentifier", curie=PTYPES.curie('mand_objectidentifier'),
                   model_uri=PTYPES.objectIdentifiers__mand_objectidentifier, domain=None, range=Union[str, ElementIdentifier])

slots.objectIdentifiers__opt_multi_objectidentifier = Slot(uri=PTYPES.opt_multi_objectidentifier, name="objectIdentifiers__opt_multi_objectidentifier", curie=PTYPES.curie('opt_multi_objectidentifier'),
                   model_uri=PTYPES.objectIdentifiers__opt_multi_objectidentifier, domain=None, range=Optional[Union[Union[str, ElementIdentifier], List[Union[str, ElementIdentifier]]]])

slots.objectIdentifiers__mand_multi_objectidentifier = Slot(uri=PTYPES.mand_multi_objectidentifier, name="objectIdentifiers__mand_multi_objectidentifier", curie=PTYPES.curie('mand_multi_objectidentifier'),
                   model_uri=PTYPES.objectIdentifiers__mand_multi_objectidentifier, domain=None, range=Union[Union[str, ElementIdentifier], List[Union[str, ElementIdentifier]]])

slots.nodeIdentifiers__opt_nodeidentifier = Slot(uri=PTYPES.opt_nodeidentifier, name="nodeIdentifiers__opt_nodeidentifier", curie=PTYPES.curie('opt_nodeidentifier'),
                   model_uri=PTYPES.nodeIdentifiers__opt_nodeidentifier, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.nodeIdentifiers__mand_nodeidentifier = Slot(uri=PTYPES.mand_nodeidentifier, name="nodeIdentifiers__mand_nodeidentifier", curie=PTYPES.curie('mand_nodeidentifier'),
                   model_uri=PTYPES.nodeIdentifiers__mand_nodeidentifier, domain=None, range=Union[str, NodeIdentifier])

slots.nodeIdentifiers__opt_multi_nodeidentifier = Slot(uri=PTYPES.opt_multi_nodeidentifier, name="nodeIdentifiers__opt_multi_nodeidentifier", curie=PTYPES.curie('opt_multi_nodeidentifier'),
                   model_uri=PTYPES.nodeIdentifiers__opt_multi_nodeidentifier, domain=None, range=Optional[Union[Union[str, NodeIdentifier], List[Union[str, NodeIdentifier]]]])

slots.nodeIdentifiers__mand_multi_nodeidentifier = Slot(uri=PTYPES.mand_multi_nodeidentifier, name="nodeIdentifiers__mand_multi_nodeidentifier", curie=PTYPES.curie('mand_multi_nodeidentifier'),
                   model_uri=PTYPES.nodeIdentifiers__mand_multi_nodeidentifier, domain=None, range=Union[Union[str, NodeIdentifier], List[Union[str, NodeIdentifier]]])

slots.inheritedTypes__opt_InheritedType = Slot(uri=PTYPES.opt_InheritedType, name="inheritedTypes__opt_InheritedType", curie=PTYPES.curie('opt_InheritedType'),
                   model_uri=PTYPES.inheritedTypes__opt_InheritedType, domain=None, range=Optional[Union[int, InheritedType]])

slots.inheritedTypes__mand_InheritedType = Slot(uri=PTYPES.mand_InheritedType, name="inheritedTypes__mand_InheritedType", curie=PTYPES.curie('mand_InheritedType'),
                   model_uri=PTYPES.inheritedTypes__mand_InheritedType, domain=None, range=Union[int, InheritedType])

slots.inheritedTypes__opt_multi_InheritedType = Slot(uri=PTYPES.opt_multi_InheritedType, name="inheritedTypes__opt_multi_InheritedType", curie=PTYPES.curie('opt_multi_InheritedType'),
                   model_uri=PTYPES.inheritedTypes__opt_multi_InheritedType, domain=None, range=Optional[Union[Union[int, InheritedType], List[Union[int, InheritedType]]]])

slots.inheritedTypes__mand_multi_InheritedType = Slot(uri=PTYPES.mand_multi_InheritedType, name="inheritedTypes__mand_multi_InheritedType", curie=PTYPES.curie('mand_multi_InheritedType'),
                   model_uri=PTYPES.inheritedTypes__mand_multi_InheritedType, domain=None, range=Union[Union[int, InheritedType], List[Union[int, InheritedType]]])

slots.inheritedType2s__opt_InheritedType2 = Slot(uri=PTYPES.opt_InheritedType2, name="inheritedType2s__opt_InheritedType2", curie=PTYPES.curie('opt_InheritedType2'),
                   model_uri=PTYPES.inheritedType2s__opt_InheritedType2, domain=None, range=Optional[Union[str, InheritedType2]])

slots.inheritedType2s__mand_InheritedType2 = Slot(uri=PTYPES.mand_InheritedType2, name="inheritedType2s__mand_InheritedType2", curie=PTYPES.curie('mand_InheritedType2'),
                   model_uri=PTYPES.inheritedType2s__mand_InheritedType2, domain=None, range=Union[str, InheritedType2])

slots.inheritedType2s__opt_multi_InheritedType2 = Slot(uri=PTYPES.opt_multi_InheritedType2, name="inheritedType2s__opt_multi_InheritedType2", curie=PTYPES.curie('opt_multi_InheritedType2'),
                   model_uri=PTYPES.inheritedType2s__opt_multi_InheritedType2, domain=None, range=Optional[Union[Union[str, InheritedType2], List[Union[str, InheritedType2]]]])

slots.inheritedType2s__mand_multi_InheritedType2 = Slot(uri=PTYPES.mand_multi_InheritedType2, name="inheritedType2s__mand_multi_InheritedType2", curie=PTYPES.curie('mand_multi_InheritedType2'),
                   model_uri=PTYPES.inheritedType2s__mand_multi_InheritedType2, domain=None, range=Union[Union[str, InheritedType2], List[Union[str, InheritedType2]]])

slots.inheritedType3s__opt_InheritedType3 = Slot(uri=PTYPES.opt_InheritedType3, name="inheritedType3s__opt_InheritedType3", curie=PTYPES.curie('opt_InheritedType3'),
                   model_uri=PTYPES.inheritedType3s__opt_InheritedType3, domain=None, range=Optional[Union[str, InheritedType3]])

slots.inheritedType3s__mand_InheritedType3 = Slot(uri=PTYPES.mand_InheritedType3, name="inheritedType3s__mand_InheritedType3", curie=PTYPES.curie('mand_InheritedType3'),
                   model_uri=PTYPES.inheritedType3s__mand_InheritedType3, domain=None, range=Union[str, InheritedType3])

slots.inheritedType3s__opt_multi_InheritedType3 = Slot(uri=PTYPES.opt_multi_InheritedType3, name="inheritedType3s__opt_multi_InheritedType3", curie=PTYPES.curie('opt_multi_InheritedType3'),
                   model_uri=PTYPES.inheritedType3s__opt_multi_InheritedType3, domain=None, range=Optional[Union[Union[str, InheritedType3], List[Union[str, InheritedType3]]]])

slots.inheritedType3s__mand_multi_InheritedType3 = Slot(uri=PTYPES.mand_multi_InheritedType3, name="inheritedType3s__mand_multi_InheritedType3", curie=PTYPES.curie('mand_multi_InheritedType3'),
                   model_uri=PTYPES.inheritedType3s__mand_multi_InheritedType3, domain=None, range=Union[Union[str, InheritedType3], List[Union[str, InheritedType3]]])

slots.keyedElement__name = Slot(uri=PTYPES.name, name="keyedElement__name", curie=PTYPES.curie('name'),
                   model_uri=PTYPES.keyedElement__name, domain=None, range=URIRef)

slots.keyedElement__value = Slot(uri=PTYPES.value, name="keyedElement__value", curie=PTYPES.curie('value'),
                   model_uri=PTYPES.keyedElement__value, domain=None, range=Optional[str])

slots.identifiedElement__id = Slot(uri=PTYPES.id, name="identifiedElement__id", curie=PTYPES.curie('id'),
                   model_uri=PTYPES.identifiedElement__id, domain=None, range=URIRef)

slots.identifiedElement__value = Slot(uri=PTYPES.value, name="identifiedElement__value", curie=PTYPES.curie('value'),
                   model_uri=PTYPES.identifiedElement__value, domain=None, range=Optional[str])