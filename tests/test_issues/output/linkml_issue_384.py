# Auto generated from linkml_issue_384.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-10-15 20:00
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
from linkml_runtime.linkml_model.types import Float, Integer, String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SDO = CurieNamespace('sdo', 'http://schema.org/')
DEFAULT_ = CurieNamespace('', 'https://w3id.org/linkml/examples/personinfo/')


# Types

# Class references



@dataclass
class Thing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["examples/personinfo/Thing"]
    class_class_curie: ClassVar[str] = "linkml:examples/personinfo/Thing"
    class_name: ClassVar[str] = "Thing"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/linkml/examples/personinfo/Thing")

    id: Optional[str] = None
    full_name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.full_name is not None and not isinstance(self.full_name, str):
            self.full_name = str(self.full_name)

        super().__post_init__(**kwargs)


@dataclass
class Person(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SDO.Person
    class_class_curie: ClassVar[str] = "sdo:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/linkml/examples/personinfo/Person")

    aliases: Optional[Union[str, List[str]]] = empty_list()
    phone: Optional[str] = None
    age: Optional[int] = None
    parent: Optional[Union[Union[dict, "Person"], List[Union[dict, "Person"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        if self.phone is not None and not isinstance(self.phone, str):
            self.phone = str(self.phone)

        if self.age is not None and not isinstance(self.age, int):
            self.age = int(self.age)

        if not isinstance(self.parent, list):
            self.parent = [self.parent] if self.parent is not None else []
        self.parent = [v if isinstance(v, Person) else Person(**as_dict(v)) for v in self.parent]

        super().__post_init__(**kwargs)


@dataclass
class Organization(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["examples/personinfo/Organization"]
    class_class_curie: ClassVar[str] = "linkml:examples/personinfo/Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/linkml/examples/personinfo/Organization")

    full_name: Optional[str] = None
    parent: Optional[Union[Union[dict, "Organization"], List[Union[dict, "Organization"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.full_name is not None and not isinstance(self.full_name, str):
            self.full_name = str(self.full_name)

        if not isinstance(self.parent, list):
            self.parent = [self.parent] if self.parent is not None else []
        self.parent = [v if isinstance(v, Organization) else Organization(**as_dict(v)) for v in self.parent]

        super().__post_init__(**kwargs)


@dataclass
class GeoObject(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["examples/personinfo/GeoObject"]
    class_class_curie: ClassVar[str] = "linkml:examples/personinfo/GeoObject"
    class_name: ClassVar[str] = "GeoObject"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/linkml/examples/personinfo/GeoObject")

    aliases: Optional[str] = None
    age: Optional[Union[dict, "GeoAge"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.aliases is not None and not isinstance(self.aliases, str):
            self.aliases = str(self.aliases)

        if self.age is not None and not isinstance(self.age, GeoAge):
            self.age = GeoAge(**as_dict(self.age))

        super().__post_init__(**kwargs)


@dataclass
class GeoAge(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["examples/personinfo/GeoAge"]
    class_class_curie: ClassVar[str] = "linkml:examples/personinfo/GeoAge"
    class_name: ClassVar[str] = "GeoAge"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/linkml/examples/personinfo/GeoAge")

    unit: Optional[str] = None
    value: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.id, domain=None, range=Optional[str])

slots.full_name = Slot(uri=DEFAULT_.full_name, name="full_name", curie=DEFAULT_.curie('full_name'),
                   model_uri=DEFAULT_.full_name, domain=None, range=Optional[str])

slots.parent = Slot(uri=DEFAULT_.parent, name="parent", curie=DEFAULT_.curie('parent'),
                   model_uri=DEFAULT_.parent, domain=None, range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]])

slots.person__aliases = Slot(uri=DEFAULT_.aliases, name="person__aliases", curie=DEFAULT_.curie('aliases'),
                   model_uri=DEFAULT_.person__aliases, domain=None, range=Optional[Union[str, List[str]]])

slots.person__phone = Slot(uri=DEFAULT_.phone, name="person__phone", curie=DEFAULT_.curie('phone'),
                   model_uri=DEFAULT_.person__phone, domain=None, range=Optional[str])

slots.person__age = Slot(uri=DEFAULT_.age, name="person__age", curie=DEFAULT_.curie('age'),
                   model_uri=DEFAULT_.person__age, domain=None, range=Optional[int])

slots.geoObject__aliases = Slot(uri=DEFAULT_.aliases, name="geoObject__aliases", curie=DEFAULT_.curie('aliases'),
                   model_uri=DEFAULT_.geoObject__aliases, domain=None, range=Optional[str])

slots.geoObject__age = Slot(uri=DEFAULT_.age, name="geoObject__age", curie=DEFAULT_.curie('age'),
                   model_uri=DEFAULT_.geoObject__age, domain=None, range=Optional[Union[dict, GeoAge]])

slots.geoAge__unit = Slot(uri=DEFAULT_.unit, name="geoAge__unit", curie=DEFAULT_.curie('unit'),
                   model_uri=DEFAULT_.geoAge__unit, domain=None, range=Optional[str])

slots.geoAge__value = Slot(uri=DEFAULT_.value, name="geoAge__value", curie=DEFAULT_.curie('value'),
                   model_uri=DEFAULT_.geoAge__value, domain=None, range=Optional[float])

slots.Person_parent = Slot(uri=DEFAULT_.parent, name="Person_parent", curie=DEFAULT_.curie('parent'),
                   model_uri=DEFAULT_.Person_parent, domain=Person, range=Optional[Union[Union[dict, "Person"], List[Union[dict, "Person"]]]])

slots.Organization_full_name = Slot(uri=DEFAULT_.full_name, name="Organization_full_name", curie=DEFAULT_.curie('full_name'),
                   model_uri=DEFAULT_.Organization_full_name, domain=Organization, range=Optional[str])

slots.Organization_parent = Slot(uri=DEFAULT_.parent, name="Organization_parent", curie=DEFAULT_.curie('parent'),
                   model_uri=DEFAULT_.Organization_parent, domain=Organization, range=Optional[Union[Union[dict, "Organization"], List[Union[dict, "Organization"]]]])