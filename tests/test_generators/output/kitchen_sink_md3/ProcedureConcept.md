# Class: ProcedureConcept




URI: [ks:ProcedureConcept](https://w3id.org/linkml/tests/kitchen_sink/ProcedureConcept)


```mermaid
 classDiagram
    class ProcedureConcept
      Concept <|-- ProcedureConcept
      
      ProcedureConcept : id
      ProcedureConcept : in_code_system
      ProcedureConcept : name
      
```




## Inheritance
* [Concept](Concept.md)
    * **ProcedureConcept**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> NONE | None  | inherited |
| [name](name.md) | 0..1 <br/> NONE | None  | inherited |
| [in code system](in_code_system.md) | 0..1 <br/> [CodeSystem](CodeSystem.md) | None  | inherited |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MedicalEvent](MedicalEvent.md) | [procedure](procedure.md) | range | ProcedureConcept |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:ProcedureConcept']|join(', ') |
| native | ['ks:ProcedureConcept']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ProcedureConcept
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: Concept

```
</details>

### Induced

<details>
```yaml
name: ProcedureConcept
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
is_a: Concept
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1
    identifier: true
    alias: id
    owner: ProcedureConcept
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
    owner: ProcedureConcept
    domain_of:
    - Friend
    - Person
    - Organization
    - Place
    - Concept
    - CodeSystem
    required: false
  in code system:
    name: in code system
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: in_code_system
    owner: ProcedureConcept
    domain_of:
    - Concept
    range: CodeSystem

```
</details>