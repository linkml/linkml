from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel as PydanticBaseModel, Field

metamodel_version = "None"
version = "None"

# class IntermediateBaseModel(PydanticBaseModel):
#    __slots__ = '__weakref__'
    
class BaseModel(PydanticBaseModel,
                validate_assignment = True, 
                validate_all = True, 
                underscore_attrs_are_private = True, 
                extra = 'forbid', 
                arbitrary_types_allowed = True):
    pass                    


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
    
    

class HasAliases(BaseModel):
    
    __slots__ = '__weakref__'
    aliases: Optional[List[str]] = Field(default_factory=list)
    


class Friend(BaseModel):
    
    __slots__ = '__weakref__'
    name: Optional[str] = Field(None)
    


class Person(HasAliases):
    """
    A person, living or dead
    """
    __slots__ = '__weakref__'
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    has_employment_history: Optional[List[EmploymentEvent]] = Field(None)
    has_familial_relationships: Optional[List[FamilialRelationship]] = Field(None)
    has_medical_history: Optional[List[MedicalEvent]] = Field(None)
    age_in_years: Optional[int] = Field(None, description="""number of years since birth""", ge=0, le=999)
    addresses: Optional[List[Address]] = Field(default_factory=list)
    has_birth_event: Optional[BirthEvent] = Field(None)
    aliases: Optional[List[str]] = Field(default_factory=list)
    


class Organization(HasAliases):
    
    __slots__ = '__weakref__'
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(default_factory=list)
    


class Place(HasAliases):
    
    __slots__ = '__weakref__'
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(default_factory=list)
    


class Address(BaseModel):
    
    __slots__ = '__weakref__'
    street: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    


class Concept(BaseModel):
    
    __slots__ = '__weakref__'
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


class DiagnosisConcept(Concept):
    
    __slots__ = '__weakref__'
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


class ProcedureConcept(Concept):
    
    __slots__ = '__weakref__'
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


class Event(BaseModel):
    
    __slots__ = '__weakref__'
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class Relationship(BaseModel):
    
    __slots__ = '__weakref__'
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    


class FamilialRelationship(Relationship):
    
    __slots__ = '__weakref__'
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: str = Field(None)
    type: FamilialRelationshipType = Field(None)
    


class BirthEvent(Event):
    
    __slots__ = '__weakref__'
    in_location: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class EmploymentEvent(Event):
    
    __slots__ = '__weakref__'
    employed_at: Optional[str] = Field(None)
    type: Optional[EmploymentEventType] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class MedicalEvent(Event):
    
    __slots__ = '__weakref__'
    in_location: Optional[str] = Field(None)
    diagnosis: Optional[DiagnosisConcept] = Field(None)
    procedure: Optional[ProcedureConcept] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class WithLocation(BaseModel):
    
    __slots__ = '__weakref__'
    in_location: Optional[str] = Field(None)
    


class MarriageEvent(WithLocation, Event):
    
    __slots__ = '__weakref__'
    married_to: Optional[str] = Field(None)
    in_location: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


class Company(Organization):
    
    __slots__ = '__weakref__'
    ceo: Optional[str] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(default_factory=list)
    


class CodeSystem(BaseModel):
    
    __slots__ = '__weakref__'
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    


class Dataset(BaseModel):
    
    __slots__ = '__weakref__'
    persons: Optional[List[Person]] = Field(default_factory=list)
    companies: Optional[List[Company]] = Field(default_factory=list)
    activities: Optional[List[Activity]] = Field(default_factory=list)
    code_systems: Optional[List[CodeSystem]] = Field(None)
    


class FakeClass(BaseModel):
    
    __slots__ = '__weakref__'
    test_attribute: Optional[str] = Field(None)
    


class ClassWithSpaces(BaseModel):
    
    __slots__ = '__weakref__'
    slot_with_space_1: Optional[str] = Field(None)
    


class SubclassTest(ClassWithSpaces):
    
    __slots__ = '__weakref__'
    slot_with_space_2: Optional[ClassWithSpaces] = Field(None)
    slot_with_space_1: Optional[str] = Field(None)
    


class Activity(BaseModel):
    """
    a provence-generating activity
    """
    __slots__ = '__weakref__'
    id: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    was_informed_by: Optional[str] = Field(None)
    was_associated_with: Optional[str] = Field(None)
    used: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    


class Agent(BaseModel):
    """
    a provence-generating agent
    """
    __slots__ = '__weakref__'
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
Activity.update_forward_refs()
Agent.update_forward_refs()
