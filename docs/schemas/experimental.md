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


