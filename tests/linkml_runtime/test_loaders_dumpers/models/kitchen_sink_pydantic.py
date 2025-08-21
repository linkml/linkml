from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel as BaseModel
from pydantic import Field

metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(WeakRefShimBaseModel):
    __signature__ = {
        "validate_assignment": True,
        "validate_all": True,
        "underscore_attrs_are_private": True,
        "extra": "forbid",
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
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
    aliases: list[str] | None = Field(default_factory=list)


class Friend(ConfiguredBaseModel):
    name: str | None = Field(None)


class Person(HasAliases):
    """
    A person, living or dead
    """

    id: str | None = Field(None)
    name: str | None = Field(None)
    has_employment_history: list[EmploymentEvent] | None = Field(None)
    has_familial_relationships: list[FamilialRelationship] | None = Field(None)
    has_medical_history: list[MedicalEvent] | None = Field(None)
    age_in_years: int | None = Field(None, description="""number of years since birth""", ge=0, le=999)
    addresses: list[Address] | None = Field(default_factory=list)
    has_birth_event: BirthEvent | None = Field(None)
    species_name: str | None = Field(None)
    stomach_count: int | None = Field(None)
    is_living: LifeStatusEnum | None = Field(None)
    aliases: list[str] | None = Field(default_factory=list)


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

    id: str | None = Field(None)
    name: str | None = Field(None)
    aliases: list[str] | None = Field(default_factory=list)


class Place(HasAliases):
    id: str | None = Field(None)
    name: str | None = Field(None)
    aliases: list[str] | None = Field(default_factory=list)


class Address(ConfiguredBaseModel):
    street: str | None = Field(None)
    city: str | None = Field(None)


class Concept(ConfiguredBaseModel):
    id: str | None = Field(None)
    name: str | None = Field(None)
    in_code_system: str | None = Field(None)


class DiagnosisConcept(Concept):
    id: str | None = Field(None)
    name: str | None = Field(None)
    in_code_system: str | None = Field(None)


class ProcedureConcept(Concept):
    id: str | None = Field(None)
    name: str | None = Field(None)
    in_code_system: str | None = Field(None)


class Event(ConfiguredBaseModel):
    started_at_time: date | None = Field(None)
    ended_at_time: date | None = Field(None)
    is_current: bool | None = Field(None)
    metadata: Any | None = Field(None, description="""Example of a slot that has an unconstrained range""")


class Relationship(ConfiguredBaseModel):
    started_at_time: date | None = Field(None)
    ended_at_time: date | None = Field(None)
    related_to: str | None = Field(None)
    type: str | None = Field(None)


class FamilialRelationship(Relationship):
    started_at_time: date | None = Field(None)
    ended_at_time: date | None = Field(None)
    related_to: str = Field(...)
    type: FamilialRelationshipType = Field(...)


class BirthEvent(Event):
    in_location: str | None = Field(None)
    started_at_time: date | None = Field(None)
    ended_at_time: date | None = Field(None)
    is_current: bool | None = Field(None)
    metadata: Any | None = Field(None, description="""Example of a slot that has an unconstrained range""")


class EmploymentEvent(Event):
    employed_at: str | None = Field(None)
    type: EmploymentEventType | None = Field(None)
    started_at_time: date | None = Field(None)
    ended_at_time: date | None = Field(None)
    is_current: bool | None = Field(None)
    metadata: Any | None = Field(None, description="""Example of a slot that has an unconstrained range""")


class MedicalEvent(Event):
    in_location: str | None = Field(None)
    diagnosis: DiagnosisConcept | None = Field(None)
    procedure: ProcedureConcept | None = Field(None)
    started_at_time: date | None = Field(None)
    ended_at_time: date | None = Field(None)
    is_current: bool | None = Field(None)
    metadata: Any | None = Field(None, description="""Example of a slot that has an unconstrained range""")


class WithLocation(ConfiguredBaseModel):
    in_location: str | None = Field(None)


class MarriageEvent(WithLocation, Event):
    married_to: str | None = Field(None)
    in_location: str | None = Field(None)
    started_at_time: date | None = Field(None)
    ended_at_time: date | None = Field(None)
    is_current: bool | None = Field(None)
    metadata: Any | None = Field(None, description="""Example of a slot that has an unconstrained range""")


class Company(Organization):
    ceo: str | None = Field(None)
    id: str | None = Field(None)
    name: str | None = Field(None)
    aliases: list[str] | None = Field(default_factory=list)


class CodeSystem(ConfiguredBaseModel):
    id: str | None = Field(None)
    name: str | None = Field(None)


class Dataset(ConfiguredBaseModel):
    metadata: Any | None = Field(None, description="""Example of a slot that has an unconstrained range""")
    persons: list[Person] | None = Field(default_factory=list)
    companies: list[Company] | None = Field(default_factory=list)
    activities: list[Activity] | None = Field(default_factory=list)
    code_systems: dict[str, CodeSystem] | None = Field(None)


class FakeClass(ConfiguredBaseModel):
    test_attribute: str | None = Field(None)


class ClassWithSpaces(ConfiguredBaseModel):
    slot_with_space_1: str | None = Field(None)


class SubclassTest(ClassWithSpaces):
    slot_with_space_2: ClassWithSpaces | None = Field(None)
    slot_with_space_1: str | None = Field(None)


class SubSubClass2(SubclassTest):
    slot_with_space_2: ClassWithSpaces | None = Field(None)
    slot_with_space_1: str | None = Field(None)


class TubSubClass1(SubclassTest):
    """
    Same depth as Sub sub class 1
    """

    slot_with_space_2: ClassWithSpaces | None = Field(None)
    slot_with_space_1: str | None = Field(None)


class Activity(ConfiguredBaseModel):
    """
    a provence-generating activity
    """

    id: str | None = Field(None)
    started_at_time: date | None = Field(None)
    ended_at_time: date | None = Field(None)
    was_informed_by: str | None = Field(None)
    was_associated_with: str | None = Field(None)
    used: str | None = Field(None)
    description: str | None = Field(None)


class Agent(ConfiguredBaseModel):
    """
    a provence-generating agent
    """

    id: str | None = Field(None)
    acted_on_behalf_of: str | None = Field(None)
    was_informed_by: str | None = Field(None)


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
