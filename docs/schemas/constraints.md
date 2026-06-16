# Adding constraints and rules

In addition to the basic [cardinality](/schemas/slots) constraints for slots, additional constraints can be specified

## Unique Keys

A class can have “unique keys”, which uniquely identify instances of that class within a certain scope.

Unless specified otherwise below, the uniqueness scope is that of the container (the multi-valued slot) that contains instances
of the identified class. That is, when a multi-valued slot has a range set to a class that has one or more “unique keys”, there
cannot be two instances with the same values for the keys throughout the entire list.

Unique keys are inherited: if a class defines a unique key, the unique key’s constraints automatically apply to all the
subclasses, if any.

There are two types of “unique keys”: “compound keys” and “singular keys”.

### Compound keys

Compound keys are defined through the [unique_keys](https://w3id.org/linkml/unique_keys) slot, which allows to list the set of
slots whose combined values must be unique for members of the class.

For example, a database of chemical entities may with to declare the tuple of atomic number and neutron number
as a unique key for an isotope:

```yaml
  ChemicalEntity:
    slots:
      - id
      - symbol
      - inchi
      - atomic_number
      - neutron_number
  ChemicalElement:
    is_a: ChemicalEntity

  Isotope:
    is_a: ChemicalEntity
    unique_keys:
      main:
        description: An isotope is uniquely identifier by atomic and neutron number
        unique_key_slots:
          - atomic_number
          - neutron_number
      symbol:
        description: An isotope is uniquely identifier by its symbol
        notes:
          - we could have opted to use a simple key slot here as this is not a compound key but this allows us to annotate the key
        unique_key_slots:
          - symbol
```

Note that a compound key may very well comprise only one slot (there is no obligation for the `unique_key_slots` to list more than
one slot). However, such a key would still be considered, as far as this documentation is concerned, a _compound_ key, to
distinguish it from a “singular unique key” (described below).

### Singular keys

“Singular keys” have the additional constraints, compared to “compound keys”, that:

- there can be only one such key in any given class;
- they are automatically _required_, even if the slot holding them is not explicitly marked as such.

Singular keys are required for [inlining as a dictionary](inlining.md).

There are two types of singular keys: “singular unique keys” and “identifiers“.

#### Singular unique keys

A “singular unique key” is defined by marking a slot with [`key: true`](https://w3id.org/linkml/key). The slot marked as such is
known as the “key slot” of the class that holds it.

Be mindful of the difference between a “singular unique key” and a “compound key” that happens to comprise only one slot!
Consider the following example:

```yaml
slots:
  name:

classes:
  Foo:
    slots:
      - name
    unique_keys:
      the_key:
        unique_key_slots:
          - name
```

which defines a _Foo_ class that has a “compound unique key” comprising only the `name` slot, and this one:

```yaml
slots:
  name:
    key: true

classes:
  Foo:
    slots:
      - name
```

which defines a _Foo_ class that has a “singular unique key” `name`.

The unicity constraints in both cases are the same (there cannot be two instances of _Foo_ with the same `name` within a given
list), but:

- only in the second form is the _Foo_ class eligible for [dict inlining](inlining.md);
- in the second form the `name` slot is implicitly required, even without `required: true` (and in fact trying to explicitly make
the slot optional with `required: false` would be ignored).

Or in other words, marking a slot with `key: true` is _not_ merely a syntactic sugar for a `unique_keys` definition with only
one slot!

#### Identifiers

An “identifier” is defined by marking a slot with [`identifier: true`](https://w3id.org/linkml/identifier). The slot marked as
such is known as the “identifier slot” of the class that holds it.

Identifiers have the additional constraint, compared to singular unique keys, that their value must be _globally_ unique (there
cannot be two instances with the same identifier anywhere). In other words, their uniqueness scope is global, instead of being
limited to an enclosing container.

The presence of an identifier is necessary to allow instances of a class to be _referenced_ rather than _inlined_.

(Note that, since (1) singular unique keys and identifiers are two subtypes of singular keys and (2) any given class can have
only one singular key, it naturally follows that a class can have _either_ a singular unique key _or_ an identifier, but not
both. Using simultaneously `key: true` and `identifier: true` on two slots of the same class is an error.)

## String serialization

A rule for generating the string value of a slot can be specified as a [string_serialization](https://w3id.org/linkml/string_serialization)

```yaml
classes:
  Person:
    attributes:
      first:
      last:
      full:
        string_serialization: "{first} {last}"
```

- Tools for performing missing value inference can then populate the `full` slot based on the other two slots
- Tools for performing validation can use this to check slot values
    - if all 3 slots are populated, missing value inference can be used to check for consistency
    - if only `full` is provided, then the string can be checked (e.g. by a regex) to ensure the syntax is consistent

See:

- [string_serialization](https://w3id.org/linkml/string_serialization) in the metamodel


## Patterns

The value of a slot can be constrained to conform to a particular string pattern using the [pattern](https://w3id.org/linkml/pattern) metaslot

Example:

```yaml
  slots:
     phone:
       pattern: "^[\\d\\(\\)\\-]+$"   ## regular expression

```


See:

- [pattern](https://w3id.org/linkml/pattern) in the metamodel


## Structured patterns

The [structured_pattern](https://w3id.org/linkml/structured_pattern) construct
allows you to provide patterns in a more structured way, and to *reuse* sub-patterns.

First you declare the patterns to be reused in the top level of your schema:

```yaml
settings:
  float: "\\d+[\\.\\d+]"
  unit: "\\S+"
  email: "\\S+@\\S+{\\.\\w}+"
```

You can then use this inside a structured pattern:

```yaml
  height:
    range: string
    structured_pattern:
      syntax: "{float} {unit.length}"
      interpolated: true
      partial_match: false
```

You can use [gen-linkml](../generators/linkml) to expand these into structured patterns

## Minimum and Maximum values

Any numeric value can have minimum and maximum values specified

 * [minimum_value](https://w3id.org/linkml/minimum_value)
 * [maximum_value](https://w3id.org/linkml/maximum_value)

## Expressions and other advanced features

The above describes the core constraint feature. See the [advanced features guide](advanced.md) for more on how
to write rules and expressions for more expressive constraints.
