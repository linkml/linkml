
# Class: prefix


prefix URI tuple

URI: [linkml:Prefix](https://w3id.org/linkml/Prefix)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SchemaDefinition],[SchemaDefinition]++-%20prefixes%200..*>[Prefix&#124;prefix_prefix(pk):ncname;prefix_reference:uri])](https://yuml.me/diagram/nofunky;dir:TB/class/[SchemaDefinition],[SchemaDefinition]++-%20prefixes%200..*>[Prefix&#124;prefix_prefix(pk):ncname;prefix_reference:uri])

## Referenced by Class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[prefixes](prefixes.md)*  <sub>0..\*</sub>  **[Prefix](Prefix.md)**

## Attributes


### Own

 * [prefix_prefix](prefix_prefix.md)  <sub>1..1</sub>
     * Description: the nsname (sans ':' for a given prefix)
     * Range: [Ncname](Ncname.md)
 * [prefix_reference](prefix_reference.md)  <sub>1..1</sub>
     * Description: A URI associated with a given prefix
     * Range: [Uri](Uri.md)
