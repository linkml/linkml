# Auto generated from issue_355.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-04-30 12:34
# Schema: issue355
#
# id: http://example.org/issue355/
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCT = CurieNamespace('sct', 'http://snomed.info/id/')
DEFAULT_ = SCT


# Types

# Class references
class ContaineeId(URIorCURIE):
    pass


@dataclass
class Container(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCT.Container
    class_class_curie: ClassVar[str] = "sct:Container"
    class_name: ClassVar[str] = "container"
    class_model_uri: ClassVar[URIRef] = SCT.Container

    entry: Optional[Union[dict[Union[str, ContaineeId], Union[dict, "Containee"]], list[Union[dict, "Containee"]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="entry", slot_type=Containee, key_name="id",  keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Containee(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCT.Containee
    class_class_curie: ClassVar[str] = "sct:Containee"
    class_name: ClassVar[str] = "containee"
    class_model_uri: ClassVar[URIRef] = SCT.Containee

    id: Union[str, ContaineeId] = None
    value: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.id is None:
            raise ValueError("id must be supplied")
        if not isinstance(self.id, ContaineeId):
            self.id = ContaineeId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.container__entry = Slot(uri=SCT.entry, name="container__entry", curie=SCT.curie('entry'),
                   model_uri=SCT.container__entry, domain=None, range=Optional[Union[dict[Union[str, ContaineeId], Union[dict, Containee]], list[Union[dict, Containee]]]])

slots.containee__id = Slot(uri=SCT.id, name="containee__id", curie=SCT.curie('id'),
                   model_uri=SCT.containee__id, domain=None, range=URIRef)

slots.containee__value = Slot(uri=SCT.value, name="containee__value", curie=SCT.curie('value'),
                   model_uri=SCT.containee__value, domain=None, range=Optional[str])
