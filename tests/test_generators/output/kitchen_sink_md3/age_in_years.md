# Slot: age_in_years
_number of years since birth_


URI: [ks:age_in_years](https://w3id.org/linkml/tests/kitchen_sink/age_in_years)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Person](Person.md) | A person, living or dead






## Properties

* Range: [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink




## LinkML Source

<details>
```yaml
name: age in years
description: number of years since birth
in_subset:
- subset A
- subset B
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
alias: age_in_years
domain_of:
- Person
range: integer
minimum_value: 0
maximum_value: 999

```
</details>