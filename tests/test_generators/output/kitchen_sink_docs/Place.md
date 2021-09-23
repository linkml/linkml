
# Class: Place




URI: [ks:Place](https://w3id.org/linkml/tests/kitchen_sink/Place)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[BirthEvent]-%20in%20location%200..1>[Place&#124;id:string;name:string%20%3F;aliases:string%20*],[MedicalEvent]-%20in%20location%200..1>[Place],[WithLocation]-%20in%20location%200..1>[Place],[Place]uses%20-.->[HasAliases],[WithLocation],[MedicalEvent],[HasAliases],[BirthEvent])](https://yuml.me/diagram/nofunky;dir:TB/class/[BirthEvent]-%20in%20location%200..1>[Place&#124;id:string;name:string%20%3F;aliases:string%20*],[MedicalEvent]-%20in%20location%200..1>[Place],[WithLocation]-%20in%20location%200..1>[Place],[Place]uses%20-.->[HasAliases],[WithLocation],[MedicalEvent],[HasAliases],[BirthEvent])

## Uses Trait

 *  mixin: [HasAliases](HasAliases.md)

## Referenced by Record

 *  **None** *[in location](in_location.md)*  <sub>0..1</sub>  **[Place](Place.md)**

## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Range: [String](String.md)
 * [name](name.md)  <sub>0..1</sub>
     * Range: [String](String.md)

### Mixed in from HasAliases:

 * [➞aliases](hasAliases__aliases.md)  <sub>0..\*</sub>
     * Range: [String](String.md)
