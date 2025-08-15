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
                 'Concept': {'attributes': {'code system': {'domain_of': ['Concept'],
                                                            'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                                            'name': 'code system',
                                                            'range': 'code system'},
                                            'mappings': {'domain_of': ['Concept'],
                                                         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                                         'multivalued': True,
                                                         'name': 'mappings',
                                                         'range': 'CrossReference',
                                                         'slot_uri': 'skos:exactMatch'}},
                             'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                             'is_a': 'NamedThing',
                             'name': 'Concept'},
                 'Container': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'name': 'Container',
                               'slots': ['persons', 'organizations', 'places'],
                               'tree_root': True},
                 'DiagnosisConcept': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                      'is_a': 'Concept',
                                      'name': 'DiagnosisConcept'},
                 'EmploymentEvent': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                     'is_a': 'Event',
                                     'name': 'EmploymentEvent',
                                     'slots': ['employed_at', 'salary']},
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
                                          'slot_usage': {'related to': {'name': 'related '
                                                                                'to',
                                                                        'range': 'Person',
                                                                        'required': True},
                                                         'type': {'name': 'type',
                                                                  'range': 'FamilialRelationshipType',
                                                                  'required': True}}},
                 'HasAliases': {'attributes': {'aliases': {'domain_of': ['HasAliases'],
                                                           'exact_mappings': ['schema:alternateName'],
                                                           'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                                           'multivalued': True,
                                                           'name': 'aliases',
                                                           'singular_name': 'alias'}},
                                'description': 'A mixin applied to any class that '
                                               'can have aliases/alternateNames',
                                'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                'mixin': True,
                                'name': 'HasAliases'},
                 'HasNewsEvents': {'attributes': {'has_news_events': {'domain_of': ['HasNewsEvents'],
                                                                      'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                                                      'multivalued': True,
                                                                      'name': 'has_news_events',
                                                                      'range': 'NewsEvent',
                                                                      'singular_name': 'has_news_event'}},
                                   'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                   'mixin': True,
                                   'name': 'HasNewsEvents'},
                 'ImagingProcedureConcept': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                             'is_a': 'ProcedureConcept',
                                             'name': 'ImagingProcedureConcept'},
                 'IntegerPrimaryKeyObject': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                             'name': 'IntegerPrimaryKeyObject',
                                             'slots': ['int_id']},
                 'InterPersonalRelationship': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                               'is_a': 'Relationship',
                                               'name': 'InterPersonalRelationship',
                                               'slot_usage': {'related to': {'name': 'related '
                                                                                     'to',
                                                                             'range': 'Person',
                                                                             'required': True},
                                                              'type': {'any_of': [{'range': 'FamilialRelationshipType'},
                                                                                  {'range': 'NonFamilialRelationshipType'}],
                                                                       'name': 'type',
                                                                       'required': True}}},
                 'MedicalEvent': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'is_a': 'Event',
                                  'mixins': ['WithLocation'],
                                  'name': 'MedicalEvent',
                                  'slots': ['diagnosis', 'procedure']},
                 'NamedThing': {'close_mappings': ['schema:Thing'],
                                'description': 'A generic grouping for any '
                                               'identifiable entity',
                                'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                'name': 'NamedThing',
                                'slots': ['id',
                                          'name',
                                          'description',
                                          'depicted_by']},
                 'NewsEvent': {'attributes': {'headline': {'domain_of': ['NewsEvent'],
                                                           'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                                           'name': 'headline'}},
                               'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'is_a': 'Event',
                               'name': 'NewsEvent'},
                 'OperationProcedureConcept': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                               'is_a': 'ProcedureConcept',
                                               'name': 'OperationProcedureConcept'},
                 'Organization': {'class_uri': 'schema:Organization',
                                  'description': 'An organization such as a '
                                                 'company or university',
                                  'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'is_a': 'NamedThing',
                                  'mixins': ['HasAliases', 'HasNewsEvents'],
                                  'name': 'Organization',
                                  'rules': [{'postconditions': {'slot_conditions': {'score': {'maximum_value': 0,
                                                                                              'name': 'score'}}},
                                             'preconditions': {'slot_conditions': {'min_salary': {'maximum_value': 80000.0,
                                                                                                  'name': 'min_salary'}}}}],
                                  'slot_usage': {'categories': {'name': 'categories',
                                                                'range': 'OrganizationType'}},
                                  'slots': ['mission_statement',
                                            'founding_date',
                                            'founding location',
                                            'categories',
                                            'score',
                                            'min_salary']},
                 'Person': {'class_uri': 'schema:Person',
                            'description': 'A person (alive, dead, undead, or '
                                           'fictional).',
                            'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                            'in_subset': ['basic_subset'],
                            'is_a': 'NamedThing',
                            'mixins': ['HasAliases', 'HasNewsEvents'],
                            'name': 'Person',
                            'slot_usage': {'age_in_years': {'name': 'age_in_years',
                                                            'recommended': True},
                                           'primary_email': {'name': 'primary_email',
                                                             'pattern': '^\\S+@[\\S+\\.]+\\S+'},
                                           'telephone': {'name': 'telephone',
                                                         'recommended': True}},
                            'slots': ['primary_email',
                                      'birth_date',
                                      'age_in_years',
                                      'gender',
                                      'current_address',
                                      'telephone',
                                      'has_employment_history',
                                      'has_familial_relationships',
                                      'has_interpersonal_relationships',
                                      'has_medical_history']},
                 'Place': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                           'mixins': ['HasAliases'],
                           'name': 'Place',
                           'slots': ['id', 'name', 'depicted_by']},
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
                                  'slots': ['in_location']},
                 'code system': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                 'name': 'code system',
                                 'slots': ['id', 'name']}},
     'default_curi_maps': ['semweb_context'],
     'default_prefix': 'personinfo',
     'default_range': 'string',
     'description': 'Information about people, based on '
                    '[schema.org](http://schema.org)',
     'emit_prefixes': ['rdf', 'rdfs', 'xsd', 'skos'],
     'enums': {'DiagnosisType': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                 'name': 'DiagnosisType',
                                 'permissible_values': {'todo': {'text': 'todo'}}},
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
                                                                                   'woman'}}},
               'NonFamilialRelationshipType': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                               'name': 'NonFamilialRelationshipType',
                                               'permissible_values': {'BEST_FRIEND_OF': {'text': 'BEST_FRIEND_OF'},
                                                                      'COWORKER_OF': {'meaning': 'famrel:70',
                                                                                      'text': 'COWORKER_OF'},
                                                                      'MORTAL_ENEMY_OF': {'text': 'MORTAL_ENEMY_OF'},
                                                                      'ROOMMATE_OF': {'meaning': 'famrel:71',
                                                                                      'text': 'ROOMMATE_OF'}}},
               'OrganizationType': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                    'name': 'OrganizationType',
                                    'permissible_values': {'charity': {'meaning': 'bizcodes:001',
                                                                       'text': 'charity'},
                                                           'for profit': {'text': 'for '
                                                                                  'profit'},
                                                           'loose organization': {'text': 'loose '
                                                                                          'organization'},
                                                           'non profit': {'text': 'non '
                                                                                  'profit'},
                                                           'offshore': {'text': 'offshore'},
                                                           'shell company': {'text': 'shell '
                                                                                     'company'}}}},
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
                  'bizcodes': {'prefix_prefix': 'bizcodes',
                               'prefix_reference': 'https://example.org/bizcodes/'},
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
                             'prefix_reference': 'http://schema.org/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'slots': {'age_in_years': {'alias': 'age',
                                'domain_of': ['Person'],
                                'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                'maximum_value': 999,
                                'minimum_value': 0,
                                'name': 'age_in_years',
                                'range': 'integer'},
               'birth_date': {'domain_of': ['Person'],
                              'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'name': 'birth_date',
                              'slot_uri': 'schema:birthDate'},
               'categories': {'domain_of': ['Organization'],
                              'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'multivalued': True,
                              'name': 'categories'},
               'city': {'domain_of': ['Address'],
                        'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                        'name': 'city'},
               'current_address': {'description': 'The address at which a person '
                                                  'currently lives',
                                   'domain_of': ['Person'],
                                   'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                   'name': 'current_address',
                                   'range': 'Address'},
               'depicted_by': {'domain_of': ['NamedThing', 'Place'],
                               'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'name': 'depicted_by',
                               'range': 'ImageURL'},
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
               'founding location': {'domain_of': ['Organization'],
                                     'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                     'name': 'founding location',
                                     'range': 'Place'},
               'founding_date': {'domain_of': ['Organization'],
                                 'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                 'name': 'founding_date'},
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
               'has_interpersonal_relationships': {'domain_of': ['Person'],
                                                   'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                                   'inlined': True,
                                                   'inlined_as_list': True,
                                                   'multivalued': True,
                                                   'name': 'has_interpersonal_relationships',
                                                   'range': 'InterPersonalRelationship'},
               'has_medical_history': {'domain_of': ['Person'],
                                       'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                       'inlined': True,
                                       'inlined_as_list': True,
                                       'multivalued': True,
                                       'name': 'has_medical_history',
                                       'range': 'MedicalEvent'},
               'id': {'domain_of': ['NamedThing', 'Place', 'code system'],
                      'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                      'identifier': True,
                      'name': 'id',
                      'range': 'uriorcurie',
                      'required': True,
                      'slot_uri': 'schema:identifier'},
               'image': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                         'name': 'image',
                         'slot_uri': 'schema:image'},
               'in_location': {'domain_of': ['WithLocation'],
                               'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                               'name': 'in_location',
                               'range': 'Place'},
               'int_id': {'domain_of': ['IntegerPrimaryKeyObject'],
                          'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                          'identifier': True,
                          'name': 'int_id',
                          'range': 'integer',
                          'required': True,
                          'slot_uri': 'schema:int_identifier'},
               'is_current': {'domain_of': ['Event'],
                              'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'name': 'is_current',
                              'range': 'boolean'},
               'min_salary': {'domain_of': ['Organization'],
                              'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'name': 'min_salary',
                              'range': 'SalaryType'},
               'mission_statement': {'domain_of': ['Organization'],
                                     'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                     'name': 'mission_statement'},
               'name': {'domain_of': ['NamedThing', 'Place', 'code system'],
                        'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                        'name': 'name',
                        'required': True,
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
               'places': {'domain_of': ['Container'],
                          'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                          'inlined': True,
                          'inlined_as_list': True,
                          'multivalued': True,
                          'name': 'places',
                          'range': 'Place'},
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
                              'name': 'related_to',
                              'range': 'Person'},
               'salary': {'domain_of': ['EmploymentEvent'],
                          'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                          'name': 'salary',
                          'range': 'SalaryType'},
               'score': {'description': 'A score between 0 and 5, represented as a '
                                        'decimal',
                         'domain_of': ['Organization'],
                         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                         'maximum_value': 5.0,
                         'minimum_value': 0.0,
                         'name': 'score',
                         'range': 'decimal'},
               'started_at_time': {'domain_of': ['Event', 'Relationship'],
                                   'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                   'name': 'started_at_time',
                                   'range': 'date',
                                   'slot_uri': 'prov:startedAtTime'},
               'street': {'domain_of': ['Address'],
                          'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                          'name': 'street'},
               'telephone': {'domain_of': ['Person'],
                             'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                             'name': 'telephone',
                             'pattern': '^[\\d\\(\\)\\-]+$',
                             'slot_uri': 'schema:telephone'},
               'type': {'domain_of': ['Relationship'],
                        'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                        'name': 'type'}},
     'source_file': 'personinfo.yaml',
     'subsets': {'basic_subset': {'description': 'A subset of the schema that '
                                                 'handles basic information',
                                  'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'name': 'basic_subset'}},
     'types': {'CrossReference': {'base': 'str',
                                  'description': 'A string URI or CURIE '
                                                 'representation of an external '
                                                 'identifier, modeled as a '
                                                 'Resource in RDF',
                                  'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                  'name': 'CrossReference',
                                  'typeof': 'uriorcurie',
                                  'uri': 'rdfs:Resource'},
               'ImageURL': {'base': 'str',
                            'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                            'name': 'ImageURL',
                            'typeof': 'uri',
                            'uri': 'xsd:anyURI'},
               'SalaryType': {'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                              'name': 'SalaryType',
                              'typeof': 'decimal'}}} )

class FamilialRelationshipType(str, Enum):
    SIBLING_OF = "SIBLING_OF"
    PARENT_OF = "PARENT_OF"
    CHILD_OF = "CHILD_OF"


class NonFamilialRelationshipType(str, Enum):
    COWORKER_OF = "COWORKER_OF"
    ROOMMATE_OF = "ROOMMATE_OF"
    BEST_FRIEND_OF = "BEST_FRIEND_OF"
    MORTAL_ENEMY_OF = "MORTAL_ENEMY_OF"


class GenderType(str, Enum):
    nonbinary_man = "nonbinary man"
    nonbinary_woman = "nonbinary woman"
    transgender_woman = "transgender woman"
    transgender_man = "transgender man"
    cisgender_man = "cisgender man"
    cisgender_woman = "cisgender woman"


class DiagnosisType(str, Enum):
    todo = "todo"


class OrganizationType(str, Enum):
    non_profit = "non profit"
    for_profit = "for profit"
    offshore = "offshore"
    charity = "charity"
    shell_company = "shell company"
    loose_organization = "loose organization"



class NamedThing(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['schema:Thing'],
         'description': 'A generic grouping for any identifiable entity',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'NamedThing',
         'slots': ['id', 'name', 'description', 'depicted_by']})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'NamedThing',
         'range': 'uriorcurie',
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'NamedThing',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'NamedThing',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'NamedThing',
         'range': 'ImageURL'} })


class HasAliases(ConfiguredBaseModel):
    """
    A mixin applied to any class that can have aliases/alternateNames
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'attributes': {'aliases': {'domain_of': ['HasAliases'],
                                    'exact_mappings': ['schema:alternateName'],
                                    'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                    'multivalued': True,
                                    'name': 'aliases',
                                    'singular_name': 'alias'}},
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
         'range': 'string',
         'singular_name': 'alias'} })


class HasNewsEvents(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'attributes': {'has_news_events': {'domain_of': ['HasNewsEvents'],
                                            'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                            'multivalued': True,
                                            'name': 'has_news_events',
                                            'range': 'NewsEvent',
                                            'singular_name': 'has_news_event'}},
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'mixin': True,
         'name': 'HasNewsEvents'})

    has_news_events: Optional[list[NewsEvent]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_news_events',
         'domain_of': ['HasNewsEvents'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'has_news_events',
         'owner': 'HasNewsEvents',
         'range': 'NewsEvent',
         'singular_name': 'has_news_event'} })


class Person(HasNewsEvents, HasAliases, NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Person',
         'description': 'A person (alive, dead, undead, or fictional).',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'in_subset': ['basic_subset'],
         'is_a': 'NamedThing',
         'mixins': ['HasAliases', 'HasNewsEvents'],
         'name': 'Person',
         'slot_usage': {'age_in_years': {'name': 'age_in_years', 'recommended': True},
                        'primary_email': {'name': 'primary_email',
                                          'pattern': '^\\S+@[\\S+\\.]+\\S+'},
                        'telephone': {'name': 'telephone', 'recommended': True}},
         'slots': ['primary_email',
                   'birth_date',
                   'age_in_years',
                   'gender',
                   'current_address',
                   'telephone',
                   'has_employment_history',
                   'has_familial_relationships',
                   'has_interpersonal_relationships',
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
    age: Optional[int] = Field(default=None, ge=0, le=999, json_schema_extra = { "linkml_meta": {'alias': 'age',
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
    telephone: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'telephone',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'telephone',
         'owner': 'Person',
         'pattern': '^[\\d\\(\\)\\-]+$',
         'range': 'string',
         'recommended': True,
         'slot_uri': 'schema:telephone'} })
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
    has_interpersonal_relationships: Optional[list[InterPersonalRelationship]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_interpersonal_relationships',
         'domain_of': ['Person'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined_as_list': True,
         'multivalued': True,
         'name': 'has_interpersonal_relationships',
         'owner': 'Person',
         'range': 'InterPersonalRelationship'} })
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
         'range': 'string',
         'singular_name': 'alias'} })
    has_news_events: Optional[list[NewsEvent]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_news_events',
         'domain_of': ['HasNewsEvents'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'has_news_events',
         'owner': 'Person',
         'range': 'NewsEvent',
         'singular_name': 'has_news_event'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'Person',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'Person',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'Person',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'Person',
         'range': 'ImageURL'} })

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

    @field_validator('telephone')
    def pattern_telephone(cls, v):
        pattern=re.compile(r"^[\d\(\)\-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid telephone format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid telephone format: {v}"
            raise ValueError(err_msg)
        return v


class Organization(HasNewsEvents, HasAliases, NamedThing):
    """
    An organization such as a company or university
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Organization',
         'description': 'An organization such as a company or university',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'NamedThing',
         'mixins': ['HasAliases', 'HasNewsEvents'],
         'name': 'Organization',
         'rules': [{'postconditions': {'slot_conditions': {'score': {'maximum_value': 0,
                                                                     'name': 'score'}}},
                    'preconditions': {'slot_conditions': {'min_salary': {'maximum_value': 80000.0,
                                                                         'name': 'min_salary'}}}}],
         'slot_usage': {'categories': {'name': 'categories',
                                       'range': 'OrganizationType'}},
         'slots': ['mission_statement',
                   'founding_date',
                   'founding location',
                   'categories',
                   'score',
                   'min_salary']})

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
         'name': 'founding location',
         'owner': 'Organization',
         'range': 'Place'} })
    categories: Optional[list[OrganizationType]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'categories',
         'domain_of': ['Organization'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'categories',
         'owner': 'Organization',
         'range': 'OrganizationType'} })
    score: Optional[Decimal] = Field(default=None, description="""A score between 0 and 5, represented as a decimal""", ge=0.0, le=5.0, json_schema_extra = { "linkml_meta": {'alias': 'score',
         'description': 'A score between 0 and 5, represented as a decimal',
         'domain_of': ['Organization'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'maximum_value': 5.0,
         'minimum_value': 0.0,
         'name': 'score',
         'owner': 'Organization',
         'range': 'decimal'} })
    min_salary: Optional[Decimal] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'min_salary',
         'domain_of': ['Organization'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'min_salary',
         'owner': 'Organization',
         'range': 'SalaryType'} })
    aliases: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'aliases',
         'owner': 'Organization',
         'range': 'string',
         'singular_name': 'alias'} })
    has_news_events: Optional[list[NewsEvent]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'has_news_events',
         'domain_of': ['HasNewsEvents'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'has_news_events',
         'owner': 'Organization',
         'range': 'NewsEvent',
         'singular_name': 'has_news_event'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'Organization',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'Organization',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'Organization',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'Organization',
         'range': 'ImageURL'} })


class Place(HasAliases):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'mixins': ['HasAliases'],
         'name': 'Place',
         'slots': ['id', 'name', 'depicted_by']})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'Place',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'Place',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'Place',
         'range': 'ImageURL'} })
    aliases: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'domain_of': ['HasAliases'],
         'exact_mappings': ['schema:alternateName'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'aliases',
         'owner': 'Place',
         'range': 'string',
         'singular_name': 'alias'} })


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


class NewsEvent(Event):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'attributes': {'headline': {'domain_of': ['NewsEvent'],
                                     'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                     'name': 'headline'}},
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Event',
         'name': 'NewsEvent'})

    headline: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'headline',
         'domain_of': ['NewsEvent'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'headline',
         'owner': 'NewsEvent',
         'range': 'string'} })
    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'started_at_time',
         'owner': 'NewsEvent',
         'range': 'date',
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'ended_at_time',
         'owner': 'NewsEvent',
         'range': 'date',
         'slot_uri': 'prov:endedAtTime'} })
    duration: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'duration',
         'domain_of': ['Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'duration',
         'owner': 'NewsEvent',
         'range': 'float'} })
    is_current: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'is_current',
         'domain_of': ['Event'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'is_current',
         'owner': 'NewsEvent',
         'range': 'boolean'} })


class Concept(NamedThing):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'attributes': {'code system': {'domain_of': ['Concept'],
                                        'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                        'name': 'code system',
                                        'range': 'code system'},
                        'mappings': {'domain_of': ['Concept'],
                                     'from_schema': 'https://w3id.org/linkml/examples/personinfo',
                                     'multivalued': True,
                                     'name': 'mappings',
                                     'range': 'CrossReference',
                                     'slot_uri': 'skos:exactMatch'}},
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'NamedThing',
         'name': 'Concept'})

    code_system: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'code_system',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'code system',
         'owner': 'Concept',
         'range': 'code system'} })
    mappings: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'mappings',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'mappings',
         'owner': 'Concept',
         'range': 'CrossReference',
         'slot_uri': 'skos:exactMatch'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'Concept',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'Concept',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'Concept',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'Concept',
         'range': 'ImageURL'} })


class DiagnosisConcept(Concept):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Concept',
         'name': 'DiagnosisConcept'})

    code_system: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'code_system',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'code system',
         'owner': 'DiagnosisConcept',
         'range': 'code system'} })
    mappings: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'mappings',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'mappings',
         'owner': 'DiagnosisConcept',
         'range': 'CrossReference',
         'slot_uri': 'skos:exactMatch'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'DiagnosisConcept',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'DiagnosisConcept',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'DiagnosisConcept',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'DiagnosisConcept',
         'range': 'ImageURL'} })


class ProcedureConcept(Concept):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Concept',
         'name': 'ProcedureConcept'})

    code_system: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'code_system',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'code system',
         'owner': 'ProcedureConcept',
         'range': 'code system'} })
    mappings: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'mappings',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'mappings',
         'owner': 'ProcedureConcept',
         'range': 'CrossReference',
         'slot_uri': 'skos:exactMatch'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'ProcedureConcept',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'ProcedureConcept',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'ProcedureConcept',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'ProcedureConcept',
         'range': 'ImageURL'} })


class IntegerPrimaryKeyObject(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'IntegerPrimaryKeyObject',
         'slots': ['int_id']})

    int_id: int = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'int_id',
         'domain_of': ['IntegerPrimaryKeyObject'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'int_id',
         'owner': 'IntegerPrimaryKeyObject',
         'range': 'integer',
         'slot_uri': 'schema:int_identifier'} })


class OperationProcedureConcept(ProcedureConcept):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'ProcedureConcept',
         'name': 'OperationProcedureConcept'})

    code_system: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'code_system',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'code system',
         'owner': 'OperationProcedureConcept',
         'range': 'code system'} })
    mappings: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'mappings',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'mappings',
         'owner': 'OperationProcedureConcept',
         'range': 'CrossReference',
         'slot_uri': 'skos:exactMatch'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'OperationProcedureConcept',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'OperationProcedureConcept',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'OperationProcedureConcept',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'OperationProcedureConcept',
         'range': 'ImageURL'} })


class ImagingProcedureConcept(ProcedureConcept):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'ProcedureConcept',
         'name': 'ImagingProcedureConcept'})

    code_system: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'code_system',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'code system',
         'owner': 'ImagingProcedureConcept',
         'range': 'code system'} })
    mappings: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'mappings',
         'domain_of': ['Concept'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'multivalued': True,
         'name': 'mappings',
         'owner': 'ImagingProcedureConcept',
         'range': 'CrossReference',
         'slot_uri': 'skos:exactMatch'} })
    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'ImagingProcedureConcept',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'ImagingProcedureConcept',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['NamedThing'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'description',
         'owner': 'ImagingProcedureConcept',
         'range': 'string',
         'slot_uri': 'schema:description'} })
    depicted_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'depicted_by',
         'domain_of': ['NamedThing', 'Place'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'depicted_by',
         'owner': 'ImagingProcedureConcept',
         'range': 'ImageURL'} })


class CodeSystem(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'code system',
         'slots': ['id', 'name']})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'identifier': True,
         'name': 'id',
         'owner': 'code system',
         'range': 'uriorcurie',
         'required': True,
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['NamedThing', 'Place', 'code system'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'name',
         'owner': 'code system',
         'range': 'string',
         'required': True,
         'slot_uri': 'schema:name'} })


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
         'range': 'Person'} })
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
         'slot_usage': {'related to': {'name': 'related to',
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
    related_to: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'related_to',
         'domain_of': ['Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'related_to',
         'owner': 'FamilialRelationship',
         'range': 'Person'} })
    type: FamilialRelationshipType = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'type',
         'owner': 'FamilialRelationship',
         'range': 'FamilialRelationshipType',
         'required': True} })


class InterPersonalRelationship(Relationship):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Relationship',
         'name': 'InterPersonalRelationship',
         'slot_usage': {'related to': {'name': 'related to',
                                       'range': 'Person',
                                       'required': True},
                        'type': {'any_of': [{'range': 'FamilialRelationshipType'},
                                            {'range': 'NonFamilialRelationshipType'}],
                                 'name': 'type',
                                 'required': True}}})

    started_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'started_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'started_at_time',
         'owner': 'InterPersonalRelationship',
         'range': 'date',
         'slot_uri': 'prov:startedAtTime'} })
    ended_at_time: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'ended_at_time',
         'domain_of': ['Event', 'Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'ended_at_time',
         'owner': 'InterPersonalRelationship',
         'range': 'date',
         'slot_uri': 'prov:endedAtTime'} })
    related_to: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'related_to',
         'domain_of': ['Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'related_to',
         'owner': 'InterPersonalRelationship',
         'range': 'Person'} })
    type: Union[FamilialRelationshipType, NonFamilialRelationshipType] = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'type',
         'any_of': [{'range': 'FamilialRelationshipType'},
                    {'range': 'NonFamilialRelationshipType'}],
         'domain_of': ['Relationship'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'type',
         'owner': 'InterPersonalRelationship',
         'range': 'string',
         'required': True} })


class EmploymentEvent(Event):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Event',
         'name': 'EmploymentEvent',
         'slots': ['employed_at', 'salary']})

    employed_at: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'employed_at',
         'domain_of': ['EmploymentEvent'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'employed_at',
         'owner': 'EmploymentEvent',
         'range': 'Organization'} })
    salary: Optional[Decimal] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'salary',
         'domain_of': ['EmploymentEvent'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'salary',
         'owner': 'EmploymentEvent',
         'range': 'SalaryType'} })
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


class WithLocation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'mixin': True,
         'name': 'WithLocation',
         'slots': ['in_location']})

    in_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'in_location',
         'domain_of': ['WithLocation'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'in_location',
         'owner': 'WithLocation',
         'range': 'Place'} })


class MedicalEvent(WithLocation, Event):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'is_a': 'Event',
         'mixins': ['WithLocation'],
         'name': 'MedicalEvent',
         'slots': ['diagnosis', 'procedure']})

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
    in_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'in_location',
         'domain_of': ['WithLocation'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'in_location',
         'owner': 'MedicalEvent',
         'range': 'Place'} })
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


class Container(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'name': 'Container',
         'slots': ['persons', 'organizations', 'places'],
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
    places: Optional[list[Place]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'places',
         'domain_of': ['Container'],
         'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'inlined': True,
         'inlined_as_list': True,
         'multivalued': True,
         'name': 'places',
         'owner': 'Container',
         'range': 'Place'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
NamedThing.model_rebuild()
HasAliases.model_rebuild()
HasNewsEvents.model_rebuild()
Person.model_rebuild()
Organization.model_rebuild()
Place.model_rebuild()
Address.model_rebuild()
Event.model_rebuild()
NewsEvent.model_rebuild()
Concept.model_rebuild()
DiagnosisConcept.model_rebuild()
ProcedureConcept.model_rebuild()
IntegerPrimaryKeyObject.model_rebuild()
OperationProcedureConcept.model_rebuild()
ImagingProcedureConcept.model_rebuild()
CodeSystem.model_rebuild()
Relationship.model_rebuild()
FamilialRelationship.model_rebuild()
InterPersonalRelationship.model_rebuild()
EmploymentEvent.model_rebuild()
WithLocation.model_rebuild()
MedicalEvent.model_rebuild()
Container.model_rebuild()
