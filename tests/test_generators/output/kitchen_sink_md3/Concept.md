# Class: Concept




URI: [ks:Concept](https://w3id.org/linkml/tests/kitchen_sink/Concept)


```mermaid
 classDiagram
    class Concept
      Concept <|-- DiagnosisConcept
      Concept <|-- ProcedureConcept
      
      Concept : id
      Concept : in_code_system
      Concept : name
      
```




## Inheritance
* **Concept**
    * [DiagnosisConcept](DiagnosisConcept.md)
    * [ProcedureConcept](ProcedureConcept.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> NONE | None  | direct |
| [name](name.md) | 0..1 <br/> NONE | None  | direct |
| [in code system](in_code_system.md) | 0..1 <br/> [CodeSystem](CodeSystem.md) | None  | direct |




## Identifier and Mapping Information


### Valid ID Prefixes

Instances of this class *should* have identifiers with one of the following prefixes:

* CODE








### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:Concept']|join(', ') |
| native | ['ks:Concept']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Concept
id_prefixes:
- CODE
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
slots:
- id
- name
- in code system

```
</details>

### Induced

<details>
```yaml
name: Concept
id_prefixes:
- CODE
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1
    identifier: true
    alias: id
    owner: Concept
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
    owner: Concept
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
    owner: Concept
    domain_of:
    - Concept
    range: CodeSystem

```
</details>