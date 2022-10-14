# Class: MarriageEvent




URI: [ks:MarriageEvent](https://w3id.org/linkml/tests/kitchen_sink/MarriageEvent)


```mermaid
 classDiagram
    class MarriageEvent
      WithLocation <|-- MarriageEvent
      Event <|-- MarriageEvent
      
      MarriageEvent : endedAtTime
      MarriageEvent : in_location
      MarriageEvent : is_current
      MarriageEvent : married_to
      MarriageEvent : metadata
      MarriageEvent : startedAtTime
      
```




## Inheritance
* [Event](Event.md)
    * **MarriageEvent** [ [WithLocation](WithLocation.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [married to](married_to.md) | 0..1 <br/> [Person](Person.md) | None  | direct |
| [in location](in_location.md) | 0..1 <br/> [Place](Place.md) | None  | inherited |
| [started at time](startedAtTime.md) | 0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) | None  | inherited |
| [ended at time](endedAtTime.md) | 0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) | None  | inherited |
| [is current](is_current.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | None  | inherited |
| [metadata](metadata.md) | 0..1 <br/> [AnyObject](AnyObject.md) | Example of a slot that has an unconstrained range  | inherited |




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:MarriageEvent']|join(', ') |
| native | ['ks:MarriageEvent']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MarriageEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: Event
mixins:
- WithLocation
slots:
- married to

```
</details>

### Induced

<details>
```yaml
name: MarriageEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: Event
mixins:
- WithLocation
attributes:
  married to:
    name: married to
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: married_to
    owner: MarriageEvent
    domain_of:
    - MarriageEvent
    range: Person
  in location:
    name: in location
    annotations:
      biolink:opposite:
        tag: biolink:opposite
        value: location_of
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: in_location
    owner: MarriageEvent
    domain_of:
    - BirthEvent
    - MedicalEvent
    - WithLocation
    range: Place
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1000
    slot_uri: prov:startedAtTime
    alias: started_at_time
    owner: MarriageEvent
    domain_of:
    - Event
    - Relationship
    - activity
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1000
    slot_uri: prov:endedAtTime
    alias: ended_at_time
    owner: MarriageEvent
    domain_of:
    - Event
    - Relationship
    - activity
    range: date
  is current:
    name: is current
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: is_current
    owner: MarriageEvent
    domain_of:
    - Event
    range: boolean
  metadata:
    name: metadata
    description: Example of a slot that has an unconstrained range
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: metadata
    owner: MarriageEvent
    domain_of:
    - Event
    range: AnyObject

```
</details>