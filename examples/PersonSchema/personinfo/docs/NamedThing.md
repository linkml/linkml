
# Class: NamedThing

A generic grouping for any identifiable entity

URI: [personinfo:NamedThing](https://w3id.org/linkml/examples/personinfo/NamedThing)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Person],[Organization],[NamedThing&#124;id:uriorcurie;name:string;description:string%20%3F;depicted_by:ImageURL%20%3F]^-[Person],[NamedThing]^-[Organization],[NamedThing]^-[Concept],[Concept])](https://yuml.me/diagram/nofunky;dir:TB/class/[Person],[Organization],[NamedThing&#124;id:uriorcurie;name:string;description:string%20%3F;depicted_by:ImageURL%20%3F]^-[Person],[NamedThing]^-[Organization],[NamedThing]^-[Concept],[Concept])

## Children

 * [Concept](Concept.md)
 * [Organization](Organization.md) - An organization such as a company or university
 * [Person](Person.md) - A person (alive, dead, undead, or fictional).

## Referenced by Class


## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [name](name.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [depicted_by](depicted_by.md)  <sub>0..1</sub>
     * Range: [ImageURL](types/ImageURL.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Close Mappings:** | | schema:Thing |
