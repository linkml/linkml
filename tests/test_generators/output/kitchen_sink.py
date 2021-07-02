# Auto generated from kitchen_sink.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-02 05:29
# Schema: kitchen_sink
#
# id: https://w3id.org/linkml/tests/kitchen_sink
# description: Kitchen Sink Schema This schema does not do anything useful. It exists to test all features of
#              linkml. This particular text field exists to demonstrate markdown within a text field: Lists: * a *
#              b * c And links, e.g to [Person](Person.md)
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj
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
from linkml_runtime.linkml_model.types import Boolean, Integer, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BFO = CurieNamespace('BFO', 'http://purl.obolibrary.org/obo/BFO_')
RO = CurieNamespace('RO', 'http://purl.obolibrary.org/obo/RO_')
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/')
CORE = CurieNamespace('core', 'https://w3id.org/linkml/tests/core/')
DCE = CurieNamespace('dce', 'http://purl.org/dc/elements/1.1/')
EX = CurieNamespace('ex', 'https://w3id.org/example/')
GOSHAPES = CurieNamespace('goshapes', 'http://purl.obolibrary.org/obo/go/shapes/')
LEGO = CurieNamespace('lego', 'http://geneontology.org/lego/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
DEFAULT_ = EX


# Types

# Class references
class PersonId(extended_str):
    pass


class OrganizationId(extended_str):
    pass


class PlaceId(extended_str):
    pass


class CompanyId(OrganizationId):
    pass


class ActivityId(extended_str):
    pass


class AgentId(extended_str):
    pass


@dataclass
class HasAliases(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.HasAliases
    class_class_curie: ClassVar[str] = "ex:HasAliases"
    class_name: ClassVar[str] = "HasAliases"
    class_model_uri: ClassVar[URIRef] = EX.HasAliases

    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Person
    class_class_curie: ClassVar[str] = "ex:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = EX.Person

    id: Union[str, PersonId] = None
    name: Optional[str] = None
    has_employment_history: Optional[Union[Union[dict, "EmploymentEvent"], List[Union[dict, "EmploymentEvent"]]]] = empty_list()
    has_familial_relationships: Optional[Union[Union[dict, "FamilialRelationship"], List[Union[dict, "FamilialRelationship"]]]] = empty_list()
    has_medical_history: Optional[Union[Union[dict, "MedicalEvent"], List[Union[dict, "MedicalEvent"]]]] = empty_list()
    age_in_years: Optional[int] = None
    addresses: Optional[Union[Union[dict, "Address"], List[Union[dict, "Address"]]]] = empty_list()
    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.has_employment_history, list):
            self.has_employment_history = [self.has_employment_history] if self.has_employment_history is not None else []
        self.has_employment_history = [v if isinstance(v, EmploymentEvent) else EmploymentEvent(**v) for v in self.has_employment_history]

        self._normalize_inlined_as_list(slot_name="has_familial_relationships", slot_type=FamilialRelationship, key_name="type", keyed=False)

        if not isinstance(self.has_medical_history, list):
            self.has_medical_history = [self.has_medical_history] if self.has_medical_history is not None else []
        self.has_medical_history = [v if isinstance(v, MedicalEvent) else MedicalEvent(**v) for v in self.has_medical_history]

        if self.age_in_years is not None and not isinstance(self.age_in_years, int):
            self.age_in_years = int(self.age_in_years)

        if not isinstance(self.addresses, list):
            self.addresses = [self.addresses] if self.addresses is not None else []
        self.addresses = [v if isinstance(v, Address) else Address(**v) for v in self.addresses]

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Organization(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Organization
    class_class_curie: ClassVar[str] = "ex:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = EX.Organization

    id: Union[str, OrganizationId] = None
    name: Optional[str] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganizationId):
            self.id = OrganizationId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Place(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Place
    class_class_curie: ClassVar[str] = "ex:Place"
    class_name: ClassVar[str] = "Place"
    class_model_uri: ClassVar[URIRef] = EX.Place

    id: Union[str, PlaceId] = None
    name: Optional[str] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PlaceId):
            self.id = PlaceId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Address(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Address
    class_class_curie: ClassVar[str] = "ex:Address"
    class_name: ClassVar[str] = "Address"
    class_model_uri: ClassVar[URIRef] = EX.Address

    street: Optional[str] = None
    city: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.street is not None and not isinstance(self.street, str):
            self.street = str(self.street)

        if self.city is not None and not isinstance(self.city, str):
            self.city = str(self.city)

        super().__post_init__(**kwargs)


@dataclass
class Event(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Event
    class_class_curie: ClassVar[str] = "ex:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = EX.Event

    started_at_time: Optional[str] = None
    ended_at_time: Optional[str] = None
    is_current: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, str):
            self.started_at_time = str(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, str):
            self.ended_at_time = str(self.ended_at_time)

        if self.is_current is not None and not isinstance(self.is_current, Bool):
            self.is_current = Bool(self.is_current)

        super().__post_init__(**kwargs)


@dataclass
class Relationship(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Relationship
    class_class_curie: ClassVar[str] = "ex:Relationship"
    class_name: ClassVar[str] = "Relationship"
    class_model_uri: ClassVar[URIRef] = EX.Relationship

    started_at_time: Optional[str] = None
    ended_at_time: Optional[str] = None
    related_to: Optional[str] = None
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, str):
            self.started_at_time = str(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, str):
            self.ended_at_time = str(self.ended_at_time)

        if self.related_to is not None and not isinstance(self.related_to, str):
            self.related_to = str(self.related_to)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass
class FamilialRelationship(Relationship):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.FamilialRelationship
    class_class_curie: ClassVar[str] = "ex:FamilialRelationship"
    class_name: ClassVar[str] = "FamilialRelationship"
    class_model_uri: ClassVar[URIRef] = EX.FamilialRelationship

    type: Union[str, "FamilialRelationshipType"] = None
    related_to: Union[str, PersonId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, FamilialRelationshipType):
            self.type = FamilialRelationshipType(self.type)

        if self._is_empty(self.related_to):
            self.MissingRequiredField("related_to")
        if not isinstance(self.related_to, PersonId):
            self.related_to = PersonId(self.related_to)

        super().__post_init__(**kwargs)


@dataclass
class EmploymentEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.EmploymentEvent
    class_class_curie: ClassVar[str] = "ex:EmploymentEvent"
    class_name: ClassVar[str] = "EmploymentEvent"
    class_model_uri: ClassVar[URIRef] = EX.EmploymentEvent

    employed_at: Optional[Union[str, CompanyId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.employed_at is not None and not isinstance(self.employed_at, CompanyId):
            self.employed_at = CompanyId(self.employed_at)

        super().__post_init__(**kwargs)


class MedicalEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.MedicalEvent
    class_class_curie: ClassVar[str] = "ex:MedicalEvent"
    class_name: ClassVar[str] = "MedicalEvent"
    class_model_uri: ClassVar[URIRef] = EX.MedicalEvent


@dataclass
class WithLocation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.WithLocation
    class_class_curie: ClassVar[str] = "ex:WithLocation"
    class_name: ClassVar[str] = "WithLocation"
    class_model_uri: ClassVar[URIRef] = EX.WithLocation

    in_location: Optional[Union[str, PlaceId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        super().__post_init__(**kwargs)


@dataclass
class MarriageEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.MarriageEvent
    class_class_curie: ClassVar[str] = "ex:MarriageEvent"
    class_name: ClassVar[str] = "MarriageEvent"
    class_model_uri: ClassVar[URIRef] = EX.MarriageEvent

    married_to: Optional[Union[str, PersonId]] = None
    in_location: Optional[Union[str, PlaceId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.married_to is not None and not isinstance(self.married_to, PersonId):
            self.married_to = PersonId(self.married_to)

        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        super().__post_init__(**kwargs)


@dataclass
class Company(Organization):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Company
    class_class_curie: ClassVar[str] = "ex:Company"
    class_name: ClassVar[str] = "Company"
    class_model_uri: ClassVar[URIRef] = EX.Company

    id: Union[str, CompanyId] = None
    ceo: Optional[Union[str, PersonId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CompanyId):
            self.id = CompanyId(self.id)

        if self.ceo is not None and not isinstance(self.ceo, PersonId):
            self.ceo = PersonId(self.ceo)

        super().__post_init__(**kwargs)


@dataclass
class Dataset(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Dataset
    class_class_curie: ClassVar[str] = "ex:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = EX.Dataset

    persons: Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]] = empty_dict()
    companies: Optional[Union[Dict[Union[str, CompanyId], Union[dict, Company]], List[Union[dict, Company]]]] = empty_dict()
    activities: Optional[Union[Dict[Union[str, ActivityId], Union[dict, "Activity"]], List[Union[dict, "Activity"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="persons", slot_type=Person, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="companies", slot_type=Company, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="activities", slot_type=Activity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Activity(YAMLRoot):
    """
    a provence-generating activity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE.Activity
    class_class_curie: ClassVar[str] = "core:Activity"
    class_name: ClassVar[str] = "activity"
    class_model_uri: ClassVar[URIRef] = EX.Activity

    id: Union[str, ActivityId] = None
    started_at_time: Optional[str] = None
    ended_at_time: Optional[str] = None
    was_informed_by: Optional[Union[str, ActivityId]] = None
    was_associated_with: Optional[Union[str, AgentId]] = None
    used: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ActivityId):
            self.id = ActivityId(self.id)

        if self.started_at_time is not None and not isinstance(self.started_at_time, str):
            self.started_at_time = str(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, str):
            self.ended_at_time = str(self.ended_at_time)

        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityId):
            self.was_informed_by = ActivityId(self.was_informed_by)

        if self.was_associated_with is not None and not isinstance(self.was_associated_with, AgentId):
            self.was_associated_with = AgentId(self.was_associated_with)

        if self.used is not None and not isinstance(self.used, str):
            self.used = str(self.used)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class Agent(YAMLRoot):
    """
    a provence-generating agent
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Agent
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "agent"
    class_model_uri: ClassVar[URIRef] = EX.Agent

    id: Union[str, AgentId] = None
    acted_on_behalf_of: Optional[Union[str, AgentId]] = None
    was_informed_by: Optional[Union[str, ActivityId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AgentId):
            self.id = AgentId(self.id)

        if self.acted_on_behalf_of is not None and not isinstance(self.acted_on_behalf_of, AgentId):
            self.acted_on_behalf_of = AgentId(self.acted_on_behalf_of)

        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityId):
            self.was_informed_by = ActivityId(self.was_informed_by)

        super().__post_init__(**kwargs)


# Enumerations
class FamilialRelationshipType(EnumDefinitionImpl):

    SIBLING_OF = PermissibleValue(text="SIBLING_OF")
    PARENT_OF = PermissibleValue(text="PARENT_OF")
    CHILD_OF = PermissibleValue(text="CHILD_OF")

    _defn = EnumDefinition(
        name="FamilialRelationshipType",
    )

class DiagnosisType(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="DiagnosisType",
    )

# Slots
class slots:
    pass

slots.employed_at = Slot(uri=EX.employed_at, name="employed at", curie=EX.curie('employed_at'),
                   model_uri=EX.employed_at, domain=None, range=Optional[Union[str, CompanyId]])

slots.is_current = Slot(uri=EX.is_current, name="is current", curie=EX.curie('is_current'),
                   model_uri=EX.is_current, domain=None, range=Optional[Union[bool, Bool]])

slots.has_employment_history = Slot(uri=EX.has_employment_history, name="has employment history", curie=EX.curie('has_employment_history'),
                   model_uri=EX.has_employment_history, domain=None, range=Optional[Union[Union[dict, EmploymentEvent], List[Union[dict, EmploymentEvent]]]])

slots.has_marriage_history = Slot(uri=EX.has_marriage_history, name="has marriage history", curie=EX.curie('has_marriage_history'),
                   model_uri=EX.has_marriage_history, domain=None, range=Optional[Union[Union[dict, MarriageEvent], List[Union[dict, MarriageEvent]]]])

slots.has_medical_history = Slot(uri=EX.has_medical_history, name="has medical history", curie=EX.curie('has_medical_history'),
                   model_uri=EX.has_medical_history, domain=None, range=Optional[Union[Union[dict, MedicalEvent], List[Union[dict, MedicalEvent]]]])

slots.has_familial_relationships = Slot(uri=EX.has_familial_relationships, name="has familial relationships", curie=EX.curie('has_familial_relationships'),
                   model_uri=EX.has_familial_relationships, domain=None, range=Optional[Union[Union[dict, FamilialRelationship], List[Union[dict, FamilialRelationship]]]])

slots.married_to = Slot(uri=EX.married_to, name="married to", curie=EX.curie('married_to'),
                   model_uri=EX.married_to, domain=None, range=Optional[Union[str, PersonId]])

slots.in_location = Slot(uri=EX.in_location, name="in location", curie=EX.curie('in_location'),
                   model_uri=EX.in_location, domain=None, range=Optional[Union[str, PlaceId]])

slots.addresses = Slot(uri=EX.addresses, name="addresses", curie=EX.curie('addresses'),
                   model_uri=EX.addresses, domain=None, range=Optional[Union[Union[dict, Address], List[Union[dict, Address]]]])

slots.age_in_years = Slot(uri=EX.age_in_years, name="age in years", curie=EX.curie('age_in_years'),
                   model_uri=EX.age_in_years, domain=None, range=Optional[int])

slots.related_to = Slot(uri=EX.related_to, name="related to", curie=EX.curie('related_to'),
                   model_uri=EX.related_to, domain=None, range=Optional[str])

slots.type = Slot(uri=EX.type, name="type", curie=EX.curie('type'),
                   model_uri=EX.type, domain=None, range=Optional[str])

slots.street = Slot(uri=EX.street, name="street", curie=EX.curie('street'),
                   model_uri=EX.street, domain=None, range=Optional[str])

slots.city = Slot(uri=EX.city, name="city", curie=EX.curie('city'),
                   model_uri=EX.city, domain=None, range=Optional[str])

slots.id = Slot(uri=CORE.id, name="id", curie=CORE.curie('id'),
                   model_uri=EX.id, domain=None, range=URIRef)

slots.name = Slot(uri=CORE.name, name="name", curie=CORE.curie('name'),
                   model_uri=EX.name, domain=None, range=Optional[str])

slots.description = Slot(uri=CORE.description, name="description", curie=CORE.curie('description'),
                   model_uri=EX.description, domain=None, range=Optional[str])

slots.started_at_time = Slot(uri=PROV.startedAtTime, name="started at time", curie=PROV.curie('startedAtTime'),
                   model_uri=EX.started_at_time, domain=None, range=Optional[str])

slots.ended_at_time = Slot(uri=PROV.endedAtTime, name="ended at time", curie=PROV.curie('endedAtTime'),
                   model_uri=EX.ended_at_time, domain=None, range=Optional[str])

slots.was_informed_by = Slot(uri=PROV.wasInformedBy, name="was informed by", curie=PROV.curie('wasInformedBy'),
                   model_uri=EX.was_informed_by, domain=None, range=Optional[Union[str, ActivityId]])

slots.was_associated_with = Slot(uri=PROV.wasAssociatedWith, name="was associated with", curie=PROV.curie('wasAssociatedWith'),
                   model_uri=EX.was_associated_with, domain=None, range=Optional[Union[str, AgentId]])

slots.acted_on_behalf_of = Slot(uri=PROV.actedOnBehalfOf, name="acted on behalf of", curie=PROV.curie('actedOnBehalfOf'),
                   model_uri=EX.acted_on_behalf_of, domain=None, range=Optional[Union[str, AgentId]])

slots.was_generated_by = Slot(uri=PROV.wasGeneratedBy, name="was generated by", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=EX.was_generated_by, domain=None, range=Optional[Union[str, ActivityId]])

slots.used = Slot(uri=PROV.used, name="used", curie=PROV.curie('used'),
                   model_uri=EX.used, domain=Activity, range=Optional[str])

slots.activity_set = Slot(uri=CORE.activity_set, name="activity set", curie=CORE.curie('activity_set'),
                   model_uri=EX.activity_set, domain=None, range=Optional[Union[Dict[Union[str, ActivityId], Union[dict, Activity]], List[Union[dict, Activity]]]])

slots.agent_set = Slot(uri=CORE.agent_set, name="agent set", curie=CORE.curie('agent_set'),
                   model_uri=EX.agent_set, domain=None, range=Optional[Union[Dict[Union[str, AgentId], Union[dict, Agent]], List[Union[dict, Agent]]]])

slots.hasAliases__aliases = Slot(uri=EX.aliases, name="hasAliases__aliases", curie=EX.curie('aliases'),
                   model_uri=EX.hasAliases__aliases, domain=None, range=Optional[Union[str, List[str]]])

slots.company__ceo = Slot(uri=EX.ceo, name="company__ceo", curie=EX.curie('ceo'),
                   model_uri=EX.company__ceo, domain=None, range=Optional[Union[str, PersonId]])

slots.dataset__persons = Slot(uri=EX.persons, name="dataset__persons", curie=EX.curie('persons'),
                   model_uri=EX.dataset__persons, domain=None, range=Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]])

slots.dataset__companies = Slot(uri=EX.companies, name="dataset__companies", curie=EX.curie('companies'),
                   model_uri=EX.dataset__companies, domain=None, range=Optional[Union[Dict[Union[str, CompanyId], Union[dict, Company]], List[Union[dict, Company]]]])

slots.dataset__activities = Slot(uri=EX.activities, name="dataset__activities", curie=EX.curie('activities'),
                   model_uri=EX.dataset__activities, domain=None, range=Optional[Union[Dict[Union[str, ActivityId], Union[dict, Activity]], List[Union[dict, Activity]]]])

slots.Person_name = Slot(uri=EX.name, name="Person_name", curie=EX.curie('name'),
                   model_uri=EX.Person_name, domain=Person, range=Optional[str],
                   pattern=re.compile(r'^\S+ \S+'))

slots.FamilialRelationship_type = Slot(uri=EX.type, name="FamilialRelationship_type", curie=EX.curie('type'),
                   model_uri=EX.FamilialRelationship_type, domain=FamilialRelationship, range=Union[str, "FamilialRelationshipType"])

slots.FamilialRelationship_related_to = Slot(uri=EX.related_to, name="FamilialRelationship_related to", curie=EX.curie('related_to'),
                   model_uri=EX.FamilialRelationship_related_to, domain=FamilialRelationship, range=Union[str, PersonId])