# Slot: has_medical_history

URI: [ks:has_medical_history](https://w3id.org/linkml/tests/kitchen_sink/has_medical_history)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Person](Person.md) | A person, living or dead






## Properties

* Range: [MedicalEvent](MedicalEvent.md)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink




## LinkML Source

<details>
```yaml
name: has medical history
in_subset:
- subset B
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 5
multivalued: true
alias: has_medical_history
domain_of:
- Person
range: MedicalEvent
inlined: true
inlined_as_list: true

```
</details>