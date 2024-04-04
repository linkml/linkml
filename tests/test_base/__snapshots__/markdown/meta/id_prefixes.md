
# Slot: id_prefixes


An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix

URI: [linkml:id_prefixes](https://w3id.org/linkml/id_prefixes)


## Domain and Range

[Element](Element.md) &#8594;  <sub>0..\*</sub> [Ncname](types/Ncname.md)

## Parents


## Children


## Used by

 * [ClassDefinition](ClassDefinition.md)
 * [Definition](Definition.md)
 * [Element](Element.md)
 * [EnumDefinition](EnumDefinition.md)
 * [SchemaDefinition](SchemaDefinition.md)
 * [SlotDefinition](SlotDefinition.md)
 * [SubsetDefinition](SubsetDefinition.md)
 * [TypeDefinition](TypeDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | Order of elements may be used to indicate priority order |
|  | | If identifiers are treated as CURIEs, then the CURIE must start with one of the indicated prefixes followed by `:` (_should_ start if the list is open) |
|  | | If identifiers are treated as URIs, then the URI string must start with the expanded for of the prefix (_should_ start if the list is open) |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
| **See also:** | | [https://github.com/linkml/linkml-model/issues/28](https://github.com/linkml/linkml-model/issues/28) |

