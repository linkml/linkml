# Place

None

URI: [ks:Place](https://w3id.org/linkml/tests/kitchen_sink/Place)




## Inheritance

* **Place** [ HasAliases]




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | NONE | 0..1 | None  | . |
| [name](name.md) | NONE | 0..1 | None  | . |
| [aliases](aliases.md) | NONE | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [BirthEvent](BirthEvent.md) | [in_location](in_location.md) | range | Place |
| [MedicalEvent](MedicalEvent.md) | [in_location](in_location.md) | range | Place |
| [WithLocation](WithLocation.md) | [in_location](in_location.md) | range | Place |
| [MarriageEvent](MarriageEvent.md) | [in_location](in_location.md) | range | Place |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: Place
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixins:
- HasAliases
slots:
- id
- name

```

Induced:

```yaml
name: Place
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixins:
- HasAliases
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    owner: Place
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    owner: Place
    required: false
  aliases:
    name: aliases
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    slot_uri: skos:altLabel
    multivalued: true
    owner: Place

```