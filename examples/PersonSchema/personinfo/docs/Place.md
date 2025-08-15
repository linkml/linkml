
# Class: Place



URI: [personinfo:Place](https://w3id.org/linkml/examples/personinfo/Place)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Organization]-%20founding%20location%200..1>[Place&#124;id:uriorcurie;name:string;depicted_by:ImageURL%20%3F;aliases:string%20*],[WithLocation]-%20in_location%200..1>[Place],[Container]++-%20places%200..*>[Place],[Place]uses%20-.->[HasAliases],[WithLocation],[Organization],[HasAliases],[Container])](https://yuml.me/diagram/nofunky;dir:TB/class/[Organization]-%20founding%20location%200..1>[Place&#124;id:uriorcurie;name:string;depicted_by:ImageURL%20%3F;aliases:string%20*],[WithLocation]-%20in_location%200..1>[Place],[Container]++-%20places%200..*>[Place],[Place]uses%20-.->[HasAliases],[WithLocation],[Organization],[HasAliases],[Container])

## Uses Mixin

 *  mixin: [HasAliases](HasAliases.md) - A mixin applied to any class that can have aliases/alternateNames

## Referenced by Class

 *  **None** *[founding location](founding_location.md)*  <sub>0..1</sub>  **[Place](Place.md)**
 *  **None** *[in_location](in_location.md)*  <sub>0..1</sub>  **[Place](Place.md)**
 *  **None** *[places](places.md)*  <sub>0..\*</sub>  **[Place](Place.md)**

## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [name](name.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [depicted_by](depicted_by.md)  <sub>0..1</sub>
     * Range: [ImageURL](types/ImageURL.md)

### Mixed in from HasAliases:

 * [➞aliases](hasAliases__aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
