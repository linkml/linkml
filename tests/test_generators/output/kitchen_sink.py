# Auto generated from kitchen_sink.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-10-15 19:59
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
from linkml_runtime.linkml_model.types import Boolean, Date, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, XSDDate

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
A = CurieNamespace('A', 'http://example.org/activities/')
BFO = CurieNamespace('BFO', 'http://purl.obolibrary.org/obo/BFO_')
CODE = CurieNamespace('CODE', 'http://example.org/code/')
P = CurieNamespace('P', 'http://example.org/person/')
RO = CurieNamespace('RO', 'http://purl.obolibrary.org/obo/RO_')
ROR = CurieNamespace('ROR', 'http://example.org/ror/')
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/')
CORE = CurieNamespace('core', 'https://w3id.org/linkml/tests/core/')
DCE = CurieNamespace('dce', 'http://purl.org/dc/elements/1.1/')
KS = CurieNamespace('ks', 'https://w3id.org/linkml/tests/kitchen_sink/')
LEGO = CurieNamespace('lego', 'http://geneontology.org/lego/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
DEFAULT_ = KS


# Types

# Class references
class PersonId(extended_str):
    pass


class OrganizationId(extended_str):
    pass


class PlaceId(extended_str):
    pass


class ConceptId(extended_str):
    pass


class DiagnosisConceptId(ConceptId):
    pass


class ProcedureConceptId(ConceptId):
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

    class_class_uri: ClassVar[URIRef] = KS.HasAliases
    class_class_curie: ClassVar[str] = "ks:HasAliases"
    class_name: ClassVar[str] = "HasAliases"
    class_model_uri: ClassVar[URIRef] = KS.HasAliases

    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Friend(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.Friend
    class_class_curie: ClassVar[str] = "ks:Friend"
    class_name: ClassVar[str] = "Friend"
    class_model_uri: ClassVar[URIRef] = KS.Friend

    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass
class Person(YAMLRoot):
    """
    A person, living or dead
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.Person
    class_class_curie: ClassVar[str] = "ks:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = KS.Person

    id: Union[str, PersonId] = None
    name: Optional[str] = None
    has_employment_history: Optional[Union[Union[dict, "EmploymentEvent"], List[Union[dict, "EmploymentEvent"]]]] = empty_list()
    has_familial_relationships: Optional[Union[Union[dict, "FamilialRelationship"], List[Union[dict, "FamilialRelationship"]]]] = empty_list()
    has_medical_history: Optional[Union[Union[dict, "MedicalEvent"], List[Union[dict, "MedicalEvent"]]]] = empty_list()
    age_in_years: Optional[int] = None
    addresses: Optional[Union[Union[dict, "Address"], List[Union[dict, "Address"]]]] = empty_list()
    has_birth_event: Optional[Union[dict, "BirthEvent"]] = None
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
        self.has_employment_history = [v if isinstance(v, EmploymentEvent) else EmploymentEvent(**as_dict(v)) for v in self.has_employment_history]

        self._normalize_inlined_as_list(slot_name="has_familial_relationships", slot_type=FamilialRelationship, key_name="type", keyed=False)

        if not isinstance(self.has_medical_history, list):
            self.has_medical_history = [self.has_medical_history] if self.has_medical_history is not None else []
        self.has_medical_history = [v if isinstance(v, MedicalEvent) else MedicalEvent(**as_dict(v)) for v in self.has_medical_history]

        if self.age_in_years is not None and not isinstance(self.age_in_years, int):
            self.age_in_years = int(self.age_in_years)

        if not isinstance(self.addresses, list):
            self.addresses = [self.addresses] if self.addresses is not None else []
        self.addresses = [v if isinstance(v, Address) else Address(**as_dict(v)) for v in self.addresses]

        if self.has_birth_event is not None and not isinstance(self.has_birth_event, BirthEvent):
            self.has_birth_event = BirthEvent(**as_dict(self.has_birth_event))

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Organization(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.Organization
    class_class_curie: ClassVar[str] = "ks:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = KS.Organization

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

    class_class_uri: ClassVar[URIRef] = KS.Place
    class_class_curie: ClassVar[str] = "ks:Place"
    class_name: ClassVar[str] = "Place"
    class_model_uri: ClassVar[URIRef] = KS.Place

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

    class_class_uri: ClassVar[URIRef] = KS.Address
    class_class_curie: ClassVar[str] = "ks:Address"
    class_name: ClassVar[str] = "Address"
    class_model_uri: ClassVar[URIRef] = KS.Address

    street: Optional[str] = None
    city: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.street is not None and not isinstance(self.street, str):
            self.street = str(self.street)

        if self.city is not None and not isinstance(self.city, str):
            self.city = str(self.city)

        super().__post_init__(**kwargs)


@dataclass
class Concept(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.Concept
    class_class_curie: ClassVar[str] = "ks:Concept"
    class_name: ClassVar[str] = "Concept"
    class_model_uri: ClassVar[URIRef] = KS.Concept

    id: Union[str, ConceptId] = None
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConceptId):
            self.id = ConceptId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass
class DiagnosisConcept(Concept):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.DiagnosisConcept
    class_class_curie: ClassVar[str] = "ks:DiagnosisConcept"
    class_name: ClassVar[str] = "DiagnosisConcept"
    class_model_uri: ClassVar[URIRef] = KS.DiagnosisConcept

    id: Union[str, DiagnosisConceptId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiagnosisConceptId):
            self.id = DiagnosisConceptId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ProcedureConcept(Concept):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.ProcedureConcept
    class_class_curie: ClassVar[str] = "ks:ProcedureConcept"
    class_name: ClassVar[str] = "ProcedureConcept"
    class_model_uri: ClassVar[URIRef] = KS.ProcedureConcept

    id: Union[str, ProcedureConceptId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcedureConceptId):
            self.id = ProcedureConceptId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Event(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.Event
    class_class_curie: ClassVar[str] = "ks:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = KS.Event

    started_at_time: Optional[Union[str, XSDDate]] = None
    ended_at_time: Optional[Union[str, XSDDate]] = None
    is_current: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDate):
            self.started_at_time = XSDDate(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDate):
            self.ended_at_time = XSDDate(self.ended_at_time)

        if self.is_current is not None and not isinstance(self.is_current, Bool):
            self.is_current = Bool(self.is_current)

        super().__post_init__(**kwargs)


@dataclass
class Relationship(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.Relationship
    class_class_curie: ClassVar[str] = "ks:Relationship"
    class_name: ClassVar[str] = "Relationship"
    class_model_uri: ClassVar[URIRef] = KS.Relationship

    started_at_time: Optional[Union[str, XSDDate]] = None
    ended_at_time: Optional[Union[str, XSDDate]] = None
    related_to: Optional[str] = None
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDate):
            self.started_at_time = XSDDate(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDate):
            self.ended_at_time = XSDDate(self.ended_at_time)

        if self.related_to is not None and not isinstance(self.related_to, str):
            self.related_to = str(self.related_to)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass
class FamilialRelationship(Relationship):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.FamilialRelationship
    class_class_curie: ClassVar[str] = "ks:FamilialRelationship"
    class_name: ClassVar[str] = "FamilialRelationship"
    class_model_uri: ClassVar[URIRef] = KS.FamilialRelationship

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
class BirthEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.BirthEvent
    class_class_curie: ClassVar[str] = "ks:BirthEvent"
    class_name: ClassVar[str] = "BirthEvent"
    class_model_uri: ClassVar[URIRef] = KS.BirthEvent

    in_location: Optional[Union[str, PlaceId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        super().__post_init__(**kwargs)


@dataclass
class EmploymentEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.EmploymentEvent
    class_class_curie: ClassVar[str] = "ks:EmploymentEvent"
    class_name: ClassVar[str] = "EmploymentEvent"
    class_model_uri: ClassVar[URIRef] = KS.EmploymentEvent

    employed_at: Optional[Union[str, CompanyId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.employed_at is not None and not isinstance(self.employed_at, CompanyId):
            self.employed_at = CompanyId(self.employed_at)

        super().__post_init__(**kwargs)


@dataclass
class MedicalEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.MedicalEvent
    class_class_curie: ClassVar[str] = "ks:MedicalEvent"
    class_name: ClassVar[str] = "MedicalEvent"
    class_model_uri: ClassVar[URIRef] = KS.MedicalEvent

    in_location: Optional[Union[str, PlaceId]] = None
    diagnosis: Optional[Union[dict, DiagnosisConcept]] = None
    procedure: Optional[Union[dict, ProcedureConcept]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        if self.diagnosis is not None and not isinstance(self.diagnosis, DiagnosisConcept):
            self.diagnosis = DiagnosisConcept(**as_dict(self.diagnosis))

        if self.procedure is not None and not isinstance(self.procedure, ProcedureConcept):
            self.procedure = ProcedureConcept(**as_dict(self.procedure))

        super().__post_init__(**kwargs)


@dataclass
class WithLocation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.WithLocation
    class_class_curie: ClassVar[str] = "ks:WithLocation"
    class_name: ClassVar[str] = "WithLocation"
    class_model_uri: ClassVar[URIRef] = KS.WithLocation

    in_location: Optional[Union[str, PlaceId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        super().__post_init__(**kwargs)


@dataclass
class MarriageEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.MarriageEvent
    class_class_curie: ClassVar[str] = "ks:MarriageEvent"
    class_name: ClassVar[str] = "MarriageEvent"
    class_model_uri: ClassVar[URIRef] = KS.MarriageEvent

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

    class_class_uri: ClassVar[URIRef] = KS.Company
    class_class_curie: ClassVar[str] = "ks:Company"
    class_name: ClassVar[str] = "Company"
    class_model_uri: ClassVar[URIRef] = KS.Company

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

    class_class_uri: ClassVar[URIRef] = KS.Dataset
    class_class_curie: ClassVar[str] = "ks:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = KS.Dataset

    persons: Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]] = empty_dict()
    companies: Optional[Union[Dict[Union[str, CompanyId], Union[dict, Company]], List[Union[dict, Company]]]] = empty_dict()
    activities: Optional[Union[Dict[Union[str, ActivityId], Union[dict, "Activity"]], List[Union[dict, "Activity"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="persons", slot_type=Person, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="companies", slot_type=Company, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="activities", slot_type=Activity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class FakeClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.FakeClass
    class_class_curie: ClassVar[str] = "ks:FakeClass"
    class_name: ClassVar[str] = "FakeClass"
    class_model_uri: ClassVar[URIRef] = KS.FakeClass

    test_attribute: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.test_attribute is not None and not isinstance(self.test_attribute, str):
            self.test_attribute = str(self.test_attribute)

        super().__post_init__(**kwargs)


@dataclass
class ClassWithSpaces(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.ClassWithSpaces
    class_class_curie: ClassVar[str] = "ks:ClassWithSpaces"
    class_name: ClassVar[str] = "class with spaces"
    class_model_uri: ClassVar[URIRef] = KS.ClassWithSpaces

    slot_with_space_1: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.slot_with_space_1 is not None and not isinstance(self.slot_with_space_1, str):
            self.slot_with_space_1 = str(self.slot_with_space_1)

        super().__post_init__(**kwargs)


@dataclass
class SubclassTest(ClassWithSpaces):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS.SubclassTest
    class_class_curie: ClassVar[str] = "ks:SubclassTest"
    class_name: ClassVar[str] = "subclass test"
    class_model_uri: ClassVar[URIRef] = KS.SubclassTest

    slot_with_space_2: Optional[Union[dict, ClassWithSpaces]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.slot_with_space_2 is not None and not isinstance(self.slot_with_space_2, ClassWithSpaces):
            self.slot_with_space_2 = ClassWithSpaces(**as_dict(self.slot_with_space_2))

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
    class_model_uri: ClassVar[URIRef] = KS.Activity

    id: Union[str, ActivityId] = None
    started_at_time: Optional[Union[str, XSDDate]] = None
    ended_at_time: Optional[Union[str, XSDDate]] = None
    was_informed_by: Optional[Union[str, ActivityId]] = None
    was_associated_with: Optional[Union[str, AgentId]] = None
    used: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ActivityId):
            self.id = ActivityId(self.id)

        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDate):
            self.started_at_time = XSDDate(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDate):
            self.ended_at_time = XSDDate(self.ended_at_time)

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
    class_model_uri: ClassVar[URIRef] = KS.Agent

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

    TODO = PermissibleValue(text="TODO")

    _defn = EnumDefinition(
        name="DiagnosisType",
    )

# Slots
class slots:
    pass

slots.employed_at = Slot(uri=KS.employed_at, name="employed at", curie=KS.curie('employed_at'),
                   model_uri=KS.employed_at, domain=None, range=Optional[Union[str, CompanyId]])

slots.is_current = Slot(uri=KS.is_current, name="is current", curie=KS.curie('is_current'),
                   model_uri=KS.is_current, domain=None, range=Optional[Union[bool, Bool]])

slots.has_employment_history = Slot(uri=KS.has_employment_history, name="has employment history", curie=KS.curie('has_employment_history'),
                   model_uri=KS.has_employment_history, domain=None, range=Optional[Union[Union[dict, EmploymentEvent], List[Union[dict, EmploymentEvent]]]])

slots.has_marriage_history = Slot(uri=KS.has_marriage_history, name="has marriage history", curie=KS.curie('has_marriage_history'),
                   model_uri=KS.has_marriage_history, domain=None, range=Optional[Union[Union[dict, MarriageEvent], List[Union[dict, MarriageEvent]]]])

slots.has_medical_history = Slot(uri=KS.has_medical_history, name="has medical history", curie=KS.curie('has_medical_history'),
                   model_uri=KS.has_medical_history, domain=None, range=Optional[Union[Union[dict, MedicalEvent], List[Union[dict, MedicalEvent]]]])

slots.has_familial_relationships = Slot(uri=KS.has_familial_relationships, name="has familial relationships", curie=KS.curie('has_familial_relationships'),
                   model_uri=KS.has_familial_relationships, domain=None, range=Optional[Union[Union[dict, FamilialRelationship], List[Union[dict, FamilialRelationship]]]])

slots.married_to = Slot(uri=KS.married_to, name="married to", curie=KS.curie('married_to'),
                   model_uri=KS.married_to, domain=None, range=Optional[Union[str, PersonId]])

slots.in_location = Slot(uri=KS.in_location, name="in location", curie=KS.curie('in_location'),
                   model_uri=KS.in_location, domain=None, range=Optional[Union[str, PlaceId]])

slots.diagnosis = Slot(uri=KS.diagnosis, name="diagnosis", curie=KS.curie('diagnosis'),
                   model_uri=KS.diagnosis, domain=None, range=Optional[Union[dict, DiagnosisConcept]])

slots.procedure = Slot(uri=KS.procedure, name="procedure", curie=KS.curie('procedure'),
                   model_uri=KS.procedure, domain=None, range=Optional[Union[dict, ProcedureConcept]])

slots.addresses = Slot(uri=KS.addresses, name="addresses", curie=KS.curie('addresses'),
                   model_uri=KS.addresses, domain=None, range=Optional[Union[Union[dict, Address], List[Union[dict, Address]]]])

slots.age_in_years = Slot(uri=KS.age_in_years, name="age in years", curie=KS.curie('age_in_years'),
                   model_uri=KS.age_in_years, domain=None, range=Optional[int])

slots.related_to = Slot(uri=KS.related_to, name="related to", curie=KS.curie('related_to'),
                   model_uri=KS.related_to, domain=None, range=Optional[str])

slots.type = Slot(uri=KS.type, name="type", curie=KS.curie('type'),
                   model_uri=KS.type, domain=None, range=Optional[str])

slots.street = Slot(uri=KS.street, name="street", curie=KS.curie('street'),
                   model_uri=KS.street, domain=None, range=Optional[str])

slots.city = Slot(uri=KS.city, name="city", curie=KS.curie('city'),
                   model_uri=KS.city, domain=None, range=Optional[str])

slots.has_birth_event = Slot(uri=KS.has_birth_event, name="has birth event", curie=KS.curie('has_birth_event'),
                   model_uri=KS.has_birth_event, domain=None, range=Optional[Union[dict, BirthEvent]])

slots.id = Slot(uri=CORE.id, name="id", curie=CORE.curie('id'),
                   model_uri=KS.id, domain=None, range=URIRef)

slots.name = Slot(uri=CORE.name, name="name", curie=CORE.curie('name'),
                   model_uri=KS.name, domain=None, range=Optional[str])

slots.description = Slot(uri=CORE.description, name="description", curie=CORE.curie('description'),
                   model_uri=KS.description, domain=None, range=Optional[str])

slots.started_at_time = Slot(uri=PROV.startedAtTime, name="started at time", curie=PROV.curie('startedAtTime'),
                   model_uri=KS.started_at_time, domain=None, range=Optional[Union[str, XSDDate]])

slots.ended_at_time = Slot(uri=PROV.endedAtTime, name="ended at time", curie=PROV.curie('endedAtTime'),
                   model_uri=KS.ended_at_time, domain=None, range=Optional[Union[str, XSDDate]])

slots.was_informed_by = Slot(uri=PROV.wasInformedBy, name="was informed by", curie=PROV.curie('wasInformedBy'),
                   model_uri=KS.was_informed_by, domain=None, range=Optional[Union[str, ActivityId]])

slots.was_associated_with = Slot(uri=PROV.wasAssociatedWith, name="was associated with", curie=PROV.curie('wasAssociatedWith'),
                   model_uri=KS.was_associated_with, domain=None, range=Optional[Union[str, AgentId]])

slots.acted_on_behalf_of = Slot(uri=PROV.actedOnBehalfOf, name="acted on behalf of", curie=PROV.curie('actedOnBehalfOf'),
                   model_uri=KS.acted_on_behalf_of, domain=None, range=Optional[Union[str, AgentId]])

slots.was_generated_by = Slot(uri=PROV.wasGeneratedBy, name="was generated by", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=KS.was_generated_by, domain=None, range=Optional[Union[str, ActivityId]])

slots.used = Slot(uri=PROV.used, name="used", curie=PROV.curie('used'),
                   model_uri=KS.used, domain=Activity, range=Optional[str])

slots.activity_set = Slot(uri=CORE.activity_set, name="activity set", curie=CORE.curie('activity_set'),
                   model_uri=KS.activity_set, domain=None, range=Optional[Union[Dict[Union[str, ActivityId], Union[dict, Activity]], List[Union[dict, Activity]]]])

slots.agent_set = Slot(uri=CORE.agent_set, name="agent set", curie=CORE.curie('agent_set'),
                   model_uri=KS.agent_set, domain=None, range=Optional[Union[Dict[Union[str, AgentId], Union[dict, Agent]], List[Union[dict, Agent]]]])

slots.hasAliases__aliases = Slot(uri=KS.aliases, name="hasAliases__aliases", curie=KS.curie('aliases'),
                   model_uri=KS.hasAliases__aliases, domain=None, range=Optional[Union[str, List[str]]])

slots.company__ceo = Slot(uri=KS.ceo, name="company__ceo", curie=KS.curie('ceo'),
                   model_uri=KS.company__ceo, domain=None, range=Optional[Union[str, PersonId]])

slots.dataset__persons = Slot(uri=KS.persons, name="dataset__persons", curie=KS.curie('persons'),
                   model_uri=KS.dataset__persons, domain=None, range=Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]])

slots.dataset__companies = Slot(uri=KS.companies, name="dataset__companies", curie=KS.curie('companies'),
                   model_uri=KS.dataset__companies, domain=None, range=Optional[Union[Dict[Union[str, CompanyId], Union[dict, Company]], List[Union[dict, Company]]]])

slots.dataset__activities = Slot(uri=KS.activities, name="dataset__activities", curie=KS.curie('activities'),
                   model_uri=KS.dataset__activities, domain=None, range=Optional[Union[Dict[Union[str, ActivityId], Union[dict, Activity]], List[Union[dict, Activity]]]])

slots.fakeClass__test_attribute = Slot(uri=KS.test_attribute, name="fakeClass__test_attribute", curie=KS.curie('test_attribute'),
                   model_uri=KS.fakeClass__test_attribute, domain=None, range=Optional[str])

slots.classWithSpaces__slot_with_space_1 = Slot(uri=KS.slot_with_space_1, name="classWithSpaces__slot_with_space_1", curie=KS.curie('slot_with_space_1'),
                   model_uri=KS.classWithSpaces__slot_with_space_1, domain=None, range=Optional[str])

slots.subclassTest__slot_with_space_2 = Slot(uri=KS.slot_with_space_2, name="subclassTest__slot_with_space_2", curie=KS.curie('slot_with_space_2'),
                   model_uri=KS.subclassTest__slot_with_space_2, domain=None, range=Optional[Union[dict, ClassWithSpaces]])

slots.Person_name = Slot(uri=CORE.name, name="Person_name", curie=CORE.curie('name'),
                   model_uri=KS.Person_name, domain=Person, range=Optional[str],
                   pattern=re.compile(r'^\S+ \S+'))

slots.FamilialRelationship_type = Slot(uri=KS.type, name="FamilialRelationship_type", curie=KS.curie('type'),
                   model_uri=KS.FamilialRelationship_type, domain=FamilialRelationship, range=Union[str, "FamilialRelationshipType"])

slots.FamilialRelationship_related_to = Slot(uri=KS.related_to, name="FamilialRelationship_related to", curie=KS.curie('related_to'),
                   model_uri=KS.FamilialRelationship_related_to, domain=FamilialRelationship, range=Union[str, PersonId])