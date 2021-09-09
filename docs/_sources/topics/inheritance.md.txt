# Inheritance

## Inheritance Related Slots

### is_a

The `is_a` slot can be used to define a hierarchy for your Biolink Model class, mixin or slot where a new class, mixin or slot is defined as a subclass of another defined class, mixin or slot.


```yaml
gene:
  is_a: gene or gene product
```

Here we define that the entity class `gene` is a sub-class of `gene or gene product`. Note that `is_a` has the characteristics of homeomorphicity: `is_a` **SHOULD** only connect either (1) two mixins (2) two classes (3) two slots.

### abstract

A model class (or slot) may be tagged with its `abstract` slot set to the boolean value `true`, to define whether it is abstract. This has comparable meaning to that in the computing science Object Oriented Paradigm: another class (or slot) can use the abstract class (or slot) as part of its inheritance hierarchy, but the abstract class itself _cannot_ be directly instantiated.


```yaml
  cell line to thing association:
    is_a: association
    defining_slots:
      - subject
    abstract: true
    description: >-
      A relationship between a cell line and another entity
    slot_usage:
      subject:
        range: cell line
```

Here we define that the association class `cell line to thing association` is an abstract class. In this case, the class simply constrains its child subclasses to have a subject range of `biolink:CellLine`.


### mixin

The `mixin:true` demarkation is used to extend the properties (or slots) of a class, without changing its
position in the class hierarchy.  Mixins can be extremely helpful in a number of ways: 1) to generalize a set
of attributes that can apply to classes in different parts of the class hierarchy, 2) reduce duplication of
shared attributes between classes that do not inherit from one another and 3) to prevent the sometimes confusing nature
of multiple inheritance noted in the '[diamond problem]'(https://tinyurl.com/4zdw9tsb).

In general, while mixin slots and classes should not be directly instantiated, or used directly as a slot in a class,
KGs can use them as a substitute for multiple inheritance. For example, a KG might wish to determine what are the parents
of a certain class.  In this case, the KG should navigate a mixin used in a domain or range of a class or slot, as it 
would the "is_a" demarkation.  


```yaml
  thing with taxon:
    mixin: true
    description: >-
      A mixin that can be used on any entity with a taxon
    slots:
      - in taxon
```
Here we define the class `thing with taxon` as a mixin class with a slot `in taxon`.   

```yaml
  molecular entity:
    is_a: biological entity
    mixins:
      - thing with taxon
      - physical essence
      - ontology class
    aliases: ['bioentity']
```

In the class `molecular entity`, we use the `thing with taxon` mixin in order to add the 'in taxon' attribute (slot)
to the molecular entity class.  The other way to do this would be to duplicate the 'in taxon' attribute in every class
manually (duplicative), or have hierarchy/parent that had the `in taxon` slot (but this parent would be a sister-class to 
'named thing' as not all named-things are taxon based).  Mixins simplify modeling and should be used when necessary.


```yaml
  regulates:
    is_a: affects
    comments:
      - This is a grouping for process-process and entity-entity relations
    mixin: true
```

Here we define the slot `regulates` as a mixin slot. This slot can be used as a `mixin` by other slots. 

Mixins can also be hierarchical.  For example:
```yaml
  frequency qualifier mixin:
    mixin: true
    description: >-
      Qualifier for frequency type associations
    slots:
      - frequency qualifier

```

Here we define the mixin `frequency qualifier mixin` to hold the parent slot, `frequency qualifier.`  
The slot, `frequency qualifier` is then inherited by every class in the subsequent `is_a` hierarchy of 
`entity to feature or disease qualifiers mixin.`  The `frequency quantifier` mixin was created with similar 
intentions (favoring consistency in modeling similar domains), though its reuse is not as evident in the model yet. 

Mixins provide the means of reusing semantics, generally by the inclusion of specific property slots or 
other semantic constraint, in different classes or slots, without the need to tie slots to the 
hierarchy of the class itself.

```yaml
positively regulates:
    comments:
      - This is a grouping for positive process-process and entity-entity regulation.
    is_a: regulates
    inverse: positively regulated by
    mixin: true
    close_mappings:
      # This RTX contributed term is tagged as a inverse of this Biolink predicate
      - RO:0002336
    exact_mappings:
      - RO:0002213
    narrow_mappings:
      - CHEMBL.MECHANISM:activator
      - DGIdb:activator
      - RO:0004032
      - RO:0004034
      - RO:0002629
      - SEMMEDDB:augments
```
`positively regulates` is another example of a mixin.  In this case, a mixin is used to store meta data about a 
predicate or relationship between two entities at a general level.  Its subsequent children, inherit these definitions
and attributes, whether or not the parent mixin class has any slots.


###  mixins

The `mixins` slot can be used to specify a list of mixins that a class (or slot) can use to 
include the added semantics of the mixins.

The `mixins` are separate from the `is_a` hierarchy and the mixin classes do not contribute to a 
classes inheritance hierarchy.

```yaml
  individual organism:
    is_a: organismal entity
    mixins:
      - thing with taxon
```

Here we define an entity class `individual organism` that uses the mixin class `thing with taxon`. 
By virtue of the mixin, the class `individual organism` will have an `in taxon` slot in addition to 
all its own slots, its parent slots, and its ancestor slots.

