# Class: Relationship




URI: [ks:Relationship](https://w3id.org/linkml/tests/kitchen_sink/Relationship)


```mermaid
 classDiagram
    class Relationship
      Relationship <|-- FamilialRelationship
      
      Relationship : endedAtTime
      Relationship : related_to
      Relationship : startedAtTime
      Relationship : type
      
```




## Inheritance
* **Relationship**
    * [FamilialRelationship](FamilialRelationship.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [started at time](startedAtTime.md) | 0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) | None  | direct |
| [ended at time](endedAtTime.md) | 0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) | None  | direct |
| [related to](related_to.md) | 0..1 <br/> NONE | None  | direct |
| [type](type.md) | 0..1 <br/> NONE | None  | direct |




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ks:Relationship']|join(', ') |
| native | ['ks:Relationship']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Relationship
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
slots:
- started at time
- ended at time
- related to
- type

```
</details>

### Induced

<details>
```yaml
name: Relationship
from_schema: https://w3id.org/linkml/tests/kitchen_sink
rank: 1000
attributes:
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1000
    slot_uri: prov:startedAtTime
    alias: started_at_time
    owner: Relationship
    domain_of:
    - Event
    - Relationship
    - activity
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    rank: 1000
    slot_uri: prov:endedAtTime
    alias: ended_at_time
    owner: Relationship
    domain_of:
    - Event
    - Relationship
    - activity
    range: date
  related to:
    name: related to
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: related_to
    owner: Relationship
    domain_of:
    - Relationship
  type:
    name: type
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    rank: 1000
    alias: type
    owner: Relationship
    domain_of:
    - Relationship
    - EmploymentEvent

```
</details>