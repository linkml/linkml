
# PERSONINFO


**metamodel version:** 1.7.0

**version:** 0.0.1


Information about people, based on [schema.org](http://schema.org)


## Class Diagram

```mermaid
classDiagram
Concept <|-- DiagnosisConcept
Concept <|-- ProcedureConcept
Event <|-- EmploymentEvent
Event <|-- MedicalEvent
Event <|-- NewsEvent
NamedThing <|-- Concept
NamedThing <|-- Organization
NamedThing <|-- Person
Relationship <|-- FamilialRelationship

```

## ERD Diagram

```mermaid
erDiagram
Address {
    string street  
    string city  
    string postal_code  
}
Container {
    string name  
}
DiagnosisConcept {
    string id  
    string name  
    string description  
    uri image  
}
EmploymentEvent {
    date started_at_time  
    date ended_at_time  
    float duration  
    boolean is_current  
}
FamilialRelationship {
    date started_at_time  
    date ended_at_time  
    FamilialRelationshipType type  
}
MedicalEvent {
    date started_at_time  
    date ended_at_time  
    float duration  
    boolean is_current  
}
NewsEvent {
    string headline  
    date started_at_time  
    date ended_at_time  
    float duration  
    boolean is_current  
}
Organization {
    string mission_statement  
    string founding_date  
    stringList aliases  
    string id  
    string name  
    string description  
    uri image  
}
Person {
    string primary_email  
    string birth_date  
    integer age_in_years  
    GenderType gender  
    stringList aliases  
    string id  
    string name  
    string description  
    uri image  
}
Place {
    string id  
    string name  
    stringList aliases  
}
ProcedureConcept {
    string id  
    string name  
    string description  
    uri image  
}

Container ||--}o Organization : "organizations"
Container ||--}o Person : "persons"
EmploymentEvent ||--|o Organization : "employed_at"
FamilialRelationship ||--|| Person : "related_to"
MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
MedicalEvent ||--|o Place : "in_location"
MedicalEvent ||--|o ProcedureConcept : "procedure"
Organization ||--|o Address : "current_address"
Organization ||--|o Place : "founding_location"
Organization ||--}o NewsEvent : "has_news_events"
Person ||--|o Address : "current_address"
Person ||--}o EmploymentEvent : "has_employment_history"
Person ||--}o FamilialRelationship : "has_familial_relationships"
Person ||--}o MedicalEvent : "has_medical_history"
Person ||--}o NewsEvent : "has_news_events"

```


## Classes


### Address



```mermaid
erDiagram
Address {

}
Organization {

}
Person {

}

Organization ||--|o Address : "current_address"
Organization ||--|o Place : "founding_location"
Organization ||--}o NewsEvent : "has_news_events"
Person ||--|o Address : "current_address"
Person ||--}o EmploymentEvent : "has_employment_history"
Person ||--}o FamilialRelationship : "has_familial_relationships"
Person ||--}o MedicalEvent : "has_medical_history"
Person ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **city** | <sub>0..1</sub> | string |  |
| **postal_code** | <sub>0..1</sub> | string |  |
| **street** | <sub>0..1</sub> | string |  |

#### Referenced by:

 *  **[Organization](#organization)** : *[current_address](#current_address)*  <sub>0..1</sub> 
 *  **[Person](#person)** : *[current_address](#current_address)*  <sub>0..1</sub> 




### Concept




#### Local class diagram

```mermaid
classDiagram
Concept <|-- DiagnosisConcept
Concept <|-- ProcedureConcept
NamedThing <|-- Concept

```

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| id | <sub>1..1</sub> | string | ID string to uniquely identify the object |
| name | <sub>0..1</sub> | string | Short human readable object name |
| description | <sub>0..1</sub> | string | Detailed free form description of the object |
| image | <sub>0..1</sub> | uri | image that visually represents the object |

#### Parents

 * [NamedThing](#namedthing) - A generic grouping for any identifiable entity

#### Children

 * [DiagnosisConcept](#diagnosisconcept)
 * [ProcedureConcept](#procedureconcept)




### Container



```mermaid
erDiagram
Container {

}
Organization {

}
Person {

}

Container ||--}o Organization : "organizations"
Container ||--}o Person : "persons"
Organization ||--|o Address : "current_address"
Organization ||--|o Place : "founding_location"
Organization ||--}o NewsEvent : "has_news_events"
Person ||--|o Address : "current_address"
Person ||--}o EmploymentEvent : "has_employment_history"
Person ||--}o FamilialRelationship : "has_familial_relationships"
Person ||--}o MedicalEvent : "has_medical_history"
Person ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **name** | <sub>0..1</sub> | string | Short human readable object name |
| **organizations** | <sub>0..\*</sub> | [Organization](#organization) |  |
| **persons** | <sub>0..\*</sub> | [Person](#person) |  |




### DiagnosisConcept



```mermaid
erDiagram
DiagnosisConcept {

}
MedicalEvent {

}

MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
MedicalEvent ||--|o Place : "in_location"
MedicalEvent ||--|o ProcedureConcept : "procedure"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| id | <sub>1..1</sub> | string | ID string to uniquely identify the object |
| name | <sub>0..1</sub> | string | Short human readable object name |
| description | <sub>0..1</sub> | string | Detailed free form description of the object |
| image | <sub>0..1</sub> | uri | image that visually represents the object |

#### Parents

 * [Concept](#concept)

#### Referenced by:

 *  **[MedicalEvent](#medicalevent)** : *[diagnosis](#diagnosis)*  <sub>0..1</sub> 




### EmploymentEvent



```mermaid
erDiagram
EmploymentEvent {

}
Organization {

}
Person {

}

EmploymentEvent ||--|o Organization : "employed_at"
Organization ||--|o Address : "current_address"
Organization ||--|o Place : "founding_location"
Organization ||--}o NewsEvent : "has_news_events"
Person ||--|o Address : "current_address"
Person ||--}o EmploymentEvent : "has_employment_history"
Person ||--}o FamilialRelationship : "has_familial_relationships"
Person ||--}o MedicalEvent : "has_medical_history"
Person ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| duration | <sub>0..1</sub> | float |  |
| ended_at_time | <sub>0..1</sub> | date |  |
| is_current | <sub>0..1</sub> | boolean |  |
| started_at_time | <sub>0..1</sub> | date |  |
| **employed_at** | <sub>0..1</sub> | [Organization](#organization) |  |

#### Parents

 * [Event](#event)

#### Referenced by:

 *  **[Person](#person)** : *[has_employment_history](#has_employment_history)*  <sub>0..\*</sub> 




### Event




#### Local class diagram

```mermaid
classDiagram
Event <|-- EmploymentEvent
Event <|-- MedicalEvent
Event <|-- NewsEvent

```

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **duration** | <sub>0..1</sub> | float |  |
| **ended_at_time** | <sub>0..1</sub> | date |  |
| **is_current** | <sub>0..1</sub> | boolean |  |
| **started_at_time** | <sub>0..1</sub> | date |  |

#### Children

 * [EmploymentEvent](#employmentevent)
 * [MedicalEvent](#medicalevent)
 * [NewsEvent](#newsevent)




### FamilialRelationship



```mermaid
erDiagram
FamilialRelationship {

}
Person {

}

FamilialRelationship ||--|| Person : "related_to"
Person ||--|o Address : "current_address"
Person ||--}o EmploymentEvent : "has_employment_history"
Person ||--}o FamilialRelationship : "has_familial_relationships"
Person ||--}o MedicalEvent : "has_medical_history"
Person ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| ended_at_time | <sub>0..1</sub> | date |  |
| related_to | <sub>0..1</sub> | string |  |
| started_at_time | <sub>0..1</sub> | date |  |
| type | <sub>0..1</sub> | string |  |
| **FamilialRelationship_related_to** | <sub>1..1</sub> | [Person](#person) |  |
| **FamilialRelationship_type** | <sub>1..1</sub> | [FamilialRelationshipType](#familialrelationshiptype) |  |

#### Parents

 * [Relationship](#relationship)

#### Referenced by:

 *  **[Person](#person)** : *[has_familial_relationships](#has_familial_relationships)*  <sub>0..\*</sub> 




### IntegerPrimaryKeyObject




#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **int_id** | <sub>1..1</sub> | integer |  |




### MedicalEvent



```mermaid
erDiagram
DiagnosisConcept {

}
MedicalEvent {

}
Person {

}
Place {

}
ProcedureConcept {

}

MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
MedicalEvent ||--|o Place : "in_location"
MedicalEvent ||--|o ProcedureConcept : "procedure"
Person ||--|o Address : "current_address"
Person ||--}o EmploymentEvent : "has_employment_history"
Person ||--}o FamilialRelationship : "has_familial_relationships"
Person ||--}o MedicalEvent : "has_medical_history"
Person ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| duration | <sub>0..1</sub> | float |  |
| ended_at_time | <sub>0..1</sub> | date |  |
| is_current | <sub>0..1</sub> | boolean |  |
| started_at_time | <sub>0..1</sub> | date |  |
| **diagnosis** | <sub>0..1</sub> | [DiagnosisConcept](#diagnosisconcept) |  |
| **in_location** | <sub>0..1</sub> | [Place](#place) |  |
| **procedure** | <sub>0..1</sub> | [ProcedureConcept](#procedureconcept) |  |

#### Parents

 * [Event](#event)

#### Referenced by:

 *  **[Person](#person)** : *[has_medical_history](#has_medical_history)*  <sub>0..\*</sub> 




### NamedThing

A generic grouping for any identifiable entity


#### Local class diagram

```mermaid
classDiagram
NamedThing <|-- Concept
NamedThing <|-- Organization
NamedThing <|-- Person

```

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **id** | <sub>1..1</sub> | string | ID string to uniquely identify the object |
| **name** | <sub>0..1</sub> | string | Short human readable object name |
| **description** | <sub>0..1</sub> | string | Detailed free form description of the object |
| **image** | <sub>0..1</sub> | uri | image that visually represents the object |

#### Children

 * [Concept](#concept)
 * [Organization](#organization) - An organization such as a company or university
 * [Person](#person) - A person (alive, dead, undead, or fictional).




### NewsEvent



```mermaid
erDiagram
HasNewsEvents {

}
NewsEvent {

}

HasNewsEvents ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| duration | <sub>0..1</sub> | float |  |
| ended_at_time | <sub>0..1</sub> | date |  |
| is_current | <sub>0..1</sub> | boolean |  |
| started_at_time | <sub>0..1</sub> | date |  |
| **headline** | <sub>0..1</sub> | None |  |
| **newsEvent__headline** | <sub>0..1</sub> | string |  |

#### Parents

 * [Event](#event)

#### Referenced by:

 *  **[HasNewsEvents](#hasnewsevents)** : *[hasNewsEvents__has_news_events](#hasNewsEvents__has_news_events)*  <sub>0..\*</sub> 




### Organization

An organization such as a company or university

```mermaid
erDiagram
Address {

}
Container {

}
EmploymentEvent {

}
NewsEvent {

}
Organization {

}
Place {

}

Container ||--}o Organization : "organizations"
Container ||--}o Person : "persons"
EmploymentEvent ||--|o Organization : "employed_at"
Organization ||--|o Address : "current_address"
Organization ||--|o Place : "founding_location"
Organization ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| id | <sub>1..1</sub> | string | ID string to uniquely identify the object |
| name | <sub>0..1</sub> | string | Short human readable object name |
| description | <sub>0..1</sub> | string | Detailed free form description of the object |
| image | <sub>0..1</sub> | uri | image that visually represents the object |
| *aliases* | <sub>0..\*</sub> | None |  |
| *hasAliases__aliases* | <sub>0..\*</sub> | string |  |
| *hasNewsEvents__has_news_events* | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |
| *has_news_events* | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |
| **current_address** | <sub>0..1</sub> | [Address](#address) | The address at which a person currently lives |
| **founding_date** | <sub>0..1</sub> | string |  |
| **founding_location** | <sub>0..1</sub> | [Place](#place) |  |
| **mission_statement** | <sub>0..1</sub> | string |  |

#### Parents

 * [NamedThing](#namedthing) - A generic grouping for any identifiable entity

#### Uses

 *  mixin: [HasAliases](#hasaliases) - A mixin applied to any class that can have aliases/alternateNames
 *  mixin: [HasNewsEvents](#hasnewsevents)

#### Referenced by:

 *  **[EmploymentEvent](#employmentevent)** : *[employed_at](#employed_at)*  <sub>0..1</sub> 
 *  **[Container](#container)** : *[organizations](#organizations)*  <sub>0..\*</sub> 




### Person

A person (alive, dead, undead, or fictional).

```mermaid
erDiagram
Address {

}
Container {

}
EmploymentEvent {

}
FamilialRelationship {

}
MedicalEvent {

}
NewsEvent {

}
Person {

}

Container ||--}o Organization : "organizations"
Container ||--}o Person : "persons"
EmploymentEvent ||--|o Organization : "employed_at"
FamilialRelationship ||--|| Person : "related_to"
MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
MedicalEvent ||--|o Place : "in_location"
MedicalEvent ||--|o ProcedureConcept : "procedure"
Person ||--|o Address : "current_address"
Person ||--}o EmploymentEvent : "has_employment_history"
Person ||--}o FamilialRelationship : "has_familial_relationships"
Person ||--}o MedicalEvent : "has_medical_history"
Person ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| id | <sub>1..1</sub> | string | ID string to uniquely identify the object |
| name | <sub>0..1</sub> | string | Short human readable object name |
| description | <sub>0..1</sub> | string | Detailed free form description of the object |
| image | <sub>0..1</sub> | uri | image that visually represents the object |
| *aliases* | <sub>0..\*</sub> | None |  |
| *hasAliases__aliases* | <sub>0..\*</sub> | string |  |
| *hasNewsEvents__has_news_events* | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |
| *has_news_events* | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |
| **Person_primary_email** | <sub>0..1</sub> | string |  |
| **age_in_years** | <sub>0..1</sub> | integer |  |
| **birth_date** | <sub>0..1</sub> | string |  |
| **current_address** | <sub>0..1</sub> | [Address](#address) | The address at which a person currently lives |
| **gender** | <sub>0..1</sub> | [GenderType](#gendertype) |  |
| **has_employment_history** | <sub>0..\*</sub> | [EmploymentEvent](#employmentevent) |  |
| **has_familial_relationships** | <sub>0..\*</sub> | [FamilialRelationship](#familialrelationship) |  |
| **has_medical_history** | <sub>0..\*</sub> | [MedicalEvent](#medicalevent) |  |

#### Parents

 * [NamedThing](#namedthing) - A generic grouping for any identifiable entity

#### Uses

 *  mixin: [HasAliases](#hasaliases) - A mixin applied to any class that can have aliases/alternateNames
 *  mixin: [HasNewsEvents](#hasnewsevents)

#### Referenced by:

 *  **[FamilialRelationship](#familialrelationship)** : *[FamilialRelationship_related_to](#FamilialRelationship_related_to)*  <sub>1..1</sub> 
 *  **[Container](#container)** : *[persons](#persons)*  <sub>0..\*</sub> 




### Place



```mermaid
erDiagram
MedicalEvent {

}
Organization {

}
Place {

}
WithLocation {

}

MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
MedicalEvent ||--|o Place : "in_location"
MedicalEvent ||--|o ProcedureConcept : "procedure"
Organization ||--|o Address : "current_address"
Organization ||--|o Place : "founding_location"
Organization ||--}o NewsEvent : "has_news_events"
WithLocation ||--|o Place : "in_location"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| *aliases* | <sub>0..\*</sub> | None |  |
| *hasAliases__aliases* | <sub>0..\*</sub> | string |  |
| **id** | <sub>1..1</sub> | string | ID string to uniquely identify the object |
| **name** | <sub>0..1</sub> | string | Short human readable object name |

#### Uses

 *  mixin: [HasAliases](#hasaliases) - A mixin applied to any class that can have aliases/alternateNames

#### Referenced by:

 *  **[Organization](#organization)** : *[founding_location](#founding_location)*  <sub>0..1</sub> 
 *  **[MedicalEvent](#medicalevent)** : *[in_location](#in_location)*  <sub>0..1</sub> 
 *  **[WithLocation](#withlocation)** : *[in_location](#in_location)*  <sub>0..1</sub> 




### ProcedureConcept



```mermaid
erDiagram
MedicalEvent {

}
ProcedureConcept {

}

MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
MedicalEvent ||--|o Place : "in_location"
MedicalEvent ||--|o ProcedureConcept : "procedure"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| id | <sub>1..1</sub> | string | ID string to uniquely identify the object |
| name | <sub>0..1</sub> | string | Short human readable object name |
| description | <sub>0..1</sub> | string | Detailed free form description of the object |
| image | <sub>0..1</sub> | uri | image that visually represents the object |

#### Parents

 * [Concept](#concept)

#### Referenced by:

 *  **[MedicalEvent](#medicalevent)** : *[procedure](#procedure)*  <sub>0..1</sub> 




### Relationship




#### Local class diagram

```mermaid
classDiagram
Relationship <|-- FamilialRelationship

```

#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **ended_at_time** | <sub>0..1</sub> | date |  |
| **related_to** | <sub>0..1</sub> | string |  |
| **started_at_time** | <sub>0..1</sub> | date |  |
| **type** | <sub>0..1</sub> | string |  |

#### Children

 * [FamilialRelationship](#familialrelationship)




## Mixins


### HasAliases

A mixin applied to any class that can have aliases/alternateNames


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **aliases** | <sub>0..\*</sub> | None |  |
| **hasAliases__aliases** | <sub>0..\*</sub> | string |  |

#### Used as mixin by

 * [Organization](#organization) - An organization such as a company or university
 * [Person](#person) - A person (alive, dead, undead, or fictional).
 * [Place](#place)

### HasNewsEvents



```mermaid
erDiagram
HasNewsEvents {

}
NewsEvent {

}

HasNewsEvents ||--}o NewsEvent : "has_news_events"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **hasNewsEvents__has_news_events** | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |
| **has_news_events** | <sub>0..\*</sub> | [NewsEvent](#newsevent) |  |

#### Used as mixin by

 * [Organization](#organization) - An organization such as a company or university
 * [Person](#person) - A person (alive, dead, undead, or fictional).

### WithLocation



```mermaid
erDiagram
Place {

}
WithLocation {

}

WithLocation ||--|o Place : "in_location"

```


#### Attributes

| Name | Cardinality: | Type | Description |
| --- | --- | --- | --- |
| **in_location** | <sub>0..1</sub> | [Place](#place) |  |

## Enums


### DiagnosisType




### FamilialRelationshipType



| Text | Meaning: | Description |
| --- | --- | --- |
| CHILD_OF | famrel:01 |  |
| PARENT_OF | famrel:02 |  |
| SIBLING_OF | famrel:01 |  |

#### Used by

 *  **[FamilialRelationship](#familialrelationship)** *[FamilialRelationship_type](#FamilialRelationship_type)*  <sub>1..1</sub> 

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
