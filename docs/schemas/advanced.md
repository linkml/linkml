# Advanced features

The following language features are experimental, behavior is not guaranteed to stay consistent

## LinkML Any type

Most of the time in LinkML, the ranges of slots are "committed" to being one of the following:

- a class
- a type
- an enum

Note that even if you don't explicitly declare a range, the [default_range](https://w3id.org/linkml/default_range) is used,
(and the default value of default_range is `string`, reflecting the most common use case).

In some cases you want to make slots more flexible, for example to allow for arbitrary objects.

The `linkml:Any` states that the range of a slot can be any object. This isn't a builtin type, 
but any class in the schema can take on this roll be being declared as `linkml:Any` using `class_uri`:

```yaml

classes:

  Any:
    class_uri: linkml:Any

  ...

  Person:
   attributes:
     id:
     metadata:
       range: Any
```

This means all the following are valid:

```yaml
name: person with string metadata 
metadata: a string
```  

```yaml
name: person with an object as metadata
metadata:
  name: a string
  age: an integer
```  

```yaml
name: person with an integer
metadata: 42
```

## Boolean constraints

The following LinkML constructs can be used to express boolean constraints:

- [any_of](https://w3id.org/linkml/any_of)
- [all_of](https://w3id.org/linkml/all_of)
- [none_of](https://w3id.org/linkml/none_of)
- [exactly_one_of](https://w3id.org/linkml/exactly_one_of)

These can be applied at the class or slot level. The range of each of these is an array of *expressions*.

### Unions as ranges

[any_of](https://w3id.org/linkml/any_of) can be used to express that a range must satisfy any of a set of ranges.

One way this can be used is to compose enums together, for example if we have a `vital_status` enum\
that can take on any a set of enums from VitalStatus OR a missing value with the type of missing value defined by an enum:

```yaml
slots:
  vital_status:
    required: true
    range: Any
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

Note that the range of `vital_status` is declared as `Any`, which is further constrained by the `any_of` expression.

Currently, it is important to always have a range declaration (even if it is `Any`), because LinkML constraint semantics are
monotonic (i.e. new constraints can be specified but existing ones cannot be overridden - see [slots](slots.md) for more on this).
If this range declaration were not explicitly stated, then the `default_range` of string would be applied. 

In future, LinkML may allow limited forms of non-monotonicity around default ranges, see:

https://github.com/linkml/linkml/issues/1483

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
        description: USA and territories must have a specific regex pattern for postal codes and phone numbers
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

## equals_expression

[equals_expression](https://w3id.org/linkml/equals_expression) can be used
to specify that the value of a slot should be equal to an evaluable expression,
where that expression can contain other slot values as terms.

For example, a schema may allow two separate age slots for specifying
age in years or in months. `equals_expression` is used to specify one in terns
of another:

```yaml
slots:
  ...
  age_in_years:
    range: decimal
    minimum_value: 0
    maximum_value: 999
    equals_expression: "{age_in_months} / 12"
  age_in_months:
    range: decimal
    equals_expression: "{age_in_years} * 12"
  is_juvenile:
    range: boolean
    equals_expression: "{age_in_years} < 18"
```

The expression is specified using a simple subset of Python.
Slot names may be enclosed in curly braces - if any of the slot
values is None then the entire expression evaluates to None.

You can insert missing values by using the `--infer` option when
running `linkml-convert`.

Documentation of the expression language is available [here](../schemas/expression-language).

See the developer documentation on [inference](../developers/inference) for
details of how to use this in code.

## URI or CURIE as a range
In some cases, you may want to use a URI or CURIE as a range. To do this,
create a class with `class_uri` set to the URI or CURIE and use that class
as the range.
