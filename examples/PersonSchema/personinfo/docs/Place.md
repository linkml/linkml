
# Class: Place




URI: [personinfo:Place](https://w3id.org/linkml/examples/personinfo/Place)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Organization]-%20founding_location%200..1>[Place&#124;id:string;name:string%20%3F;aliases:string%20*],[MedicalEvent]-%20in_location%200..1>[Place],[WithLocation]-%20in_location%200..1>[Place],[Place]uses%20-.->[HasAliases],[WithLocation],[Organization],[MedicalEvent],[HasAliases])](https://yuml.me/diagram/nofunky;dir:TB/class/[Organization]-%20founding_location%200..1>[Place&#124;id:string;name:string%20%3F;aliases:string%20*],[MedicalEvent]-%20in_location%200..1>[Place],[WithLocation]-%20in_location%200..1>[Place],[Place]uses%20-.->[HasAliases],[WithLocation],[Organization],[MedicalEvent],[HasAliases])

## Uses Mixin

 *  mixin: [HasAliases](HasAliases.md) - A mixin applied to any class that can have aliases/alternateNames

## Referenced by Class

 *  **None** *[founding_location](founding_location.md)*  <sub>0..1</sub>  **[Place](Place.md)**
 *  **None** *[in_location](in_location.md)*  <sub>0..1</sub>  **[Place](Place.md)**

## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [name](name.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

### Mixed in from HasAliases:

 * [➞aliases](hasAliases__aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
