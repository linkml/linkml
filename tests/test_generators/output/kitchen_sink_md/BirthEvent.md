# BirthEvent

None

URI: [ks:BirthEvent](https://w3id.org/linkml/tests/kitchen_sink/BirthEvent)




## Inheritance

* [Event](Event.md)
    * **BirthEvent**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [in_location](in_location.md) | [Place](Place.md) | 0..1 | None  | . |
| [started_at_time](started_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [ended_at_time](ended_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [is_current](is_current.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [metadata](metadata.md) | [AnyObject](AnyObject.md) | 0..1 | Example of a slot that has an unconstrained range  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Person](Person.md) | [has_birth_event](has_birth_event.md) | range | BirthEvent |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: BirthEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Event
slots:
- in location

```

Induced:

```yaml
name: BirthEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Event
attributes:
  in location:
    name: in location
    annotations:
      biolink:opposite:
        tag: biolink:opposite
        value: location_of
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: BirthEvent
    range: Place
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:startedAtTime
    owner: BirthEvent
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:endedAtTime
    owner: BirthEvent
    range: date
  is current:
    name: is current
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: BirthEvent
    range: boolean
  metadata:
    name: metadata
    description: Example of a slot that has an unconstrained range
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: BirthEvent
    range: AnyObject

```