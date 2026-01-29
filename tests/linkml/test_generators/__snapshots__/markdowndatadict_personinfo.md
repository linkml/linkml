
# PERSONINFO


**metamodel version:** 1.7.0

**version:** None


Information about people, based on [schema.org](http://schema.org)


## Class Diagram

<svg>mock</svg>

## ERD Diagram

<svg>mock</svg>

## Base Classes


Foundational classes in the hierarchy (root classes and direct children of Thing):

| Class | Description |
| --- | --- |
| [Event](#event) |  |
| [NamedThing](#namedthing) | A generic grouping for any identifiable entity |
| [Relationship](#relationship) |  |

## Standalone Classes


These classes are completely isolated with no relationships and are not used as base classes:

| Class | Description |
| --- | --- |
| [IntegerPrimaryKeyObject](#integerprimarykeyobject) |  |

## Classes


### Address




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
Address:
  slots:
  - street
  - city
  - postal_code

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[city](#city)** | <sub>0..1</sub> | string |  |
| **[postal_code](#postal_code)** | <sub>0..1</sub> | string |  |
| **[street](#street)** | <sub>0..1</sub> | string |  |

#### Referenced by:

 *  **[Person](#person)** : current_address  <sub>0..1</sub> 




### Concept




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
Concept:
  is_a: NamedThing
  slots:
  - id
  - name
  - description
  - depicted_by
  - concept__code_system
  - concept__mappings
  attributes:
    code system:
      range: code system
    mappings:
      range: CrossReference
      multivalued: true

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>0..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[description](#description)** | <sub>0..1</sub> | string |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |
| **[code system](#code system)** | <sub>0..1</sub> | [CodeSystem](#codesystem) |  |
| **[mappings](#mappings)** | <sub>0..\*</sub> | CrossReference |  |

#### Parents

 * [NamedThing](#namedthing) - A generic grouping for any identifiable entity

#### Children

 * [DiagnosisConcept](#diagnosisconcept)
 * [ProcedureConcept](#procedureconcept)




### Container




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
Container:
  slots:
  - persons
  - organizations
  - places

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[organizations](#organizations)** | <sub>0..\*</sub> | [Organization](#organization) |  |
| **[persons](#persons)** | <sub>0..\*</sub> | [Person](#person) |  |
| **[places](#places)** | <sub>0..\*</sub> | [Place](#place) |  |




### DiagnosisConcept




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
DiagnosisConcept:
  is_a: Concept
  slots:
  - id
  - name
  - description
  - depicted_by
  - concept__code_system
  - concept__mappings

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[description](#description)** | <sub>0..1</sub> | string |  |
| **[code system](#code system)** | <sub>0..1</sub> | [CodeSystem](#codesystem) |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |
| **[mappings](#mappings)** | <sub>0..\*</sub> | CrossReference |  |

#### Parents

 * [Concept](#concept)

#### Referenced by:

 *  **[MedicalEvent](#medicalevent)** : diagnosis  <sub>0..1</sub> 




### EmploymentEvent




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
EmploymentEvent:
  is_a: Event
  slots:
  - started_at_time
  - ended_at_time
  - duration
  - is_current
  - employed_at
  - salary

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[duration](#duration)** | <sub>0..1</sub> | float |  |
| **[ended_at_time](#ended_at_time)** | <sub>0..1</sub> | date |  |
| **[is_current](#is_current)** | <sub>0..1</sub> | boolean |  |
| **[started_at_time](#started_at_time)** | <sub>0..1</sub> | date |  |
| **[employed_at](#employed_at)** | <sub>0..1</sub> | [Organization](#organization) |  |
| **[salary](#salary)** | <sub>0..1</sub> | SalaryType |  |

#### Parents

 * [Event](#event)

#### Referenced by:

 *  **[Person](#person)** : has_employment_history  <sub>0..\*</sub> 




### Event




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
Event:
  slots:
  - started_at_time
  - ended_at_time
  - duration
  - is_current

```
</details>


#### Local class diagram

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[duration](#duration)** | <sub>0..1</sub> | float |  |
| **[ended_at_time](#ended_at_time)** | <sub>0..1</sub> | date |  |
| **[is_current](#is_current)** | <sub>0..1</sub> | boolean |  |
| **[started_at_time](#started_at_time)** | <sub>0..1</sub> | date |  |

#### Children

 * [EmploymentEvent](#employmentevent)
 * [MedicalEvent](#medicalevent)
 * [NewsEvent](#newsevent)




### FamilialRelationship




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
FamilialRelationship:
  is_a: Relationship
  slots:
  - started_at_time
  - ended_at_time
  - related_to
  - FamilialRelationship_type
  - FamilialRelationship_related to
  slot_usage:
    type:
      range: FamilialRelationshipType
      required: true
    related to:
      range: Person
      required: true

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[ended_at_time](#ended_at_time)** | <sub>0..1</sub> | date |  |
| **[related_to](#related_to)** | <sub>0..1</sub> | [Person](#person) |  |
| **[started_at_time](#started_at_time)** | <sub>0..1</sub> | date |  |
| **[type](#type)** | <sub>1..1</sub> | [FamilialRelationshipType](#familialrelationshiptype) |  |

#### Parents

 * [Relationship](#relationship)

#### Referenced by:

 *  **[Person](#person)** : has_familial_relationships  <sub>0..\*</sub> 




### ImagingProcedureConcept




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
ImagingProcedureConcept:
  is_a: ProcedureConcept
  slots:
  - id
  - name
  - description
  - depicted_by
  - concept__code_system
  - concept__mappings

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[description](#description)** | <sub>0..1</sub> | string |  |
| **[code system](#code system)** | <sub>0..1</sub> | [CodeSystem](#codesystem) |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |
| **[mappings](#mappings)** | <sub>0..\*</sub> | CrossReference |  |

#### Parents

 * [ProcedureConcept](#procedureconcept)




### IntegerPrimaryKeyObject




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
IntegerPrimaryKeyObject:
  slots:
  - int_id

```
</details>


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[int_id](#int_id)** | <sub>0..1</sub> | integer |  |




### InterPersonalRelationship




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
InterPersonalRelationship:
  is_a: Relationship
  slots:
  - started_at_time
  - ended_at_time
  - related_to
  - InterPersonalRelationship_type
  - InterPersonalRelationship_related to
  slot_usage:
    type:
      required: true
    related to:
      range: Person
      required: true

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[ended_at_time](#ended_at_time)** | <sub>0..1</sub> | date |  |
| **[related_to](#related_to)** | <sub>0..1</sub> | [Person](#person) |  |
| **[started_at_time](#started_at_time)** | <sub>0..1</sub> | date |  |
| **[type](#type)** | <sub>1..1</sub> | string |  |

#### Parents

 * [Relationship](#relationship)

#### Referenced by:

 *  **[Person](#person)** : has_interpersonal_relationships  <sub>0..\*</sub> 




### MedicalEvent




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
MedicalEvent:
  is_a: Event
  mixins:
  - WithLocation
  slots:
  - started_at_time
  - ended_at_time
  - duration
  - is_current
  - diagnosis
  - procedure
  - in_location

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[duration](#duration)** | <sub>0..1</sub> | float |  |
| **[ended_at_time](#ended_at_time)** | <sub>0..1</sub> | date |  |
| **[is_current](#is_current)** | <sub>0..1</sub> | boolean |  |
| **[started_at_time](#started_at_time)** | <sub>0..1</sub> | date |  |
| **[in_location](#in_location)** | <sub>0..1</sub> | [Place](#place) |  |
| **[diagnosis](#diagnosis)** | <sub>0..1</sub> | [DiagnosisConcept](#diagnosisconcept) |  |
| **[procedure](#procedure)** | <sub>0..1</sub> | [ProcedureConcept](#procedureconcept) |  |

#### Parents

 * [Event](#event)

#### Uses

 *  mixin: [WithLocation](#withlocation)

#### Referenced by:

 *  **[Person](#person)** : has_medical_history  <sub>0..\*</sub> 




### NamedThing

A generic grouping for any identifiable entity


#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
NamedThing:
  description: A generic grouping for any identifiable entity
  slots:
  - id
  - name
  - description
  - depicted_by

```
</details>


#### Local class diagram

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[description](#description)** | <sub>0..1</sub> | string |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |

#### Children

 * [Concept](#concept)
 * [Organization](#organization) - An organization such as a company or university
 * [Person](#person) - A person (alive, dead, undead, or fictional).




### NewsEvent




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
NewsEvent:
  is_a: Event
  slots:
  - started_at_time
  - ended_at_time
  - duration
  - is_current
  - newsEvent__headline

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[duration](#duration)** | <sub>0..1</sub> | float |  |
| **[ended_at_time](#ended_at_time)** | <sub>0..1</sub> | date |  |
| **[is_current](#is_current)** | <sub>0..1</sub> | boolean |  |
| **[started_at_time](#started_at_time)** | <sub>0..1</sub> | date |  |
| **[headline](#headline)** | <sub>0..1</sub> | string |  |

#### Parents

 * [Event](#event)

#### Referenced by:

 *  **[HasNewsEvents](#hasnewsevents)** : hasNewsEvents__has_news_events  <sub>0..\*</sub> 




### OperationProcedureConcept




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
OperationProcedureConcept:
  is_a: ProcedureConcept
  slots:
  - id
  - name
  - description
  - depicted_by
  - concept__code_system
  - concept__mappings

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[description](#description)** | <sub>0..1</sub> | string |  |
| **[code system](#code system)** | <sub>0..1</sub> | [CodeSystem](#codesystem) |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |
| **[mappings](#mappings)** | <sub>0..\*</sub> | CrossReference |  |

#### Parents

 * [ProcedureConcept](#procedureconcept)




### Organization

An organization such as a company or university


#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
Organization:
  is_a: NamedThing
  mixins:
  - HasAliases
  - HasNewsEvents
  description: An organization such as a company or university
  slots:
  - id
  - name
  - description
  - depicted_by
  - mission_statement
  - founding_date
  - founding location
  - Organization_categories
  - score
  - min_salary
  - hasAliases__aliases
  - hasNewsEvents__has_news_events
  slot_usage:
    categories:
      range: OrganizationType

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[description](#description)** | <sub>0..1</sub> | string |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |
| **[aliases](#aliases)** | <sub>0..\*</sub> | string |  |
| **[has_news_events](#has_news_events)** | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |
| **[categories](#categories)** | <sub>0..\*</sub> | [OrganizationType](#organizationtype) |  |
| **[founding location](#founding location)** | <sub>0..1</sub> | [Place](#place) |  |
| **[founding_date](#founding_date)** | <sub>0..1</sub> | string |  |
| **[min_salary](#min_salary)** | <sub>0..1</sub> | SalaryType |  |
| **[mission_statement](#mission_statement)** | <sub>0..1</sub> | string |  |
| **[score](#score)** | <sub>0..1</sub> | decimal | A score between 0 and 5, represented as a decimal |

#### Parents

 * [NamedThing](#namedthing) - A generic grouping for any identifiable entity

#### Uses

 *  mixin: [HasAliases](#hasaliases) - A mixin applied to any class that can have aliases/alternateNames
 *  mixin: [HasNewsEvents](#hasnewsevents)

#### Referenced by:

 *  **[EmploymentEvent](#employmentevent)** : employed_at  <sub>0..1</sub> 
 *  **[Container](#container)** : organizations  <sub>0..\*</sub> 




### Person

A person (alive, dead, undead, or fictional).


#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
Person:
  is_a: NamedThing
  mixins:
  - HasAliases
  - HasNewsEvents
  description: A person (alive, dead, undead, or fictional).
  slots:
  - id
  - name
  - description
  - depicted_by
  - Person_primary_email
  - birth_date
  - Person_age_in_years
  - gender
  - current_address
  - Person_telephone
  - has_employment_history
  - has_familial_relationships
  - has_interpersonal_relationships
  - has_medical_history
  - hasAliases__aliases
  - hasNewsEvents__has_news_events

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[description](#description)** | <sub>0..1</sub> | string |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |
| **[aliases](#aliases)** | <sub>0..\*</sub> | string |  |
| **[has_news_events](#has_news_events)** | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |
| **[age_in_years](#age_in_years)** | <sub>0..1</sub> | integer |  |
| **[birth_date](#birth_date)** | <sub>0..1</sub> | string |  |
| **[current_address](#current_address)** | <sub>0..1</sub> | [Address](#address) | The address at which a person currently lives |
| **[gender](#gender)** | <sub>0..1</sub> | [GenderType](#gendertype) |  |
| **[has_employment_history](#has_employment_history)** | <sub>0..\*</sub> | [EmploymentEvent](#employmentevent) |  |
| **[has_familial_relationships](#has_familial_relationships)** | <sub>0..\*</sub> | [FamilialRelationship](#familialrelationship) |  |
| **[has_interpersonal_relationships](#has_interpersonal_relationships)** | <sub>0..\*</sub> | [InterPersonalRelationship](#interpersonalrelationship) |  |
| **[has_medical_history](#has_medical_history)** | <sub>0..\*</sub> | [MedicalEvent](#medicalevent) |  |
| **[primary_email](#primary_email)** | <sub>0..1</sub> | string |  |
| **[telephone](#telephone)** | <sub>0..1</sub> | string |  |

#### Parents

 * [NamedThing](#namedthing) - A generic grouping for any identifiable entity

#### Uses

 *  mixin: [HasAliases](#hasaliases) - A mixin applied to any class that can have aliases/alternateNames
 *  mixin: [HasNewsEvents](#hasnewsevents)

#### Referenced by:

 *  **[FamilialRelationship](#familialrelationship)** : related to  <sub>1..1</sub> 
 *  **[InterPersonalRelationship](#interpersonalrelationship)** : related to  <sub>1..1</sub> 
 *  **[Container](#container)** : persons  <sub>0..\*</sub> 
 *  **[Relationship](#relationship)** : related_to  <sub>0..1</sub> 




### Place




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
Place:
  mixins:
  - HasAliases
  slots:
  - id
  - name
  - depicted_by
  - hasAliases__aliases

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[aliases](#aliases)** | <sub>0..\*</sub> | string |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |

#### Uses

 *  mixin: [HasAliases](#hasaliases) - A mixin applied to any class that can have aliases/alternateNames

#### Referenced by:

 *  **[Organization](#organization)** : founding location  <sub>0..1</sub> 
 *  **[WithLocation](#withlocation)** : in_location  <sub>0..1</sub> 
 *  **[Container](#container)** : places  <sub>0..\*</sub> 




### ProcedureConcept




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
ProcedureConcept:
  is_a: Concept
  slots:
  - id
  - name
  - description
  - depicted_by
  - concept__code_system
  - concept__mappings

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |
| **[description](#description)** | <sub>0..1</sub> | string |  |
| **[code system](#code system)** | <sub>0..1</sub> | [CodeSystem](#codesystem) |  |
| **[depicted_by](#depicted_by)** | <sub>0..1</sub> | ImageURL |  |
| **[mappings](#mappings)** | <sub>0..\*</sub> | CrossReference |  |

#### Parents

 * [Concept](#concept)

#### Children

 * [ImagingProcedureConcept](#imagingprocedureconcept)
 * [OperationProcedureConcept](#operationprocedureconcept)

#### Referenced by:

 *  **[MedicalEvent](#medicalevent)** : procedure  <sub>0..1</sub> 




### Relationship




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
Relationship:
  slots:
  - started_at_time
  - ended_at_time
  - related_to
  - type

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[ended_at_time](#ended_at_time)** | <sub>0..1</sub> | date |  |
| **[related_to](#related_to)** | <sub>0..1</sub> | [Person](#person) |  |
| **[started_at_time](#started_at_time)** | <sub>0..1</sub> | date |  |
| **[type](#type)** | <sub>0..1</sub> | string |  |

#### Children

 * [FamilialRelationship](#familialrelationship)
 * [InterPersonalRelationship](#interpersonalrelationship)




### CodeSystem




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
code system:
  slots:
  - id
  - name

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[id](#id)** | <sub>1..1</sub> | uriorcurie |  |
| **[name](#name)** | <sub>1..1</sub> | string |  |

#### Referenced by:

 *  **[Concept](#concept)** : concept__code_system  <sub>0..1</sub> 




## Mixins


### HasAliases

A mixin applied to any class that can have aliases/alternateNames


#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
HasAliases:
  mixin: true
  description: A mixin applied to any class that can have aliases/alternateNames
  slots:
  - hasAliases__aliases
  attributes:
    aliases:
      multivalued: true

```
</details>


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[aliases](#aliases)** | <sub>0..\*</sub> | string |  |

#### Used as mixin by

 * [Organization](#organization) - An organization such as a company or university
 * [Person](#person) - A person (alive, dead, undead, or fictional).
 * [Place](#place)

### HasNewsEvents




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
HasNewsEvents:
  mixin: true
  slots:
  - hasNewsEvents__has_news_events
  attributes:
    has_news_events:
      range: NewsEvent
      multivalued: true

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[has_news_events](#has_news_events)** | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |

#### Used as mixin by

 * [Organization](#organization) - An organization such as a company or university
 * [Person](#person) - A person (alive, dead, undead, or fictional).

### WithLocation




#### YAML Definition

<details>
<summary>Click to expand</summary>

```yaml
WithLocation:
  mixin: true
  slots:
  - in_location

```
</details>

<svg>mock</svg>

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **[in_location](#in_location)** | <sub>0..1</sub> | [Place](#place) |  |

#### Used as mixin by

 * [MedicalEvent](#medicalevent)

## Slots

| Name | Cardinality/Range | Used By |
| --- | --- | --- |
| <a id="id"></a>**id** | <sub>1..1</sub><br/>uriorcurie | [Concept](#concept), [DiagnosisConcept](#diagnosisconcept), [ImagingProcedureConcept](#imagingprocedureconcept), [NamedThing](#namedthing), [OperationProcedureConcept](#operationprocedureconcept), [Organization](#organization), [Person](#person), [Place](#place), [ProcedureConcept](#procedureconcept), [CodeSystem](#codesystem) |
| <a id="name"></a>**name** | <sub>1..1</sub><br/>string | [Concept](#concept), [DiagnosisConcept](#diagnosisconcept), [ImagingProcedureConcept](#imagingprocedureconcept), [NamedThing](#namedthing), [OperationProcedureConcept](#operationprocedureconcept), [Organization](#organization), [Person](#person), [Place](#place), [ProcedureConcept](#procedureconcept), [CodeSystem](#codesystem) |
| <a id="description"></a>**description** | <sub>0..1</sub><br/>string | [Concept](#concept), [DiagnosisConcept](#diagnosisconcept), [ImagingProcedureConcept](#imagingprocedureconcept), [NamedThing](#namedthing), [OperationProcedureConcept](#operationprocedureconcept), [Organization](#organization), [Person](#person), [ProcedureConcept](#procedureconcept) |
| <a id="familialrelationship_related to"></a>**FamilialRelationship_related to** | <sub>1..1</sub><br/>[Person](#person) |  |
| <a id="familialrelationship_type"></a>**FamilialRelationship_type** | <sub>1..1</sub><br/>[FamilialRelationshipType](#familialrelationshiptype) |  |
| <a id="interpersonalrelationship_related to"></a>**InterPersonalRelationship_related to** | <sub>1..1</sub><br/>[Person](#person) |  |
| <a id="interpersonalrelationship_type"></a>**InterPersonalRelationship_type** | <sub>1..1</sub><br/>string |  |
| <a id="organization_categories"></a>**Organization_categories** | <sub>0..\*</sub><br/>[OrganizationType](#organizationtype) |  |
| <a id="person_age_in_years"></a>**Person_age_in_years** | <sub>0..1</sub><br/>integer |  |
| <a id="person_primary_email"></a>**Person_primary_email** | <sub>0..1</sub><br/>string |  |
| <a id="person_telephone"></a>**Person_telephone** | <sub>0..1</sub><br/>string |  |
| <a id="age_in_years"></a>**age_in_years** | <sub>0..1</sub><br/>integer | [Person](#person) |
| <a id="birth_date"></a>**birth_date** | <sub>0..1</sub><br/>string | [Person](#person) |
| <a id="categories"></a>**categories** | <sub>0..\*</sub><br/>string | [Organization](#organization) |
| <a id="city"></a>**city** | <sub>0..1</sub><br/>string | [Address](#address) |
| <a id="concept__code_system"></a>**concept__code_system** | <sub>0..1</sub><br/>[CodeSystem](#codesystem) |  |
| <a id="concept__mappings"></a>**concept__mappings** | <sub>0..\*</sub><br/>CrossReference |  |
| <a id="current_address"></a>**current_address**<br/>The address at which a person currently lives | <sub>0..1</sub><br/>[Address](#address) | [Person](#person) |
| <a id="depicted_by"></a>**depicted_by** | <sub>0..1</sub><br/>ImageURL | [Concept](#concept), [DiagnosisConcept](#diagnosisconcept), [ImagingProcedureConcept](#imagingprocedureconcept), [NamedThing](#namedthing), [OperationProcedureConcept](#operationprocedureconcept), [Organization](#organization), [Person](#person), [Place](#place), [ProcedureConcept](#procedureconcept) |
| <a id="diagnosis"></a>**diagnosis** | <sub>0..1</sub><br/>[DiagnosisConcept](#diagnosisconcept) | [MedicalEvent](#medicalevent) |
| <a id="duration"></a>**duration** | <sub>0..1</sub><br/>float | [EmploymentEvent](#employmentevent), [Event](#event), [MedicalEvent](#medicalevent), [NewsEvent](#newsevent) |
| <a id="employed_at"></a>**employed_at** | <sub>0..1</sub><br/>[Organization](#organization) | [EmploymentEvent](#employmentevent) |
| <a id="ended_at_time"></a>**ended_at_time** | <sub>0..1</sub><br/>date | [EmploymentEvent](#employmentevent), [Event](#event), [FamilialRelationship](#familialrelationship), [InterPersonalRelationship](#interpersonalrelationship), [MedicalEvent](#medicalevent), [NewsEvent](#newsevent), [Relationship](#relationship) |
| <a id="founding location"></a>**founding location** | <sub>0..1</sub><br/>[Place](#place) | [Organization](#organization) |
| <a id="founding_date"></a>**founding_date** | <sub>0..1</sub><br/>string | [Organization](#organization) |
| <a id="gender"></a>**gender** | <sub>0..1</sub><br/>[GenderType](#gendertype) | [Person](#person) |
| <a id="hasaliases__aliases"></a>**hasAliases__aliases** | <sub>0..\*</sub><br/>string |  |
| <a id="hasnewsevents__has_news_events"></a>**hasNewsEvents__has_news_events** | <sub>0..\*</sub><br/>[NewsEvent](#newsevent) |  |
| <a id="has_employment_history"></a>**has_employment_history** | <sub>0..\*</sub><br/>[EmploymentEvent](#employmentevent) | [Person](#person) |
| <a id="has_familial_relationships"></a>**has_familial_relationships** | <sub>0..\*</sub><br/>[FamilialRelationship](#familialrelationship) | [Person](#person) |
| <a id="has_interpersonal_relationships"></a>**has_interpersonal_relationships** | <sub>0..\*</sub><br/>[InterPersonalRelationship](#interpersonalrelationship) | [Person](#person) |
| <a id="has_medical_history"></a>**has_medical_history** | <sub>0..\*</sub><br/>[MedicalEvent](#medicalevent) | [Person](#person) |
| <a id="image"></a>**image** | <sub>0..1</sub><br/>string |  |
| <a id="in_location"></a>**in_location** | <sub>0..1</sub><br/>[Place](#place) | [MedicalEvent](#medicalevent), [WithLocation](#withlocation) |
| <a id="int_id"></a>**int_id** | <sub>1..1</sub><br/>integer | [IntegerPrimaryKeyObject](#integerprimarykeyobject) |
| <a id="is_current"></a>**is_current** | <sub>0..1</sub><br/>boolean | [EmploymentEvent](#employmentevent), [Event](#event), [MedicalEvent](#medicalevent), [NewsEvent](#newsevent) |
| <a id="min_salary"></a>**min_salary** | <sub>0..1</sub><br/>SalaryType | [Organization](#organization) |
| <a id="mission_statement"></a>**mission_statement** | <sub>0..1</sub><br/>string | [Organization](#organization) |
| <a id="newsevent__headline"></a>**newsEvent__headline** | <sub>0..1</sub><br/>string |  |
| <a id="organizations"></a>**organizations** | <sub>0..\*</sub><br/>[Organization](#organization) | [Container](#container) |
| <a id="persons"></a>**persons** | <sub>0..\*</sub><br/>[Person](#person) | [Container](#container) |
| <a id="places"></a>**places** | <sub>0..\*</sub><br/>[Place](#place) | [Container](#container) |
| <a id="postal_code"></a>**postal_code** | <sub>0..1</sub><br/>string | [Address](#address) |
| <a id="primary_email"></a>**primary_email** | <sub>0..1</sub><br/>string | [Person](#person) |
| <a id="procedure"></a>**procedure** | <sub>0..1</sub><br/>[ProcedureConcept](#procedureconcept) | [MedicalEvent](#medicalevent) |
| <a id="related to"></a>**related to** | <sub>1..1</sub><br/>[Person](#person) |  |
| <a id="related_to"></a>**related_to** | <sub>0..1</sub><br/>[Person](#person) | [FamilialRelationship](#familialrelationship), [InterPersonalRelationship](#interpersonalrelationship), [Relationship](#relationship) |
| <a id="salary"></a>**salary** | <sub>0..1</sub><br/>SalaryType | [EmploymentEvent](#employmentevent) |
| <a id="score"></a>**score**<br/>A score between 0 and 5, represented as a decimal | <sub>0..1</sub><br/>decimal | [Organization](#organization) |
| <a id="started_at_time"></a>**started_at_time** | <sub>0..1</sub><br/>date | [EmploymentEvent](#employmentevent), [Event](#event), [FamilialRelationship](#familialrelationship), [InterPersonalRelationship](#interpersonalrelationship), [MedicalEvent](#medicalevent), [NewsEvent](#newsevent), [Relationship](#relationship) |
| <a id="street"></a>**street** | <sub>0..1</sub><br/>string | [Address](#address) |
| <a id="telephone"></a>**telephone** | <sub>0..1</sub><br/>string | [Person](#person) |
| <a id="type"></a>**type** | <sub>0..1</sub><br/>string | [FamilialRelationship](#familialrelationship), [InterPersonalRelationship](#interpersonalrelationship), [Relationship](#relationship) |

## Enums


### DiagnosisType



| Text | Meaning: | Description |
| --- | --- | --- |
| todo | None |  |

### FamilialRelationshipType



| Text | Meaning: | Description |
| --- | --- | --- |
| CHILD_OF | famrel:03 |  |
| PARENT_OF | famrel:02 |  |
| SIBLING_OF | famrel:01 |  |

#### Used by

 *  **[FamilialRelationship](#familialrelationship)** *[FamilialRelationship_type](#familialrelationship_type)*  <sub>1..1</sub> 

### GenderType



| Text | Meaning: | Description |
| --- | --- | --- |
| cisgender man | GSSO:000371 |  |
| cisgender woman | GSSO:000385 |  |
| nonbinary man | GSSO:009254 |  |
| nonbinary woman | GSSO:009253 |  |
| transgender man | GSSO:000372 |  |
| transgender woman | GSSO:000384 |  |

#### Used by

 *  **[Person](#person)** *[gender](#gender)*  <sub>0..1</sub> 

### NonFamilialRelationshipType



| Text | Meaning: | Description |
| --- | --- | --- |
| BEST_FRIEND_OF | None |  |
| COWORKER_OF | famrel:70 |  |
| MORTAL_ENEMY_OF | None |  |
| ROOMMATE_OF | famrel:71 |  |

### OrganizationType



| Text | Meaning: | Description |
| --- | --- | --- |
| charity | bizcodes:001 |  |
| for profit | None |  |
| loose organization | None |  |
| non profit | None |  |
| offshore | None |  |
| shell company | None |  |

#### Used by

 *  **[Organization](#organization)** *[Organization_categories](#organization_categories)*  <sub>0..\*</sub>
