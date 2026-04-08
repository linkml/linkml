# Slots

Slots operate the same way as "fields" in traditional object languages and the same ways as "columns" in spreadsheets and relational databases.

If you have a JSON object that is conformant to a LinkML schema, then
the keys for that object must correspond to slots in the schema, that
are applicable to that class.

for example, if we have an object instantiating a Person class:

```json
{
  "id": "PERSON001",
  "name": "....",
  "email": "...."
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

To use a URI or CURIE as a range, create a class with class_uri set to the URI or CURIE and use that class as the range.

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

The [slot_usage](https://w3id.org/linkml/slot_usage) slot can be used to *refine* the meaning of a slot in the context of a particular class.

For example, imagine a schema with classes `Vehicle` and `VehiclePart`, which vehicles can be disassembled into parts:


```yaml
classes:
  Vehicle:
    slots:
      - make
      - parts
  VehiclePart:
    slots:
      - part_number

slots:
  make:
    range: string
  part_number:
    range: string
  parts:
    range: VehiclePart
    multivalued: true
```

We can refine the hierarchy:

```yaml
classes:
  ...
  Car:
    is_a: Vehicle
    slot_usage:
      parts:
        range: CarPart
  Bicycle:
    is_a: Vehicle
    slot_usage:
      parts:
        range: BicyclePart
  CarPart:
    is_a: VehiclePart
  BicyclePart:
    is_a: VehiclePart
```

In this example, `Car` and `Bicycle` are subclasses of `Vehicle`, and `CarPart` and `BicyclePart` are subclasses of `VehiclePart`.
The `parts` slot is refined to have a range of `CarPart` for `Car` and `BicyclePart` for `Bicycle`.

Note that LinkML schemas are [monotonic](https://en.wikipedia.org/wiki/Monotonicity_of_entailment). This means
it's not possible to *override* existing constraints, new constraints are always additive and "layered on".

In the above example, you can think of a `Car` having *two* constraints on the `parts` slot:

- one from the `Vehicle` class, stating that the range is `VehiclePart`
- and one from the `Car` class, stating that the range is `CarPart`

Rather than the first overriding the second, the two constraints are combined, and the first becomes redundant
(because `CarPart` is a subclass of `VehiclePart`)

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

See the [type-designators](type-designators.md) section of the docs for more details.

## Cardinality

In LinkML, slots can be required (mandatory), and they can be singlevalued or multivalued. These are controlled
via `required` and `multivalued` boolean slots. Additionally, when a slot is multivalued, specific cardinality ranges can be supplied
using `maximum_cardinality` and `minimum_cardinality`.

Collectively, these metamodel slots define the *cardinality* of a slot in a data model.

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


### required

The [required](https://w3id.org/linkml/required) slot can be used to define whether a slot is required.

When a slot is declared as required, any class that uses that slot must have a value for that slot.

### recommended

The [recommended](https://w3id.org/linkml/recommended) slot can be used to define whether a slot is recommended.

If data is missing a recommended slot, it is still considered valid. However, validators may choose to issue warnings.

### explicit cardinality ranges

When a field is multivalued, cardinality can be explicit specified using the following metamodel slots:

- [minimum_cardinality](https://w3id.org/linkml/minimum_cardinality) minimum (inclusive) length of the list of elements
- [maximum_cardinality](https://w3id.org/linkml/maximum_cardinality) maximum (inclusive) length of the list of elements
- [exact_cardinality](https://w3id.org/linkml/exact_cardinality) exact length of the list of elements

Note that specifying `exact` entails both `maximum` and `minimum`, and setting `maximum` and `minimum` to be equal entails `exact`.

### Writing cardinality using UML notation

Cardinality can also be written in UML notation. The following gives an explanation of UML notation and how this maps to LinkML.

* `1` - Only 1 (`required` and not `multivalued`)
* `0..1` - Zero or one (not `required` and not `multivalued`)
* `1..*` - One or more (`required` and `multivalued`, with no minimum and maximum cardinality specified)
* `*` - Many (not `required` and `multivalued`, with no minimum and maximum cardinality specified)
* `n` - n (where n>1) (`multivalued`, with `exact_cardinality=n`)
* `0..n` - Zero to n (where n>1) (not `required` and `multivalued`, with `maximum_cardinality=n`)
* `1..n` - One to n (where n>1) (`required` and `multivalued`, with `maximum_cardinality=n`)
* `m..n` - m to n (where m,n>1) (`required` and `multivalued`, with `minimum_cardnality=m` and `maximum_cardinality=n`)


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
  my_enum_slot:
    range: FamilialRelationshipType
    ifabsent: FamilialRelationshipType(PARENT_OF)
```


## logical characteristics

Additional logical characteristics can be specified for a slot; these are all boolean:

* [transitive](https://w3id.org/linkml/transitive)
* [symmetric](https://w3id.org/linkml/symmetric)
* [antisymmetric](https://w3id.org/linkml/symmetric)
* [reflexive](https://w3id.org/linkml/reflexive)
* [locally_reflexive](https://w3id.org/linkml/locally_reflexive)
