# Class: Activity
_a provence-generating activity_





URI: [core:Activity](https://w3id.org/linkml/tests/core/Activity)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | NONE | 0..1 | None  | . |
| [started_at_time](started_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [ended_at_time](ended_at_time.md) | [date](date.md) | 0..1 | None  | . |
| [was_informed_by](was_informed_by.md) | [Activity](Activity.md) | 0..1 | None  | . |
| [was_associated_with](was_associated_with.md) | [Agent](Agent.md) | 0..1 | None  | . |
| [used](used.md) | NONE | 0..1 | None  | . |
| [description](description.md) | NONE | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Dataset](Dataset.md) | [activities](activities.md) | range | activity |
| [Activity](Activity.md) | [was_informed_by](was_informed_by.md) | range | activity |
| [Activity](Activity.md) | [used](used.md) | domain | activity |
| [Agent](Agent.md) | [was_informed_by](was_informed_by.md) | range | activity |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: activity
description: a provence-generating activity
from_schema: https://w3id.org/linkml/tests/core
mappings:
- prov:Activity
slots:
- id
- started at time
- ended at time
- was informed by
- was associated with
- used
- description

```
</details>

### Induced

<details>
```yaml
name: activity
description: a provence-generating activity
from_schema: https://w3id.org/linkml/tests/core
mappings:
- prov:Activity
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    alias: id
    owner: activity
  started at time:
    name: started at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:startedAtTime
    alias: started_at_time
    owner: activity
    range: date
  ended at time:
    name: ended at time
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:endedAtTime
    alias: ended_at_time
    owner: activity
    range: date
  was informed by:
    name: was informed by
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:wasInformedBy
    alias: was_informed_by
    owner: activity
    range: activity
  was associated with:
    name: was associated with
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:wasAssociatedWith
    alias: was_associated_with
    owner: activity
    range: agent
    inlined: false
  used:
    name: used
    from_schema: https://w3id.org/linkml/tests/core
    domain: activity
    slot_uri: prov:used
    alias: used
    owner: activity
  description:
    name: description
    from_schema: https://w3id.org/linkml/tests/core
    alias: description
    owner: activity

```
</details>