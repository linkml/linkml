# Metadata

### aliases

The `aliases` slot can be used to define a list of aliases for a Biolink Model class (or slot). This is useful for adding synonymous names to your class (or slot).


```yaml
gene:
  is_a: gene or gene product
  aliases:
    - locus
```

Here we define that the entity class `gene` has an alias `locus`.


### description

The `description` slot can be used to provide a human-readable description of a class (or slot).

```yaml
  genetically interacts with:
    is_a: interacts with
    description: >-
      holds between two genes whose phenotypic effects are dependent on each other in some way - such that their combined phenotypic effects are the result of some interaction between the activity of their gene products. Examples include epistasis and synthetic lethality.
    domain: gene
    range: gene
```

Here we define a human readable description that describes the predicate slot `genetically interacts with` and its purpose.


