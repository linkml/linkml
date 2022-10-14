# Class: WithLocation



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [ks:WithLocation](https://w3id.org/linkml/tests/kitchen_sink/WithLocation)


```mermaid
 classDiagram
    class WithLocation
      WithLocation <|-- MarriageEvent
      
      WithLocation : in_location
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [in location](in_location.md) | 0..1 <br/> [Place](Place.md) | None  | direct |




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:WithLocation']|join(', ') |
| native | ['ks:WithLocation']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: WithLocation
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
mixin: true
slots:
- in location

```
</details>

### Induced

<details>
```yaml
name: WithLocation
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
mixin: true
attributes:
  in location:
    name: in location
    annotations:
      biolink:opposite:
        tag: biolink:opposite
        value: location_of
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: in_location
    owner: WithLocation
    domain_of:
    - BirthEvent
    - MedicalEvent
    - WithLocation
    range: Place

```
</details>