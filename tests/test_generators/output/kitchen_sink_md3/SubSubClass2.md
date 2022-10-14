# Class: SubSubClass2




URI: [ks:SubSubClass2](https://w3id.org/linkml/tests/kitchen_sink/SubSubClass2)


```mermaid
 classDiagram
    class SubSubClass2
      SubclassTest <|-- SubSubClass2
      
      SubSubClass2 : slot_with_space_1
      SubSubClass2 : slot_with_space_2
      
```




## Inheritance
* [ClassWithSpaces](ClassWithSpaces.md)
    * [SubclassTest](SubclassTest.md)
        * **Sub sub class 2**



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
| self | ['ks:SubSubClass2']|join(', ') |
| native | ['ks:SubSubClass2']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Sub sub class 2
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: subclass test

```
</details>

### Induced

<details>
```yaml
name: Sub sub class 2
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: subclass test
attributes:
  slot with space 2:
    name: slot with space 2
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: slot_with_space_2
    owner: Sub sub class 2
    domain_of:
    - subclass test
    range: class with spaces
  slot with space 1:
    name: slot with space 1
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: slot_with_space_1
    owner: Sub sub class 2
    domain_of:
    - class with spaces

```
</details>