# Auto generated from linkml_issue_576.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-11-18T12:51:30
# Schema: personinfo
#
# id: https://w3id.org/linkml/examples/personinfo
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Namespaces
EX = CurieNamespace('ex', 'https://example.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PERSONINFO = CurieNamespace('personinfo', 'https://w3id.org/linkml/personinfo/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = PERSONINFO


# Types
class Code(String):
    """ An identifier that is encoded in a string.  This is used to represent identifiers that are not URIs, but are encoded as strings.  For example, a person's social security number is an encoded identifier. """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "Code"
    type_model_uri = PERSONINFO.Code


# Class references
class PersonId(URIorCURIE):
    pass


class PetId(extended_str):
    pass


class OrganizationId(Code):
    pass


@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.Person
    class_class_curie: ClassVar[str] = "schema:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Person

    id: Union[str, PersonId] = None
    name: Optional[str] = None
    friends: Optional[Union[Union[str, PersonId], list[Union[str, PersonId]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.friends, list):
            self.friends = [self.friends] if self.friends is not None else []
        self.friends = [v if isinstance(v, PersonId) else PersonId(v) for v in self.friends]

        super().__post_init__(**kwargs)


@dataclass
class Pet(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Pet
    class_class_curie: ClassVar[str] = "personinfo:Pet"
    class_name: ClassVar[str] = "Pet"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Pet

    id: Union[str, PetId] = None
    name: Optional[str] = None
    owner: Optional[Union[str, PersonId]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PetId):
            self.id = PetId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.owner is not None and not isinstance(self.owner, PersonId):
            self.owner = PersonId(self.owner)

        super().__post_init__(**kwargs)


@dataclass
class Organization(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.Organization
    class_class_curie: ClassVar[str] = "schema:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Organization

    id: Union[str, OrganizationId] = None
    name: Optional[str] = None
    part_of: Optional[Union[Union[str, OrganizationId], list[Union[str, OrganizationId]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganizationId):
            self.id = OrganizationId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.part_of, list):
            self.part_of = [self.part_of] if self.part_of is not None else []
        self.part_of = [v if isinstance(v, OrganizationId) else OrganizationId(v) for v in self.part_of]

        super().__post_init__(**kwargs)


@dataclass
class Dataset(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Dataset
    class_class_curie: ClassVar[str] = "personinfo:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Dataset

    source: Optional[Union[str, URIorCURIE]] = None
    persons: Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]] = empty_dict()
    organizations: Optional[Union[dict[Union[str, OrganizationId], Union[dict, Organization]], list[Union[dict, Organization]]]] = empty_dict()
    pets: Optional[Union[dict[Union[str, PetId], Union[dict, Pet]], list[Union[dict, Pet]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        self._normalize_inlined_as_dict(slot_name="persons", slot_type=Person, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="organizations", slot_type=Organization, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="pets", slot_type=Pet, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.person__id = Slot(uri=PERSONINFO.id, name="person__id", curie=PERSONINFO.curie('id'),
                   model_uri=PERSONINFO.person__id, domain=None, range=URIRef)

slots.person__name = Slot(uri=SCHEMA.name, name="person__name", curie=SCHEMA.curie('name'),
                   model_uri=PERSONINFO.person__name, domain=None, range=Optional[str])

slots.person__friends = Slot(uri=PERSONINFO.friends, name="person__friends", curie=PERSONINFO.curie('friends'),
                   model_uri=PERSONINFO.person__friends, domain=None, range=Optional[Union[Union[str, PersonId], list[Union[str, PersonId]]]])

slots.pet__id = Slot(uri=PERSONINFO.id, name="pet__id", curie=PERSONINFO.curie('id'),
                   model_uri=PERSONINFO.pet__id, domain=None, range=URIRef)

slots.pet__name = Slot(uri=SCHEMA.name, name="pet__name", curie=SCHEMA.curie('name'),
                   model_uri=PERSONINFO.pet__name, domain=None, range=Optional[str])

slots.pet__owner = Slot(uri=SCHEMA.owner, name="pet__owner", curie=SCHEMA.curie('owner'),
                   model_uri=PERSONINFO.pet__owner, domain=None, range=Optional[Union[str, PersonId]])

slots.organization__id = Slot(uri=PERSONINFO.id, name="organization__id", curie=PERSONINFO.curie('id'),
                   model_uri=PERSONINFO.organization__id, domain=None, range=URIRef)

slots.organization__name = Slot(uri=SCHEMA.name, name="organization__name", curie=SCHEMA.curie('name'),
                   model_uri=PERSONINFO.organization__name, domain=None, range=Optional[str])

slots.organization__part_of = Slot(uri=PERSONINFO.part_of, name="organization__part_of", curie=PERSONINFO.curie('part_of'),
                   model_uri=PERSONINFO.organization__part_of, domain=None, range=Optional[Union[Union[str, OrganizationId], list[Union[str, OrganizationId]]]])

slots.dataset__source = Slot(uri=PERSONINFO.source, name="dataset__source", curie=PERSONINFO.curie('source'),
                   model_uri=PERSONINFO.dataset__source, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.dataset__persons = Slot(uri=PERSONINFO.persons, name="dataset__persons", curie=PERSONINFO.curie('persons'),
                   model_uri=PERSONINFO.dataset__persons, domain=None, range=Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]])

slots.dataset__organizations = Slot(uri=PERSONINFO.organizations, name="dataset__organizations", curie=PERSONINFO.curie('organizations'),
                   model_uri=PERSONINFO.dataset__organizations, domain=None, range=Optional[Union[dict[Union[str, OrganizationId], Union[dict, Organization]], list[Union[dict, Organization]]]])

slots.dataset__pets = Slot(uri=PERSONINFO.pets, name="dataset__pets", curie=PERSONINFO.curie('pets'),
                   model_uri=PERSONINFO.dataset__pets, domain=None, range=Optional[Union[dict[Union[str, PetId], Union[dict, Pet]], list[Union[dict, Pet]]]])
