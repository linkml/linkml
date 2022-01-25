# ProcedureConcept

None

URI: [ks:ProcedureConcept](https://w3id.org/linkml/tests/kitchen_sink/ProcedureConcept)




## Inheritance

* [Concept](Concept.md)
    * **ProcedureConcept**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | NONE | 0..1 | None  | . |
| [name](name.md) | NONE | 0..1 | None  | . |
| [in_code_system](in_code_system.md) | [CodeSystem](CodeSystem.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MedicalEvent](MedicalEvent.md) | [procedure](procedure.md) | range | ProcedureConcept |



## Identifier and Mapping Information






## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: ProcedureConcept
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Concept

```

Induced:

```yaml
name: ProcedureConcept
from_schema: https://w3id.org/linkml/tests/kitchen_sink
is_a: Concept
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    owner: ProcedureConcept
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    owner: ProcedureConcept
    required: false
  in code system:
    name: in code system
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: ProcedureConcept
    range: CodeSystem

```