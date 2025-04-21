# Auto generated from linkml_issue_817.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-06-01T18:51:29
# Schema: personinfo
#
# id: https://w3id.org/linkml/examples/personinfo
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from jsonasobj2 import as_dict
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace

metamodel_version = "1.7.0"
version = None

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PERSONINFO = CurieNamespace('personinfo', 'https://w3id.org/linkml/examples/personinfo/')
RDF = CurieNamespace('rdf', 'http://example.org/UNKNOWN/rdf/')
RDFS = CurieNamespace('rdfs', 'http://example.org/UNKNOWN/rdfs/')
SKOS = CurieNamespace('skos', 'http://example.org/UNKNOWN/skos/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = PERSONINFO


# Types

# Class references
class PersonId(extended_str):
    pass


@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Person
    class_class_curie: ClassVar[str] = "personinfo:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Person

    id: Union[str, PersonId] = None
    name: Optional[str] = None
    vital_status: Optional[Union[str, "VitalStatusEnum"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.vital_status is not None and not isinstance(self.vital_status, VitalStatusEnum):
            self.vital_status = VitalStatusEnum(self.vital_status)

        super().__post_init__(**kwargs)


@dataclass
class PersonNoId(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.PersonNoId
    class_class_curie: ClassVar[str] = "personinfo:PersonNoId"
    class_name: ClassVar[str] = "PersonNoId"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.PersonNoId

    name: Optional[str] = None
    vital_status: Optional[Union[str, "VitalStatusEnum"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.vital_status is not None and not isinstance(self.vital_status, VitalStatusEnum):
            self.vital_status = VitalStatusEnum(self.vital_status)

        super().__post_init__(**kwargs)


@dataclass
class Container(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Container
    class_class_curie: ClassVar[str] = "personinfo:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Container

    name: Optional[str] = None
    persons_as_list: Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]] = empty_dict()
    persons_as_dict: Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]] = empty_dict()
    single_person_inlined: Optional[Union[dict, Person]] = None
    noidobj_as_list: Optional[Union[Union[dict, PersonNoId], list[Union[dict, PersonNoId]]]] = empty_list()
    single_noidobj_inlined: Optional[Union[dict, PersonNoId]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        self._normalize_inlined_as_list(slot_name="persons_as_list", slot_type=Person, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="persons_as_dict", slot_type=Person, key_name="id", keyed=True)

        if self.single_person_inlined is not None and not isinstance(self.single_person_inlined, Person):
            self.single_person_inlined = Person(**as_dict(self.single_person_inlined))

        if not isinstance(self.noidobj_as_list, list):
            self.noidobj_as_list = [self.noidobj_as_list] if self.noidobj_as_list is not None else []
        self.noidobj_as_list = [v if isinstance(v, PersonNoId) else PersonNoId(**as_dict(v)) for v in self.noidobj_as_list]

        if self.single_noidobj_inlined is not None and not isinstance(self.single_noidobj_inlined, PersonNoId):
            self.single_noidobj_inlined = PersonNoId(**as_dict(self.single_noidobj_inlined))

        super().__post_init__(**kwargs)


# Enumerations
class VitalStatusEnum(EnumDefinitionImpl):

    LIVING = PermissibleValue(text="LIVING")
    DEAD = PermissibleValue(text="DEAD")

    _defn = EnumDefinition(
        name="VitalStatusEnum",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=PERSONINFO.id, name="id", curie=PERSONINFO.curie('id'),
                   model_uri=PERSONINFO.id, domain=None, range=URIRef)

slots.name = Slot(uri=PERSONINFO.name, name="name", curie=PERSONINFO.curie('name'),
                   model_uri=PERSONINFO.name, domain=None, range=Optional[str])

slots.persons_as_list = Slot(uri=PERSONINFO.persons_as_list, name="persons_as_list", curie=PERSONINFO.curie('persons_as_list'),
                   model_uri=PERSONINFO.persons_as_list, domain=None, range=Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]])

slots.persons_as_dict = Slot(uri=PERSONINFO.persons_as_dict, name="persons_as_dict", curie=PERSONINFO.curie('persons_as_dict'),
                   model_uri=PERSONINFO.persons_as_dict, domain=None, range=Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]])

slots.single_person_inlined = Slot(uri=PERSONINFO.single_person_inlined, name="single_person_inlined", curie=PERSONINFO.curie('single_person_inlined'),
                   model_uri=PERSONINFO.single_person_inlined, domain=None, range=Optional[Union[dict, Person]])

slots.noidobj_as_list = Slot(uri=PERSONINFO.noidobj_as_list, name="noidobj_as_list", curie=PERSONINFO.curie('noidobj_as_list'),
                   model_uri=PERSONINFO.noidobj_as_list, domain=None, range=Optional[Union[Union[dict, PersonNoId], list[Union[dict, PersonNoId]]]])

slots.single_noidobj_inlined = Slot(uri=PERSONINFO.single_noidobj_inlined, name="single_noidobj_inlined", curie=PERSONINFO.curie('single_noidobj_inlined'),
                   model_uri=PERSONINFO.single_noidobj_inlined, domain=None, range=Optional[Union[dict, PersonNoId]])

slots.vital_status = Slot(uri=PERSONINFO.vital_status, name="vital_status", curie=PERSONINFO.curie('vital_status'),
                   model_uri=PERSONINFO.vital_status, domain=None, range=Optional[Union[str, "VitalStatusEnum"]])
