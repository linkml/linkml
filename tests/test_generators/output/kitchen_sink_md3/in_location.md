# Slot: in_location

URI: [ks:in_location](https://w3id.org/linkml/tests/kitchen_sink/in_location)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[BirthEvent](BirthEvent.md) | None
[MedicalEvent](MedicalEvent.md) | None
[WithLocation](WithLocation.md) | None
[MarriageEvent](MarriageEvent.md) | None






## Properties

* Range: [Place](Place.md)
* Multivalued: None







## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| biolink:opposite | location_of |



### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink




## LinkML Source

<details>
```yaml
name: in location
annotations:
  biolink:opposite:
    tag: biolink:opposite
    value: location_of
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
alias: in_location
domain_of:
- BirthEvent
- MedicalEvent
- WithLocation
range: Place

```
</details>