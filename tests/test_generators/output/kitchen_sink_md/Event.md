# Event

None

URI: [ks:Event](https://w3id.org/linkml/tests/kitchen_sink/Event)




## Inheritance

* **Event**
    * [BirthEvent](BirthEvent.md)
    * [EmploymentEvent](EmploymentEvent.md)
    * [MedicalEvent](MedicalEvent.md)
    * [MarriageEvent](MarriageEvent.md) [ WithLocation]




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [started_at_time](started_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [ended_at_time](ended_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [is_current](is_current.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [metadata](metadata.md) | [AnyObject](AnyObject.md) | 0..1 | Example of a slot that has an unconstrained range  | . |


## Usages



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: Event
from_schema: https://w3id.org/linkml/tests/kitchen_sink
slots:
- started at time
- ended at time
- is current
- metadata

```

Induced:

```yaml
name: Event
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:startedAtTime
    owner: Event
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:endedAtTime
    owner: Event
    range: date
  is current:
    name: is current
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: Event
    range: boolean
  metadata:
    name: metadata
    description: Example of a slot that has an unconstrained range
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: Event
    range: AnyObject

```