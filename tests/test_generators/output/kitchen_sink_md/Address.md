# Address

None

URI: [ks:Address](https://w3id.org/linkml/tests/kitchen_sink/Address)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [street](street.md) | NONE | 0..1 | None  | . |
| [city](city.md) | NONE | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Person](Person.md) | [addresses](addresses.md) | range | Address |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: Address
from_schema: https://w3id.org/linkml/tests/kitchen_sink
slots:
- street
- city

```

Induced:

```yaml
name: Address
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  street:
    name: street
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: Address
  city:
    name: city
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: Address

```