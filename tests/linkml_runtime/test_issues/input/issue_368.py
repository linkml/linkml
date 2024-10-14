# Auto generated from issue_368.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-26 14:21
# Schema: bms
#
# id: https://microbiomedata/schema
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from .issue_368_imports import ParentClass, SampleEnum

metamodel_version = "1.7.0"

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://microbiomedata/schema/')


# Types

# Class references



@dataclass
class SampleClass(ParentClass):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/SampleClass")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "SampleClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/SampleClass")

    slot_1: Optional[Union[str, "SampleEnum"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.slot_1 is not None and not isinstance(self.slot_1, SampleEnum):
            self.slot_1 = SampleEnum(self.slot_1)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.slot_1 = Slot(uri=DEFAULT_.slot_1, name="slot_1", curie=DEFAULT_.curie('slot_1'),
                   model_uri=DEFAULT_.slot_1, domain=None, range=Optional[Union[str, "SampleEnum"]])
