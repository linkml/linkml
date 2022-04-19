# Inheritance

## Linking classes and slots with is_a

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

## abstract classes and slots

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

This forces data providers to always provide a more specific class than the generic "NamedThing"

Some generators may also choose to utilize abstract tags, e.g to mask generation of abstract classes.

**Note**: Slots can also be declared abstract.


## mixin classes and slots

* The [mixin](https://w3id.org/linkml/mixin) boolean slot to declare a class as a mixin
* The [mixins](https://w3id.org/linkml/mixins) multiavlued slot which specifies a range of mixin parents.

Mixin parents operate similarly to is_a parents, but they do not have the constraint if forming a tree.

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



