# FakeClass

None

URI: [ks:FakeClass](https://w3id.org/linkml/tests/kitchen_sink/FakeClass)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [test_attribute](test_attribute.md) | NONE | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: FakeClass
deprecated: this is not a real class, we are using it to test deprecation
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  test_attribute:
    name: test_attribute
    from_schema: https://w3id.org/linkml/tests/kitchen_sink

```

Induced:

```yaml
name: FakeClass
deprecated: this is not a real class, we are using it to test deprecation
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  test_attribute:
    name: test_attribute
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: FakeClass

```