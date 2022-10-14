# Class: BirthEvent




URI: [ks:BirthEvent](https://w3id.org/linkml/tests/kitchen_sink/BirthEvent)


```mermaid
 classDiagram
    class BirthEvent
      Event <|-- BirthEvent
      
      BirthEvent : endedAtTime
      BirthEvent : in_location
      BirthEvent : is_current
      BirthEvent : metadata
      BirthEvent : startedAtTime
      
```




## Inheritance
* [Event](Event.md)
    * **BirthEvent**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [in location](in_location.md) | 0..1 <br/> [Place](Place.md) | None  | direct |
| [started at time](startedAtTime.md) | 0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) | None  | inherited |
| [ended at time](endedAtTime.md) | 0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) | None  | inherited |
| [is current](is_current.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | None  | inherited |
| [metadata](metadata.md) | 0..1 <br/> [AnyObject](AnyObject.md) | Example of a slot that has an unconstrained range  | inherited |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Person](Person.md) | [has birth event](has_birth_event.md) | range | BirthEvent |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:BirthEvent']|join(', ') |
| native | ['ks:BirthEvent']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: BirthEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: Event
slots:
- in location

```
</details>

### Induced

<details>
```yaml
name: BirthEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: Event
attributes:
  in location:
    name: in location
    annotations:
      biolink:opposite:
        tag: biolink:opposite
        value: location_of
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: in_location
    owner: BirthEvent
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
    owner: BirthEvent
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
    owner: BirthEvent
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
    owner: BirthEvent
    domain_of:
    - Event
    range: boolean
  metadata:
    name: metadata
    description: Example of a slot that has an unconstrained range
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: metadata
    owner: BirthEvent
    domain_of:
    - Event
    range: AnyObject

```
</details>