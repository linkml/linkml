# Class: SubclassTest




URI: [ks:SubclassTest](https://w3id.org/linkml/tests/kitchen_sink/SubclassTest)




## Inheritance

* [ClassWithSpaces](ClassWithSpaces.md)
    * **SubclassTest**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [slot_with_space_2](slot_with_space_2.md) | [ClassWithSpaces](ClassWithSpaces.md) | 0..1 | None  | . |
| [slot_with_space_1](slot_with_space_1.md) | NONE | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: subclass test
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: class with spaces
attributes:
  slot with space 2:
    name: slot with space 2
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    range: class with spaces

```
</details>

### Induced

<details>
```yaml
name: subclass test
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: class with spaces
attributes:
  slot with space 2:
    name: slot with space 2
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: slot_with_space_2
    owner: subclass test
    range: class with spaces
  slot with space 1:
    name: slot with space 1
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: slot_with_space_1
    owner: subclass test

```
</details>