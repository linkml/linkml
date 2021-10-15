# Auto generated from multi_id.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-10-15 20:00
# Schema: multi_id
#
# id: http://example.org/example/multi_id
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
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CurieNamespace('', 'http://example.org/example/multi_id/')


# Types
class Uri(URIorCURIE):
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "uri"
    type_model_uri = URIRef("http://example.org/example/multi_id/Uri")


class IdentifierType(Uri):
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "identifier type"
    type_model_uri = URIRef("http://example.org/example/multi_id/IdentifierType")


# Class references
class NamedThingId(URIorCURIE):
    pass


class SequenceVariantId(NamedThingId):
    pass


@dataclass
class NamedThing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = ["node_property", "id"]

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/example/multi_id/NamedThing")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "named thing"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/example/multi_id/NamedThing")

    id: Union[URIorCURIE, NamedThingId] = None
    node_property: Optional[Union[URIorCURIE, IdentifierType]] = None
    not_overridden: Optional[Union[URIorCURIE, IdentifierType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.node_property is not None and not isinstance(self.node_property, IdentifierType):
            self.node_property = IdentifierType(self.node_property)

        if self.not_overridden is not None and not isinstance(self.not_overridden, IdentifierType):
            self.not_overridden = IdentifierType(self.not_overridden)

        super().__post_init__(**kwargs)


@dataclass
class SequenceVariant(NamedThing):
    _inherited_slots: ClassVar[List[str]] = ["id", "node_property"]

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/example/multi_id/SequenceVariant")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "sequence variant"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/example/multi_id/SequenceVariant")

    id: Union[URIorCURIE, SequenceVariantId] = None
    node_property: Optional[Union[URIorCURIE, IdentifierType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SequenceVariantId):
            self.id = SequenceVariantId(self.id)

        if self.node_property is not None and not isinstance(self.node_property, IdentifierType):
            self.node_property = IdentifierType(self.node_property)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.node_property = Slot(uri=DEFAULT_.node_property, name="node property", curie=DEFAULT_.curie('node_property'),
                   model_uri=DEFAULT_.node_property, domain=NamedThing, range=Optional[Union[URIorCURIE, IdentifierType]])

slots.not_overridden = Slot(uri=DEFAULT_.not_overridden, name="not overridden", curie=DEFAULT_.curie('not_overridden'),
                   model_uri=DEFAULT_.not_overridden, domain=NamedThing, range=Optional[Union[URIorCURIE, IdentifierType]])

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.id, domain=NamedThing, range=Union[URIorCURIE, NamedThingId])

slots.sequence_variant_id = Slot(uri=DEFAULT_.id, name="sequence variant_id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.sequence_variant_id, domain=SequenceVariant, range=Union[URIorCURIE, SequenceVariantId])

slots.sequence_variant_node_property = Slot(uri=DEFAULT_.node_property, name="sequence variant_node property", curie=DEFAULT_.curie('node_property'),
                   model_uri=DEFAULT_.sequence_variant_node_property, domain=SequenceVariant, range=Optional[Union[URIorCURIE, IdentifierType]])
