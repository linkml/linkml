
# Class: FamilialRelationship




URI: [ks:FamilialRelationship](https://w3id.org/linkml/tests/kitchen_sink/FamilialRelationship)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Relationship],[Person],[Person]<related%20to%201..1-%20[FamilialRelationship&#124;type:FamilialRelationshipType;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F],[Person]++-%20has%20familial%20relationships%200..*>[FamilialRelationship],[Relationship]^-[FamilialRelationship])](https://yuml.me/diagram/nofunky;dir:TB/class/[Relationship],[Person],[Person]<related%20to%201..1-%20[FamilialRelationship&#124;type:FamilialRelationshipType;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F],[Person]++-%20has%20familial%20relationships%200..*>[FamilialRelationship],[Relationship]^-[FamilialRelationship])

## Parents

 *  is_a: [Relationship](Relationship.md)

## Referenced by Record

 *  **None** *[has familial relationships](has_familial_relationships.md)*  <sub>0..\*</sub>  **[FamilialRelationship](FamilialRelationship.md)**

## Attributes


### Own

 * [FamilialRelationship➞type](FamilialRelationship_type.md)  <sub>1..1</sub>
     * Range: [FamilialRelationshipType](FamilialRelationshipType.md)
 * [FamilialRelationship➞related to](FamilialRelationship_related_to.md)  <sub>1..1</sub>
     * Range: [Person](Person.md)

### Inherited from Relationship:

 * [started at time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](Date.md)
 * [ended at time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](Date.md)
