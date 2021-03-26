# Auto generated from extensions.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-26 14:19
# Schema: extensions
#
# id: https://w3id.org/linkml/extensions
# description: Extension mixin
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass

from linkml.utils.slot import Slot
from linkml.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml.utils.formatutils import camelcase, underscore, sfx
from linkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace
from linkml.utils.metamodelcore import URIorCURIE
from linkml_model.types import String, Uriorcurie

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = LINKML


# Types

# Class references



@dataclass
class Extension(YAMLRoot):
    """
    a tag/value pair used to add non-model information to an entry
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Extension
    class_class_curie: ClassVar[str] = "linkml:Extension"
    class_name: ClassVar[str] = "extension"
    class_model_uri: ClassVar[URIRef] = LINKML.Extension

    tag: Union[str, URIorCURIE] = None
    value: str = None
    extensions: Optional[Union[Union[dict, "Extension"], List[Union[dict, "Extension"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.tag is None:
            raise ValueError("tag must be supplied")
        if not isinstance(self.tag, URIorCURIE):
            self.tag = URIorCURIE(self.tag)

        if self.value is None:
            raise ValueError("value must be supplied")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        if self.extensions is None:
            self.extensions = []
        if not isinstance(self.extensions, list):
            self.extensions = [self.extensions]
        self._normalize_inlined_slot(slot_name="extensions", slot_type=Extension, key_name="tag", inlined_as_list=True, keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Extensible(YAMLRoot):
    """
    mixin for classes that support extension
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Extensible
    class_class_curie: ClassVar[str] = "linkml:Extensible"
    class_name: ClassVar[str] = "extensible"
    class_model_uri: ClassVar[URIRef] = LINKML.Extensible

    extensions: Optional[Union[Union[dict, Extension], List[Union[dict, Extension]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.extensions is None:
            self.extensions = []
        if not isinstance(self.extensions, list):
            self.extensions = [self.extensions]
        self._normalize_inlined_slot(slot_name="extensions", slot_type=Extension, key_name="tag", inlined_as_list=True, keyed=False)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.extensions = Slot(uri=LINKML.extensions, name="extensions", curie=LINKML.curie('extensions'),
                   model_uri=LINKML.extensions, domain=None, range=Optional[Union[Union[dict, Extension], List[Union[dict, Extension]]]])

slots.extension_tag = Slot(uri=LINKML.tag, name="extension_tag", curie=LINKML.curie('tag'),
                   model_uri=LINKML.extension_tag, domain=Extension, range=Union[str, URIorCURIE])

slots.extension_value = Slot(uri=LINKML.value, name="extension_value", curie=LINKML.curie('value'),
                   model_uri=LINKML.extension_value, domain=Extension, range=str)