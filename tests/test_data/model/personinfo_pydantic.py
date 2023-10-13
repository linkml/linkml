from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel as BaseModel
from pydantic import Field

metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(
    WeakRefShimBaseModel,
    validate_assignment=True,
    validate_all=True,
    underscore_attrs_are_private=True,
    extra="forbid",
    arbitrary_types_allowed=True,
):
    pass


class FamilialRelationshipType(str, Enum):
    SIBLING_OF = "SIBLING_OF"
    PARENT_OF = "PARENT_OF"
    CHILD_OF = "CHILD_OF"


class GenderType(str, Enum):
    nonbinary_man = "nonbinary_man"
    nonbinary_woman = "nonbinary_woman"
    transgender_woman = "transgender_woman"
    transgender_man = "transgender_man"
    cisgender_man = "cisgender_man"
    cisgender_woman = "cisgender_woman"


class DiagnosisType(str, Enum):
    dummy = "dummy"


class NamedThing(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity
    """

    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class HasAliases(ConfiguredBaseModel):
    """
    A mixin applied to any class that can have aliases/alternateNames
    """

    aliases: Optional[List[str]] = Field(default_factory=list)


class HasNewsEvents(ConfiguredBaseModel):
    has_news_events: Optional[List[NewsEvent]] = Field(default_factory=list)


class Person(HasNewsEvents, HasAliases, NamedThing):
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
    has_news_events: Optional[List[NewsEvent]] = Field(default_factory=list)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class Organization(HasNewsEvents, HasAliases, NamedThing):
    """
    An organization such as a company or university
    """

    mission_statement: Optional[str] = Field(None)
    founding_date: Optional[str] = Field(None)
    founding_location: Optional[str] = Field(None)
    current_address: Optional[Address] = Field(None, description="""The address at which a person currently lives""")
    aliases: Optional[List[str]] = Field(default_factory=list)
    has_news_events: Optional[List[NewsEvent]] = Field(default_factory=list)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class Place(HasAliases):
    id: Optional[str] = Field(None)
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
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class DiagnosisConcept(Concept):
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class ProcedureConcept(Concept):
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class Relationship(ConfiguredBaseModel):
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: Optional[str] = Field(None)
    type: Optional[FamilialRelationshipType] = Field(None)


class FamilialRelationship(Relationship):
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    related_to: str = Field(None)
    type: FamilialRelationshipType = Field(None)


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


class NewsEvent(Event):
    headline: Optional[str] = Field(None)
    started_at_time: Optional[date] = Field(None)
    ended_at_time: Optional[date] = Field(None)
    duration: Optional[float] = Field(None)
    is_current: Optional[bool] = Field(None)


class WithLocation(ConfiguredBaseModel):
    in_location: Optional[str] = Field(None)


class BiologicalSpecimen(NamedThing):
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image: Optional[str] = Field(None)


class Container(ConfiguredBaseModel):
    name: Optional[str] = Field(None)
    persons: Optional[List[Person]] = Field(default_factory=list)
    organizations: Optional[List[Organization]] = Field(default_factory=list)
    places: Optional[List[Place]] = Field(default_factory=list)


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
NamedThing.update_forward_refs()
HasAliases.update_forward_refs()
HasNewsEvents.update_forward_refs()
Person.update_forward_refs()
Organization.update_forward_refs()
Place.update_forward_refs()
Address.update_forward_refs()
Event.update_forward_refs()
Concept.update_forward_refs()
DiagnosisConcept.update_forward_refs()
ProcedureConcept.update_forward_refs()
Relationship.update_forward_refs()
FamilialRelationship.update_forward_refs()
EmploymentEvent.update_forward_refs()
MedicalEvent.update_forward_refs()
NewsEvent.update_forward_refs()
WithLocation.update_forward_refs()
BiologicalSpecimen.update_forward_refs()
Container.update_forward_refs()
