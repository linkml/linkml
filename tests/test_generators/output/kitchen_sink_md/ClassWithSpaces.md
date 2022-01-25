# ClassWithSpaces

None

URI: [ks:ClassWithSpaces](https://w3id.org/linkml/tests/kitchen_sink/ClassWithSpaces)




## Inheritance

* **ClassWithSpaces**
    * [SubclassTest](SubclassTest.md)




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [slot_with_space_1](slot_with_space_1.md) | NONE | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SubclassTest](SubclassTest.md) | [slot_with_space_2](slot_with_space_2.md) | range | class with spaces |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: class with spaces
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  slot with space 1:
    name: slot with space 1
    from_schema: https://w3id.org/linkml/tests/kitchen_sink

```

Induced:

```yaml
name: class with spaces
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  slot with space 1:
    name: slot with space 1
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: class with spaces

```