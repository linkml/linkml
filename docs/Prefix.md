
# Class: Prefix


prefix URI tuple

URI: [meta:Prefix](https://w3id.org/linkml/meta/Prefix)


![img](images/Prefix.svg)

## Referenced by class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[prefixes](prefixes.md)*  <sub>0..*</sub>  **[Prefix](Prefix.md)**

## Attributes


### Own

 * [prefix_prefix](prefix_prefix.md)  <sub>REQ</sub>
     * Description: the nsname (sans ':' for a given prefix)
     * range: [Ncname](types/Ncname.md)
 * [prefix_reference](prefix_reference.md)  <sub>REQ</sub>
     * Description: A URI associated with a given prefix
     * range: [Uri](types/Uri.md)
