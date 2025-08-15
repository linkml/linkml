
# Class: Person

A person (alive, dead, undead, or fictional).

URI: [personinfo:Person](https://w3id.org/linkml/examples/personinfo/Person)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MedicalEvent]<has_medical_history%200..*-++[Person&#124;primary_email:string%20%3F;birth_date:string%20%3F;age:integer%20%3F;gender:GenderType%20%3F;telephone:string%20%3F;aliases:string%20*;id(i):uriorcurie;name(i):string;description(i):string%20%3F;depicted_by(i):ImageURL%20%3F],[InterPersonalRelationship]<has_interpersonal_relationships%200..*-++[Person],[FamilialRelationship]<has_familial_relationships%200..*-++[Person],[EmploymentEvent]<has_employment_history%200..*-++[Person],[Address]<current_address%200..1-++[Person],[FamilialRelationship]-%20related%20to%201..1>[Person],[InterPersonalRelationship]-%20related%20to%201..1>[Person],[Container]++-%20persons%200..*>[Person],[Relationship]-%20related_to%200..1>[Person],[Person]uses%20-.->[HasAliases],[Person]uses%20-.->[HasNewsEvents],[NamedThing]^-[Person],[Relationship],[NewsEvent],[NamedThing],[MedicalEvent],[InterPersonalRelationship],[HasNewsEvents],[HasAliases],[FamilialRelationship],[EmploymentEvent],[Container],[Address])](https://yuml.me/diagram/nofunky;dir:TB/class/[MedicalEvent]<has_medical_history%200..*-++[Person&#124;primary_email:string%20%3F;birth_date:string%20%3F;age:integer%20%3F;gender:GenderType%20%3F;telephone:string%20%3F;aliases:string%20*;id(i):uriorcurie;name(i):string;description(i):string%20%3F;depicted_by(i):ImageURL%20%3F],[InterPersonalRelationship]<has_interpersonal_relationships%200..*-++[Person],[FamilialRelationship]<has_familial_relationships%200..*-++[Person],[EmploymentEvent]<has_employment_history%200..*-++[Person],[Address]<current_address%200..1-++[Person],[FamilialRelationship]-%20related%20to%201..1>[Person],[InterPersonalRelationship]-%20related%20to%201..1>[Person],[Container]++-%20persons%200..*>[Person],[Relationship]-%20related_to%200..1>[Person],[Person]uses%20-.->[HasAliases],[Person]uses%20-.->[HasNewsEvents],[NamedThing]^-[Person],[Relationship],[NewsEvent],[NamedThing],[MedicalEvent],[InterPersonalRelationship],[HasNewsEvents],[HasAliases],[FamilialRelationship],[EmploymentEvent],[Container],[Address])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - A generic grouping for any identifiable entity

## Uses Mixin

 *  mixin: [HasAliases](HasAliases.md) - A mixin applied to any class that can have aliases/alternateNames
 *  mixin: [HasNewsEvents](HasNewsEvents.md)

## Referenced by Class

 *  **[FamilialRelationship](FamilialRelationship.md)** *[FamilialRelationship➞related to](FamilialRelationship_related_to.md)*  <sub>1..1</sub>  **[Person](Person.md)**
 *  **[InterPersonalRelationship](InterPersonalRelationship.md)** *[InterPersonalRelationship➞related to](InterPersonalRelationship_related_to.md)*  <sub>1..1</sub>  **[Person](Person.md)**
 *  **None** *[persons](persons.md)*  <sub>0..\*</sub>  **[Person](Person.md)**
 *  **None** *[related to](related_to.md)*  <sub>1..1</sub>  **[Person](Person.md)**
 *  **None** *[related_to](related_to.md)*  <sub>0..1</sub>  **[Person](Person.md)**

## Attributes


### Own

 * [Person➞primary_email](Person_primary_email.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [birth_date](birth_date.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [Person➞age](Person_age_in_years.md)  <sub>0..1</sub>
     * Range: [Integer](types/Integer.md)
 * [gender](gender.md)  <sub>0..1</sub>
     * Range: [GenderType](GenderType.md)
 * [current_address](current_address.md)  <sub>0..1</sub>
     * Description: The address at which a person currently lives
     * Range: [Address](Address.md)
 * [Person➞telephone](Person_telephone.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [has_employment_history](has_employment_history.md)  <sub>0..\*</sub>
     * Range: [EmploymentEvent](EmploymentEvent.md)
 * [has_familial_relationships](has_familial_relationships.md)  <sub>0..\*</sub>
     * Range: [FamilialRelationship](FamilialRelationship.md)
 * [has_interpersonal_relationships](has_interpersonal_relationships.md)  <sub>0..\*</sub>
     * Range: [InterPersonalRelationship](InterPersonalRelationship.md)
 * [has_medical_history](has_medical_history.md)  <sub>0..\*</sub>
     * Range: [MedicalEvent](MedicalEvent.md)

### Inherited from NamedThing:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [name](name.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [depicted_by](depicted_by.md)  <sub>0..1</sub>
     * Range: [ImageURL](types/ImageURL.md)

### Mixed in from HasAliases:

 * [➞aliases](hasAliases__aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)

### Mixed in from HasNewsEvents:

 * [➞has_news_events](hasNewsEvents__has_news_events.md)  <sub>0..\*</sub>
     * Range: [NewsEvent](NewsEvent.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | schema:Person |
| **In Subsets:** | | basic_subset |
