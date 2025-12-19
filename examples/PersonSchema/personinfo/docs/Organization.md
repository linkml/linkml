
# Class: Organization

An organization such as a company or university

URI: [personinfo:Organization](https://w3id.org/linkml/examples/personinfo/Organization)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Place],[Place]<founding%20location%200..1-%20[Organization&#124;mission_statement:string%20%3F;founding_date:string%20%3F;categories:OrganizationType%20*;score:decimal%20%3F;min_salary:SalaryType%20%3F;aliases:string%20*;id(i):uriorcurie;name(i):string;description(i):string%20%3F;depicted_by(i):ImageURL%20%3F],[EmploymentEvent]-%20employed_at%200..1>[Organization],[Container]++-%20organizations%200..*>[Organization],[Organization]uses%20-.->[HasAliases],[Organization]uses%20-.->[HasNewsEvents],[NamedThing]^-[Organization],[NewsEvent],[NamedThing],[HasNewsEvents],[HasAliases],[EmploymentEvent],[Container])](https://yuml.me/diagram/nofunky;dir:TB/class/[Place],[Place]<founding%20location%200..1-%20[Organization&#124;mission_statement:string%20%3F;founding_date:string%20%3F;categories:OrganizationType%20*;score:decimal%20%3F;min_salary:SalaryType%20%3F;aliases:string%20*;id(i):uriorcurie;name(i):string;description(i):string%20%3F;depicted_by(i):ImageURL%20%3F],[EmploymentEvent]-%20employed_at%200..1>[Organization],[Container]++-%20organizations%200..*>[Organization],[Organization]uses%20-.->[HasAliases],[Organization]uses%20-.->[HasNewsEvents],[NamedThing]^-[Organization],[NewsEvent],[NamedThing],[HasNewsEvents],[HasAliases],[EmploymentEvent],[Container])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - A generic grouping for any identifiable entity

## Uses Mixin

 *  mixin: [HasAliases](HasAliases.md) - A mixin applied to any class that can have aliases/alternateNames
 *  mixin: [HasNewsEvents](HasNewsEvents.md)

## Referenced by Class

 *  **None** *[employed_at](employed_at.md)*  <sub>0..1</sub>  **[Organization](Organization.md)**
 *  **None** *[organizations](organizations.md)*  <sub>0..\*</sub>  **[Organization](Organization.md)**

## Attributes


### Own

 * [mission_statement](mission_statement.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [founding_date](founding_date.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [founding location](founding_location.md)  <sub>0..1</sub>
     * Range: [Place](Place.md)
 * [Organization➞categories](Organization_categories.md)  <sub>0..\*</sub>
     * Range: [OrganizationType](OrganizationType.md)
 * [score](score.md)  <sub>0..1</sub>
     * Description: A score between 0 and 5, represented as a decimal
     * Range: [Decimal](types/Decimal.md)
 * [min_salary](min_salary.md)  <sub>0..1</sub>
     * Range: [SalaryType](types/SalaryType.md)

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
| **Mappings:** | | schema:Organization |
