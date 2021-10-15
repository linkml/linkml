# Auto generated from inheritedid.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-10-15 20:00
# Schema: test_inherited_id
#
# id: https://example.org/inheritedid
# description: Test
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
from linkml_runtime.utils.metamodelcore import URI

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = LINKML


# Types
class String(str):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = LINKML.String


class Uri(URI):
    """ a complete URI """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "uri"
    type_model_uri = LINKML.Uri


class IdentifierType(String):
    """ A string that is intended to uniquely identify a thing May be URI in full or compact (CURIE) form """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "identifier type"
    type_model_uri = LINKML.IdentifierType


class LabelType(String):
    """ A string that provides a human-readable name for a thing """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "label type"
    type_model_uri = LINKML.LabelType


# Class references
class NamedThingId(IdentifierType):
    pass


class AttributeId(IdentifierType):
    pass


class BiologicalSexId(AttributeId):
    pass


class OntologyClassId(NamedThingId):
    pass


@dataclass
class NamedThing(YAMLRoot):
    """
    a databased entity or concept/class
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.NamedThing
    class_class_curie: ClassVar[str] = "linkml:NamedThing"
    class_name: ClassVar[str] = "named thing"
    class_model_uri: ClassVar[URIRef] = LINKML.NamedThing

    id: Union[str, NamedThingId] = None
    name: Optional[Union[str, LabelType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.name is not None and not isinstance(self.name, LabelType):
            self.name = LabelType(self.name)

        super().__post_init__(**kwargs)


@dataclass
class Attribute(YAMLRoot):
    """
    A property or characteristic of an entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Attribute
    class_class_curie: ClassVar[str] = "linkml:Attribute"
    class_name: ClassVar[str] = "attribute"
    class_model_uri: ClassVar[URIRef] = LINKML.Attribute

    id: Union[str, AttributeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AttributeId):
            self.id = AttributeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class BiologicalSex(Attribute):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.BiologicalSex
    class_class_curie: ClassVar[str] = "linkml:BiologicalSex"
    class_name: ClassVar[str] = "biological sex"
    class_model_uri: ClassVar[URIRef] = LINKML.BiologicalSex

    id: Union[str, BiologicalSexId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BiologicalSexId):
            self.id = BiologicalSexId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class OntologyClass(NamedThing):
    """
    a concept or class in an ontology, vocabulary or thesaurus
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.OntologyClass
    class_class_curie: ClassVar[str] = "linkml:OntologyClass"
    class_name: ClassVar[str] = "ontology class"
    class_model_uri: ClassVar[URIRef] = LINKML.OntologyClass

    id: Union[str, OntologyClassId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OntologyClassId):
            self.id = OntologyClassId(self.id)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=LINKML.id, name="id", curie=LINKML.curie('id'),
                   model_uri=LINKML.id, domain=NamedThing, range=Union[str, NamedThingId])

slots.name = Slot(uri=LINKML.name, name="name", curie=LINKML.curie('name'),
                   model_uri=LINKML.name, domain=NamedThing, range=Optional[Union[str, LabelType]])
