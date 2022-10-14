# Class: CodeSystem




URI: [ks:CodeSystem](https://w3id.org/linkml/tests/kitchen_sink/CodeSystem)


```mermaid
 classDiagram
    class CodeSystem
      CodeSystem : id
      CodeSystem : name
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> NONE | None  | direct |
| [name](name.md) | 0..1 <br/> NONE | None  | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Concept](Concept.md) | [in code system](in_code_system.md) | range | CodeSystem |
| [DiagnosisConcept](DiagnosisConcept.md) | [in code system](in_code_system.md) | range | CodeSystem |
| [ProcedureConcept](ProcedureConcept.md) | [in code system](in_code_system.md) | range | CodeSystem |
| [Dataset](Dataset.md) | [code systems](code_systems.md) | range | CodeSystem |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:CodeSystem']|join(', ') |
| native | ['ks:CodeSystem']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: CodeSystem
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
slots:
- id
- name

```
</details>

### Induced

<details>
```yaml
name: CodeSystem
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1
    identifier: true
    alias: id
    owner: CodeSystem
    domain_of:
    - Person
    - Organization
    - Place
    - Concept
    - CodeSystem
    - activity
    - agent
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    rank: 2
    alias: name
    owner: CodeSystem
    domain_of:
    - Friend
    - Person
    - Organization
    - Place
    - Concept
    - CodeSystem
    required: false

```
</details>