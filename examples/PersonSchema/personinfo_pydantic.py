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
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'classes': {'Address': {'class_uri': 'schema:PostalAddress',
                             'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                             'name': 'Address',
                             'slots': ['street', 'city', 'postal_code']},
                 'Concept': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                             'is_a': 'NamedThing',
                             'name': 'Concept'},
                 'Container': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'name': 'Container',
                               'slots': ['persons', 'organizations'],
                               'tree_root': True},
                 'DiagnosisConcept': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                      'is_a': 'Concept',
                                      'name': 'DiagnosisConcept'},
                 'EmploymentEvent': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                     'is_a': 'Event',
                                     'name': 'EmploymentEvent',
                                     'slots': ['employed_at']},
                 'Event': {'close_mappings': ['schema:Event'],
                           'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                           'name': 'Event',
                           'slots': ['started_at_time',
                                     'ended_at_time',
                                     'duration',
                                     'is_current']},
                 'FamilialRelationship': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                          'is_a': 'Relationship',
                                          'name': 'FamilialRelationship',
                                          'slot_usage': {'related_to': {'name': 'related_to',
                                                                        'range': 'Person',
                                                                        'required': True},
                                                         'type': {'name': 'type',
                                                                  'range': 'FamilialRelationshipType',
                                                                  'required': True}}},
                 'HasAliases': {'attributes': {'aliases': {'domain_of': ['HasAliases'],
                                                           'exact_mappings': ['schema:alternateName'],
                                                           'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                                           'multivalued': True,
                                                           'name': 'aliases'}},
                                'description': 'A mixin applied to any class that '
                                               'can have aliases/alternateNames',
                                'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                'mixin': True,
                                'name': 'HasAliases'},
                 'MedicalEvent': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'is_a': 'Event',
                                  'name': 'MedicalEvent',
                                  'slots': ['in_location',
                                            'diagnosis',
                                            'procedure']},
                 'NamedThing': {'close_mappings': ['schema:Thing'],
                                'description': 'A generic grouping for any '
                                               'identifiable entity',
                                'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                'name': 'NamedThing',
                                'slots': ['id', 'name', 'description', 'image']},
                 'Organization': {'class_uri': 'schema:Organization',
                                  'description': 'An organization such as a '
                                                 'company or university',
                                  'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'is_a': 'NamedThing',
                                  'mixins': ['HasAliases'],
                                  'name': 'Organization',
                                  'slots': ['mission_statement',
                                            'founding_date',
                                            'founding_location']},
                 'Person': {'class_uri': 'schema:Person',
                            'description': 'A person (alive, dead, undead, or '
                                           'fictional).',
                            'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                            'in_subset': ['basic_subset'],
                            'is_a': 'NamedThing',
                            'mixins': ['HasAliases'],
                            'name': 'Person',
                            'slot_usage': {'age_in_years': {'name': 'age_in_years',
                                                            'recommended': True},
                                           'primary_email': {'name': 'primary_email',
                                                             'pattern': '^\\S+@[\\S+\\.]+\\S+'}},
                            'slots': ['primary_email',
                                      'birth_date',
                                      'age_in_years',
                                      'gender',
                                      'current_address',
                                      'has_employment_history',
                                      'has_familial_relationships',
                                      'has_medical_history']},
                 'Place': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                           'mixins': ['HasAliases'],
                           'name': 'Place',
                           'slots': ['id', 'name']},
                 'ProcedureConcept': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                      'is_a': 'Concept',
                                      'name': 'ProcedureConcept'},
                 'Relationship': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'name': 'Relationship',
                                  'slots': ['started_at_time',
                                            'ended_at_time',
                                            'related_to',
                                            'type']},
                 'WithLocation': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'mixin': True,
                                  'name': 'WithLocation',
                                  'slots': ['in_location']}},
     'default_curi_maps': ['semweb_context'],
     'default_prefix': 'personinfo',
     'default_range': 'string',
     'description': 'Information about people, based on '
                    '[schema.org](http://schema.org)',
     'emit_prefixes': ['rdf', 'rdfs', 'xsd', 'skos'],
     'enums': {'DiagnosisType': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                 'name': 'DiagnosisType'},
               'FamilialRelationshipType': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                            'name': 'FamilialRelationshipType',
                                            'permissible_values': {'CHILD_OF': {'meaning': 'famrel:03',
                                                                                'text': 'CHILD_OF'},
                                                                   'PARENT_OF': {'meaning': 'famrel:02',
                                                                                 'text': 'PARENT_OF'},
                                                                   'SIBLING_OF': {'meaning': 'famrel:01',
                                                                                  'text': 'SIBLING_OF'}}},
               'GenderType': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'name': 'GenderType',
                              'permissible_values': {'cisgender man': {'meaning': 'GSSO:000371',
                                                                       'text': 'cisgender '
                                                                               'man'},
                                                     'cisgender woman': {'meaning': 'GSSO:000385',
                                                                         'text': 'cisgender '
                                                                                 'woman'},
                                                     'nonbinary man': {'meaning': 'GSSO:009254',
                                                                       'text': 'nonbinary '
                                                                               'man'},
                                                     'nonbinary woman': {'meaning': 'GSSO:009253',
                                                                         'text': 'nonbinary '
                                                                                 'woman'},
                                                     'transgender man': {'meaning': 'GSSO:000372',
                                                                         'text': 'transgender '
                                                                                 'man'},
                                                     'transgender woman': {'meaning': 'GSSO:000384',
                                                                           'text': 'transgender '
                                                                                   'woman'}}}},
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
     'slots': {'age_in_years': {'domain_of': ['Person'],
                                'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                'maximum_value': 999,
                                'minimum_value': 0,
                                'name': 'age_in_years',
                                'range': 'integer'},
               'birth_date': {'domain_of': ['Person'],
                              'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'name': 'birth_date',
                              'slot_uri': 'schema:birthDate'},
               'city': {'domain_of': ['Address'],
                        'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                        'name': 'city'},
               'current_address': {'description': 'The address at which a person '
                                                  'currently lives',
                                   'domain_of': ['Person'],
                                   'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                   'name': 'current_address',
                                   'range': 'Address'},
               'description': {'domain_of': ['NamedThing'],
                               'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'name': 'description',
                               'slot_uri': 'schema:description'},
               'diagnosis': {'domain_of': ['MedicalEvent'],
                             'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                             'inlined': True,
                             'name': 'diagnosis',
                             'range': 'DiagnosisConcept'},
               'duration': {'domain_of': ['Event'],
                            'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                            'name': 'duration',
                            'range': 'float'},
               'employed_at': {'domain_of': ['EmploymentEvent'],
                               'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'name': 'employed_at',
                               'range': 'Organization'},
               'ended_at_time': {'domain_of': ['Event', 'Relationship'],
                                 'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                 'name': 'ended_at_time',
                                 'range': 'date',
                                 'slot_uri': 'prov:endedAtTime'},
               'founding_date': {'domain_of': ['Organization'],
                                 'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                 'name': 'founding_date'},
               'founding_location': {'domain_of': ['Organization'],
                                     'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                     'name': 'founding_location',
                                     'range': 'Place'},
               'gender': {'domain_of': ['Person'],
                          'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                          'name': 'gender',
                          'range': 'GenderType',
                          'slot_uri': 'schema:gender'},
               'has_employment_history': {'domain_of': ['Person'],
                                          'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                          'inlined': True,
                                          'inlined_as_list': True,
                                          'multivalued': True,
                                          'name': 'has_employment_history',
                                          'range': 'EmploymentEvent'},
               'has_familial_relationships': {'domain_of': ['Person'],
                                              'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                              'inlined': True,
                                              'inlined_as_list': True,
                                              'multivalued': True,
                                              'name': 'has_familial_relationships',
                                              'range': 'FamilialRelationship'},
               'has_medical_history': {'domain_of': ['Person'],
                                       'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                       'inlined': True,
                                       'inlined_as_list': True,
                                       'multivalued': True,
                                       'name': 'has_medical_history',
                                       'range': 'MedicalEvent'},
               'id': {'domain_of': ['NamedThing', 'Place'],
                      'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                      'identifier': True,
                      'name': 'id',
                      'required': True,
                      'slot_uri': 'schema:identifier'},
               'image': {'domain_of': ['NamedThing'],
                         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                         'name': 'image',
                         'slot_uri': 'schema:image'},
               'in_location': {'domain_of': ['MedicalEvent', 'WithLocation'],
                               'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'name': 'in_location',
                               'range': 'Place'},
               'is_current': {'domain_of': ['Event'],
                              'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'name': 'is_current',
                              'range': 'boolean'},
               'mission_statement': {'domain_of': ['Organization'],
                                     'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                     'name': 'mission_statement'},
               'name': {'domain_of': ['NamedThing', 'Place'],
                        'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                        'name': 'name',
                        'slot_uri': 'schema:name'},
               'organizations': {'domain_of': ['Container'],
                                 'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                 'inlined': True,
                                 'inlined_as_list': True,
                                 'multivalued': True,
                                 'name': 'organizations',
                                 'range': 'Organization'},
               'persons': {'domain_of': ['Container'],
                           'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                           'inlined': True,
                           'inlined_as_list': True,
                           'multivalued': True,
                           'name': 'persons',
                           'range': 'Person'},
               'postal_code': {'domain_of': ['Address'],
                               'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'name': 'postal_code',
                               'range': 'string'},
               'primary_email': {'domain_of': ['Person'],
                                 'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                 'name': 'primary_email',
                                 'slot_uri': 'schema:email'},
               'procedure': {'domain_of': ['MedicalEvent'],
                             'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                             'inlined': True,
                             'name': 'procedure',
                             'range': 'ProcedureConcept'},
               'related_to': {'domain_of': ['Relationship'],
                              'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'name': 'related_to'},
               'started_at_time': {'domain_of': ['Event', 'Relationship'],
                                   'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                   'name': 'started_at_time',
                                   'range': 'date',
                                   'slot_uri': 'prov:startedAtTime'},
               'street': {'domain_of': ['Address'],
                          'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                          'name': 'street'},
               'type': {'domain_of': ['Relationship'],
                        'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                        'name': 'type'}},
     'source_file': 'personinfo.yaml',
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
         'description': 'A generic grouping for any identifiable entity',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'NamedThing',
         'slots': ['id', 'name', 'description', 'image']})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'NamedThing',
         'range': 'string',
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'NamedThing',
         'range': 'string',
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'NamedThing',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'image',
         'owner': 'NamedThing',
         'range': 'string',
         'slot_uri': 'schema:image'} })


class HasAliases(ConfiguredBaseModel):
    """
    A mixin applied to any class that can have aliases/alternateNames
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'attributes': {'aliases': {'domain_of': ['HasAliases'],
                                    'exact_mappings': ['schema:alternateName'],
                                    'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                    'multivalued': True,
                                    'name': 'aliases'}},
         'description': 'A mixin applied to any class that can have '
                        'aliases/alternateNames',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'mixin': True,
         'name': 'HasAliases'})

    aliases: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'aliases',
         'owner': 'HasAliases',
         'range': 'string'} })


class Person(HasAliases, NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Person',
         'description': 'A person (alive, dead, undead, or fictional).',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'in_subset': ['basic_subset'],
         'is_a': 'NamedThing',
         'mixins': ['HasAliases'],
         'name': 'Person',
         'slot_usage': {'age_in_years': {'name': 'age_in_years', 'recommended': True},
                        'primary_email': {'name': 'primary_email',
                                          'pattern': '^\\S+@[\\S+\\.]+\\S+'}},
         'slots': ['primary_email',
                   'birth_date',
                   'age_in_years',
                   'gender',
                   'current_address',
                   'has_employment_history',
                   'has_familial_relationships',
                   'has_medical_history']})

    primary_email: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'primary_email',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'primary_email',
         'owner': 'Person',
         'pattern': '^\\S+@[\\S+\\.]+\\S+',
         'range': 'string',
         'slot_uri': 'schema:email'} })
    birth_date: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'birth_date',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'birth_date',
         'owner': 'Person',
         'range': 'string',
         'slot_uri': 'schema:birthDate'} })
    age_in_years: Optional[int] = Field(default=None, ge=0, le=999, json_schema_extra = { "linkml_meta": {'alias': 'age_in_years',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'maximum_value': 999,
         'minimum_value': 0,
         'name': 'age_in_years',
         'owner': 'Person',
         'range': 'integer',
         'recommended': True} })
    gender: Optional[GenderType] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'gender',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'gender',
         'owner': 'Person',
         'range': 'GenderType',
         'slot_uri': 'schema:gender'} })
    current_address: Optional[Address] = Field(default=None, description="""The address at which a person currently lives""", json_schema_extra = { "linkml_meta": {'alias': 'current_address',
         'description': 'The address at which a person currently lives',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'current_address',
         'owner': 'Person',
         'range': 'Address'} })
    has_employment_history: Optional[list[EmploymentEvent]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_employment_history',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined_as_list': True,
         'multivalued': True,
         'name': 'has_employment_history',
         'owner': 'Person',
         'range': 'EmploymentEvent'} })
    has_familial_relationships: Optional[list[FamilialRelationship]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_familial_relationships',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined_as_list': True,
         'multivalued': True,
         'name': 'has_familial_relationships',
         'owner': 'Person',
         'range': 'FamilialRelationship'} })
    has_medical_history: Optional[list[MedicalEvent]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_medical_history',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined_as_list': True,
         'multivalued': True,
         'name': 'has_medical_history',
         'owner': 'Person',
         'range': 'MedicalEvent'} })
    aliases: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'aliases',
         'owner': 'Person',
         'range': 'string'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'Person',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'Person',
         'range': 'string',
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'Person',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'image',
         'owner': 'Person',
         'range': 'string',
         'slot_uri': 'schema:image'} })

    @field_validator('primary_email')
    def pattern_primary_email(cls, v):
        pattern=re.compile(r"^\S+@[\S+\.]+\S+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid primary_email format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid primary_email format: {v}"
            raise ValueError(err_msg)
        return v


class Organization(HasAliases, NamedThing):
    """
    An organization such as a company or university
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Organization',
         'description': 'An organization such as a company or university',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'NamedThing',
         'mixins': ['HasAliases'],
         'name': 'Organization',
         'slots': ['mission_statement', 'founding_date', 'founding_location']})

    mission_statement: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'mission_statement',
         'domain_of': ['Organization'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'mission_statement',
         'owner': 'Organization',
         'range': 'string'} })
    founding_date: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'founding_date',
         'domain_of': ['Organization'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'founding_date',
         'owner': 'Organization',
         'range': 'string'} })
    founding_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'founding_location',
         'domain_of': ['Organization'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'founding_location',
         'owner': 'Organization',
         'range': 'Place'} })
    aliases: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'aliases',
         'owner': 'Organization',
         'range': 'string'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'Organization',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'Organization',
         'range': 'string',
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'Organization',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'image',
         'owner': 'Organization',
         'range': 'string',
         'slot_uri': 'schema:image'} })


class Place(HasAliases):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'mixins': ['HasAliases'],
         'name': 'Place',
         'slots': ['id', 'name']})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'Place',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'Place',
         'range': 'string',
         'slot_uri': 'schema:name'} })
    aliases: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'aliases',
         'owner': 'Place',
         'range': 'string'} })


class Address(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:PostalAddress',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'Address',
         'slots': ['street', 'city', 'postal_code']})

    street: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'street',
         'domain_of': ['Address'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'street',
         'owner': 'Address',
         'range': 'string'} })
    city: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'city',
         'domain_of': ['Address'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'city',
         'owner': 'Address',
         'range': 'string'} })
    postal_code: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'postal_code',
         'domain_of': ['Address'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'postal_code',
         'owner': 'Address',
         'range': 'string'} })


class Event(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['schema:Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'Event',
         'slots': ['started_at_time', 'ended_at_time', 'duration', 'is_current']})

    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'started_at_time',
         'owner': 'Event',
         'range': 'date',
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'ended_at_time',
         'owner': 'Event',
         'range': 'date',
         'slot_uri': 'prov:endedAtTime'} })
    duration: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'duration',
         'domain_of': ['Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'duration',
         'owner': 'Event',
         'range': 'float'} })
    is_current: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'is_current',
         'domain_of': ['Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'is_current',
         'owner': 'Event',
         'range': 'boolean'} })


class Concept(NamedThing):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'NamedThing',
         'name': 'Concept'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'Concept',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'Concept',
         'range': 'string',
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'Concept',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'image',
         'owner': 'Concept',
         'range': 'string',
         'slot_uri': 'schema:image'} })


class DiagnosisConcept(Concept):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Concept',
         'name': 'DiagnosisConcept'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'DiagnosisConcept',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'DiagnosisConcept',
         'range': 'string',
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'DiagnosisConcept',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'image',
         'owner': 'DiagnosisConcept',
         'range': 'string',
         'slot_uri': 'schema:image'} })


class ProcedureConcept(Concept):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Concept',
         'name': 'ProcedureConcept'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'ProcedureConcept',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'ProcedureConcept',
         'range': 'string',
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'ProcedureConcept',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    image: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'image',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'image',
         'owner': 'ProcedureConcept',
         'range': 'string',
         'slot_uri': 'schema:image'} })


class Relationship(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'Relationship',
         'slots': ['started_at_time', 'ended_at_time', 'related_to', 'type']})

    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'started_at_time',
         'owner': 'Relationship',
         'range': 'date',
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'ended_at_time',
         'owner': 'Relationship',
         'range': 'date',
         'slot_uri': 'prov:endedAtTime'} })
    related_to: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'related_to',
         'domain_of': ['Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'related_to',
         'owner': 'Relationship',
         'range': 'string'} })
    type: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'type',
         'owner': 'Relationship',
         'range': 'string'} })


class FamilialRelationship(Relationship):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Relationship',
         'name': 'FamilialRelationship',
         'slot_usage': {'related_to': {'name': 'related_to',
                                       'range': 'Person',
                                       'required': True},
                        'type': {'name': 'type',
                                 'range': 'FamilialRelationshipType',
                                 'required': True}}})

    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'started_at_time',
         'owner': 'FamilialRelationship',
         'range': 'date',
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'ended_at_time',
         'owner': 'FamilialRelationship',
         'range': 'date',
         'slot_uri': 'prov:endedAtTime'} })
    related_to: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'related_to',
         'domain_of': ['Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'related_to',
         'owner': 'FamilialRelationship',
         'range': 'Person',
         'required': True} })
    type: FamilialRelationshipType = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'type',
         'owner': 'FamilialRelationship',
         'range': 'FamilialRelationshipType',
         'required': True} })


class EmploymentEvent(Event):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Event',
         'name': 'EmploymentEvent',
         'slots': ['employed_at']})

    employed_at: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'employed_at',
         'domain_of': ['EmploymentEvent'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'employed_at',
         'owner': 'EmploymentEvent',
         'range': 'Organization'} })
    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'started_at_time',
         'owner': 'EmploymentEvent',
         'range': 'date',
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'ended_at_time',
         'owner': 'EmploymentEvent',
         'range': 'date',
         'slot_uri': 'prov:endedAtTime'} })
    duration: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'duration',
         'domain_of': ['Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'duration',
         'owner': 'EmploymentEvent',
         'range': 'float'} })
    is_current: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'is_current',
         'domain_of': ['Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'is_current',
         'owner': 'EmploymentEvent',
         'range': 'boolean'} })


class MedicalEvent(Event):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Event',
         'name': 'MedicalEvent',
         'slots': ['in_location', 'diagnosis', 'procedure']})

    in_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'in_location',
         'domain_of': ['MedicalEvent', 'WithLocation'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'in_location',
         'owner': 'MedicalEvent',
         'range': 'Place'} })
    diagnosis: Optional[DiagnosisConcept] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'diagnosis',
         'domain_of': ['MedicalEvent'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined': True,
         'name': 'diagnosis',
         'owner': 'MedicalEvent',
         'range': 'DiagnosisConcept'} })
    procedure: Optional[ProcedureConcept] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'procedure',
         'domain_of': ['MedicalEvent'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined': True,
         'name': 'procedure',
         'owner': 'MedicalEvent',
         'range': 'ProcedureConcept'} })
    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'started_at_time',
         'owner': 'MedicalEvent',
         'range': 'date',
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'ended_at_time',
         'owner': 'MedicalEvent',
         'range': 'date',
         'slot_uri': 'prov:endedAtTime'} })
    duration: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'duration',
         'domain_of': ['Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'duration',
         'owner': 'MedicalEvent',
         'range': 'float'} })
    is_current: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'is_current',
         'domain_of': ['Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'is_current',
         'owner': 'MedicalEvent',
         'range': 'boolean'} })


class WithLocation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'mixin': True,
         'name': 'WithLocation',
         'slots': ['in_location']})

    in_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'in_location',
         'domain_of': ['MedicalEvent', 'WithLocation'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'in_location',
         'owner': 'WithLocation',
         'range': 'Place'} })


class Container(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'Container',
         'slots': ['persons', 'organizations'],
         'tree_root': True})

    persons: Optional[list[Person]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'persons',
         'domain_of': ['Container'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined': True,
         'inlined_as_list': True,
         'multivalued': True,
         'name': 'persons',
         'owner': 'Container',
         'range': 'Person'} })
    organizations: Optional[list[Organization]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'organizations',
         'domain_of': ['Container'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined': True,
         'inlined_as_list': True,
         'multivalued': True,
         'name': 'organizations',
         'owner': 'Container',
         'range': 'Organization'} })


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
