# Class: Address




URI: [ks:Address](https://w3id.org/linkml/tests/kitchen_sink/Address)




```mermaid
 classDiagram
    class Address
      Address : city
      Address : street
      





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







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:Address'] |
| native | ['ks:Address'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Address
from_schema: https://w3id.org/linkml/tests/kitchen_sink
slots:
- street
- city

```
</details>

### Induced

<details>
```yaml
name: Address
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  street:
    name: street
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: street
    owner: Address
  city:
    name: city
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: city
    owner: Address

```
</details>