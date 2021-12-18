# Organization

None

URI: [ks:Organization](https://w3id.org/linkml/tests/kitchen_sink/Organization)




## Inheritance

* **Organization** [ HasAliases]
    * [Company](Company.md)




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | NONE | 0..1 | None  | . |
| [name](name.md) | NONE | 0..1 | None  | . |
| [aliases](aliases.md) | NONE | 0..* | None  | . |


## Usages



## Identifier and Mapping Information


### Valid ID Prefixes

Instances of this class *should* have identifiers with one of the following prefixes:

* ROR







## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: Organization
id_prefixes:
- ROR
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixins:
- HasAliases
slots:
- id
- name

```

Induced:

```yaml
name: Organization
id_prefixes:
- ROR
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixins:
- HasAliases
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    owner: Organization
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    owner: Organization
    required: false
  aliases:
    name: aliases
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    slot_uri: skos:altLabel
    multivalued: true
    owner: Organization

```