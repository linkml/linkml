# Class: WithLocation



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [ks:WithLocation](https://w3id.org/linkml/tests/kitchen_sink/WithLocation)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [in_location](in_location.md) | [Place](Place.md) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: WithLocation
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixin: true
slots:
- in location

```
</details>

### Induced

<details>
```yaml
name: WithLocation
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixin: true
attributes:
  in location:
    name: in location
    annotations:
      biolink:opposite:
        tag: biolink:opposite
        value: location_of
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: in_location
    owner: WithLocation
    range: Place

```
</details>