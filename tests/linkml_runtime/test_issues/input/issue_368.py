# Auto generated from issue_368.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-26 14:21
# Schema: bms
#
# id: https://microbiomedata/schema
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
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
from . issue_368_imports import ParentClass, SampleEnum

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://microbiomedata/schema/')


# Types

# Class references



@dataclass
class SampleClass(ParentClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/SampleClass")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "SampleClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/SampleClass")

    slot_1: Optional[Union[str, "SampleEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.slot_1 is not None and not isinstance(self.slot_1, SampleEnum):
            self.slot_1 = SampleEnum(self.slot_1)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.slot_1 = Slot(uri=DEFAULT_.slot_1, name="slot_1", curie=DEFAULT_.curie('slot_1'),
                   model_uri=DEFAULT_.slot_1, domain=None, range=Optional[Union[str, "SampleEnum"]])
