# Subsets

The `in_subset` slot can be used tag your class (or slot) to belong to a pre-defined subset.

The actual subset names are defined as part of the Schema definition.

```yaml
  genetically interacts with:
    is_a: interacts with
    domain: gene
    range: gene
    in_subset:
      - translator_minimal
```

Here we define the slot `genetically interacts with` as part of the `translator_minimal` subset.

You can restrict most generators to one subset with `--subset NAME`. The option keeps the subset's members and the
elements they need. See [generators](../generators/index).
