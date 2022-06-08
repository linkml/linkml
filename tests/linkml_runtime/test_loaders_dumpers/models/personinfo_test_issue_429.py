# Auto generated from personinfo_test_issue_429.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-06-08T11:49:50
# Schema: personinfo
#
# id: https://w3id.org/linkml/examples/personinfo
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ORCID = CurieNamespace('ORCID', 'https://orcid.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PERSONINFO = CurieNamespace('personinfo', 'https://w3id.org/linkml/examples/personinfo/')
SDO = CurieNamespace('sdo', 'http://schema.org/')
DEFAULT_ = PERSONINFO


# Types

# Class references
class PersonId(extended_str):
    pass


@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SDO.Person
    class_class_curie: ClassVar[str] = "sdo:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Person

    id: Union[str, PersonId] = None
    full_name: Optional[str] = None
    age: Optional[str] = None
    phone: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.full_name is not None and not isinstance(self.full_name, str):
            self.full_name = str(self.full_name)

        if self.age is not None and not isinstance(self.age, str):
            self.age = str(self.age)

        if self.phone is not None and not isinstance(self.phone, str):
            self.phone = str(self.phone)

        super().__post_init__(**kwargs)


@dataclass
class Container(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Container
    class_class_curie: ClassVar[str] = "personinfo:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Container

    persons: Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="persons", slot_type=Person, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=PERSONINFO.id, name="id", curie=PERSONINFO.curie('id'),
                   model_uri=PERSONINFO.id, domain=None, range=URIRef)

slots.full_name = Slot(uri=PERSONINFO.full_name, name="full_name", curie=PERSONINFO.curie('full_name'),
                   model_uri=PERSONINFO.full_name, domain=None, range=Optional[str])

slots.age = Slot(uri=PERSONINFO.age, name="age", curie=PERSONINFO.curie('age'),
                   model_uri=PERSONINFO.age, domain=None, range=Optional[str])

slots.phone = Slot(uri=PERSONINFO.phone, name="phone", curie=PERSONINFO.curie('phone'),
                   model_uri=PERSONINFO.phone, domain=None, range=Optional[str])

slots.container__persons = Slot(uri=PERSONINFO.persons, name="container__persons", curie=PERSONINFO.curie('persons'),
                   model_uri=PERSONINFO.container__persons, domain=None, range=Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]])
