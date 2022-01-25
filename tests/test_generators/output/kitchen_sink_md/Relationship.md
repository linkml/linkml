# Relationship

None

URI: [ks:Relationship](https://w3id.org/linkml/tests/kitchen_sink/Relationship)




## Inheritance

* **Relationship**
    * [FamilialRelationship](FamilialRelationship.md)




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [started_at_time](started_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [ended_at_time](ended_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [related_to](related_to.md) | NONE | 0..1 | None  | . |
| [type](type.md) | NONE | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: Relationship
from_schema: https://w3id.org/linkml/tests/kitchen_sink
slots:
- started at time
- ended at time
- related to
- type

```

Induced:

```yaml
name: Relationship
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:startedAtTime
    owner: Relationship
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:endedAtTime
    owner: Relationship
    range: date
  related to:
    name: related to
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: Relationship
  type:
    name: type
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: Relationship

```