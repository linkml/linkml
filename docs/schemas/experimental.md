# Experimental features

The following language features are experimental, behavior is not guaranteed to stay consistent

## LinkML Any type

LinkML is currently best suited to 'strict' schemas, and doesn't have full support for being able to model arbitrary dictionaries/objects. Each slot must have a defined range, the range must be exactly one of a Class, Type, or Enum. It is currently impossible to define unions of these core ranges.

The `linkml:Any` type is an experimental feature for allowing arbitrary objects

```yaml

classes:

  MetaObject:
    class_uri: linkml:Any

  ...

  Person:
   attributes:
     id:
     name:
     metadata:
       range: MetaObject
```

## Unions as ranges

[any_of](https://w3id.org/linkml/any_of) can be used to express that a range must satisfy any of a set of ranges.

One way this can be used is to compose enums together, for example if we have a `vital_status` enum that can take on any a set of enums from VitalStatus OR a missing value with the type of missing value defined by an enum:


```yaml
slots:
  vital_status:
    required: true
    any_of:
      - range: MissingValueEnum
      - range: VitalStatusEnum
enums:
  MissingValueEnum:
    permissible_values:
      INAPPLICABLE:
      NOT_COLLECTED:
      RESTRICTED:
      OTHER:
  VitalStatusEnum:
    permissible_values:
      LIVING:
      DEAD:
      UNDEAD:
```

Note that these constructs may ignored by some generators in the linkml 1.1 series.

In the 1.2 series:

- generated python should use a Union
- jsonschema should use [conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals.html)
- OWL should use UnionOf

## Rules

Any class can have a [rules](https://w3id.org/linkml/rules) block, consisting of (optional) [preconditions](https://w3id.org/linkml/preconditions) and [postconditions](https://w3id.org/linkml/postconditions). This can express basic if-then logic:

```
classes:
  Address:
    slots:
      - street_address
      - country
    rules:
      - preconditions:
          slot_conditions:
            country:
              any_of:
                - equals_string: USA
                - equals_string: USA_territory
        postconditions:
          slot_conditions:
            postal_code:
              pattern: "[0-9]{5}(-[0-9]{4})?"
            telephone:
              pattern: "^\\+1 "
        description: USA and territories must have a specific regex patern for postal codes and phone numbers
```

See above for implementation status

## Defining slots

A subset of slots for a class can be declared as [defining
slots](https://w3id.org/linkml/), indicating that membership of the
class can be inferred based on ranges of those slots

```yaml
classes:

  Interaction:
    slots:
      - subject
      - object

  ProteinProteinInteraction:
    is_a: Interaction
    slot_usage:
      subject:
        range: Protein
      object:
        range: Protein
    defining_slots:
      - subject
      - object
```

This indicates that if we have an interaction object `I`, and the subject and object slot values for `I` are both of type Protein, then `I` can be inferred to be of type ProteinProteinInteraction

When translating to OWL, this will make an equilance axiom:

```
ProteinProteinInteraction = Interaction and subject some Protein and object some Protein
```

And using an OWL reasoner will give the intended inferences.

This feature is experimental, and may be replaced by a more general rules mechanism in future.

