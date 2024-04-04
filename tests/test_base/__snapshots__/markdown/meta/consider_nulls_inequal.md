
# Slot: consider_nulls_inequal


By default, None values are considered equal for the purposes of comparisons in determining uniqueness. Set this to true to treat missing values as per ANSI-SQL NULLs, i.e NULL=NULL is always False.

URI: [linkml:consider_nulls_inequal](https://w3id.org/linkml/consider_nulls_inequal)


## Domain and Range

[UniqueKey](UniqueKey.md) &#8594;  <sub>0..1</sub> [Boolean](types/Boolean.md)

## Parents


## Children


## Used by

 * [UniqueKey](UniqueKey.md)
