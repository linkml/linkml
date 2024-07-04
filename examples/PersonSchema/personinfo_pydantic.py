from __future__ import annotations
from datetime import (
    datetime,
    date
)
from decimal import Decimal
from enum import Enum
import re
from typing import (
    Any,
    List,
    Literal,
    Dict,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)

metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True)
    pass


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


class DiagnosisType(str):
    pass


class NamedThing(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity
    """
    id: str = Field(...)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class HasAliases(ConfiguredBaseModel):
    """
    A mixin applied to any class that can have aliases/alternateNames
    """
    aliases: Optional[List[str]] = Field(default_factory=list)


class Person(HasAliases, NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    primary_email: Optional[str] = Field(None)
    birth_date: Optional[str] = Field(None)
    age_in_years: Optional[int] = Field(None, ge=0, le=999)
    gender: Optional[GenderType] = Field(None)
    current_address: Optional[Address] = Field(None, description="""The address at which a person currently lives""")
    has_employment_history: Optional[List[EmploymentEvent]] = Field(default_factory=list)
    has_familial_relationships: Optional[List[FamilialRelationship]] = Field(default_factory=list)
    has_medical_history: Optional[List[MedicalEvent]] = Field(default_factory=list)
    aliases: Optional[List[str]] = Field(default_factory=list)
    id: str = Field(...)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)

    @field_validator('primary_email')
    def pattern_primary_email(cls, v):
        pattern=re.compile(r"^\S+@[\S+\.]+\S+")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid primary_email format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid primary_email format: {v}")
        return v


class Organization(HasAliases, NamedThing):
    """
    An organization such as a company or university
    """
    mission_statement: Optional[str] = Field(None)
    founding_date: Optional[str] = Field(None)
    founding_location: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(default_factory=list)
    id: str = Field(...)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class Place(HasAliases):
    id: str = Field(...)
    name: Optional[str] = Field(None)
    aliases: Optional[List[str]] = Field(default_factory=list)


class Address(ConfiguredBaseModel):
    street: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    postal_code: Optional[str] = Field(None)


class Event(ConfiguredBaseModel):
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    duration: Optional[float] = Field(None)
    is_current: Optional[bool] = Field(None)


class Concept(NamedThing):
    id: str = Field(...)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class DiagnosisConcept(Concept):
    id: str = Field(...)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class ProcedureConcept(Concept):
    id: str = Field(...)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


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


class EmploymentEvent(Event):
    employed_at: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    duration: Optional[float] = Field(None)
    is_current: Optional[bool] = Field(None)


class MedicalEvent(Event):
    in_location: Optional[str] = Field(None)
    diagnosis: Optional[DiagnosisConcept] = Field(None)
    procedure: Optional[ProcedureConcept] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    duration: Optional[float] = Field(None)
    is_current: Optional[bool] = Field(None)


class WithLocation(ConfiguredBaseModel):
    in_location: Optional[str] = Field(None)


class Container(ConfiguredBaseModel):
    persons: Optional[List[Person]] = Field(default_factory=list)
    organizations: Optional[List[Organization]] = Field(default_factory=list)


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
NamedThing.model_rebuild()
HasAliases.model_rebuild()
Person.model_rebuild()
Organization.model_rebuild()
Place.model_rebuild()
Address.model_rebuild()
Event.model_rebuild()
Concept.model_rebuild()
DiagnosisConcept.model_rebuild()
ProcedureConcept.model_rebuild()
Relationship.model_rebuild()
FamilialRelationship.model_rebuild()
EmploymentEvent.model_rebuild()
MedicalEvent.model_rebuild()
WithLocation.model_rebuild()
Container.model_rebuild()
