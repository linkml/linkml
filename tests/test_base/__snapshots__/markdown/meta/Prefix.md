
# Class: prefix


prefix URI tuple

URI: [linkml:Prefix](https://w3id.org/linkml/Prefix)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SchemaDefinition],[SchemaDefinition]++-%20prefixes%200..*>[Prefix&#124;prefix_prefix(pk):ncname;prefix_reference:uri])](https://yuml.me/diagram/nofunky;dir:TB/class/[SchemaDefinition],[SchemaDefinition]++-%20prefixes%200..*>[Prefix&#124;prefix_prefix(pk):ncname;prefix_reference:uri])

## Referenced by Class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[prefixes](prefixes.md)*  <sub>0..\*</sub>  **[Prefix](Prefix.md)**

## Attributes


### Own

 * [prefix_prefix](prefix_prefix.md)  <sub>1..1</sub>
     * Description: The prefix components of a prefix expansions. This is the part that appears before the colon in a CURIE.
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [prefix_reference](prefix_reference.md)  <sub>1..1</sub>
     * Description: The namespace to which a prefix expands to.
     * Range: [Uri](types/Uri.md)
     * in subsets: (SpecificationSubset,BasicSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |

