# CodeSystem

None

URI: [ks:CodeSystem](https://w3id.org/linkml/tests/kitchen_sink/CodeSystem)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | NONE | 0..1 | None  | . |
| [name](name.md) | NONE | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Concept](Concept.md) | [in_code_system](in_code_system.md) | range | CodeSystem |
| [DiagnosisConcept](DiagnosisConcept.md) | [in_code_system](in_code_system.md) | range | CodeSystem |
| [ProcedureConcept](ProcedureConcept.md) | [in_code_system](in_code_system.md) | range | CodeSystem |
| [Dataset](Dataset.md) | [code_systems](code_systems.md) | range | CodeSystem |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: CodeSystem
from_schema: https://w3id.org/linkml/tests/kitchen_sink
slots:
- id
- name

```

Induced:

```yaml
name: CodeSystem
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    owner: CodeSystem
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    owner: CodeSystem
    required: false

```