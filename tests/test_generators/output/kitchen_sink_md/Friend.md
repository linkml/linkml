# Class: Friend


* __NOTE__: this is an abstract class and should not be instantiated directly



URI: [ks:Friend](https://w3id.org/linkml/tests/kitchen_sink/Friend)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [name](name.md) | NONE | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Friend
from_schema: https://w3id.org/linkml/tests/kitchen_sink
abstract: true
slots:
- name

```
</details>

### Induced

<details>
```yaml
name: Friend
from_schema: https://w3id.org/linkml/tests/kitchen_sink
abstract: true
attributes:
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    alias: name
    owner: Friend
    required: false

```
</details>