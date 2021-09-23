
# Class: Company




URI: [ks:Company](https://w3id.org/linkml/tests/kitchen_sink/Company)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Person],[Organization],[Person]<ceo%200..1-%20[Company&#124;id(i):string;name(i):string%20%3F;aliases(i):string%20*],[Dataset]++-%20companies%200..*>[Company],[EmploymentEvent]-%20employed%20at%200..1>[Company],[Organization]^-[Company],[EmploymentEvent],[Dataset])](https://yuml.me/diagram/nofunky;dir:TB/class/[Person],[Organization],[Person]<ceo%200..1-%20[Company&#124;id(i):string;name(i):string%20%3F;aliases(i):string%20*],[Dataset]++-%20companies%200..*>[Company],[EmploymentEvent]-%20employed%20at%200..1>[Company],[Organization]^-[Company],[EmploymentEvent],[Dataset])

## Parents

 *  is_a: [Organization](Organization.md)

## Referenced by Record

 *  **None** *[➞companies](dataset__companies.md)*  <sub>0..\*</sub>  **[Company](Company.md)**
 *  **None** *[employed at](employed_at.md)*  <sub>0..1</sub>  **[Company](Company.md)**

## Attributes


### Own

 * [➞ceo](company__ceo.md)  <sub>0..1</sub>
     * Range: [Person](Person.md)

### Inherited from Organization:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [String](String.md)
 * [name](name.md)  <sub>0..1</sub>
     * Range: [String](String.md)
