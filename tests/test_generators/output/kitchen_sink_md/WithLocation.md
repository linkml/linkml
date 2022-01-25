# WithLocation

None

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

Direct:

```yaml
name: WithLocation
from_schema: https://w3id.org/linkml/tests/kitchen_sink
mixin: true
slots:
- in location

```

Induced:

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
    owner: WithLocation
    range: Place

```