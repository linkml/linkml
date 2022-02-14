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
    

class GenderType(str, Enum):
    
    nonbinary_man = "nonbinary man"
    nonbinary_woman = "nonbinary woman"
    transgender_woman = "transgender woman"
    transgender_man = "transgender man"
    cisgender_man = "cisgender man"
    cisgender_woman = "cisgender woman"
    

class DiagnosisType(str, Enum):
    
    

@dataclass(config=PydanticConfig)
class NamedThing:
    """
    A generic grouping for any identifiable entity
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class HasAliases:
    """
    A mixin applied to any class that can have aliases/alternateNames
    """
    aliases: Optional[List[str]] = Field(None)
    


@dataclass(config=PydanticConfig)
class Person(NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    primary_email: Optional[str] = Field(None)
    birth_date: Optional[str] = Field(None)
    age_in_years: Optional[int] = Field(None, ge=0, le=999)
    gender: Optional[GenderType] = Field(None)
    current_address: Optional[Address] = Field(None, description="""The address at which a person currently lives""")
    has_employment_history: Optional[List[EmploymentEvent]] = Field(None)
    has_familial_relationships: Optional[List[FamilialRelationship]] = Field(None)
    has_medical_history: Optional[List[MedicalEvent]] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Organization(NamedThing):
    """
    An organization such as a company or university
    """
    mission_statement: Optional[str] = Field(None)
    founding_date: Optional[str] = Field(None)
    founding_location: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Place:
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(None)
    


@dataclass(config=PydanticConfig)
class Address:
    
    street: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    postal_code: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Event:
    
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    duration: Optional[float] = Field(None)
    is_current: Optional[bool] = Field(None)
    


@dataclass(config=PydanticConfig)
class Concept(NamedThing):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class DiagnosisConcept(Concept):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class ProcedureConcept(Concept):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)
    


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
    related_to: Optional[str] = Field(None)
    type: FamilialRelationshipType = Field(None)
    


@dataclass(config=PydanticConfig)
class EmploymentEvent(Event):
    
    employed_at: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    duration: Optional[float] = Field(None)
    is_current: Optional[bool] = Field(None)
    


@dataclass(config=PydanticConfig)
class MedicalEvent(Event):
    
    in_location: Optional[str] = Field(None)
    diagnosis: Optional[DiagnosisConcept] = Field(None)
    procedure: Optional[ProcedureConcept] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    duration: Optional[float] = Field(None)
    is_current: Optional[bool] = Field(None)
    


@dataclass(config=PydanticConfig)
class WithLocation:
    
    in_location: Optional[str] = Field(None)
    


@dataclass(config=PydanticConfig)
class Container:
    
    persons: Optional[List[Person]] = Field(None)
    organizations: Optional[List[Organization]] = Field(None)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
NamedThing.__pydantic_model__.update_forward_refs()
HasAliases.__pydantic_model__.update_forward_refs()
Person.__pydantic_model__.update_forward_refs()
Organization.__pydantic_model__.update_forward_refs()
Place.__pydantic_model__.update_forward_refs()
Address.__pydantic_model__.update_forward_refs()
Event.__pydantic_model__.update_forward_refs()
Concept.__pydantic_model__.update_forward_refs()
DiagnosisConcept.__pydantic_model__.update_forward_refs()
ProcedureConcept.__pydantic_model__.update_forward_refs()
Relationship.__pydantic_model__.update_forward_refs()
FamilialRelationship.__pydantic_model__.update_forward_refs()
EmploymentEvent.__pydantic_model__.update_forward_refs()
MedicalEvent.__pydantic_model__.update_forward_refs()
WithLocation.__pydantic_model__.update_forward_refs()
Container.__pydantic_model__.update_forward_refs()

