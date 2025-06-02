from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
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
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_curi_maps': ['semweb_context'],
     'default_prefix': 'personinfo',
     'default_range': 'string',
     'description': 'Information about people, based on '
                    '[schema.org](http://schema.org)',
     'emit_prefixes': ['rdf', 'rdfs', 'xsd', 'skos'],
     'id': 'https://w3id.org/linkml/examples/personinfo',
     'imports': ['linkml:types'],
     'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
     'name': 'personinfo',
     'prefixes': {'CODE': {'prefix_prefix': 'CODE',
                           'prefix_reference': 'http://example.org/code/'},
                  'GEO': {'prefix_prefix': 'GEO',
                          'prefix_reference': 'http://example.org/geoloc/'},
                  'GSSO': {'prefix_prefix': 'GSSO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/GSSO_'},
                  'P': {'prefix_prefix': 'P',
                        'prefix_reference': 'http://example.org/P/'},
                  'ROR': {'prefix_prefix': 'ROR',
                          'prefix_reference': 'http://example.org/ror/'},
                  'famrel': {'prefix_prefix': 'famrel',
                             'prefix_reference': 'https://example.org/FamilialRelations#'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'personinfo': {'prefix_prefix': 'personinfo',
                                 'prefix_reference': 'https://w3id.org/linkml/examples/personinfo/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'source_file': '../examples/PersonSchema/personinfo.yaml',
     'subsets': {'basic_subset': {'description': 'A subset of the schema that '
                                                 'handles basic information',
                                  'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'name': 'basic_subset'}}} )

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
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['schema:Thing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image', 'domain_of': ['NamedThing'], 'slot_uri': 'schema:image'} })


class HasAliases(ConfiguredBaseModel):
    """
    A mixin applied to any class that can have aliases/alternateNames
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo', 'mixin': True})

    aliases: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName']} })


class Person(HasAliases, NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Person',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'in_subset': ['basic_subset'],
         'mixins': ['HasAliases'],
         'slot_usage': {'age_in_years': {'name': 'age_in_years', 'recommended': True},
                        'primary_email': {'name': 'primary_email',
                                          'pattern': '^\\S+@[\\S+\\.]+\\S+'}}})

    primary_email: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'primary_email', 'domain_of': ['Person'], 'slot_uri': 'schema:email'} })
    birth_date: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'birth_date', 'domain_of': ['Person'], 'slot_uri': 'schema:birthDate'} })
    age_in_years: Optional[int] = Field(default=None, ge=0, le=999, json_schema_extra = { "linkml_meta": {'alias': 'age_in_years', 'domain_of': ['Person'], 'recommended': True} })
    gender: Optional[GenderType] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'gender', 'domain_of': ['Person'], 'slot_uri': 'schema:gender'} })
    current_address: Optional[Address] = Field(default=None, description="""The address at which a person currently lives""", json_schema_extra = { "linkml_meta": {'alias': 'current_address', 'domain_of': ['Person']} })
    has_employment_history: Optional[List[EmploymentEvent]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_employment_history', 'domain_of': ['Person']} })
    has_familial_relationships: Optional[List[FamilialRelationship]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_familial_relationships', 'domain_of': ['Person']} })
    has_medical_history: Optional[List[MedicalEvent]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_medical_history', 'domain_of': ['Person']} })
    aliases: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName']} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image', 'domain_of': ['NamedThing'], 'slot_uri': 'schema:image'} })

    @field_validator('primary_email')
    def pattern_primary_email(cls, v):
        pattern=re.compile(r"^\S+@[\S+\.]+\S+")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid primary_email format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid primary_email format: {v}")
        return v


class Organization(HasAliases, NamedThing):
    """
    An organization such as a company or university
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Organization',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'mixins': ['HasAliases']})

    mission_statement: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'mission_statement', 'domain_of': ['Organization']} })
    founding_date: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'founding_date', 'domain_of': ['Organization']} })
    founding_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'founding_location', 'domain_of': ['Organization']} })
    aliases: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName']} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image', 'domain_of': ['NamedThing'], 'slot_uri': 'schema:image'} })


class Place(HasAliases):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'mixins': ['HasAliases']})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:name'} })
    aliases: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName']} })


class Address(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:PostalAddress',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    street: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'street', 'domain_of': ['Address']} })
    city: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'city', 'domain_of': ['Address']} })
    postal_code: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'postal_code', 'domain_of': ['Address']} })


class Event(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['schema:Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:endedAtTime'} })
    duration: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'duration', 'domain_of': ['Event']} })
    is_current: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'is_current', 'domain_of': ['Event']} })


class Concept(NamedThing):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image', 'domain_of': ['NamedThing'], 'slot_uri': 'schema:image'} })


class DiagnosisConcept(Concept):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image', 'domain_of': ['NamedThing'], 'slot_uri': 'schema:image'} })


class ProcedureConcept(Concept):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image', 'domain_of': ['NamedThing'], 'slot_uri': 'schema:image'} })


class Relationship(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:endedAtTime'} })
    related_to: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'related_to', 'domain_of': ['Relationship']} })
    type: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Relationship']} })


class FamilialRelationship(Relationship):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'slot_usage': {'related_to': {'name': 'related_to',
                                       'range': 'Person',
                                       'required': True},
                        'type': {'name': 'type',
                                 'range': 'FamilialRelationshipType',
                                 'required': True}}})

    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:endedAtTime'} })
    related_to: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'related_to', 'domain_of': ['Relationship']} })
    type: FamilialRelationshipType = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Relationship']} })


class EmploymentEvent(Event):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    employed_at: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'employed_at', 'domain_of': ['EmploymentEvent']} })
    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:endedAtTime'} })
    duration: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'duration', 'domain_of': ['Event']} })
    is_current: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'is_current', 'domain_of': ['Event']} })


class MedicalEvent(Event):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    in_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'in_location', 'domain_of': ['MedicalEvent', 'WithLocation']} })
    diagnosis: Optional[DiagnosisConcept] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'diagnosis', 'domain_of': ['MedicalEvent']} })
    procedure: Optional[ProcedureConcept] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'procedure', 'domain_of': ['MedicalEvent']} })
    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'slot_uri': 'prov:endedAtTime'} })
    duration: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'duration', 'domain_of': ['Event']} })
    is_current: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'is_current', 'domain_of': ['Event']} })


class WithLocation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo', 'mixin': True})

    in_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'in_location', 'domain_of': ['MedicalEvent', 'WithLocation']} })


class Container(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'tree_root': True})

    persons: Optional[List[Person]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'persons', 'domain_of': ['Container']} })
    organizations: Optional[List[Organization]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'organizations', 'domain_of': ['Container']} })


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
