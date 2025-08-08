
# Class: Relationship



URI: [personinfo:Relationship](https://w3id.org/linkml/examples/personinfo/Relationship)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Person]<related_to%200..1-%20[Relationship&#124;started_at_time:date%20%3F;ended_at_time:date%20%3F;type:string%20%3F],[Relationship]^-[InterPersonalRelationship],[Relationship]^-[FamilialRelationship],[Person],[InterPersonalRelationship],[FamilialRelationship])](https://yuml.me/diagram/nofunky;dir:TB/class/[Person]<related_to%200..1-%20[Relationship&#124;started_at_time:date%20%3F;ended_at_time:date%20%3F;type:string%20%3F],[Relationship]^-[InterPersonalRelationship],[Relationship]^-[FamilialRelationship],[Person],[InterPersonalRelationship],[FamilialRelationship])

## Children

 * [FamilialRelationship](FamilialRelationship.md)
 * [InterPersonalRelationship](InterPersonalRelationship.md)

## Referenced by Class


## Attributes


### Own

 * [started_at_time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended_at_time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [related_to](related_to.md)  <sub>0..1</sub>
     * Range: [Person](Person.md)
 * [type](type.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
