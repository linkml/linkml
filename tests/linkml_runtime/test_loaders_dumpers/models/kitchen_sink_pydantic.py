from __future__ import annotations
from datetime import date
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel as BaseModel, Field

metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel):
    __signature__ = {
        "validate_assignment": True,
        "validate_all": True,
        "underscore_attrs_are_private": True,
        "extra": 'forbid',
        "arbitrary_types_allowed": True,
        "use_enum_values": True
    }


class FamilialRelationshipType(str, Enum):
    
    SIBLING_OF = "SIBLING_OF"
    PARENT_OF = "PARENT_OF"
    CHILD_OF = "CHILD_OF"
    
    

class DiagnosisType(str, Enum):
    
    TODO = "TODO"
    
    

class EmploymentEventType(str, Enum):
    
    HIRE = "HIRE"
    FIRE = "FIRE"
    PROMOTION = "PROMOTION"
    TRANSFER = "TRANSFER"
    
    

class OtherCodes(str, Enum):
    
    a_b = "a b"
    
    

class LifeStatusEnum(str, Enum):
    
    LIVING = "LIVING"
    DEAD = "DEAD"
    UNKNOWN = "UNKNOWN"
    
    

class HasAliases(ConfiguredBaseModel):
    
    aliases: Optional[list[str]] = Field(default_factory=list)
    


class Friend(ConfiguredBaseModel):
    
    name: Optional[str] = Field(None)
    


class Person(HasAliases):
    """
    A person, living or dead
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    has_employment_history: Optional[list[EmploymentEvent]] = Field(None)
    has_familial_relationships: Optional[list[FamilialRelationship]] = Field(None)
    has_medical_history: Optional[list[MedicalEvent]] = Field(None)
    age_in_years: Optional[int] = Field(None, description="""number of years since birth""", ge=0, le=999)
    addresses: Optional[list[Address]] = Field(default_factory=list)
    has_birth_event: Optional[BirthEvent] = Field(None)
    species_name: Optional[str] = Field(None)
    stomach_count: Optional[int] = Field(None)
    is_living: Optional[LifeStatusEnum] = Field(None)
    aliases: Optional[list[str]] = Field(default_factory=list)
    


class Organization(HasAliases):
    """
    An organization.

This description
includes newlines

## Markdown headers

 * and
 * a
 * list
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[list[str]] = Field(default_factory=list)
    


class Place(HasAliases):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[list[str]] = Field(default_factory=list)
    


class Address(ConfiguredBaseModel):
    
    street: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    


class Concept(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


class DiagnosisConcept(Concept):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


class ProcedureConcept(Concept):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


class Event(ConfiguredBaseModel):
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class Relationship(ConfiguredBaseModel):
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    


class FamilialRelationship(Relationship):
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: str = Field(...)
    type: FamilialRelationshipType = Field(...)
    


class BirthEvent(Event):
    
    in_location: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class EmploymentEvent(Event):
    
    employed_at: Optional[str] = Field(None)
    type: Optional[EmploymentEventType] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class MedicalEvent(Event):
    
    in_location: Optional[str] = Field(None)
    diagnosis: Optional[DiagnosisConcept] = Field(None)
    procedure: Optional[ProcedureConcept] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class WithLocation(ConfiguredBaseModel):
    
    in_location: Optional[str] = Field(None)
    


class MarriageEvent(WithLocation, Event):
    
    married_to: Optional[str] = Field(None)
    in_location: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class Company(Organization):
    
    ceo: Optional[str] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[list[str]] = Field(default_factory=list)
    


class CodeSystem(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    


class Dataset(ConfiguredBaseModel):
    
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    persons: Optional[list[Person]] = Field(default_factory=list)
    companies: Optional[list[Company]] = Field(default_factory=list)
    activities: Optional[list[Activity]] = Field(default_factory=list)
    code_systems: Optional[dict[str, CodeSystem]] = Field(None)
    


class FakeClass(ConfiguredBaseModel):
    
    test_attribute: Optional[str] = Field(None)
    


class ClassWithSpaces(ConfiguredBaseModel):
    
    slot_with_space_1: Optional[str] = Field(None)
    


class SubclassTest(ClassWithSpaces):
    
    slot_with_space_2: Optional[ClassWithSpaces] = Field(None)
    slot_with_space_1: Optional[str] = Field(None)
    


class SubSubClass2(SubclassTest):
    
    slot_with_space_2: Optional[ClassWithSpaces] = Field(None)
    slot_with_space_1: Optional[str] = Field(None)
    


class TubSubClass1(SubclassTest):
    """
    Same depth as Sub sub class 1
    """
    slot_with_space_2: Optional[ClassWithSpaces] = Field(None)
    slot_with_space_1: Optional[str] = Field(None)
    


class Activity(ConfiguredBaseModel):
    """
    a provence-generating activity
    """
    id: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    was_informed_by: Optional[str] = Field(None)
    was_associated_with: Optional[str] = Field(None)
    used: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    


class Agent(ConfiguredBaseModel):
    """
    a provence-generating agent
    """
    id: Optional[str] = Field(None)
    acted_on_behalf_of: Optional[str] = Field(None)
    was_informed_by: Optional[str] = Field(None)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
HasAliases.update_forward_refs()
Friend.update_forward_refs()
Person.update_forward_refs()
Organization.update_forward_refs()
Place.update_forward_refs()
Address.update_forward_refs()
Concept.update_forward_refs()
DiagnosisConcept.update_forward_refs()
ProcedureConcept.update_forward_refs()
Event.update_forward_refs()
Relationship.update_forward_refs()
FamilialRelationship.update_forward_refs()
BirthEvent.update_forward_refs()
EmploymentEvent.update_forward_refs()
MedicalEvent.update_forward_refs()
WithLocation.update_forward_refs()
MarriageEvent.update_forward_refs()
Company.update_forward_refs()
CodeSystem.update_forward_refs()
Dataset.update_forward_refs()
FakeClass.update_forward_refs()
ClassWithSpaces.update_forward_refs()
SubclassTest.update_forward_refs()
SubSubClass2.update_forward_refs()
TubSubClass1.update_forward_refs()
Activity.update_forward_refs()
Agent.update_forward_refs()

