
# Class: InterPersonalRelationship



URI: [personinfo:InterPersonalRelationship](https://w3id.org/linkml/examples/personinfo/InterPersonalRelationship)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Relationship],[Person],[Person]<related%20to%201..1-%20[InterPersonalRelationship&#124;type:string;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F],[Person]++-%20has_interpersonal_relationships%200..*>[InterPersonalRelationship],[Relationship]^-[InterPersonalRelationship])](https://yuml.me/diagram/nofunky;dir:TB/class/[Relationship],[Person],[Person]<related%20to%201..1-%20[InterPersonalRelationship&#124;type:string;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F],[Person]++-%20has_interpersonal_relationships%200..*>[InterPersonalRelationship],[Relationship]^-[InterPersonalRelationship])

## Parents

 *  is_a: [Relationship](Relationship.md)

## Referenced by Class

 *  **None** *[has_interpersonal_relationships](has_interpersonal_relationships.md)*  <sub>0..\*</sub>  **[InterPersonalRelationship](InterPersonalRelationship.md)**

## Attributes


### Own

 * [InterPersonalRelationship➞type](InterPersonalRelationship_type.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [InterPersonalRelationship➞related to](InterPersonalRelationship_related_to.md)  <sub>1..1</sub>
     * Range: [Person](Person.md)

### Inherited from Relationship:

 * [started_at_time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended_at_time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [related_to](related_to.md)  <sub>0..1</sub>
     * Range: [Person](Person.md)
