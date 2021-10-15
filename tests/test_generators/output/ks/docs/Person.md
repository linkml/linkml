
# Class: Person


A person, living or dead

URI: [ks:Person](https://w3id.org/linkml/tests/kitchen_sink/Person)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[BirthEvent]<has%20birth%20event%200..1-++[Person&#124;id:string;name:string%20%3F;age_in_years:integer%20%3F;aliases:string%20*],[Address]<addresses%200..*-++[Person],[MedicalEvent]<has%20medical%20history%200..*-++[Person],[FamilialRelationship]<has%20familial%20relationships%200..*-++[Person],[EmploymentEvent]<has%20employment%20history%200..*-++[Person],[FamilialRelationship]-%20related%20to%201..1>[Person],[Company]-%20ceo%200..1>[Person],[Dataset]++-%20persons%200..*>[Person],[MarriageEvent]-%20married%20to%200..1>[Person],[Person]uses%20-.->[HasAliases],[MedicalEvent],[MarriageEvent],[HasAliases],[FamilialRelationship],[EmploymentEvent],[Dataset],[Company],[BirthEvent],[Address])](https://yuml.me/diagram/nofunky;dir:TB/class/[BirthEvent]<has%20birth%20event%200..1-++[Person&#124;id:string;name:string%20%3F;age_in_years:integer%20%3F;aliases:string%20*],[Address]<addresses%200..*-++[Person],[MedicalEvent]<has%20medical%20history%200..*-++[Person],[FamilialRelationship]<has%20familial%20relationships%200..*-++[Person],[EmploymentEvent]<has%20employment%20history%200..*-++[Person],[FamilialRelationship]-%20related%20to%201..1>[Person],[Company]-%20ceo%200..1>[Person],[Dataset]++-%20persons%200..*>[Person],[MarriageEvent]-%20married%20to%200..1>[Person],[Person]uses%20-.->[HasAliases],[MedicalEvent],[MarriageEvent],[HasAliases],[FamilialRelationship],[EmploymentEvent],[Dataset],[Company],[BirthEvent],[Address])

## Uses Mixin

 *  mixin: [HasAliases](HasAliases.md)

## Referenced by Class

 *  **[FamilialRelationship](FamilialRelationship.md)** *[FamilialRelationship➞related to](FamilialRelationship_related_to.md)*  <sub>1..1</sub>  **[Person](Person.md)**
 *  **None** *[➞ceo](company__ceo.md)*  <sub>0..1</sub>  **[Person](Person.md)**
 *  **None** *[➞persons](dataset__persons.md)*  <sub>0..\*</sub>  **[Person](Person.md)**
 *  **None** *[married to](married_to.md)*  <sub>0..1</sub>  **[Person](Person.md)**

## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [Person➞name](Person_name.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [has employment history](has_employment_history.md)  <sub>0..\*</sub>
     * Range: [EmploymentEvent](EmploymentEvent.md)
     * in subsets: (subset B)
 * [has familial relationships](has_familial_relationships.md)  <sub>0..\*</sub>
     * Range: [FamilialRelationship](FamilialRelationship.md)
     * in subsets: (subset B)
 * [has medical history](has_medical_history.md)  <sub>0..\*</sub>
     * Range: [MedicalEvent](MedicalEvent.md)
     * in subsets: (subset B)
 * [age in years](age_in_years.md)  <sub>0..1</sub>
     * Description: number of years since birth
     * Range: [Integer](types/Integer.md)
     * in subsets: (subset A,subset B)
 * [addresses](addresses.md)  <sub>0..\*</sub>
     * Range: [Address](Address.md)
 * [has birth event](has_birth_event.md)  <sub>0..1</sub>
     * Range: [BirthEvent](BirthEvent.md)

### Mixed in from HasAliases:

 * [➞aliases](hasAliases__aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | subset A |

