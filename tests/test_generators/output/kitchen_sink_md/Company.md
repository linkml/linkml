# Class: Company




URI: [ks:Company](https://w3id.org/linkml/tests/kitchen_sink/Company)




## Inheritance

* [Organization](Organization.md) [ HasAliases]
    * **Company**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [ceo](ceo.md) | [Person](Person.md) | 0..1 | None  | . |
| [id](id.md) | NONE | 0..1 | None  | . |
| [name](name.md) | NONE | 0..1 | None  | . |
| [aliases](aliases.md) | NONE | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [EmploymentEvent](EmploymentEvent.md) | [employed_at](employed_at.md) | range | Company |
| [Dataset](Dataset.md) | [companies](companies.md) | range | Company |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Company
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Organization
attributes:
  ceo:
    name: ceo
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    slot_uri: schema:ceo
    range: Person

```
</details>

### Induced

<details>
```yaml
name: Company
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Organization
attributes:
  ceo:
    name: ceo
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    slot_uri: schema:ceo
    alias: ceo
    owner: Company
    range: Person
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    alias: id
    owner: Company
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    alias: name
    owner: Company
    required: false
  aliases:
    name: aliases
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    slot_uri: skos:altLabel
    multivalued: true
    alias: aliases
    owner: Company

```
</details>