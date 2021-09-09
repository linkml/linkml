# Slots

### slot_usage

The `slot_usage` slot can be used to specify how a particular slot ought to be used in a class.

This is useful for documenting what a particular slot means for instances of a particular class.


```yaml
  gene to gene association:
    aliases: ['molecular or genetic interaction']
    is_a: association
    defining_slots:
      - subject
      - object
    description: >-
      abstract parent class for different kinds of gene-gene or gene product to gene product relationships.
      Includes homology and interaction.
    slot_usage:
      subject:
        range: gene or gene product
        description: >-
          the subject gene in the association. If the relation is symmetric, subject vs object is arbitrary.
          We allow a gene product to stand as proxy for the gene or vice versa
      object:
        range: gene or gene product
        description: >-
          the object gene in the association. If the relation is symmetric, subject vs object is arbitrary.
          We allow a gene product to stand as proxy for the gene or vice versa
```

Here we document the association class `gene to gene association` with information on how the slot `subject` and `object` ought to be used to represent this association properly.

In the `slot_usage` section we define the range and provide a description for the slot `subject` and `object`.

### required

The `required` slot can be used to define whether a slot is required.

When a slot is declared as required, any class that uses that slot must have a value for that slot.

```yaml
  id:
    is_a: node property
    required: true
    domain: named thing
    mappings:
      - alliancegenome:primaryId
      - gff3:ID
      - gpi:DB_Object_ID
```

Here we define the property slot `id` as a required field for all instances of the entity class `named thing`.


## Slots Relating to Constraints on Slot Composition


### domain

The `domain` slot mimics the idea of `rdfs:domain` where you constrain the type of classes that a given Biolink Model slot can be a part of.


```yaml
  genetically interacts with:
    is_a: interacts with
    domain: gene
```

Here we define that the subject (source node) of the predicate slot `genetically interacts with` must be an instance of class `gene`.


### range

The `range` slot mimics the idea of `rdfs:range` where you can constrain the type of classes (or data types) a given Biolink Model slot can have as its value.

```yaml
  genetically interacts with:
    is_a: interacts with
    domain: gene
    range: gene
```

Here we define that both the subject (source node) and object (target node) of the predicate slot `genetically interacts with` must be instances of class `gene`.


### symmetric

The `symmetric` slot can be used to specify whether a Biolink Model predicate slot is symmetric in its semantics.

i.e. if `A -[r]-> B` and `r` is symmetric then one can infer `B -[r]-> A`


```yaml
  genetically interacts with:
    is_a: interacts with
    domain: gene
    range: gene
    in_subset:
      - translator_minimal
    symmetric: true
```

Here we define that the predicate slot `genetically interacts with` is symmetric.

**Note:** This property is not inherited by descendants of this predicate slot. You will have to explicitly define every predicate slot that should be considered as symmetric.


## Slots Relating Semantic Mappings and Anchoring to External Ontology

### symmetric

The `symmetric` slot can be used to specify whether a given predicate slot is symmetric.

```yaml
  interacts with:
    domain: named thing
    range: named thing
    description: >-
      holds between any two entities that directly or indirectly interact with each other
    is_a: related to
    in_subset:
      - translator_minimal
    symmetric: true
``` 

**Note:** The symmetric nature of the predicate is not inherited by descendants of the predicate.


### inverse

The `inverse` slot can be used to specify the inverse predicate of a given predicate slot relationship.

```yaml
  affects:
    is_a: related to
    description: >-
      describes an entity that has a direct affect on the state or quality
      of another existing entity. Use of the 'affects' predicate implies that
      the affected entity already exists, unlike predicates such as
      'affects risk for' and 'prevents, where the outcome is something
      that may or may not come to be.
    inverse: affected by
    in_subset:
      - translator_minimal
```
