# Auto generated from annotations.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-06-27T23:15:03
# Schema: annotations
#
# id: https://w3id.org/linkml/annotations
# description: Annotations mixin
# license: https://creativecommons.org/publicdomain/zero/1.0/

from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from .extensions import AnyValue, Extension, ExtensionTag

metamodel_version = "1.7.0"
version = "2.0.0"

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = LINKML


# Types

# Class references
class AnnotationTag(ExtensionTag):
    pass


@dataclass
class Annotatable(YAMLRoot):
    """
    mixin for classes that support annotations
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Annotatable"]
    class_class_curie: ClassVar[str] = "linkml:Annotatable"
    class_name: ClassVar[str] = "annotatable"
    class_model_uri: ClassVar[URIRef] = LINKML.Annotatable

    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, "Annotation"]], list[Union[dict, "Annotation"]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Annotation(Extension):
    """
    a tag/value pair with the semantics of OWL Annotation
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Annotation"]
    class_class_curie: ClassVar[str] = "linkml:Annotation"
    class_name: ClassVar[str] = "annotation"
    class_model_uri: ClassVar[URIRef] = LINKML.Annotation

    tag: Union[str, AnnotationTag] = None
    value: Union[dict, AnyValue] = None
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, "Annotation"]], list[Union[dict, "Annotation"]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.tag):
            self.MissingRequiredField("tag")
        if not isinstance(self.tag, AnnotationTag):
            self.tag = AnnotationTag(self.tag)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.annotations = Slot(uri=LINKML.annotations, name="annotations", curie=LINKML.curie('annotations'),
                   model_uri=LINKML.annotations, domain=None, range=Optional[Union[dict[Union[str, AnnotationTag], Union[dict, "Annotation"]], list[Union[dict, "Annotation"]]]])
