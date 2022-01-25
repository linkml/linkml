# Dataset

None

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

Direct:

```yaml
name: Dataset
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  persons:
    name: persons
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    inlined: true
    inlined_as_list: true
    range: Person
  companies:
    name: companies
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    inlined: true
    inlined_as_list: true
    range: Company
  activities:
    name: activities
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    inlined: true
    inlined_as_list: true
    range: activity
  code systems:
    name: code systems
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    inlined: true
    range: CodeSystem
tree_root: true

```

Induced:

```yaml
name: Dataset
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  persons:
    name: persons
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    inlined: true
    inlined_as_list: true
    owner: Dataset
    range: Person
  companies:
    name: companies
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    inlined: true
    inlined_as_list: true
    owner: Dataset
    range: Company
  activities:
    name: activities
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    inlined: true
    inlined_as_list: true
    owner: Dataset
    range: activity
  code systems:
    name: code systems
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    inlined: true
    owner: Dataset
    range: CodeSystem
tree_root: true

```