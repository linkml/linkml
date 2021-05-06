
# Class: Prefix


prefix URI tuple

URI: [linkml:Prefix](https://w3id.org/linkml/Prefix)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SchemaDefinition],[SchemaDefinition]++-%20prefixes%200..*>[Prefix&#124;prefix_prefix(pk):ncname;prefix_reference:uri])

## Referenced by class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[prefixes](prefixes.md)*  <sub>0..*</sub>
  **[Prefix](Prefix.md)**

## Attributes


### Own

 * [prefix_prefix](prefix_prefix.md)  <sub>REQ</sub>

     * Description: the nsname (sans ':' for a given prefix)
     * range: [Ncname](types/Ncname.md)
 * [prefix_reference](prefix_reference.md)  <sub>REQ</sub>

     * Description: A URI associated with a given prefix
     * range: [Uri](types/Uri.md)
