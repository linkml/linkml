# Concept

None

URI: [ks:Concept](https://w3id.org/linkml/tests/kitchen_sink/Concept)




## Inheritance

* **Concept**
    * [DiagnosisConcept](DiagnosisConcept.md)
    * [ProcedureConcept](ProcedureConcept.md)




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | NONE | 0..1 | None  | . |
| [name](name.md) | NONE | 0..1 | None  | . |
| [in_code_system](in_code_system.md) | [CodeSystem](CodeSystem.md) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information


### Valid ID Prefixes

Instances of this class *should* have identifiers with one of the following prefixes:

* CODE







## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

Direct:

```yaml
name: Concept
id_prefixes:
- CODE
from_schema: https://w3id.org/linkml/tests/kitchen_sink
slots:
- id
- name
- in code system

```

Induced:

```yaml
name: Concept
id_prefixes:
- CODE
from_schema: https://w3id.org/linkml/tests/kitchen_sink
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    owner: Concept
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    owner: Concept
    required: false
  in code system:
    name: in code system
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    owner: Concept
    range: CodeSystem

```