from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class FamilialRelationshipType(str, Enum):
    
    SIBLING_OF = "SIBLING_OF"
    PARENT_OF = "PARENT_OF"
    CHILD_OF = "CHILD_OF"
    

class DiagnosisType(str, Enum):
    
    TODO = "TODO"
    



class HasAliases(BaseModel):
    
    aliases: Optional[List[str]] = Field(None)
    
    

class Friend(BaseModel):
    
    name: Optional[str] = Field(None)
    
    

class Person(BaseModel):
    """
    A person, living or dead
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    has_employment_history: Optional[List[EmploymentEvent]] = Field(None)
    has_familial_relationships: Optional[List[FamilialRelationship]] = Field(None)
    has_medical_history: Optional[List[MedicalEvent]] = Field(None)
    age_in_years: Optional[int] = Field(None, description="number of years since birth", ge=0, le=999)
    addresses: Optional[List[Address]] = Field(None)
    has_birth_event: Optional[BirthEvent] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    
    

class Organization(BaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    
    

class Place(BaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    
    

class Address(BaseModel):
    
    street: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    
    

class Concept(BaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    
    

class DiagnosisConcept(Concept):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    
    

class ProcedureConcept(Concept):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    
    

class Event(BaseModel):
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    
    

class Relationship(BaseModel):
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: str = Field(None)
    type: FamilialRelationshipType = Field(None)
    
    

class FamilialRelationship(Relationship):
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: str = Field(None)
    type: FamilialRelationshipType = Field(None)
    
    

class BirthEvent(Event):
    
    in_location: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    
    

class EmploymentEvent(Event):
    
    employed_at: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    
    

class MedicalEvent(Event):
    
    in_location: Optional[str] = Field(None)
    diagnosis: Optional[DiagnosisConcept] = Field(None)
    procedure: Optional[ProcedureConcept] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    
    

class WithLocation(BaseModel):
    
    in_location: Optional[str] = Field(None)
    
    

class MarriageEvent(Event):
    
    married_to: Optional[str] = Field(None)
    in_location: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    
    

class Company(Organization):
    
    ceo: Optional[str] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    
    

class Dataset(BaseModel):
    
    persons: Optional[List[Person]] = Field(None)
    companies: Optional[List[Company]] = Field(None)
    activities: Optional[List[Activity]] = Field(None)
    
    

class FakeClass(BaseModel):
    
    test_attribute: Optional[str] = Field(None)
    
    

class ClassWithSpaces(BaseModel):
    
    slot_with_space_1: Optional[str] = Field(None)
    
    

class SubclassTest(ClassWithSpaces):
    
    slot_with_space_2: Optional[ClassWithSpaces] = Field(None)
    slot_with_space_1: Optional[str] = Field(None)
    
    

class Activity(BaseModel):
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
    
    

class Agent(BaseModel):
    """
    a provence-generating agent
    """
    id: Optional[str] = Field(None)
    acted_on_behalf_of: Optional[str] = Field(None)
    was_informed_by: Optional[str] = Field(None)
    
    



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

Dataset.update_forward_refs()

FakeClass.update_forward_refs()

ClassWithSpaces.update_forward_refs()

SubclassTest.update_forward_refs()

Activity.update_forward_refs()

Agent.update_forward_refs()
