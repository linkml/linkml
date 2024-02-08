# Auto generated from extensions.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-02-07T17:29:29
# Schema: extensions
#
# id: https://w3id.org/linkml/extensions
# description: Extension mixin
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
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
from .types import Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = "2.0.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = LINKML


# Types

# Class references
class ExtensionTag(URIorCURIE):
    pass


AnyValue = Any

@dataclass
class Extension(YAMLRoot):
    """
    a tag/value pair used to add non-model information to an entry
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Extension"]
    class_class_curie: ClassVar[str] = "linkml:Extension"
    class_name: ClassVar[str] = "extension"
    class_model_uri: ClassVar[URIRef] = LINKML.Extension

    tag: Union[str, ExtensionTag] = None
    value: Union[dict, AnyValue] = None
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, "Extension"]], List[Union[dict, "Extension"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.tag):
            self.MissingRequiredField("tag")
        if not isinstance(self.tag, ExtensionTag):
            self.tag = ExtensionTag(self.tag)

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Extensible(YAMLRoot):
    """
    mixin for classes that support extension
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Extensible"]
    class_class_curie: ClassVar[str] = "linkml:Extensible"
    class_name: ClassVar[str] = "extensible"
    class_model_uri: ClassVar[URIRef] = LINKML.Extensible

    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.extensions = Slot(uri=LINKML.extensions, name="extensions", curie=LINKML.curie('extensions'),
                   model_uri=LINKML.extensions, domain=None, range=Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]])

slots.extension_tag = Slot(uri=LINKML.tag, name="extension_tag", curie=LINKML.curie('tag'),
                   model_uri=LINKML.extension_tag, domain=Extension, range=Union[str, ExtensionTag])

slots.extension_value = Slot(uri=LINKML.value, name="extension_value", curie=LINKML.curie('value'),
                   model_uri=LINKML.extension_value, domain=Extension, range=Union[dict, AnyValue])
