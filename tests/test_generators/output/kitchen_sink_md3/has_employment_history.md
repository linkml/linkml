# Slot: has_employment_history

URI: [ks:has_employment_history](https://w3id.org/linkml/tests/kitchen_sink/has_employment_history)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Person](Person.md) | A person, living or dead






## Properties

* Range: [EmploymentEvent](EmploymentEvent.md)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink




## LinkML Source

<details>
```yaml
name: has employment history
in_subset:
- subset B
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 7
multivalued: true
alias: has_employment_history
domain_of:
- Person
range: EmploymentEvent
inlined: true
inlined_as_list: true

```
</details>