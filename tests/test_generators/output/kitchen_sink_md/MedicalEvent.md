# Class: MedicalEvent




URI: [ks:MedicalEvent](https://w3id.org/linkml/tests/kitchen_sink/MedicalEvent)




## Inheritance

* [Event](Event.md)
    * **MedicalEvent**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [in_location](in_location.md) | [Place](Place.md) | 0..1 | None  | . |
| [diagnosis](diagnosis.md) | [DiagnosisConcept](DiagnosisConcept.md) | 0..1 | None  | . |
| [procedure](procedure.md) | [ProcedureConcept](ProcedureConcept.md) | 0..1 | None  | . |
| [started_at_time](started_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [ended_at_time](ended_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [is_current](is_current.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [metadata](metadata.md) | [AnyObject](AnyObject.md) | 0..1 | Example of a slot that has an unconstrained range  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Person](Person.md) | [has_medical_history](has_medical_history.md) | range | MedicalEvent |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MedicalEvent
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Event
slots:
- in location
- diagnosis
- procedure

```
</details>

### Induced

<details>
```yaml
name: MedicalEvent
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
    alias: in_location
    owner: MedicalEvent
    range: Place
  diagnosis:
    name: diagnosis
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: diagnosis
    owner: MedicalEvent
    range: DiagnosisConcept
    inlined: true
  procedure:
    name: procedure
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: procedure
    owner: MedicalEvent
    range: ProcedureConcept
    inlined: true
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:startedAtTime
    alias: started_at_time
    owner: MedicalEvent
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:endedAtTime
    alias: ended_at_time
    owner: MedicalEvent
    range: date
  is current:
    name: is current
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: is_current
    owner: MedicalEvent
    range: boolean
  metadata:
    name: metadata
    description: Example of a slot that has an unconstrained range
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: metadata
    owner: MedicalEvent
    range: AnyObject

```
</details>