# HasAliases

None

URI: [ks:HasAliases](https://w3id.org/linkml/tests/kitchen_sink/HasAliases)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [aliases](aliases.md) | NONE | 0..* | None  | . |


## Usages



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: HasAliases
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixin: true
attributes:
  aliases:
    name: aliases
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    slot_uri: skos:altLabel
    multivalued: true

```

Induced:

```yaml
name: HasAliases
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixin: true
attributes:
  aliases:
    name: aliases
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    slot_uri: skos:altLabel
    multivalued: true
    owner: HasAliases

```