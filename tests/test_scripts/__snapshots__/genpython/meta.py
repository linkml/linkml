# Auto generated from kitchen_sink.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: kitchen_sink
#
# id: https://w3id.org/linkml/tests/kitchen_sink
# description: Kitchen Sink Schema
#
#   This schema does not do anything useful. It exists to test all features of linkml.
#
#   This particular text field exists to demonstrate markdown within a text field:
#
#   Lists:
#
#      * a
#      * b
#      * c
#
#   And links, e.g to [Person](Person.md)
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Decimal, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, Decimal, XSDDate

metamodel_version = "1.7.0"
version = None

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
BIZCODES = CurieNamespace('bizcodes', 'https://example.org/bizcodes/')
CORE = CurieNamespace('core', 'https://w3id.org/linkml/tests/core/')
DCE = CurieNamespace('dce', 'http://purl.org/dc/elements/1.1/')
KS = CurieNamespace('ks', 'https://w3id.org/linkml/tests/kitchen_sink/')
LEGO = CurieNamespace('lego', 'http://geneontology.org/lego/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = KS


# Types
class PhoneNumberType(str):
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "phone number type"
    type_model_uri = KS.PhoneNumberType


class AgeInYearsType(int):
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "age in years type"
    type_model_uri = KS.AgeInYearsType


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


class CodeSystemId(extended_str):
    pass


class ActivityId(extended_str):
    pass


class AgentId(extended_str):
    pass


@dataclass(repr=False)
class AnyOfSimpleType(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["AnyOfSimpleType"]
    class_class_curie: ClassVar[str] = "ks:AnyOfSimpleType"
    class_name: ClassVar[str] = "AnyOfSimpleType"
    class_model_uri: ClassVar[URIRef] = KS.AnyOfSimpleType

    attribute1: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.attribute1 is not None and not isinstance(self.attribute1, str):
            self.attribute1 = str(self.attribute1)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnyOfClasses(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["AnyOfClasses"]
    class_class_curie: ClassVar[str] = "ks:AnyOfClasses"
    class_name: ClassVar[str] = "AnyOfClasses"
    class_model_uri: ClassVar[URIRef] = KS.AnyOfClasses

    attribute2: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.attribute2 is not None and not isinstance(self.attribute2, str):
            self.attribute2 = str(self.attribute2)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnyOfEnums(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["AnyOfEnums"]
    class_class_curie: ClassVar[str] = "ks:AnyOfEnums"
    class_name: ClassVar[str] = "AnyOfEnums"
    class_model_uri: ClassVar[URIRef] = KS.AnyOfEnums

    attribute3: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.attribute3 is not None and not isinstance(self.attribute3, str):
            self.attribute3 = str(self.attribute3)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnyOfMix(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["AnyOfMix"]
    class_class_curie: ClassVar[str] = "ks:AnyOfMix"
    class_name: ClassVar[str] = "AnyOfMix"
    class_model_uri: ClassVar[URIRef] = KS.AnyOfMix

    attribute4: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.attribute4 is not None and not isinstance(self.attribute4, str):
            self.attribute4 = str(self.attribute4)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EqualsString(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["EqualsString"]
    class_class_curie: ClassVar[str] = "ks:EqualsString"
    class_name: ClassVar[str] = "EqualsString"
    class_model_uri: ClassVar[URIRef] = KS.EqualsString

    attribute5: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.attribute5 is not None and not isinstance(self.attribute5, str):
            self.attribute5 = str(self.attribute5)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EqualsStringIn(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["EqualsStringIn"]
    class_class_curie: ClassVar[str] = "ks:EqualsStringIn"
    class_name: ClassVar[str] = "EqualsStringIn"
    class_model_uri: ClassVar[URIRef] = KS.EqualsStringIn

    attribute6: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.attribute6 is not None and not isinstance(self.attribute6, str):
            self.attribute6 = str(self.attribute6)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HasAliases(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["HasAliases"]
    class_class_curie: ClassVar[str] = "ks:HasAliases"
    class_name: ClassVar[str] = "HasAliases"
    class_model_uri: ClassVar[URIRef] = KS.HasAliases

    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Friend(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Friend"]
    class_class_curie: ClassVar[str] = "ks:Friend"
    class_name: ClassVar[str] = "Friend"
    class_model_uri: ClassVar[URIRef] = KS.Friend

    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Person(YAMLRoot):
    """
    A person, living or dead
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Person"]
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
    species_name: Optional[str] = None
    stomach_count: Optional[int] = None
    is_living: Optional[Union[str, "LifeStatusEnum"]] = None
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

        if not isinstance(self.has_familial_relationships, list):
            self.has_familial_relationships = [self.has_familial_relationships] if self.has_familial_relationships is not None else []
        self.has_familial_relationships = [v if isinstance(v, FamilialRelationship) else FamilialRelationship(**as_dict(v)) for v in self.has_familial_relationships]

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

        if self.species_name is not None and not isinstance(self.species_name, str):
            self.species_name = str(self.species_name)

        if self.stomach_count is not None and not isinstance(self.stomach_count, int):
            self.stomach_count = int(self.stomach_count)

        if self.is_living is not None and self.is_living not in LifeStatusEnum:
            self.is_living = LifeStatusEnum(self.is_living)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Organization(YAMLRoot):
    """
    An organization.

    This description
    includes newlines

    ## Markdown headers

    * and
    * a
    * list
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Organization"]
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


@dataclass(repr=False)
class Place(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Place"]
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


@dataclass(repr=False)
class Address(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Address"]
    class_class_curie: ClassVar[str] = "ks:Address"
    class_name: ClassVar[str] = "Address"
    class_model_uri: ClassVar[URIRef] = KS.Address

    street: Optional[str] = None
    city: Optional[str] = None
    altitude: Optional[Decimal] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.street is not None and not isinstance(self.street, str):
            self.street = str(self.street)

        if self.city is not None and not isinstance(self.city, str):
            self.city = str(self.city)

        if self.altitude is not None and not isinstance(self.altitude, Decimal):
            self.altitude = Decimal(self.altitude)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Concept(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Concept"]
    class_class_curie: ClassVar[str] = "ks:Concept"
    class_name: ClassVar[str] = "Concept"
    class_model_uri: ClassVar[URIRef] = KS.Concept

    id: Union[str, ConceptId] = None
    name: Optional[str] = None
    in_code_system: Optional[Union[str, CodeSystemId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConceptId):
            self.id = ConceptId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.in_code_system is not None and not isinstance(self.in_code_system, CodeSystemId):
            self.in_code_system = CodeSystemId(self.in_code_system)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DiagnosisConcept(Concept):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["DiagnosisConcept"]
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


@dataclass(repr=False)
class ProcedureConcept(Concept):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["ProcedureConcept"]
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


@dataclass(repr=False)
class Event(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Event"]
    class_class_curie: ClassVar[str] = "ks:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = KS.Event

    started_at_time: Optional[Union[str, XSDDate]] = None
    ended_at_time: Optional[Union[str, XSDDate]] = None
    is_current: Optional[Union[bool, Bool]] = None
    metadata: Optional[Union[dict, "AnyObject"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDate):
            self.started_at_time = XSDDate(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDate):
            self.ended_at_time = XSDDate(self.ended_at_time)

        if self.is_current is not None and not isinstance(self.is_current, Bool):
            self.is_current = Bool(self.is_current)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Relationship(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Relationship"]
    class_class_curie: ClassVar[str] = "ks:Relationship"
    class_name: ClassVar[str] = "Relationship"
    class_model_uri: ClassVar[URIRef] = KS.Relationship

    started_at_time: Optional[Union[str, XSDDate]] = None
    ended_at_time: Optional[Union[str, XSDDate]] = None
    related_to: Optional[str] = None
    type: Optional[str] = None
    cordialness: Optional[Union[str, "CordialnessEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDate):
            self.started_at_time = XSDDate(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDate):
            self.ended_at_time = XSDDate(self.ended_at_time)

        if self.related_to is not None and not isinstance(self.related_to, str):
            self.related_to = str(self.related_to)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.cordialness is not None and self.cordialness not in CordialnessEnum:
            self.cordialness = CordialnessEnum(self.cordialness)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FamilialRelationship(Relationship):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["FamilialRelationship"]
    class_class_curie: ClassVar[str] = "ks:FamilialRelationship"
    class_name: ClassVar[str] = "FamilialRelationship"
    class_model_uri: ClassVar[URIRef] = KS.FamilialRelationship

    type: Union[str, "FamilialRelationshipType"] = None
    related_to: Union[str, PersonId] = None
    cordialness: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, FamilialRelationshipType):
            self.type = FamilialRelationshipType(self.type)

        if self._is_empty(self.related_to):
            self.MissingRequiredField("related_to")
        if not isinstance(self.related_to, PersonId):
            self.related_to = PersonId(self.related_to)

        if self.cordialness is not None and not isinstance(self.cordialness, str):
            self.cordialness = str(self.cordialness)

        if self.cordialness is not None and self.cordialness not in CordialnessEnum:
            self.cordialness = CordialnessEnum(self.cordialness)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BirthEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["BirthEvent"]
    class_class_curie: ClassVar[str] = "ks:BirthEvent"
    class_name: ClassVar[str] = "BirthEvent"
    class_model_uri: ClassVar[URIRef] = KS.BirthEvent

    in_location: Optional[Union[str, PlaceId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EmploymentEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["EmploymentEvent"]
    class_class_curie: ClassVar[str] = "ks:EmploymentEvent"
    class_name: ClassVar[str] = "EmploymentEvent"
    class_model_uri: ClassVar[URIRef] = KS.EmploymentEvent

    employed_at: Optional[Union[str, CompanyId]] = None
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.employed_at is not None and not isinstance(self.employed_at, CompanyId):
            self.employed_at = CompanyId(self.employed_at)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MedicalEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["MedicalEvent"]
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


@dataclass(repr=False)
class WithLocation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["WithLocation"]
    class_class_curie: ClassVar[str] = "ks:WithLocation"
    class_name: ClassVar[str] = "WithLocation"
    class_model_uri: ClassVar[URIRef] = KS.WithLocation

    in_location: Optional[Union[str, PlaceId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MarriageEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["MarriageEvent"]
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


@dataclass(repr=False)
class Company(Organization):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Company"]
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


@dataclass(repr=False)
class CodeSystem(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["CodeSystem"]
    class_class_curie: ClassVar[str] = "ks:CodeSystem"
    class_name: ClassVar[str] = "CodeSystem"
    class_model_uri: ClassVar[URIRef] = KS.CodeSystem

    id: Union[str, CodeSystemId] = None
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CodeSystemId):
            self.id = CodeSystemId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Dataset(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["Dataset"]
    class_class_curie: ClassVar[str] = "ks:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = KS.Dataset

    metadata: Optional[Union[dict, "AnyObject"]] = None
    persons: Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]] = empty_dict()
    companies: Optional[Union[Dict[Union[str, CompanyId], Union[dict, Company]], List[Union[dict, Company]]]] = empty_dict()
    activities: Optional[Union[Dict[Union[str, ActivityId], Union[dict, "Activity"]], List[Union[dict, "Activity"]]]] = empty_dict()
    code_systems: Optional[Union[Dict[Union[str, CodeSystemId], Union[dict, CodeSystem]], List[Union[dict, CodeSystem]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="persons", slot_type=Person, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="companies", slot_type=Company, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="activities", slot_type=Activity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="code_systems", slot_type=CodeSystem, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FakeClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["FakeClass"]
    class_class_curie: ClassVar[str] = "ks:FakeClass"
    class_name: ClassVar[str] = "FakeClass"
    class_model_uri: ClassVar[URIRef] = KS.FakeClass

    test_attribute: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.test_attribute is not None and not isinstance(self.test_attribute, str):
            self.test_attribute = str(self.test_attribute)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClassWithSpaces(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["ClassWithSpaces"]
    class_class_curie: ClassVar[str] = "ks:ClassWithSpaces"
    class_name: ClassVar[str] = "class with spaces"
    class_model_uri: ClassVar[URIRef] = KS.ClassWithSpaces

    slot_with_space_1: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.slot_with_space_1 is not None and not isinstance(self.slot_with_space_1, str):
            self.slot_with_space_1 = str(self.slot_with_space_1)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SubclassTest(ClassWithSpaces):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["SubclassTest"]
    class_class_curie: ClassVar[str] = "ks:SubclassTest"
    class_name: ClassVar[str] = "subclass test"
    class_model_uri: ClassVar[URIRef] = KS.SubclassTest

    slot_with_space_2: Optional[Union[dict, ClassWithSpaces]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.slot_with_space_2 is not None and not isinstance(self.slot_with_space_2, ClassWithSpaces):
            self.slot_with_space_2 = ClassWithSpaces(**as_dict(self.slot_with_space_2))

        super().__post_init__(**kwargs)


class SubSubClass2(SubclassTest):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["SubSubClass2"]
    class_class_curie: ClassVar[str] = "ks:SubSubClass2"
    class_name: ClassVar[str] = "Sub sub class 2"
    class_model_uri: ClassVar[URIRef] = KS.SubSubClass2


class TubSubClass1(SubclassTest):
    """
    Same depth as Sub sub class 1
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KS["TubSubClass1"]
    class_class_curie: ClassVar[str] = "ks:TubSubClass1"
    class_name: ClassVar[str] = "tub sub class 1"
    class_model_uri: ClassVar[URIRef] = KS.TubSubClass1


AnyObject = Any

@dataclass(repr=False)
class Activity(YAMLRoot):
    """
    a provence-generating activity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE["Activity"]
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


@dataclass(repr=False)
class Agent(YAMLRoot):
    """
    a provence-generating agent
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Agent"]
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

class EmploymentEventType(EnumDefinitionImpl):
    """
    codes for different kinds of employment/HR related events
    """
    HIRE = PermissibleValue(
        text="HIRE",
        description="event for a new employee",
        meaning=BIZCODES["001"])
    FIRE = PermissibleValue(
        text="FIRE",
        meaning=BIZCODES["002"])
    PROMOTION = PermissibleValue(
        text="PROMOTION",
        description="promotion event",
        meaning=BIZCODES["003"])
    TRANSFER = PermissibleValue(
        text="TRANSFER",
        description="transfer internally",
        meaning=BIZCODES["004"])

    _defn = EnumDefinition(
        name="EmploymentEventType",
        description="codes for different kinds of employment/HR related events",
    )

class OtherCodes(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="OtherCodes",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "a b",
            PermissibleValue(text="a b"))

class LifeStatusEnum(EnumDefinitionImpl):

    LIVING = PermissibleValue(text="LIVING")
    DEAD = PermissibleValue(text="DEAD")
    UNKNOWN = PermissibleValue(text="UNKNOWN")

    _defn = EnumDefinition(
        name="LifeStatusEnum",
    )

class CordialnessEnum(EnumDefinitionImpl):

    heartfelt = PermissibleValue(
        text="heartfelt",
        description="warm and hearty friendliness")
    hateful = PermissibleValue(
        text="hateful",
        description="spiteful")
    indifferent = PermissibleValue(
        text="indifferent",
        description="not overly friendly nor obnoxiously spiteful")

    _defn = EnumDefinition(
        name="CordialnessEnum",
    )

class KitchenStatus(EnumDefinitionImpl):

    DIRTY = PermissibleValue(text="DIRTY")
    CLEAN = PermissibleValue(text="CLEAN")

    _defn = EnumDefinition(
        name="KitchenStatus",
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

slots.in_code_system = Slot(uri=KS.in_code_system, name="in code system", curie=KS.curie('in_code_system'),
                   model_uri=KS.in_code_system, domain=None, range=Optional[Union[str, CodeSystemId]])

slots.metadata = Slot(uri=KS.metadata, name="metadata", curie=KS.curie('metadata'),
                   model_uri=KS.metadata, domain=None, range=Optional[Union[dict, AnyObject]])

slots.species_name = Slot(uri=KS.species_name, name="species name", curie=KS.curie('species_name'),
                   model_uri=KS.species_name, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[A-Z]+[a-z]+(-[A-Z]+[a-z]+)?\\.[A-Z]+(-[0-9]{4})?$'))

slots.stomach_count = Slot(uri=KS.stomach_count, name="stomach count", curie=KS.curie('stomach_count'),
                   model_uri=KS.stomach_count, domain=None, range=Optional[int])

slots.tree_slot_A = Slot(uri=KS.A, name="tree_slot_A", curie=KS.curie('A'),
                   model_uri=KS.tree_slot_A, domain=None, range=Optional[str])

slots.tree_slot_B = Slot(uri=KS.B, name="tree_slot_B", curie=KS.curie('B'),
                   model_uri=KS.tree_slot_B, domain=None, range=Optional[str])

slots.tree_slot_C = Slot(uri=KS.C, name="tree_slot_C", curie=KS.curie('C'),
                   model_uri=KS.tree_slot_C, domain=None, range=Optional[str])

slots.mixin_slot_I = Slot(uri=KS.mixin_slot_I, name="mixin_slot_I", curie=KS.curie('mixin_slot_I'),
                   model_uri=KS.mixin_slot_I, domain=None, range=Optional[str])

slots.life_status = Slot(uri=KS.life_status, name="life_status", curie=KS.curie('life_status'),
                   model_uri=KS.life_status, domain=None, range=Optional[Union[str, "LifeStatusEnum"]])

slots.cordialness = Slot(uri=KS.cordialness, name="cordialness", curie=KS.curie('cordialness'),
                   model_uri=KS.cordialness, domain=None, range=Optional[str])

slots.altitude = Slot(uri=KS.altitude, name="altitude", curie=KS.curie('altitude'),
                   model_uri=KS.altitude, domain=None, range=Optional[Decimal])

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

slots.anyOfSimpleType__attribute1 = Slot(uri=KS.attribute1, name="anyOfSimpleType__attribute1", curie=KS.curie('attribute1'),
                   model_uri=KS.anyOfSimpleType__attribute1, domain=None, range=Optional[str])

slots.anyOfClasses__attribute2 = Slot(uri=KS.attribute2, name="anyOfClasses__attribute2", curie=KS.curie('attribute2'),
                   model_uri=KS.anyOfClasses__attribute2, domain=None, range=Optional[str])

slots.anyOfEnums__attribute3 = Slot(uri=KS.attribute3, name="anyOfEnums__attribute3", curie=KS.curie('attribute3'),
                   model_uri=KS.anyOfEnums__attribute3, domain=None, range=Optional[str])

slots.anyOfMix__attribute4 = Slot(uri=KS.attribute4, name="anyOfMix__attribute4", curie=KS.curie('attribute4'),
                   model_uri=KS.anyOfMix__attribute4, domain=None, range=Optional[str])

slots.equalsString__attribute5 = Slot(uri=KS.attribute5, name="equalsString__attribute5", curie=KS.curie('attribute5'),
                   model_uri=KS.equalsString__attribute5, domain=None, range=Optional[str])

slots.equalsStringIn__attribute6 = Slot(uri=KS.attribute6, name="equalsStringIn__attribute6", curie=KS.curie('attribute6'),
                   model_uri=KS.equalsStringIn__attribute6, domain=None, range=Optional[str])

slots.hasAliases__aliases = Slot(uri=SKOS.altLabel, name="hasAliases__aliases", curie=SKOS.curie('altLabel'),
                   model_uri=KS.hasAliases__aliases, domain=None, range=Optional[Union[str, List[str]]])

slots.person__is_living = Slot(uri=KS.is_living, name="person__is_living", curie=KS.curie('is_living'),
                   model_uri=KS.person__is_living, domain=None, range=Optional[Union[str, "LifeStatusEnum"]])

slots.company__ceo = Slot(uri=SCHEMA.ceo, name="company__ceo", curie=SCHEMA.curie('ceo'),
                   model_uri=KS.company__ceo, domain=None, range=Optional[Union[str, PersonId]])

slots.dataset__persons = Slot(uri=KS.persons, name="dataset__persons", curie=KS.curie('persons'),
                   model_uri=KS.dataset__persons, domain=None, range=Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]])

slots.dataset__companies = Slot(uri=KS.companies, name="dataset__companies", curie=KS.curie('companies'),
                   model_uri=KS.dataset__companies, domain=None, range=Optional[Union[Dict[Union[str, CompanyId], Union[dict, Company]], List[Union[dict, Company]]]])

slots.dataset__activities = Slot(uri=KS.activities, name="dataset__activities", curie=KS.curie('activities'),
                   model_uri=KS.dataset__activities, domain=None, range=Optional[Union[Dict[Union[str, ActivityId], Union[dict, Activity]], List[Union[dict, Activity]]]])

slots.dataset__code_systems = Slot(uri=KS.code_systems, name="dataset__code_systems", curie=KS.curie('code_systems'),
                   model_uri=KS.dataset__code_systems, domain=None, range=Optional[Union[Dict[Union[str, CodeSystemId], Union[dict, CodeSystem]], List[Union[dict, CodeSystem]]]])

slots.fakeClass__test_attribute = Slot(uri=KS.test_attribute, name="fakeClass__test_attribute", curie=KS.curie('test_attribute'),
                   model_uri=KS.fakeClass__test_attribute, domain=None, range=Optional[str])

slots.classWithSpaces__slot_with_space_1 = Slot(uri=KS.slot_with_space_1, name="classWithSpaces__slot_with_space_1", curie=KS.curie('slot_with_space_1'),
                   model_uri=KS.classWithSpaces__slot_with_space_1, domain=None, range=Optional[str])

slots.subclassTest__slot_with_space_2 = Slot(uri=KS.slot_with_space_2, name="subclassTest__slot_with_space_2", curie=KS.curie('slot_with_space_2'),
                   model_uri=KS.subclassTest__slot_with_space_2, domain=None, range=Optional[Union[dict, ClassWithSpaces]])

slots.Person_name = Slot(uri=CORE.name, name="Person_name", curie=CORE.curie('name'),
                   model_uri=KS.Person_name, domain=Person, range=Optional[str],
                   pattern=re.compile(r'^\S+ \S+$'))

slots.Person_species_name = Slot(uri=KS.species_name, name="Person_species name", curie=KS.curie('species_name'),
                   model_uri=KS.Person_species_name, domain=Person, range=Optional[str],
                   pattern=re.compile(r'^[A-Z]+[a-z]+(-[A-Z]+[a-z]+)?\\.[A-Z]+(-[0-9]{4})?$'))

slots.Person_stomach_count = Slot(uri=KS.stomach_count, name="Person_stomach count", curie=KS.curie('stomach_count'),
                   model_uri=KS.Person_stomach_count, domain=Person, range=Optional[int])

slots.Relationship_cordialness = Slot(uri=KS.cordialness, name="Relationship_cordialness", curie=KS.curie('cordialness'),
                   model_uri=KS.Relationship_cordialness, domain=Relationship, range=Optional[Union[str, "CordialnessEnum"]])

slots.FamilialRelationship_type = Slot(uri=KS.type, name="FamilialRelationship_type", curie=KS.curie('type'),
                   model_uri=KS.FamilialRelationship_type, domain=FamilialRelationship, range=Union[str, "FamilialRelationshipType"])

slots.FamilialRelationship_related_to = Slot(uri=KS.related_to, name="FamilialRelationship_related to", curie=KS.curie('related_to'),
                   model_uri=KS.FamilialRelationship_related_to, domain=FamilialRelationship, range=Union[str, PersonId])

slots.FamilialRelationship_cordialness = Slot(uri=KS.cordialness, name="FamilialRelationship_cordialness", curie=KS.curie('cordialness'),
                   model_uri=KS.FamilialRelationship_cordialness, domain=FamilialRelationship, range=Optional[Union[str, "CordialnessEnum"]])

slots.EmploymentEvent_type = Slot(uri=KS.type, name="EmploymentEvent_type", curie=KS.curie('type'),
                   model_uri=KS.EmploymentEvent_type, domain=EmploymentEvent, range=Optional[str])
