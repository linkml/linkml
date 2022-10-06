
# Class: FamilialRelationship




URI: [personinfo:FamilialRelationship](https://w3id.org/linkml/examples/personinfo/FamilialRelationship)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Relationship],[Person],[Person]<related%20to%201..1-%20[FamilialRelationship&#124;type:FamilialRelationshipType;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;related_to(i):string%20%3F],[Person]++-%20has_familial_relationships%200..*>[FamilialRelationship],[Relationship]^-[FamilialRelationship])](https://yuml.me/diagram/nofunky;dir:TB/class/[Relationship],[Person],[Person]<related%20to%201..1-%20[FamilialRelationship&#124;type:FamilialRelationshipType;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;related_to(i):string%20%3F],[Person]++-%20has_familial_relationships%200..*>[FamilialRelationship],[Relationship]^-[FamilialRelationship])

## Parents

 *  is_a: [Relationship](Relationship.md)

## Referenced by Class

 *  **None** *[has_familial_relationships](has_familial_relationships.md)*  <sub>0..\*</sub>  **[FamilialRelationship](FamilialRelationship.md)**

## Attributes


### Own

 * [FamilialRelationship➞type](FamilialRelationship_type.md)  <sub>1..1</sub>
     * Range: [FamilialRelationshipType](FamilialRelationshipType.md)
 * [FamilialRelationship➞related to](FamilialRelationship_related_to.md)  <sub>1..1</sub>
     * Range: [Person](Person.md)

### Inherited from Relationship:

 * [started_at_time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended_at_time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [related_to](related_to.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
