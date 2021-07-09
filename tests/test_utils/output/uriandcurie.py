# Auto generated from uriandcurie.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:26
# Schema: uriandcurie
#
# id: http://example.org/test/uriandcurie
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
from linkml_runtime.utils.metamodelcore import Curie, ElementIdentifier, NCName, NodeIdentifier, URI, URIorCURIE

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
M = CurieNamespace('m', 'http://example.org/test/uriandcurie')
SHEX = CurieNamespace('shex', 'http://www.w3.org/ns/shex#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = M


# Types
class String(str):
    """ A character string """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = M.String


class Uriorcurie(URIorCURIE):
    """ a URI or a CURIE """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "uriorcurie"
    type_model_uri = M.Uriorcurie


class Uri(URI):
    """ a complete URI """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "uri"
    type_model_uri = M.Uri


class Curie(Curie):
    """ a CURIE """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "curie"
    type_model_uri = M.Curie


class Ncname(NCName):
    """ Prefix part of CURIE """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "ncname"
    type_model_uri = M.Ncname


class Objectidentifier(ElementIdentifier):
    """ A URI or CURIE that represents an object in the model. """
    type_class_uri = SHEX.iri
    type_class_curie = "shex:iri"
    type_name = "objectidentifier"
    type_model_uri = M.Objectidentifier


class Nodeidentifier(NodeIdentifier):
    """ A URI, CURIE or BNODE that represents a node in a model. """
    type_class_uri = SHEX.nonliteral
    type_class_curie = "shex:nonliteral"
    type_name = "nodeidentifier"
    type_model_uri = M.Nodeidentifier


# Class references
class C1Id(ElementIdentifier):
    pass


@dataclass
class C1(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = M.C1
    class_class_curie: ClassVar[str] = "m:C1"
    class_name: ClassVar[str] = "c1"
    class_model_uri: ClassVar[URIRef] = M.C1

    id: Union[str, C1Id] = None
    hasCurie: Optional[Union[str, Curie]] = None
    hasURI: Optional[Union[str, URI]] = None
    hasNcName: Optional[Union[str, NCName]] = None
    id2: Optional[Union[str, NodeIdentifier]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, C1Id):
            self.id = C1Id(self.id)

        if self.hasCurie is not None and not isinstance(self.hasCurie, Curie):
            self.hasCurie = Curie(self.hasCurie)

        if self.hasURI is not None and not isinstance(self.hasURI, URI):
            self.hasURI = URI(self.hasURI)

        if self.hasNcName is not None and not isinstance(self.hasNcName, NCName):
            self.hasNcName = NCName(self.hasNcName)

        if self.id2 is not None and not isinstance(self.id2, NodeIdentifier):
            self.id2 = NodeIdentifier(self.id2)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=M.id, name="id", curie=M.curie('id'),
                   model_uri=M.id, domain=None, range=URIRef)

slots.hasCurie = Slot(uri=M.hasCurie, name="hasCurie", curie=M.curie('hasCurie'),
                   model_uri=M.hasCurie, domain=None, range=Optional[Union[str, Curie]])

slots.hasURI = Slot(uri=M.hasURI, name="hasURI", curie=M.curie('hasURI'),
                   model_uri=M.hasURI, domain=None, range=Optional[Union[str, URI]])

slots.hasNcName = Slot(uri=M.hasNcName, name="hasNcName", curie=M.curie('hasNcName'),
                   model_uri=M.hasNcName, domain=None, range=Optional[Union[str, NCName]])

slots.id2 = Slot(uri=M.id2, name="id2", curie=M.curie('id2'),
                   model_uri=M.id2, domain=None, range=Optional[Union[str, NodeIdentifier]])