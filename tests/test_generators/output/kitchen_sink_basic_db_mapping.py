
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

from output.kitchen_sink import *


tbl_activity = Table('activity', metadata, 
    Column('id', Text),
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('was_informed_by', Text),
    Column('was_associated_with', Text),
    Column('used', Text),
    Column('description', Text),
)
tbl_Address = Table('Address', metadata, 
    Column('street', Text),
    Column('city', Text),
)
tbl_agent = Table('agent', metadata, 
    Column('id', Text),
    Column('acted_on_behalf_of', Text),
    Column('was_informed_by', Text),
)
tbl_BirthEvent = Table('BirthEvent', metadata, 
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('is_current', Text),
    Column('in_location', Text),
)
tbl_class_with_spaces = Table('class_with_spaces', metadata, 
    Column('slot_with_space_1', Text),
)
tbl_Company = Table('Company', metadata, 
    Column('id', Text),
    Column('name', Text),
    Column('aliases', Text),
    Column('ceo', Text),
)
tbl_Concept = Table('Concept', metadata, 
    Column('id', Text),
    Column('name', Text),
)
tbl_Dataset = Table('Dataset', metadata, 
    Column('persons', Text),
    Column('companies', Text),
    Column('activities', Text),
)
tbl_DiagnosisConcept = Table('DiagnosisConcept', metadata, 
    Column('id', Text),
    Column('name', Text),
)
tbl_EmploymentEvent = Table('EmploymentEvent', metadata, 
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('is_current', Text),
    Column('employed_at', Text),
)
tbl_Event = Table('Event', metadata, 
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('is_current', Text),
)
tbl_FakeClass = Table('FakeClass', metadata, 
    Column('test_attribute', Text),
)
tbl_FamilialRelationship = Table('FamilialRelationship', metadata, 
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('type', Text),
    Column('related_to', Text),
)
tbl_MarriageEvent = Table('MarriageEvent', metadata, 
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('is_current', Text),
    Column('married_to', Text),
    Column('in_location', Text),
)
tbl_MedicalEvent = Table('MedicalEvent', metadata, 
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('is_current', Text),
    Column('in_location', Text),
    Column('diagnosis', Text),
    Column('procedure', Text),
)
tbl_Organization = Table('Organization', metadata, 
    Column('id', Text),
    Column('name', Text),
    Column('aliases', Text),
)
tbl_Person = Table('Person', metadata, 
    Column('id', Text),
    Column('name', Text),
    Column('has_employment_history', Text),
    Column('has_familial_relationships', Text),
    Column('has_medical_history', Text),
    Column('age_in_years', Text),
    Column('addresses', Text),
    Column('has_birth_event', Text),
    Column('aliases', Text),
)
tbl_Place = Table('Place', metadata, 
    Column('id', Text),
    Column('name', Text),
    Column('aliases', Text),
)
tbl_ProcedureConcept = Table('ProcedureConcept', metadata, 
    Column('id', Text),
    Column('name', Text),
)
tbl_Relationship = Table('Relationship', metadata, 
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('related_to', Text),
    Column('type', Text),
)
tbl_subclass_test = Table('subclass_test', metadata, 
    Column('slot_with_space_1', Text),
    Column('slot_with_space_2', Text),
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
})
mapper_registry.map_imperatively(Place, tbl_Place, properties={
})
mapper_registry.map_imperatively(ProcedureConcept, tbl_ProcedureConcept, properties={
})
mapper_registry.map_imperatively(Relationship, tbl_Relationship, properties={
})
mapper_registry.map_imperatively(SubclassTest, tbl_subclass_test, properties={
})
