# Class: Agent
_a provence-generating agent_





URI: [prov:Agent](http://www.w3.org/ns/prov#Agent)


```mermaid
 classDiagram
    class Agent
      Agent : actedOnBehalfOf
      Agent : id
      Agent : wasInformedBy
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> NONE | None  | direct |
| [acted on behalf of](actedOnBehalfOf.md) | 0..1 <br/> [Agent](Agent.md) | None  | direct |
| [was informed by](wasInformedBy.md) | 0..1 <br/> [Activity](Activity.md) | None  | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Activity](Activity.md) | [was associated with](wasAssociatedWith.md) | range | agent |
| [Agent](Agent.md) | [acted on behalf of](actedOnBehalfOf.md) | range | agent |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/core





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['prov:Agent']|join(', ') |
| native | ['core:Agent']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: agent
description: a provence-generating agent
from_schema: https://w3id.org/linkml/tests/core
rank: 1000
slots:
- id
- acted on behalf of
- was informed by
class_uri: prov:Agent

```
</details>

### Induced

<details>
```yaml
name: agent
description: a provence-generating agent
from_schema: https://w3id.org/linkml/tests/core
rank: 1000
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1
    identifier: true
    alias: id
    owner: agent
    domain_of:
    - Person
    - Organization
    - Place
    - Concept
    - CodeSystem
    - activity
    - agent
  acted on behalf of:
    name: acted on behalf of
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1000
    slot_uri: prov:actedOnBehalfOf
    alias: acted_on_behalf_of
    owner: agent
    domain_of:
    - agent
    range: agent
  was informed by:
    name: was informed by
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1000
    slot_uri: prov:wasInformedBy
    alias: was_informed_by
    owner: agent
    domain_of:
    - activity
    - agent
    range: activity
class_uri: prov:Agent

```
</details>