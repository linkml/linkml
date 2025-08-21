# Auto generated from annotations.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: annotations
#
# id: https://w3id.org/linkml/annotations
# description: Annotations mixin
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.extensions import AnyValue, Extension, ExtensionTag
from linkml_runtime.linkml_model.types import Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = "2.0.0"

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = LINKML


# Types

# Class references
class AnnotationTag(ExtensionTag):
    pass


@dataclass(repr=False)
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

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
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

    def __post_init__(self, *_: str, **kwargs: Any):
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
