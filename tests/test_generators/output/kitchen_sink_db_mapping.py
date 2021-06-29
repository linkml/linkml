
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
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()
metadata = MetaData()

from output.kitchen_sink import *


tbl_activity = Table('activity', metadata, 
    Column('id', Text, primary_key=True),
    Column('started_at_time', Text),
    Column('ended_at_time', Text),
    Column('was_informed_by_id', Text, ForeignKey('activity.id')),
    Column('was_associated_with_id', Text, ForeignKey('agent.id')),
    Column('used', Text),
    Column('description', Text),
)
tbl_agent = Table('agent', metadata, 
    Column('id', Text, primary_key=True),
    Column('acted_on_behalf_of_id', Text, ForeignKey('agent.id')),
    Column('was_informed_by_id', Text, ForeignKey('activity.id')),
)
tbl_Company = Table('Company', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
    Column('ceo_id', Text, ForeignKey('Person.id')),
)
tbl_Company_to_aliases = Table('Company_to_aliases', metadata, 
    Column('aliases', Text, primary_key=True),
    Column('backlink_Company', Text, ForeignKey('Company.id'), primary_key=True),
)
tbl_Dataset = Table('Dataset', metadata, 
    Column('id', Text, primary_key=True),
)
tbl_Dataset_to_persons_id = Table('Dataset_to_persons_id', metadata, 
    Column('persons_id', Text, ForeignKey('Person.id'), primary_key=True),
    Column('backlink_Dataset', Text, ForeignKey('Dataset.id'), primary_key=True),
)
tbl_Dataset_to_companies_id = Table('Dataset_to_companies_id', metadata, 
    Column('companies_id', Text, ForeignKey('Company.id'), primary_key=True),
    Column('backlink_Dataset', Text, ForeignKey('Dataset.id'), primary_key=True),
)
tbl_Dataset_to_activities_id = Table('Dataset_to_activities_id', metadata, 
    Column('activities_id', Text, ForeignKey('activity.id'), primary_key=True),
    Column('backlink_Dataset', Text, ForeignKey('Dataset.id'), primary_key=True),
)
tbl_EmploymentEvent = Table('EmploymentEvent', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
    Column('employed_at_id', Text, ForeignKey('Company.id'), primary_key=True),
)
tbl_Event = Table('Event', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
)
tbl_FamilialRelationship = Table('FamilialRelationship', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('type', Text, primary_key=True),
    Column('related_to_id', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_HasAliases = Table('HasAliases', metadata, 
    Column('id', Text, primary_key=True),
)
tbl_HasAliases_to_aliases = Table('HasAliases_to_aliases', metadata, 
    Column('aliases', Text, primary_key=True),
    Column('backlink_HasAliases', Text, ForeignKey('HasAliases.id'), primary_key=True),
)
tbl_MarriageEvent = Table('MarriageEvent', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
    Column('married_to_id', Text, ForeignKey('Person.id'), primary_key=True),
    Column('in_location_id', Text, ForeignKey('Place.id'), primary_key=True),
)
tbl_MedicalEvent = Table('MedicalEvent', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('is_current', Text, primary_key=True),
)
tbl_Organization = Table('Organization', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
)
tbl_Organization_to_aliases = Table('Organization_to_aliases', metadata, 
    Column('aliases', Text, primary_key=True),
    Column('backlink_Organization', Text, ForeignKey('Organization.id'), primary_key=True),
)
tbl_Person = Table('Person', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
    Column('age_in_years', Text),
)
tbl_Person_to_has_employment_history = Table('Person_to_has_employment_history', metadata, 
    Column('has_employment_history', Text, primary_key=True),
    Column('backlink_Person', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_Person_to_has_familial_relationships = Table('Person_to_has_familial_relationships', metadata, 
    Column('has_familial_relationships', Text, primary_key=True),
    Column('backlink_Person', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_Person_to_has_medical_history = Table('Person_to_has_medical_history', metadata, 
    Column('has_medical_history', Text, primary_key=True),
    Column('backlink_Person', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_Person_to_aliases = Table('Person_to_aliases', metadata, 
    Column('aliases', Text, primary_key=True),
    Column('backlink_Person', Text, ForeignKey('Person.id'), primary_key=True),
)
tbl_Place = Table('Place', metadata, 
    Column('id', Text, primary_key=True),
    Column('name', Text),
)
tbl_Place_to_aliases = Table('Place_to_aliases', metadata, 
    Column('aliases', Text, primary_key=True),
    Column('backlink_Place', Text, ForeignKey('Place.id'), primary_key=True),
)
tbl_Relationship = Table('Relationship', metadata, 
    Column('started_at_time', Text, primary_key=True),
    Column('ended_at_time', Text, primary_key=True),
    Column('related_to', Text, primary_key=True),
    Column('type', Text, primary_key=True),
)
tbl_WithLocation = Table('WithLocation', metadata, 
    Column('in_location_id', Text, ForeignKey('Place.id'), primary_key=True),
)
mapper_registry.map_imperatively(Activity, tbl_activity, properties={
})
mapper_registry.map_imperatively(Agent, tbl_agent, properties={
})
mapper_registry.map_imperatively(Company, tbl_Company, properties={
})
mapper_registry.map_imperatively(Dataset, tbl_Dataset, properties={
})
mapper_registry.map_imperatively(EmploymentEvent, tbl_EmploymentEvent, properties={
})
mapper_registry.map_imperatively(Event, tbl_Event, properties={
})
mapper_registry.map_imperatively(FamilialRelationship, tbl_FamilialRelationship, properties={
})
mapper_registry.map_imperatively(HasAliases, tbl_HasAliases, properties={
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
mapper_registry.map_imperatively(Relationship, tbl_Relationship, properties={
})
mapper_registry.map_imperatively(WithLocation, tbl_WithLocation, properties={
})
