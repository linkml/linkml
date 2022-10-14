# Class: Organization
_An organization.

This description
includes newlines

## Markdown headers

 * and
 * a
 * list_





URI: [ks:Organization](https://w3id.org/linkml/tests/kitchen_sink/Organization)


```mermaid
 classDiagram
    class Organization
      HasAliases <|-- Organization
      
      Organization : altLabel
      Organization : id
      Organization : name
      

      Organization <|-- Company
      
      Organization : altLabel
      Organization : id
      Organization : name
      
```




## Inheritance
* **Organization** [ [HasAliases](HasAliases.md)]
    * [Company](Company.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> NONE | None  | direct |
| [name](name.md) | 0..1 <br/> NONE | None  | direct |
| [aliases](altLabel.md) | 0..* <br/> NONE | None  | inherited |




## Identifier and Mapping Information


### Valid ID Prefixes

Instances of this class *should* have identifiers with one of the following prefixes:

* ROR








### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:Organization']|join(', ') |
| native | ['ks:Organization']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Organization
id_prefixes:
- ROR
description: "An organization.\n\nThis description\nincludes newlines\n\n## Markdown\
  \ headers\n\n * and\n * a\n * list"
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 3
mixins:
- HasAliases
slots:
- id
- name

```
</details>

### Induced

<details>
```yaml
name: Organization
id_prefixes:
- ROR
description: "An organization.\n\nThis description\nincludes newlines\n\n## Markdown\
  \ headers\n\n * and\n * a\n * list"
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 3
mixins:
- HasAliases
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1
    identifier: true
    alias: id
    owner: Organization
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
    owner: Organization
    domain_of:
    - Friend
    - Person
    - Organization
    - Place
    - Concept
    - CodeSystem
    required: false
  aliases:
    name: aliases
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    slot_uri: skos:altLabel
    multivalued: true
    alias: aliases
    owner: Organization
    domain_of:
    - HasAliases

```
</details>