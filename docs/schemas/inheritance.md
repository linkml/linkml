# Inheritance

## Linking classes and slots with `is_a`

The [is_a](https://w3id.org/linkml/is_a) metamodel slot can be used to define a backbone hierarchy for your class. All inheritable metamodel slots are propagated down the is_a hierarchy.


```yaml
classes:
  NamedThing:
    slots:
      - id
      - name
      - description
      - image

  Person:
    is_a: NamedThing
    mixins:
      - HasAliases
    slots:
      - primary_email
      - birth_date
      - age_in_years
      - gender
      - current_address
      - has_employment_history
      - has_familial_relationships
      - has_medical_history
```

Here Person will inherit the four slots from NamedThing.

**Note**: Slots can also be organized in hierarchies using `is_a`.

## Abstract classes and slots

A model class (or slot) may be tagged with its [abstract](https://w3id.org/linkml/abstract) slot set to the boolean value `true`, to define whether it is abstract. This has comparable meaning to that in the computing science Object Oriented Paradigm: another class (or slot) can use the abstract class (or slot) as part of its inheritance hierarchy, but the abstract class itself _cannot_ be directly instantiated.


```yaml
classes:
  NamedThing:
    abstract: true
    slots:
      - id
      - name
      - description
      - image

```

This forces data providers to always provide a more specific class than the generic "`NamedThing`".

This also provides a very useful piece of metadata that can be used by tools that
present schemas to domain scientists and subject matter experts. Abstract classes can be filtered
from displays, with their properties "rolled down".

Some generators may choose to utilize abstract tags, e.g to mask generation of abstract classes.

**Note**: Slots can also be declared abstract.

See also:

 - the [wikipedia page on Abstract Types](https://en.wikipedia.org/wiki/Abstract_type)

## Mixin classes and slots

* The [mixin](https://w3id.org/linkml/mixin) boolean slot to declare a class as a mixin
* The [mixins](https://w3id.org/linkml/mixins) multivalued slot which specifies a range of mixin parents.

Mixin parents operate similarly to `is_a` parents, but they do not have the constraint of forming a tree.

Mixins can be extremely helpful in a number of ways: 1) to generalize a set
of attributes that can apply to classes in different parts of the class hierarchy, 2) reduce duplication of
shared attributes between classes that do not inherit from one another and 3) to prevent the sometimes confusing nature
of multiple inheritance noted in the [diamond problem](https://tinyurl.com/4zdw9tsb).


```yaml
classes:
  NamedThing:
    slots:
      - id
      - name
      - description
      - image

  Person:
    is_a: NamedThing
    mixins:
      - HasAliases
    slots:
      - primary_email
      - birth_date
      - age_in_years
      - gender
      - current_address
      - has_employment_history
      - has_familial_relationships
      - has_medical_history

  HasAliases:
    mixin: true
    slots:
      - aliases
```

Note that `is_a` has the characteristics of homeomorphicity: `is_a` **SHOULD** only connect either (1) two mixins (2) two non-mixin elements

See also the [Wikipedia page on mixins](https://en.wikipedia.org/wiki/Mixin)

## Materializing inherited slots

the [linkml generator](../generators/linkml) can be used with the
`--materialize-attributes` option to *materialize* all induced slots
as attributes. This is useful if you want to make a version of your
schema for distribution that frees the program that uses the schema
from the need to traverse hierarchies and implement propagation logic.

For example, if this option is used with the above schema, then the
Person class will have attributes from both NamedThing and Person
combined. Furthermore, if Person uses `slot_usage` (see next section)
to refine the meaning of a generic slot in the context of Person, then
these will be materialized for Person.
