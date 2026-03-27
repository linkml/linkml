
from typing import List, Optional
from decimal import Decimal
from datetime import date, datetime, time

from sqlalchemy import ForeignKey, Index, Table, String, Text, Integer, Float, Numeric, Boolean, Time, DateTime, Date, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

class Base(DeclarativeBase):
    pass

metadata = Base.metadata


class NamedThing(Base):
    """
    A generic grouping for any identifiable entity
    """
    __tablename__ = 'NamedThing'

    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    description: Mapped[Optional[str]] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    

    def __repr__(self):
        return f"NamedThing(id={self.id},name={self.name},description={self.description},depicted_by={self.depicted_by},)"


    


class HasAliases(Base):
    """
    A mixin applied to any class that can have aliases/alternateNames
    """
    __tablename__ = 'HasAliases'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    
    
    aliases_rel: Mapped[List["HasAliasesAlias"]] = relationship()
    aliases: AssociationProxy[List[str]] = association_proxy("aliases_rel", "alias",
                                  creator=lambda x_: HasAliasesAlias(alias=x_))
    

    def __repr__(self):
        return f"HasAliases(id={self.id},)"


    


class HasNewsEvents(Base):
    """
    None
    """
    __tablename__ = 'HasNewsEvents'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    
    
    # ManyToMany
    has_news_events: Mapped[List["NewsEvent"]] = relationship(secondary="HasNewsEvents_has_news_event")
    

    def __repr__(self):
        return f"HasNewsEvents(id={self.id},)"


    


class Place(Base):
    """
    None
    """
    __tablename__ = 'Place'

    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    Container_id: Mapped[Optional[int]] = mapped_column(Integer(), ForeignKey('Container.id'))
    
    
    aliases_rel: Mapped[List["PlaceAlias"]] = relationship()
    aliases: AssociationProxy[List[str]] = association_proxy("aliases_rel", "alias",
                                  creator=lambda x_: PlaceAlias(alias=x_))
    

    def __repr__(self):
        return f"Place(id={self.id},name={self.name},depicted_by={self.depicted_by},Container_id={self.Container_id},)"


    


class Address(Base):
    """
    None
    """
    __tablename__ = 'Address'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    street: Mapped[Optional[str]] = mapped_column(Text())
    city: Mapped[Optional[str]] = mapped_column(Text())
    postal_code: Mapped[Optional[str]] = mapped_column(Text())
    

    def __repr__(self):
        return f"Address(id={self.id},street={self.street},city={self.city},postal_code={self.postal_code},)"


    


class Event(Base):
    """
    None
    """
    __tablename__ = 'Event'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    started_at_time: Mapped[Optional[date]] = mapped_column(Date())
    ended_at_time: Mapped[Optional[date]] = mapped_column(Date())
    duration: Mapped[Optional[float]] = mapped_column(Float())
    is_current: Mapped[Optional[bool]] = mapped_column(Boolean())
    

    def __repr__(self):
        return f"Event(id={self.id},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},duration={self.duration},is_current={self.is_current},)"


    


class IntegerPrimaryKeyObject(Base):
    """
    None
    """
    __tablename__ = 'IntegerPrimaryKeyObject'

    int_id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    

    def __repr__(self):
        return f"IntegerPrimaryKeyObject(int_id={self.int_id},)"


    


class CodeSystem(Base):
    """
    None
    """
    __tablename__ = 'code system'

    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    

    def __repr__(self):
        return f"code system(id={self.id},name={self.name},)"


    


class Relationship(Base):
    """
    None
    """
    __tablename__ = 'Relationship'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    started_at_time: Mapped[Optional[date]] = mapped_column(Date())
    ended_at_time: Mapped[Optional[date]] = mapped_column(Date())
    related_to: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Person.id'))
    type: Mapped[Optional[str]] = mapped_column(Text())
    

    def __repr__(self):
        return f"Relationship(id={self.id},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},related_to={self.related_to},type={self.type},)"


    


class WithLocation(Base):
    """
    None
    """
    __tablename__ = 'WithLocation'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    in_location: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Place.id'))
    

    def __repr__(self):
        return f"WithLocation(id={self.id},in_location={self.in_location},)"


    


class Container(Base):
    """
    None
    """
    __tablename__ = 'Container'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    
    
    # One-To-Many: OneToAnyMapping(source_class='Container', source_slot='persons', mapping_type=None, target_class='Person', target_slot='Container_id', join_class=None, uses_join_table=None, multivalued=False)
    persons: Mapped[List["Person"]] = relationship(foreign_keys="[Person.Container_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='Container', source_slot='organizations', mapping_type=None, target_class='Organization', target_slot='Container_id', join_class=None, uses_join_table=None, multivalued=False)
    organizations: Mapped[List["Organization"]] = relationship(foreign_keys="[Organization.Container_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='Container', source_slot='places', mapping_type=None, target_class='Place', target_slot='Container_id', join_class=None, uses_join_table=None, multivalued=False)
    places: Mapped[List["Place"]] = relationship(foreign_keys="[Place.Container_id]")
    

    def __repr__(self):
        return f"Container(id={self.id},)"


    


class PersonAlias(Base):
    """
    None
    """
    __tablename__ = 'Person_alias'

    Person_id: Mapped[str] = mapped_column(Text(), ForeignKey('Person.id'), primary_key=True)
    alias: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"Person_alias(Person_id={self.Person_id},alias={self.alias},)"


    


class PersonHasNewsEvent(Base):
    """
    None
    """
    __tablename__ = 'Person_has_news_event'

    Person_id: Mapped[str] = mapped_column(Text(), ForeignKey('Person.id'), primary_key=True)
    has_news_event_id: Mapped[int] = mapped_column(Integer(), ForeignKey('NewsEvent.id'), primary_key=True)
    

    def __repr__(self):
        return f"Person_has_news_event(Person_id={self.Person_id},has_news_event_id={self.has_news_event_id},)"


    


class HasAliasesAlias(Base):
    """
    None
    """
    __tablename__ = 'HasAliases_alias'

    HasAliases_id: Mapped[int] = mapped_column(Integer(), ForeignKey('HasAliases.id'), primary_key=True)
    alias: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"HasAliases_alias(HasAliases_id={self.HasAliases_id},alias={self.alias},)"


    


class HasNewsEventsHasNewsEvent(Base):
    """
    None
    """
    __tablename__ = 'HasNewsEvents_has_news_event'

    HasNewsEvents_id: Mapped[int] = mapped_column(Integer(), ForeignKey('HasNewsEvents.id'), primary_key=True)
    has_news_event_id: Mapped[int] = mapped_column(Integer(), ForeignKey('NewsEvent.id'), primary_key=True)
    

    def __repr__(self):
        return f"HasNewsEvents_has_news_event(HasNewsEvents_id={self.HasNewsEvents_id},has_news_event_id={self.has_news_event_id},)"


    


class OrganizationCategories(Base):
    """
    None
    """
    __tablename__ = 'Organization_categories'

    Organization_id: Mapped[str] = mapped_column(Text(), ForeignKey('Organization.id'), primary_key=True)
    categories: Mapped[str] = mapped_column(Enum('non profit', 'for profit', 'offshore', 'charity', 'shell company', 'loose organization', name='OrganizationType'), primary_key=True)
    

    def __repr__(self):
        return f"Organization_categories(Organization_id={self.Organization_id},categories={self.categories},)"


    


class OrganizationAlias(Base):
    """
    None
    """
    __tablename__ = 'Organization_alias'

    Organization_id: Mapped[str] = mapped_column(Text(), ForeignKey('Organization.id'), primary_key=True)
    alias: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"Organization_alias(Organization_id={self.Organization_id},alias={self.alias},)"


    


class OrganizationHasNewsEvent(Base):
    """
    None
    """
    __tablename__ = 'Organization_has_news_event'

    Organization_id: Mapped[str] = mapped_column(Text(), ForeignKey('Organization.id'), primary_key=True)
    has_news_event_id: Mapped[int] = mapped_column(Integer(), ForeignKey('NewsEvent.id'), primary_key=True)
    

    def __repr__(self):
        return f"Organization_has_news_event(Organization_id={self.Organization_id},has_news_event_id={self.has_news_event_id},)"


    


class PlaceAlias(Base):
    """
    None
    """
    __tablename__ = 'Place_alias'

    Place_id: Mapped[str] = mapped_column(Text(), ForeignKey('Place.id'), primary_key=True)
    alias: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"Place_alias(Place_id={self.Place_id},alias={self.alias},)"


    


class ConceptMappings(Base):
    """
    None
    """
    __tablename__ = 'Concept_mappings'

    Concept_id: Mapped[str] = mapped_column(Text(), ForeignKey('Concept.id'), primary_key=True)
    mappings: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"Concept_mappings(Concept_id={self.Concept_id},mappings={self.mappings},)"


    


class DiagnosisConceptMappings(Base):
    """
    None
    """
    __tablename__ = 'DiagnosisConcept_mappings'

    DiagnosisConcept_id: Mapped[str] = mapped_column(Text(), ForeignKey('DiagnosisConcept.id'), primary_key=True)
    mappings: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"DiagnosisConcept_mappings(DiagnosisConcept_id={self.DiagnosisConcept_id},mappings={self.mappings},)"


    


class ProcedureConceptMappings(Base):
    """
    None
    """
    __tablename__ = 'ProcedureConcept_mappings'

    ProcedureConcept_id: Mapped[str] = mapped_column(Text(), ForeignKey('ProcedureConcept.id'), primary_key=True)
    mappings: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"ProcedureConcept_mappings(ProcedureConcept_id={self.ProcedureConcept_id},mappings={self.mappings},)"


    


class OperationProcedureConceptMappings(Base):
    """
    None
    """
    __tablename__ = 'OperationProcedureConcept_mappings'

    OperationProcedureConcept_id: Mapped[str] = mapped_column(Text(), ForeignKey('OperationProcedureConcept.id'), primary_key=True)
    mappings: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"OperationProcedureConcept_mappings(OperationProcedureConcept_id={self.OperationProcedureConcept_id},mappings={self.mappings},)"


    


class ImagingProcedureConceptMappings(Base):
    """
    None
    """
    __tablename__ = 'ImagingProcedureConcept_mappings'

    ImagingProcedureConcept_id: Mapped[str] = mapped_column(Text(), ForeignKey('ImagingProcedureConcept.id'), primary_key=True)
    mappings: Mapped[str] = mapped_column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"ImagingProcedureConcept_mappings(ImagingProcedureConcept_id={self.ImagingProcedureConcept_id},mappings={self.mappings},)"


    


class Person(NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    __tablename__ = 'Person'

    primary_email: Mapped[Optional[str]] = mapped_column(Text())
    birth_date: Mapped[Optional[str]] = mapped_column(Text())
    age: Mapped[Optional[int]] = mapped_column(Integer())
    gender: Mapped[Optional[str]] = mapped_column(Enum('nonbinary man', 'nonbinary woman', 'transgender woman', 'transgender man', 'cisgender man', 'cisgender woman', name='GenderType'))
    telephone: Mapped[Optional[str]] = mapped_column(Text())
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    description: Mapped[Optional[str]] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    Container_id: Mapped[Optional[int]] = mapped_column(Integer(), ForeignKey('Container.id'))
    current_address_id: Mapped[Optional[int]] = mapped_column(Integer(), ForeignKey('Address.id'))
    current_address: Mapped[Optional["Address"]] = relationship(foreign_keys=[current_address_id])
    
    
    # One-To-Many: OneToAnyMapping(source_class='Person', source_slot='has_employment_history', mapping_type=None, target_class='EmploymentEvent', target_slot='Person_id', join_class=None, uses_join_table=None, multivalued=False)
    has_employment_history: Mapped[List["EmploymentEvent"]] = relationship(foreign_keys="[EmploymentEvent.Person_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='Person', source_slot='has_familial_relationships', mapping_type=None, target_class='FamilialRelationship', target_slot='Person_id', join_class=None, uses_join_table=None, multivalued=False)
    has_familial_relationships: Mapped[List["FamilialRelationship"]] = relationship(foreign_keys="[FamilialRelationship.Person_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='Person', source_slot='has_interpersonal_relationships', mapping_type=None, target_class='InterPersonalRelationship', target_slot='Person_id', join_class=None, uses_join_table=None, multivalued=False)
    has_interpersonal_relationships: Mapped[List["InterPersonalRelationship"]] = relationship(foreign_keys="[InterPersonalRelationship.Person_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='Person', source_slot='has_medical_history', mapping_type=None, target_class='MedicalEvent', target_slot='Person_id', join_class=None, uses_join_table=None, multivalued=False)
    has_medical_history: Mapped[List["MedicalEvent"]] = relationship(foreign_keys="[MedicalEvent.Person_id]")
    
    
    aliases_rel: Mapped[List["PersonAlias"]] = relationship()
    aliases: AssociationProxy[List[str]] = association_proxy("aliases_rel", "alias",
                                  creator=lambda x_: PersonAlias(alias=x_))
    
    
    # ManyToMany
    has_news_events: Mapped[List["NewsEvent"]] = relationship(secondary="Person_has_news_event")
    

    def __repr__(self):
        return f"Person(primary_email={self.primary_email},birth_date={self.birth_date},age={self.age},gender={self.gender},telephone={self.telephone},id={self.id},name={self.name},description={self.description},depicted_by={self.depicted_by},Container_id={self.Container_id},current_address_id={self.current_address_id},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class NewsEvent(Event):
    """
    None
    """
    __tablename__ = 'NewsEvent'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    headline: Mapped[Optional[str]] = mapped_column(Text())
    started_at_time: Mapped[Optional[date]] = mapped_column(Date())
    ended_at_time: Mapped[Optional[date]] = mapped_column(Date())
    duration: Mapped[Optional[float]] = mapped_column(Float())
    is_current: Mapped[Optional[bool]] = mapped_column(Boolean())
    

    def __repr__(self):
        return f"NewsEvent(id={self.id},headline={self.headline},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},duration={self.duration},is_current={self.is_current},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class Organization(NamedThing):
    """
    An organization such as a company or university
    """
    __tablename__ = 'Organization'

    mission_statement: Mapped[Optional[str]] = mapped_column(Text())
    founding_date: Mapped[Optional[str]] = mapped_column(Text())
    founding_location: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Place.id'))
    score: Mapped[Optional[Decimal]] = mapped_column(Numeric())
    min_salary: Mapped[Optional[str]] = mapped_column(Text())
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    description: Mapped[Optional[str]] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    Container_id: Mapped[Optional[int]] = mapped_column(Integer(), ForeignKey('Container.id'))
    
    
    categories_rel: Mapped[List["OrganizationCategories"]] = relationship()
    categories: AssociationProxy[List[str]] = association_proxy("categories_rel", "categories",
                                  creator=lambda x_: OrganizationCategories(categories=x_))
    
    
    aliases_rel: Mapped[List["OrganizationAlias"]] = relationship()
    aliases: AssociationProxy[List[str]] = association_proxy("aliases_rel", "alias",
                                  creator=lambda x_: OrganizationAlias(alias=x_))
    
    
    # ManyToMany
    has_news_events: Mapped[List["NewsEvent"]] = relationship(secondary="Organization_has_news_event")
    

    def __repr__(self):
        return f"Organization(mission_statement={self.mission_statement},founding_date={self.founding_date},founding_location={self.founding_location},score={self.score},min_salary={self.min_salary},id={self.id},name={self.name},description={self.description},depicted_by={self.depicted_by},Container_id={self.Container_id},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class Concept(NamedThing):
    """
    None
    """
    __tablename__ = 'Concept'

    code_system: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('code system.id'))
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    description: Mapped[Optional[str]] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    
    
    mappings_rel: Mapped[List["ConceptMappings"]] = relationship()
    mappings: AssociationProxy[List[str]] = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: ConceptMappings(mappings=x_))
    

    def __repr__(self):
        return f"Concept(code_system={self.code_system},id={self.id},name={self.name},description={self.description},depicted_by={self.depicted_by},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class FamilialRelationship(Relationship):
    """
    None
    """
    __tablename__ = 'FamilialRelationship'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    started_at_time: Mapped[Optional[date]] = mapped_column(Date())
    ended_at_time: Mapped[Optional[date]] = mapped_column(Date())
    related_to: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Person.id'))
    type: Mapped[str] = mapped_column(Enum('SIBLING_OF', 'PARENT_OF', 'CHILD_OF', name='FamilialRelationshipType'))
    Person_id: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Person.id'))
    

    def __repr__(self):
        return f"FamilialRelationship(id={self.id},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},related_to={self.related_to},type={self.type},Person_id={self.Person_id},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class InterPersonalRelationship(Relationship):
    """
    None
    """
    __tablename__ = 'InterPersonalRelationship'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    started_at_time: Mapped[Optional[date]] = mapped_column(Date())
    ended_at_time: Mapped[Optional[date]] = mapped_column(Date())
    related_to: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Person.id'))
    type: Mapped[str] = mapped_column(Text())
    Person_id: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Person.id'))
    

    def __repr__(self):
        return f"InterPersonalRelationship(id={self.id},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},related_to={self.related_to},type={self.type},Person_id={self.Person_id},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class EmploymentEvent(Event):
    """
    None
    """
    __tablename__ = 'EmploymentEvent'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    employed_at: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Organization.id'))
    salary: Mapped[Optional[str]] = mapped_column(Text())
    started_at_time: Mapped[Optional[date]] = mapped_column(Date())
    ended_at_time: Mapped[Optional[date]] = mapped_column(Date())
    duration: Mapped[Optional[float]] = mapped_column(Float())
    is_current: Mapped[Optional[bool]] = mapped_column(Boolean())
    Person_id: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Person.id'))
    

    def __repr__(self):
        return f"EmploymentEvent(id={self.id},employed_at={self.employed_at},salary={self.salary},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},duration={self.duration},is_current={self.is_current},Person_id={self.Person_id},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class MedicalEvent(Event):
    """
    None
    """
    __tablename__ = 'MedicalEvent'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    in_location: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Place.id'))
    started_at_time: Mapped[Optional[date]] = mapped_column(Date())
    ended_at_time: Mapped[Optional[date]] = mapped_column(Date())
    duration: Mapped[Optional[float]] = mapped_column(Float())
    is_current: Mapped[Optional[bool]] = mapped_column(Boolean())
    Person_id: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('Person.id'))
    diagnosis_id: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('DiagnosisConcept.id'))
    diagnosis: Mapped[Optional["DiagnosisConcept"]] = relationship(foreign_keys=[diagnosis_id])
    procedure_id: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('ProcedureConcept.id'))
    procedure: Mapped[Optional["ProcedureConcept"]] = relationship(foreign_keys=[procedure_id])
    

    def __repr__(self):
        return f"MedicalEvent(id={self.id},in_location={self.in_location},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},duration={self.duration},is_current={self.is_current},Person_id={self.Person_id},diagnosis_id={self.diagnosis_id},procedure_id={self.procedure_id},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class DiagnosisConcept(Concept):
    """
    None
    """
    __tablename__ = 'DiagnosisConcept'

    code_system: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('code system.id'))
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    description: Mapped[Optional[str]] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    
    
    mappings_rel: Mapped[List["DiagnosisConceptMappings"]] = relationship()
    mappings: AssociationProxy[List[str]] = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: DiagnosisConceptMappings(mappings=x_))
    

    def __repr__(self):
        return f"DiagnosisConcept(code_system={self.code_system},id={self.id},name={self.name},description={self.description},depicted_by={self.depicted_by},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ProcedureConcept(Concept):
    """
    None
    """
    __tablename__ = 'ProcedureConcept'

    code_system: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('code system.id'))
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    description: Mapped[Optional[str]] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    
    
    mappings_rel: Mapped[List["ProcedureConceptMappings"]] = relationship()
    mappings: AssociationProxy[List[str]] = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: ProcedureConceptMappings(mappings=x_))
    

    def __repr__(self):
        return f"ProcedureConcept(code_system={self.code_system},id={self.id},name={self.name},description={self.description},depicted_by={self.depicted_by},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OperationProcedureConcept(ProcedureConcept):
    """
    None
    """
    __tablename__ = 'OperationProcedureConcept'

    code_system: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('code system.id'))
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    description: Mapped[Optional[str]] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    
    
    mappings_rel: Mapped[List["OperationProcedureConceptMappings"]] = relationship()
    mappings: AssociationProxy[List[str]] = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: OperationProcedureConceptMappings(mappings=x_))
    

    def __repr__(self):
        return f"OperationProcedureConcept(code_system={self.code_system},id={self.id},name={self.name},description={self.description},depicted_by={self.depicted_by},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ImagingProcedureConcept(ProcedureConcept):
    """
    None
    """
    __tablename__ = 'ImagingProcedureConcept'

    code_system: Mapped[Optional[str]] = mapped_column(Text(), ForeignKey('code system.id'))
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    description: Mapped[Optional[str]] = mapped_column(Text())
    depicted_by: Mapped[Optional[str]] = mapped_column(Text())
    
    
    mappings_rel: Mapped[List["ImagingProcedureConceptMappings"]] = relationship()
    mappings: AssociationProxy[List[str]] = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: ImagingProcedureConceptMappings(mappings=x_))
    

    def __repr__(self):
        return f"ImagingProcedureConcept(code_system={self.code_system},id={self.id},name={self.name},description={self.description},depicted_by={self.depicted_by},)"


    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    

