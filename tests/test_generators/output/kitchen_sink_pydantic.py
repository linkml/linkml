from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

metamodel_version = "None"
version = "None"

# Pydantic config and validators
class PydanticConfig:
    """ Pydantic config https://pydantic-docs.helpmanual.io/usage/model_config/ """

    validate_assignment = True
    validate_all = True
    underscore_attrs_are_private = True
    extra = 'forbid'
    arbitrary_types_allowed = True  # TODO re-evaluate this


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
    
    

@dataclass(config=PydanticConfig)
class HasAliases:
    
    aliases: Optional[List[str]] = Field(None)
    


@dataclass(config=PydanticConfig)
class Friend:
    
    name: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Person:
    """
    A person, living or dead
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    has_employment_history: Optional[List[EmploymentEvent]] = Field(None)
    has_familial_relationships: Optional[List[FamilialRelationship]] = Field(None)
    has_medical_history: Optional[List[MedicalEvent]] = Field(None)
    age_in_years: Optional[int] = Field(None, description="""number of years since birth""", ge=0, le=999)
    addresses: Optional[List[Address]] = Field(None)
    has_birth_event: Optional[BirthEvent] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    


@dataclass(config=PydanticConfig)
class Organization:
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    


@dataclass(config=PydanticConfig)
class Place:
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    


@dataclass(config=PydanticConfig)
class Address:
    
    street: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Concept:
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class DiagnosisConcept(Concept):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class ProcedureConcept(Concept):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    in_code_system: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Event:
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


@dataclass(config=PydanticConfig)
class Relationship:
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class FamilialRelationship(Relationship):
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: str = Field(None)
    type: FamilialRelationshipType = Field(None)
    


@dataclass(config=PydanticConfig)
class BirthEvent(Event):
    
    in_location: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


@dataclass(config=PydanticConfig)
class EmploymentEvent(Event):
    
    employed_at: Optional[str] = Field(None)
    type: Optional[EmploymentEventType] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


@dataclass(config=PydanticConfig)
class MedicalEvent(Event):
    
    in_location: Optional[str] = Field(None)
    diagnosis: Optional[DiagnosisConcept] = Field(None)
    procedure: Optional[ProcedureConcept] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


@dataclass(config=PydanticConfig)
class WithLocation:
    
    in_location: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class MarriageEvent(Event):
    
    married_to: Optional[str] = Field(None)
    in_location: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    is_current: Optional[bool] = Field(None)
    metadata: Optional[Any] = Field(None, description="""Example of a slot that has an unconstrained range""")
    


@dataclass(config=PydanticConfig)
class Company(Organization):
    
    ceo: Optional[str] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    


@dataclass(config=PydanticConfig)
class CodeSystem:
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Dataset:
    
    persons: Optional[List[Person]] = Field(None)
    companies: Optional[List[Company]] = Field(None)
    activities: Optional[List[Activity]] = Field(None)
    code_systems: Optional[List[CodeSystem]] = Field(None)
    


@dataclass(config=PydanticConfig)
class FakeClass:
    
    test_attribute: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class ClassWithSpaces:
    
    slot_with_space_1: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class SubclassTest(ClassWithSpaces):
    
    slot_with_space_2: Optional[ClassWithSpaces] = Field(None)
    slot_with_space_1: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Activity:
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
    


@dataclass(config=PydanticConfig)
class Agent:
    """
    a provence-generating agent
    """
    id: Optional[str] = Field(None)
    acted_on_behalf_of: Optional[str] = Field(None)
    was_informed_by: Optional[str] = Field(None)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
HasAliases.__pydantic_model__.update_forward_refs()
Friend.__pydantic_model__.update_forward_refs()
Person.__pydantic_model__.update_forward_refs()
Organization.__pydantic_model__.update_forward_refs()
Place.__pydantic_model__.update_forward_refs()
Address.__pydantic_model__.update_forward_refs()
Concept.__pydantic_model__.update_forward_refs()
DiagnosisConcept.__pydantic_model__.update_forward_refs()
ProcedureConcept.__pydantic_model__.update_forward_refs()
Event.__pydantic_model__.update_forward_refs()
Relationship.__pydantic_model__.update_forward_refs()
FamilialRelationship.__pydantic_model__.update_forward_refs()
BirthEvent.__pydantic_model__.update_forward_refs()
EmploymentEvent.__pydantic_model__.update_forward_refs()
MedicalEvent.__pydantic_model__.update_forward_refs()
WithLocation.__pydantic_model__.update_forward_refs()
MarriageEvent.__pydantic_model__.update_forward_refs()
Company.__pydantic_model__.update_forward_refs()
CodeSystem.__pydantic_model__.update_forward_refs()
Dataset.__pydantic_model__.update_forward_refs()
FakeClass.__pydantic_model__.update_forward_refs()
ClassWithSpaces.__pydantic_model__.update_forward_refs()
SubclassTest.__pydantic_model__.update_forward_refs()
Activity.__pydantic_model__.update_forward_refs()
Agent.__pydantic_model__.update_forward_refs()
