# Auto generated from annotations.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-01-04 21:52
# Schema: annotations
#
# id: https://w3id.org/linkml/annotations
# description: Annotations mixin
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass

from linkml.utils.slot import Slot
from linkml.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
if sys.version_info < (3, 7, 6):
    from linkml.utils.dataclass_extensions_375 import dataclasses_init_fn_with_kwargs
else:
    from linkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml.utils.formatutils import camelcase, underscore, sfx
from linkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace
from linkml.utils.metamodelcore import URIorCURIE
from includes.extensions import Extension
from includes.types import String, Uriorcurie

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
META = CurieNamespace('meta', 'https://w3id.org/linkml/meta/')
DEFAULT_ = META


# Types

# Class references



@dataclass
class Annotatable(YAMLRoot):
    """
    mixin for classes that support annotations
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.Annotatable
    class_class_curie: ClassVar[str] = "meta:Annotatable"
    class_name: ClassVar[str] = "annotatable"
    class_model_uri: ClassVar[URIRef] = META.Annotatable

    annotations: Optional[Union[Union[dict, "Annotation"], List[Union[dict, "Annotation"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.annotations is None:
            self.annotations = []
        if not isinstance(self.annotations, list):
            self.annotations = [self.annotations]
        self._normalize_inlined_slot(slot_name="annotations", slot_type=Annotation, key_name="tag", inlined_as_list=True, keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Annotation(Extension):
    """
    a tag/value pair with the semantics of OWL Annotation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.Annotation
    class_class_curie: ClassVar[str] = "meta:Annotation"
    class_name: ClassVar[str] = "annotation"
    class_model_uri: ClassVar[URIRef] = META.Annotation

    tag: Union[str, URIorCURIE] = None
    value: str = None
    annotations: Optional[Union[Union[dict, "Annotation"], List[Union[dict, "Annotation"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.annotations is None:
            self.annotations = []
        if not isinstance(self.annotations, list):
            self.annotations = [self.annotations]
        self._normalize_inlined_slot(slot_name="annotations", slot_type=Annotation, key_name="tag", inlined_as_list=True, keyed=False)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.annotations = Slot(uri=META.annotations, name="annotations", curie=META.curie('annotations'),
                   model_uri=META.annotations, domain=None, range=Optional[Union[Union[dict, "Annotation"], List[Union[dict, "Annotation"]]]])
