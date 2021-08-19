# Auto generated from extensions.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-08-19 17:51
# Schema: extensions
#
# id: https://w3id.org/linkml/extensions
# description: Extension mixin
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from .types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

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
        if self._is_empty(self.tag):
            self.MissingRequiredField("tag")
        if not isinstance(self.tag, URIorCURIE):
            self.tag = URIorCURIE(self.tag)

        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=False)

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
        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=False)

        super().__post_init__(**kwargs)


# Enumerations


# Slots

