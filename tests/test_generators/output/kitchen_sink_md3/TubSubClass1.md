# Class: TubSubClass1
_Same depth as Sub sub class 1_





URI: [ks:TubSubClass1](https://w3id.org/linkml/tests/kitchen_sink/TubSubClass1)


```mermaid
 classDiagram
    class TubSubClass1
      SubclassTest <|-- TubSubClass1
      
      TubSubClass1 : slot_with_space_1
      TubSubClass1 : slot_with_space_2
      
```




## Inheritance
* [ClassWithSpaces](ClassWithSpaces.md)
    * [SubclassTest](SubclassTest.md)
        * **tub sub class 1**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [slot with space 2](slot_with_space_2.md) | 0..1 <br/> [ClassWithSpaces](ClassWithSpaces.md) | None  | inherited |
| [slot with space 1](slot_with_space_1.md) | 0..1 <br/> NONE | None  | inherited |




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:TubSubClass1']|join(', ') |
| native | ['ks:TubSubClass1']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: tub sub class 1
description: Same depth as Sub sub class 1
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: subclass test

```
</details>

### Induced

<details>
```yaml
name: tub sub class 1
description: Same depth as Sub sub class 1
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: subclass test
attributes:
  slot with space 2:
    name: slot with space 2
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: slot_with_space_2
    owner: tub sub class 1
    domain_of:
    - subclass test
    range: class with spaces
  slot with space 1:
    name: slot with space 1
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: slot_with_space_1
    owner: tub sub class 1
    domain_of:
    - class with spaces

```
</details>