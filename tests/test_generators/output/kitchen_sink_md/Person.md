# Class: Person
_A person, living or dead_





URI: [ks:Person](https://w3id.org/linkml/tests/kitchen_sink/Person)




## Inheritance

* **Person** [ HasAliases]




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | NONE | 0..1 | None  | . |
| [name](name.md) | NONE | 0..1 | None  | . |
| [has_employment_history](has_employment_history.md) | [EmploymentEvent](EmploymentEvent.md) | 0..* | None  | . |
| [has_familial_relationships](has_familial_relationships.md) | [FamilialRelationship](FamilialRelationship.md) | 0..* | None  | . |
| [has_medical_history](has_medical_history.md) | [MedicalEvent](MedicalEvent.md) | 0..* | None  | . |
| [age_in_years](age_in_years.md) | [integer](integer.md) | 0..1 | number of years since birth  | . |
| [addresses](addresses.md) | [Address](Address.md) | 0..* | None  | . |
| [has_birth_event](has_birth_event.md) | [BirthEvent](BirthEvent.md) | 0..1 | None  | . |
| [aliases](aliases.md) | NONE | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [FamilialRelationship](FamilialRelationship.md) | [related_to](related_to.md) | range | Person |
| [MarriageEvent](MarriageEvent.md) | [married_to](married_to.md) | range | Person |
| [Company](Company.md) | [ceo](ceo.md) | range | Person |
| [Dataset](Dataset.md) | [persons](persons.md) | range | Person |



## Identifier and Mapping Information


### Valid ID Prefixes

Instances of this class *should* have identifiers with one of the following prefixes:

* P










## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Person
id_prefixes:
- P
description: A person, living or dead
in_subset:
- subset A
from_schema: https://w3id.org/linkml/tests/kitchen_sink
exact_mappings:
- schema:Person
mixins:
- HasAliases
slots:
- id
- name
- has employment history
- has familial relationships
- has medical history
- age in years
- addresses
- has birth event
slot_usage:
  name:
    name: name
    pattern: ^\S+ \S+

```
</details>

### Induced

<details>
```yaml
name: Person
id_prefixes:
- P
description: A person, living or dead
in_subset:
- subset A
from_schema: https://w3id.org/linkml/tests/kitchen_sink
exact_mappings:
- schema:Person
mixins:
- HasAliases
slot_usage:
  name:
    name: name
    pattern: ^\S+ \S+
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/tests/core
    identifier: true
    alias: id
    owner: Person
  name:
    name: name
    from_schema: https://w3id.org/linkml/tests/core
    alias: name
    owner: Person
    required: false
    pattern: ^\S+ \S+
  has employment history:
    name: has employment history
    in_subset:
    - subset B
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    alias: has_employment_history
    owner: Person
    range: EmploymentEvent
    inlined: true
    inlined_as_list: true
  has familial relationships:
    name: has familial relationships
    in_subset:
    - subset B
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    alias: has_familial_relationships
    owner: Person
    range: FamilialRelationship
    inlined: true
    inlined_as_list: true
  has medical history:
    name: has medical history
    in_subset:
    - subset B
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    alias: has_medical_history
    owner: Person
    range: MedicalEvent
    inlined: true
    inlined_as_list: true
  age in years:
    name: age in years
    description: number of years since birth
    in_subset:
    - subset A
    - subset B
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: age_in_years
    owner: Person
    range: integer
    minimum_value: 0
    maximum_value: 999
  addresses:
    name: addresses
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    multivalued: true
    alias: addresses
    owner: Person
    range: Address
  has birth event:
    name: has birth event
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    alias: has_birth_event
    owner: Person
    range: BirthEvent
  aliases:
    name: aliases
    from_schema: https://w3id.org/linkml/tests/kitchen_sink
    slot_uri: skos:altLabel
    multivalued: true
    alias: aliases
    owner: Person

```
</details>