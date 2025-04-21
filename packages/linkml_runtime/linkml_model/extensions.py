# Auto generated from extensions.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-06-27T23:15:16
# Schema: extensions
#
# id: https://w3id.org/linkml/extensions
# description: Extension mixin
# license: https://creativecommons.org/publicdomain/zero/1.0/

from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = "2.0.0"

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
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Extension"]
    class_class_curie: ClassVar[str] = "linkml:Extension"
    class_name: ClassVar[str] = "extension"
    class_model_uri: ClassVar[URIRef] = LINKML.Extension

    tag: Union[str, ExtensionTag] = None
    value: Union[dict, AnyValue] = None
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, "Extension"]], list[Union[dict, "Extension"]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Extensible"]
    class_class_curie: ClassVar[str] = "linkml:Extensible"
    class_name: ClassVar[str] = "extensible"
    class_model_uri: ClassVar[URIRef] = LINKML.Extensible

    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.extensions = Slot(uri=LINKML.extensions, name="extensions", curie=LINKML.curie('extensions'),
                   model_uri=LINKML.extensions, domain=None, range=Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]])

slots.extension_tag = Slot(uri=LINKML.tag, name="extension_tag", curie=LINKML.curie('tag'),
                   model_uri=LINKML.extension_tag, domain=Extension, range=Union[str, ExtensionTag])

slots.extension_value = Slot(uri=LINKML.value, name="extension_value", curie=LINKML.curie('value'),
                   model_uri=LINKML.extension_value, domain=Extension, range=Union[dict, AnyValue])
