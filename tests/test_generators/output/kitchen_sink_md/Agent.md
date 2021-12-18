# Agent

a provence-generating agent

URI: [prov:Agent](http://www.w3.org/ns/prov#Agent)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | NONE | 0..1 | None  | . |
| [acted_on_behalf_of](acted_on_behalf_of.md) | [Agent](Agent.md) | 0..1 | None  | . |
| [was_informed_by](was_informed_by.md) | [Activity](Activity.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Activity](Activity.md) | [was_associated_with](was_associated_with.md) | range | agent |
| [Agent](Agent.md) | [acted_on_behalf_of](acted_on_behalf_of.md) | range | agent |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: agent
description: a provence-generating agent
from_schema: https://w3id.org/linkml/tests/core
slots:
- id
- acted on behalf of
- was informed by
class_uri: prov:Agent

```

Induced:

```yaml
name: agent
description: a provence-generating agent
from_schema: https://w3id.org/linkml/tests/core
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    owner: agent
  acted on behalf of:
    name: acted on behalf of
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:actedOnBehalfOf
    owner: agent
    range: agent
  was informed by:
    name: was informed by
    from_schema: https://w3id.org/linkml/tests/core
    slot_uri: prov:wasInformedBy
    owner: agent
    range: activity
class_uri: prov:Agent

```