
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class NamedThing(Base):
    """
    A generic grouping for any identifiable entity
    """
    __tablename__ = 'NamedThing'

    id = Column(Text(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    image = Column(Text())


    def __repr__(self):
        return f"NamedThing(id={self.id},name={self.name},description={self.description},image={self.image},)"






class HasAliases(Base):
    """
    A mixin applied to any class that can have aliases/alternateNames
    """
    __tablename__ = 'HasAliases'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )


    aliases_rel = relationship( "HasAliasesAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: HasAliasesAliases(aliases=x_))


    def __repr__(self):
        return f"HasAliases(id={self.id},)"






class Place(Base):
    """

    """
    __tablename__ = 'Place'

    id = Column(Text(), primary_key=True, nullable=False )
    name = Column(Text())


    aliases_rel = relationship( "PlaceAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: PlaceAliases(aliases=x_))


    def __repr__(self):
        return f"Place(id={self.id},name={self.name},)"






class Address(Base):
    """

    """
    __tablename__ = 'Address'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    street = Column(Text())
    city = Column(Text())
    postal_code = Column(Text())


    def __repr__(self):
        return f"Address(id={self.id},street={self.street},city={self.city},postal_code={self.postal_code},)"






class Event(Base):
    """

    """
    __tablename__ = 'Event'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    started_at_time = Column(Date())
    ended_at_time = Column(Date())
    duration = Column(Float())
    is_current = Column(Boolean())


    def __repr__(self):
        return f"Event(id={self.id},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},duration={self.duration},is_current={self.is_current},)"






class Relationship(Base):
    """

    """
    __tablename__ = 'Relationship'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    started_at_time = Column(Date())
    ended_at_time = Column(Date())
    related_to = Column(Text())
    type = Column(Text())


    def __repr__(self):
        return f"Relationship(id={self.id},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},related_to={self.related_to},type={self.type},)"






class WithLocation(Base):
    """

    """
    __tablename__ = 'WithLocation'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    in_location = Column(Text(), ForeignKey('Place.id'))


    def __repr__(self):
        return f"WithLocation(id={self.id},in_location={self.in_location},)"






class Container(Base):
    """

    """
    __tablename__ = 'Container'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )


    # One-To-Many: OneToAnyMapping(source_class='Container', source_slot='persons', mapping_type=None, target_class='Person', target_slot='Container_id', join_class=None, uses_join_table=None, multivalued=False)
    persons = relationship( "Person", foreign_keys="[Person.Container_id]")


    # One-To-Many: OneToAnyMapping(source_class='Container', source_slot='organizations', mapping_type=None, target_class='Organization', target_slot='Container_id', join_class=None, uses_join_table=None, multivalued=False)
    organizations = relationship( "Organization", foreign_keys="[Organization.Container_id]")


    def __repr__(self):
        return f"Container(id={self.id},)"






class PersonAliases(Base):
    """

    """
    __tablename__ = 'Person_aliases'

    Person_id = Column(Text(), ForeignKey('Person.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)


    def __repr__(self):
        return f"Person_aliases(Person_id={self.Person_id},aliases={self.aliases},)"






class HasAliasesAliases(Base):
    """

    """
    __tablename__ = 'HasAliases_aliases'

    HasAliases_id = Column(Integer(), ForeignKey('HasAliases.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)


    def __repr__(self):
        return f"HasAliases_aliases(HasAliases_id={self.HasAliases_id},aliases={self.aliases},)"






class OrganizationAliases(Base):
    """

    """
    __tablename__ = 'Organization_aliases'

    Organization_id = Column(Text(), ForeignKey('Organization.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)


    def __repr__(self):
        return f"Organization_aliases(Organization_id={self.Organization_id},aliases={self.aliases},)"






class PlaceAliases(Base):
    """

    """
    __tablename__ = 'Place_aliases'

    Place_id = Column(Text(), ForeignKey('Place.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)


    def __repr__(self):
        return f"Place_aliases(Place_id={self.Place_id},aliases={self.aliases},)"






class Person(NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    __tablename__ = 'Person'

    primary_email = Column(Text())
    birth_date = Column(Text())
    age_in_years = Column(Integer())
    gender = Column(Enum('nonbinary man', 'nonbinary woman', 'transgender woman', 'transgender man', 'cisgender man', 'cisgender woman', name='GenderType'))
    id = Column(Text(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    image = Column(Text())
    Container_id = Column(Integer(), ForeignKey('Container.id'))
    current_address_id = Column(Integer(), ForeignKey('Address.id'))
    current_address = relationship("Address", uselist=False, foreign_keys=[current_address_id])


    # One-To-Many: OneToAnyMapping(source_class='Person', source_slot='has_employment_history', mapping_type=None, target_class='EmploymentEvent', target_slot='Person_id', join_class=None, uses_join_table=None, multivalued=False)
    has_employment_history = relationship( "EmploymentEvent", foreign_keys="[EmploymentEvent.Person_id]")


    # One-To-Many: OneToAnyMapping(source_class='Person', source_slot='has_familial_relationships', mapping_type=None, target_class='FamilialRelationship', target_slot='Person_id', join_class=None, uses_join_table=None, multivalued=False)
    has_familial_relationships = relationship( "FamilialRelationship", foreign_keys="[FamilialRelationship.Person_id]")


    # One-To-Many: OneToAnyMapping(source_class='Person', source_slot='has_medical_history', mapping_type=None, target_class='MedicalEvent', target_slot='Person_id', join_class=None, uses_join_table=None, multivalued=False)
    has_medical_history = relationship( "MedicalEvent", foreign_keys="[MedicalEvent.Person_id]")


    aliases_rel = relationship( "PersonAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: PersonAliases(aliases=x_))


    def __repr__(self):
        return f"Person(primary_email={self.primary_email},birth_date={self.birth_date},age_in_years={self.age_in_years},gender={self.gender},id={self.id},name={self.name},description={self.description},image={self.image},Container_id={self.Container_id},current_address_id={self.current_address_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Organization(NamedThing):
    """
    An organization such as a company or university
    """
    __tablename__ = 'Organization'

    mission_statement = Column(Text())
    founding_date = Column(Text())
    founding_location = Column(Text(), ForeignKey('Place.id'))
    id = Column(Text(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    image = Column(Text())
    Container_id = Column(Integer(), ForeignKey('Container.id'))


    aliases_rel = relationship( "OrganizationAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: OrganizationAliases(aliases=x_))


    def __repr__(self):
        return f"Organization(mission_statement={self.mission_statement},founding_date={self.founding_date},founding_location={self.founding_location},id={self.id},name={self.name},description={self.description},image={self.image},Container_id={self.Container_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Concept(NamedThing):
    """

    """
    __tablename__ = 'Concept'

    id = Column(Text(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    image = Column(Text())


    def __repr__(self):
        return f"Concept(id={self.id},name={self.name},description={self.description},image={self.image},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FamilialRelationship(Relationship):
    """

    """
    __tablename__ = 'FamilialRelationship'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    started_at_time = Column(Date())
    ended_at_time = Column(Date())
    related_to = Column(Text(), ForeignKey('Person.id'), nullable=False )
    type = Column(Enum('SIBLING_OF', 'PARENT_OF', 'CHILD_OF', name='FamilialRelationshipType'), nullable=False )
    Person_id = Column(Text(), ForeignKey('Person.id'))


    def __repr__(self):
        return f"FamilialRelationship(id={self.id},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},related_to={self.related_to},type={self.type},Person_id={self.Person_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class EmploymentEvent(Event):
    """

    """
    __tablename__ = 'EmploymentEvent'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    employed_at = Column(Text(), ForeignKey('Organization.id'))
    started_at_time = Column(Date())
    ended_at_time = Column(Date())
    duration = Column(Float())
    is_current = Column(Boolean())
    Person_id = Column(Text(), ForeignKey('Person.id'))


    def __repr__(self):
        return f"EmploymentEvent(id={self.id},employed_at={self.employed_at},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},duration={self.duration},is_current={self.is_current},Person_id={self.Person_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class MedicalEvent(Event):
    """

    """
    __tablename__ = 'MedicalEvent'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    in_location = Column(Text(), ForeignKey('Place.id'))
    started_at_time = Column(Date())
    ended_at_time = Column(Date())
    duration = Column(Float())
    is_current = Column(Boolean())
    Person_id = Column(Text(), ForeignKey('Person.id'))
    diagnosis_id = Column(Text(), ForeignKey('DiagnosisConcept.id'))
    diagnosis = relationship("DiagnosisConcept", uselist=False, foreign_keys=[diagnosis_id])
    procedure_id = Column(Text(), ForeignKey('ProcedureConcept.id'))
    procedure = relationship("ProcedureConcept", uselist=False, foreign_keys=[procedure_id])


    def __repr__(self):
        return f"MedicalEvent(id={self.id},in_location={self.in_location},started_at_time={self.started_at_time},ended_at_time={self.ended_at_time},duration={self.duration},is_current={self.is_current},Person_id={self.Person_id},diagnosis_id={self.diagnosis_id},procedure_id={self.procedure_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class DiagnosisConcept(Concept):
    """

    """
    __tablename__ = 'DiagnosisConcept'

    id = Column(Text(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    image = Column(Text())


    def __repr__(self):
        return f"DiagnosisConcept(id={self.id},name={self.name},description={self.description},image={self.image},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ProcedureConcept(Concept):
    """

    """
    __tablename__ = 'ProcedureConcept'

    id = Column(Text(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    image = Column(Text())


    def __repr__(self):
        return f"ProcedureConcept(id={self.id},name={self.name},description={self.description},image={self.image},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
