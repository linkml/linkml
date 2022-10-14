# Class: EmploymentEvent




URI: [ks:EmploymentEvent](https://w3id.org/linkml/tests/kitchen_sink/EmploymentEvent)


```mermaid
 classDiagram
    class EmploymentEvent
      Event <|-- EmploymentEvent
      
      EmploymentEvent : employed_at
      EmploymentEvent : endedAtTime
      EmploymentEvent : is_current
      EmploymentEvent : metadata
      EmploymentEvent : startedAtTime
      EmploymentEvent : type
      
```




## Inheritance
* [Event](Event.md)
    * **EmploymentEvent**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [employed at](employed_at.md) | 0..1 <br/> [Company](Company.md) | None  | direct |
| [type](type.md) | 0..1 <br/> [EmploymentEventType](EmploymentEventType.md) | None  | direct |
| [started at time](startedAtTime.md) | 0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) | None  | inherited |
| [ended at time](endedAtTime.md) | 0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) | None  | inherited |
| [is current](is_current.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | None  | inherited |
| [metadata](metadata.md) | 0..1 <br/> [AnyObject](AnyObject.md) | Example of a slot that has an unconstrained range  | inherited |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Person](Person.md) | [has employment history](has_employment_history.md) | range | EmploymentEvent |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:EmploymentEvent']|join(', ') |
| native | ['ks:EmploymentEvent']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: EmploymentEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 6
is_a: Event
slots:
- employed at
- type
slot_usage:
  type:
    name: type
    domain_of:
    - Relationship
    - EmploymentEvent
    - Relationship
    - EmploymentEvent
    range: EmploymentEventType
    required: false

```
</details>

### Induced

<details>
```yaml
name: EmploymentEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 6
is_a: Event
slot_usage:
  type:
    name: type
    domain_of:
    - Relationship
    - EmploymentEvent
    - Relationship
    - EmploymentEvent
    range: EmploymentEventType
    required: false
attributes:
  employed at:
    name: employed at
    in_subset:
    - subset A
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: employed_at
    owner: EmploymentEvent
    domain_of:
    - EmploymentEvent
    range: Company
  type:
    name: type
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: type
    owner: EmploymentEvent
    domain_of:
    - Relationship
    - EmploymentEvent
    - Relationship
    - EmploymentEvent
    range: EmploymentEventType
    required: false
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1000
    slot_uri: prov:startedAtTime
    alias: started_at_time
    owner: EmploymentEvent
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
    owner: EmploymentEvent
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
    owner: EmploymentEvent
    domain_of:
    - Event
    range: boolean
  metadata:
    name: metadata
    description: Example of a slot that has an unconstrained range
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: metadata
    owner: EmploymentEvent
    domain_of:
    - Event
    range: AnyObject

```
</details>