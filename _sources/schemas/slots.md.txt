# Slots

Slots operate the same way as "fields" in traditional object languages and the same ways as "columns" in spreadsheets and relational databases.

If you have a JSON object that is conformant to a LinkML schema, then
the keys for that object must correspond to slots in the schema, that
are applicable to that class.

for example, if we have an object instantiating a Person class:

```json
{"id": "PERSON001",
 "name": "....",
 "email": "....",
 ...
}
```

then `id`, `email`, `name` should all be valid slots, as in the following schema:

```yaml
classes:
  Person:
    slots:
      - id
      - name
      - email
```


If we have tabular data

|id|name|email|
|---|---|---|
|PERSON0001|...|...|

then the same constraints hold.

## ranges

Each slot must have a [range](https://w3id.org/linkml/range) - if this is not declared explicitly, then [default_range](https://w3id.org/linkml/default_range) is used.

The range must be one of:

 * A [ClassDefinition](https://w3id.org/linkml/ClassDefinition), when the value of the slot is a complex object
 * A [TypeDefinition](https://w3id.org/linkml/TypeDefinition), when the value of the slot is an atomic object
 * An [EnumDefinition](https://w3id.org/linkml/EnumDefinition), when the value of the slot is a token that represents a vocabulary element
 * A boolean combination of the above

Examples:

```yaml
slots:
  gender:
    slot_uri: schema:gender
    range: GenderType  ## range is an enum
  has_medical_history:
    range: MedicalEvent ## range is a class
    multivalued: true
    inlined_as_list: true
  age_in_years:
    range: integer  ## range is a type
    minimum_value: 0
    maximum_value: 999
```

## slot_usage

The [slot_usage](https://w3id.org/linkml/slot_usage) slot can be used to refine the meaning of a slot in the context of a particular class.

For example, imagine a schema with a generic "Relationship" class:

```yaml
  Relationship:
    slots:
      - started_at_time
      - ended_at_time
      - related_to
      - type
```

with subtypes such as `FamilialRelationship`, `BusinessRelationship`, etc

we can use `slot_usage` to constrain the meaning of more generic slots such as `type` and `related to`:

```yaml
  FamilialRelationship:
    is_a: Relationship
    slot_usage:
      type:
        range: FamilialRelationshipType
        required: true
      related to:
        range: Person
        required: true
```        

## Identifiers


If a slot is declared as an [identifier](https://w3id.org/linkml/identifier)
then it serves as a unique key for members of that class. It can also
be used for [inlining](inlining) as a dict in JSON serializations.


```yaml
slots:
  id:
    identifier: true
```

the range of an identifier can be any type, but it is a good idea to have these be of type [Uriorcurie](https://w3id.org/linkml/Uriorcurie)

A class must not have more than one identifier (asserted or derived). `identifier` marks the *primary* identifier.

If you need to mark additional fields as unique, or a collection of slots that when considered as a tuple are unique, use
`unique_keys` (see the [constraints](constraints.md) section of the docs).

## Type designator

The `designates_type` slot can be used to indicate the type or category of instances of a class.

```yaml
slots:
  category:
    designates_type: true
```

See the [type-designators](type-designator.md) section of the docs for more details.

## Slot cardinality

The cardinality of a slot is indicative of two properties on a slot. It tells us about whether a slot is *required* or not, and also about how many values it is allowed to have, i.e., whether it is *single-valued* or *multi-valued*.

The following list summarizes the expansions of the various possible combinations of cardinalities that can be asserted on a slot:
* `1..*` - slot is *required* and *multivalued*
* `1..1` - slot is *required* but *not multivalued*
* `0..*` - slot is *not required* but if provided it must be *mulitvalued*
* `0..1` - slot is *not required* and *not multivalued*

### multivalued

The [multivalued](https://w3id.org/linkml/multivalued) indicates that the range of the slot is a list

Example:

```yaml
slots:
  has_medical_history:
    range: MedicalEvent
    multivalued: true
    inlined_as_list: true
```

## default values

The `ifabsent` slot can be used to specify a default value for a slot using the syntax shown in the examples below.

Examples: 

```yaml
slots:
  my_string_slot:
    range: string
    ifabsent: string(default value)
  my_int_slot:
    range: integer
    ifabsent: int(42)
  my_float_slot:
    range: float
    ifabsent: float(0.5)
  my_bool_slot:
    range: boolean
    ifabsent: True
  my_date_slot:
    range: date
    ifabsent: date("2020-01-31")
  my_datetime_slot:
    range: datetime
    ifabsent: datetime("2020-01-31T12:00:00Z")
```

### required

The [required](https://w3id.org/linkml/required) slot can be used to define whether a slot is required.

When a slot is declared as required, any class that uses that slot must have a value for that slot.

### recommended

The [recommended](https://w3id.org/linkml/recommended) slot can be used to define whether a slot is recommended.

If data is missing a recommended slot, it is still considered valid. However, validators may choose to issue warnings.

## inverse

The `inverse` slot can be used to specify the inverse predicate of a given predicate slot relationship.

```yaml
  parent_of:
    is_a: famlially_related_to
    inverse: child_of
```

For most purposes, the specification of an inverse acts as additional documentation and doesn't
affect programming semantics. However, some frameworks like RDF/OWL allow for the inference of
inverses.

## logical characteristics

Additional logical characteristics can be specified for a slot; these are all boolean:

* [transitive](https://w3id.org/linkml/transitive)
* [symmetric](https://w3id.org/linkml/symmetric)
* [antisymmetric](https://w3id.org/linkml/symmetric)
* [reflexive](https://w3id.org/linkml/reflexive)
* [locally_reflexive](https://w3id.org/linkml/locally_reflexive)
