# Part 9: Larger schemas

personinfo.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
description: |-
  Information about people, based on [schema.org](http://schema.org)
license: https://creativecommons.org/publicdomain/zero/1.0/
default_curi_maps:
  - semweb_context
imports:
  - linkml:types
prefixes:
  personinfo: https://w3id.org/linkml/examples/personinfo/
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  prov: http://www.w3.org/ns/prov#
  GSSO: http://purl.obolibrary.org/obo/GSSO_
  famrel: https://example.org/FamilialRelations#
default_prefix: personinfo
default_range: string

emit_prefixes:
  - rdf
  - rdfs
  - xsd
  - skos

classes:

  NamedThing:
    description: >-
      A generic grouping for any identifiable entity
    slots:
      - id
      - name
      - description
      - image
    close_mappings:
     - schema:Thing

  Person:
    is_a: NamedThing
    description: >-
      A person (alive, dead, undead, or fictional).
    class_uri: schema:Person
    mixins:
      - HasAliases
    slots:
      - primary_email
      - birth_date
      - age_in_years
      - gender
      - current_address
      - has_employment_history
      - has_familial_relationships
      - has_medical_history
    slot_usage:
      primary_email:
        pattern: "^\\S+@[\\S+\\.]+\\S+"
    in_subset:
      - basic_subset
  
  HasAliases:
    description: >-
      A mixin applied to any class that can have aliases/alternateNames
    mixin: true
    attributes:
      aliases:
        multivalued: true
        exact_mappings:
          - schema:alternateName


  Organization:
    description: >-
      An organization such as a company or university
    is_a: NamedThing
    class_uri: schema:Organization
    mixins:
      - HasAliases
    slots:
      - mission_statement
      - founding_date
      - founding_location

  Place:
    mixins:
      - HasAliases
    slots:
      - id
      - name
      
  Address:
    class_uri: schema:PostalAddress
    slots:
      - street
      - city
      - postal_code

  Event:
    slots:
      - started_at_time
      - ended_at_time
      - duration
      - is_current
    close_mappings:
      - schema:Event

  Concept:
    is_a: NamedThing

  DiagnosisConcept:
    is_a: Concept

  ProcedureConcept:
    is_a: Concept
      

  Relationship:
    slots:
      - started_at_time
      - ended_at_time
      - related_to
      - type

  FamilialRelationship:
    is_a: Relationship
    slot_usage:
      type:
        range: FamilialRelationshipType
        required: true
      related to:
        range: Person
        required: true

  EmploymentEvent:
    is_a: Event
    slots:
      - employed_at

  MedicalEvent:
    is_a: Event
    slots:
      - in_location
      - diagnosis
      - procedure

  WithLocation:
    mixin: true
    slots:
      - in_location

  # TODO: annotate that this is a container/root class
  Container:
    slots:
      - persons
      - organizations

slots:
  id:
    identifier: true
    slot_uri: schema:identifier
  name:
    slot_uri: schema:name
  description:
    slot_uri: schema:description
  image:
    slot_uri: schema:image
  gender:
    slot_uri: schema:gender
    range: GenderType
  primary_email:
    slot_uri: schema:email
  birth_date:
    slot_uri: schema:birthDate
  employed_at:
    range: Organization
  is_current:
    range: boolean
  has_employment_history:
    range: EmploymentEvent
    multivalued: true
    inlined_as_list: true
  has_medical_history:
    range: MedicalEvent
    multivalued: true
    inlined_as_list: true
  has_familial_relationships:
    range: FamilialRelationship
    multivalued: true
    inlined_as_list: true
  in_location:
    range: Place
  current_address:
    description: >-
      The address at which a person currently lives
    range: Address
  age_in_years:
    range: integer
    minimum_value: 0
    maximum_value: 999
  related_to:
  type:
  street:
  city:
  mission_statement:
  founding_date:
  founding_location:
    range: Place
  postal_code:
    range: string
  started_at_time:
    slot_uri: prov:startedAtTime
    range: date
  duration:
    range: float
  diagnosis:
    range: DiagnosisConcept
    inlined: true
  procedure:
    range: ProcedureConcept
    inlined: true

  ended_at_time:
    slot_uri: prov:endedAtTime
    range: date

  persons:
    range: Person
    inlined: true
    inlined_as_list: true
    multivalued: true
  organizations:
    range: Organization
    inlined_as_list: true
    inlined: true
    multivalued: true
    
enums:
  FamilialRelationshipType:
    permissible_values:
      SIBLING_OF:
        meaning: famrel:01
      PARENT_OF:
        meaning: famrel:02
      CHILD_OF:
        meaning: famrel:01
  GenderType:
    permissible_values:
      nonbinary man:
        meaning: GSSO:009254
      nonbinary woman:
        meaning: GSSO:009253
      transgender woman:
        meaning: GSSO:000384
      transgender man:
        meaning: GSSO:000372
      cisgender man:
        meaning: GSSO:000371
      cisgender woman:
        meaning: GSSO:000385
  DiagnosisType:

subsets:
  basic_subset:
    description: A subset of the schema that handles basic information

```

Get a summary:

```bash
gen-yaml -v personinfo.yaml
```

Will output something like:

```text
Classes: 16
        Referenced by: 9 classes, 15 slots, 0 types, 0 enums 
        Root: 8
        Leaf: 10
        Standalone: 15
        Declared mixin: 2
        Undeclared mixin: 0
        Abstract: 0

Slots: 35
        Referenced by: 16 classes, 3 slots, 0 types, 0 enums 
        Root: 32
        Leaf: 32
        Standalone: 40
        Declared mixin: 0
        Undeclared mixin: 0
        Abstract: 0
        Domain unspecified: 32
        Ranges:
                Type:
                        boolean: 1
                        date: 2
                        float: 1
                        integer: 1
                        string: 15
                Class:
                        Address: 1
                        DiagnosisConcept: 1
                        EmploymentEvent: 1
                        FamilialRelationship: 1
                        MedicalEvent: 1
                        Organization: 2
                        Person: 3
                        Place: 2
                        ProcedureConcept: 1
                Unknown:
                        FamilialRelationshipType: 1
                        GenderType: 1                        
```


...

