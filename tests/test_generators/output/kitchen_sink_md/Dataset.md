# Class: Dataset




URI: [ks:Dataset](https://w3id.org/linkml/tests/kitchen_sink/Dataset)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [persons](persons.md) | [Person](Person.md) | 0..* | None  | . |
| [companies](companies.md) | [Company](Company.md) | 0..* | None  | . |
| [activities](activities.md) | [Activity](Activity.md) | 0..* | None  | . |
| [code_systems](code_systems.md) | [CodeSystem](CodeSystem.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Dataset
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  persons:
    name: persons
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    range: Person
    inlined: true
    inlined_as_list: true
  companies:
    name: companies
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    range: Company
    inlined: true
    inlined_as_list: true
  activities:
    name: activities
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    range: activity
    inlined: true
    inlined_as_list: true
  code systems:
    name: code systems
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    range: CodeSystem
    inlined: true
tree_root: true

```
</details>

### Induced

<details>
```yaml
name: Dataset
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  persons:
    name: persons
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    alias: persons
    owner: Dataset
    range: Person
    inlined: true
    inlined_as_list: true
  companies:
    name: companies
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    alias: companies
    owner: Dataset
    range: Company
    inlined: true
    inlined_as_list: true
  activities:
    name: activities
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    alias: activities
    owner: Dataset
    range: activity
    inlined: true
    inlined_as_list: true
  code systems:
    name: code systems
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    alias: code_systems
    owner: Dataset
    range: CodeSystem
    inlined: true
tree_root: true

```
</details>