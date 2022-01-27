# EmploymentEvent

None

URI: [ks:EmploymentEvent](https://w3id.org/linkml/tests/kitchen_sink/EmploymentEvent)




## Inheritance

* [Event](Event.md)
    * **EmploymentEvent**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [employed_at](employed_at.md) | [Company](Company.md) | 0..1 | None  | . |
| [type](type.md) | [EmploymentEventType](EmploymentEventType.md) | 0..1 | None  | . |
| [started_at_time](started_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [ended_at_time](ended_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [is_current](is_current.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [metadata](metadata.md) | [AnyObject](AnyObject.md) | 0..1 | Example of a slot that has an unconstrained range  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Person](Person.md) | [has_employment_history](has_employment_history.md) | range | EmploymentEvent |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: EmploymentEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Event
slots:
- employed at
- type
slot_usage:
  type:
    name: type
    range: EmploymentEventType
    required: false

```

Induced:

```yaml
name: EmploymentEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Event
slot_usage:
  type:
    name: type
    range: EmploymentEventType
    required: false
attributes:
  employed at:
    name: employed at
    in_subset:
    - subset A
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: EmploymentEvent
    range: Company
  type:
    name: type
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: EmploymentEvent
    range: EmploymentEventType
    required: false
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:startedAtTime
    owner: EmploymentEvent
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:endedAtTime
    owner: EmploymentEvent
    range: date
  is current:
    name: is current
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: EmploymentEvent
    range: boolean
  metadata:
    name: metadata
    description: Example of a slot that has an unconstrained range
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: EmploymentEvent
    range: AnyObject

```