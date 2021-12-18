# FamilialRelationship

None

URI: [ks:FamilialRelationship](https://w3id.org/linkml/tests/kitchen_sink/FamilialRelationship)




## Inheritance

* [Relationship](Relationship.md)
    * **FamilialRelationship**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [started_at_time](started_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [ended_at_time](ended_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [related_to](related_to.md) | [Person](Person.md) | 1..1 | None  | . |
| [type](type.md) | [FamilialRelationshipType](FamilialRelationshipType.md) | 1..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Person](Person.md) | [has_familial_relationships](has_familial_relationships.md) | range | FamilialRelationship |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: FamilialRelationship
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Relationship
slot_usage:
  type:
    name: type
    range: FamilialRelationshipType
    required: true
  related to:
    name: related to
    range: Person
    required: true

```

Induced:

```yaml
name: FamilialRelationship
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Relationship
slot_usage:
  type:
    name: type
    range: FamilialRelationshipType
    required: true
  related to:
    name: related to
    range: Person
    required: true
attributes:
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:startedAtTime
    owner: FamilialRelationship
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:endedAtTime
    owner: FamilialRelationship
    range: date
  related to:
    name: related to
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: FamilialRelationship
    range: Person
    required: true
  type:
    name: type
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: FamilialRelationship
    range: FamilialRelationshipType
    required: true

```