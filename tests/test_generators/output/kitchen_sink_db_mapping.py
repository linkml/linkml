
from dataclasses import dataclass
from dataclasses import field
from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()
metadata = MetaData()

from .kitchen_sink import *


tbl_activity = Table('activity', metadata, 
    Column('id', Text, primary_key=True),
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('was_informed_by', Text, ForeignKey('activity.id')),
    Column('was_associated_with', Text, ForeignKey('agent.id')),
    Column('used', Text),
    Column('description', Text),
)
tbl_Address = Table('Address', metadata, 
    Column('street', Text, primary_key=True),
    Column('city', Text, primary_key=True),
    Column('Person_id', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_agent = Table('agent', metadata, 
    Column('id', Text, primary_key=True),
    Column('acted_on_behalf_of', Text, ForeignKey('agent.id')),
    Column('was_informed_by', Text, ForeignKey('activity.id')),
)
tbl_BirthEvent = Table('BirthEvent', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
    Column('in_location', Text, ForeignKey('Place.id'), primary_key=True),
)
tbl_class_with_spaces = Table('class_with_spaces', metadata, 
    Column('slot_with_space_1', Text, primary_key=True),
)
tbl_Company = Table('Company', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
    Column('ceo', Text, ForeignKey('Person.id')),
)
tbl_Concept = Table('Concept', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
)
tbl_Dataset = Table('Dataset', metadata, 
    Column('persons', Text, primary_key=True),
    Column('companies', Text, primary_key=True),
    Column('activities', Text, primary_key=True),
)
tbl_DiagnosisConcept = Table('DiagnosisConcept', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
)
tbl_EmploymentEvent = Table('EmploymentEvent', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
    Column('employed_at', Text, ForeignKey('Company.id'), primary_key=True),
    Column('Person_id', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_Event = Table('Event', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
)
tbl_FakeClass = Table('FakeClass', metadata, 
    Column('test_attribute', Text, primary_key=True),
)
tbl_FamilialRelationship = Table('FamilialRelationship', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('type', Text, primary_key=True),
    Column('related_to', Text, ForeignKey('Person.id'), primary_key=True),
    Column('Person_id', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_MarriageEvent = Table('MarriageEvent', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
    Column('married_to', Text, ForeignKey('Person.id'), primary_key=True),
    Column('in_location', Text, ForeignKey('Place.id'), primary_key=True),
)
tbl_MedicalEvent = Table('MedicalEvent', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
    Column('in_location', Text, ForeignKey('Place.id'), primary_key=True),
    Column('diagnosis', Text, ForeignKey('DiagnosisConcept.id'), primary_key=True),
    Column('procedure', Text, ForeignKey('ProcedureConcept.id'), primary_key=True),
    Column('Person_id', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_Organization = Table('Organization', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
)
tbl_Person = Table('Person', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
    Column('age_in_years', Text),
    Column('has_birth_event', Text),
)
tbl_Place = Table('Place', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
)
tbl_ProcedureConcept = Table('ProcedureConcept', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
)
tbl_Relationship = Table('Relationship', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('related_to', Text, primary_key=True),
    Column('type', Text, primary_key=True),
)
tbl_subclass_test = Table('subclass_test', metadata, 
    Column('slot_with_space_1', Text, primary_key=True),
    Column('slot_with_space_2', Text, primary_key=True),
)
tbl_Company_aliases = Table('Company_aliases', metadata, 
    Column('backref_id', Text, ForeignKey('Company.id'), primary_key=True),
    Column('aliases', Text, primary_key=True),
)
tbl_Organization_aliases = Table('Organization_aliases', metadata, 
    Column('backref_id', Text, ForeignKey('Organization.id'), primary_key=True),
    Column('aliases', Text, primary_key=True),
)
tbl_Person_aliases = Table('Person_aliases', metadata, 
    Column('backref_id', Text, ForeignKey('Person.id'), primary_key=True),
    Column('aliases', Text, primary_key=True),
)
tbl_Place_aliases = Table('Place_aliases', metadata, 
    Column('backref_id', Text, ForeignKey('Place.id'), primary_key=True),
    Column('aliases', Text, primary_key=True),
)
mapper_registry.map_imperatively(Activity, tbl_activity, properties={
})
mapper_registry.map_imperatively(Address, tbl_Address, properties={
})
mapper_registry.map_imperatively(Agent, tbl_agent, properties={
})
mapper_registry.map_imperatively(BirthEvent, tbl_BirthEvent, properties={
})
mapper_registry.map_imperatively(ClassWithSpaces, tbl_class_with_spaces, properties={
})
mapper_registry.map_imperatively(Company, tbl_Company, properties={
})
mapper_registry.map_imperatively(Concept, tbl_Concept, properties={
})
mapper_registry.map_imperatively(Dataset, tbl_Dataset, properties={
})
mapper_registry.map_imperatively(DiagnosisConcept, tbl_DiagnosisConcept, properties={
})
mapper_registry.map_imperatively(EmploymentEvent, tbl_EmploymentEvent, properties={
})
mapper_registry.map_imperatively(Event, tbl_Event, properties={
})
mapper_registry.map_imperatively(FakeClass, tbl_FakeClass, properties={
})
mapper_registry.map_imperatively(FamilialRelationship, tbl_FamilialRelationship, properties={
})
mapper_registry.map_imperatively(MarriageEvent, tbl_MarriageEvent, properties={
})
mapper_registry.map_imperatively(MedicalEvent, tbl_MedicalEvent, properties={
})
mapper_registry.map_imperatively(Organization, tbl_Organization, properties={
})
mapper_registry.map_imperatively(Person, tbl_Person, properties={

    'has_employment_history': 
        relationship(EmploymentEvent, 
                      foreign_keys=tbl_EmploymentEvent.columns["Person_id"],
                      backref='Person'),


    'has_familial_relationships': 
        relationship(FamilialRelationship, 
                      foreign_keys=tbl_FamilialRelationship.columns["Person_id"],
                      backref='Person'),


    'has_medical_history': 
        relationship(MedicalEvent, 
                      foreign_keys=tbl_MedicalEvent.columns["Person_id"],
                      backref='Person'),


    'addresses': 
        relationship(Address, 
                      foreign_keys=tbl_Address.columns["Person_id"],
                      backref='Person'),

})
mapper_registry.map_imperatively(Place, tbl_Place, properties={
})
mapper_registry.map_imperatively(ProcedureConcept, tbl_ProcedureConcept, properties={
})
mapper_registry.map_imperatively(Relationship, tbl_Relationship, properties={
})
mapper_registry.map_imperatively(SubclassTest, tbl_subclass_test, properties={
})
