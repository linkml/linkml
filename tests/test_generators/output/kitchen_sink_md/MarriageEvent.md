# Class: MarriageEvent




URI: [ks:MarriageEvent](https://w3id.org/linkml/tests/kitchen_sink/MarriageEvent)




```mermaid
 classDiagram
      WithLocation <|-- MarriageEvent
      Event <|-- MarriageEvent
      
      MarriageEvent : ended_at_time
      MarriageEvent : in_location
      MarriageEvent : is_current
      MarriageEvent : married_to
      MarriageEvent : metadata
      MarriageEvent : started_at_time
      

```





## Inheritance
* [Event](Event.md)
    * **MarriageEvent** [ WithLocation]



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [married_to](married_to.md) | [Person](Person.md) | 0..1 | None  | . |
| [in_location](in_location.md) | [Place](Place.md) | 0..1 | None  | . |
| [started_at_time](started_at_time.md) | [xsd:date](http://www.w3.org/2001/XMLSchema#date) | 0..1 | None  | . |
| [ended_at_time](ended_at_time.md) | [xsd:date](http://www.w3.org/2001/XMLSchema#date) | 0..1 | None  | . |
| [is_current](is_current.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [metadata](metadata.md) | [AnyObject](AnyObject.md) | 0..1 | Example of a slot that has an unconstrained range  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:MarriageEvent'] |
| native | ['ks:MarriageEvent'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MarriageEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
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
is_a: Event
mixins:
- WithLocation
attributes:
  married to:
    name: married to
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: married_to
    owner: MarriageEvent
    range: Person
  in location:
    name: in location
    annotations:
      biolink:opposite:
        tag: biolink:opposite
        value: location_of
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: in_location
    owner: MarriageEvent
    range: Place
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:startedAtTime
    alias: started_at_time
    owner: MarriageEvent
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:endedAtTime
    alias: ended_at_time
    owner: MarriageEvent
    range: date
  is current:
    name: is current
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: is_current
    owner: MarriageEvent
    range: boolean
  metadata:
    name: metadata
    description: Example of a slot that has an unconstrained range
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: metadata
    owner: MarriageEvent
    range: AnyObject

```
</details>