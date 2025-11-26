
# Class: Concept



URI: [personinfo:Concept](https://w3id.org/linkml/examples/personinfo/Concept)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[CodeSystem],[ProcedureConcept],[NamedThing],[DiagnosisConcept],[CodeSystem]<code%20system%200..1-%20[Concept&#124;mappings:CrossReference%20*;id(i):uriorcurie;name(i):string;description(i):string%20%3F;depicted_by(i):ImageURL%20%3F],[Concept]^-[ProcedureConcept],[Concept]^-[DiagnosisConcept],[NamedThing]^-[Concept])](https://yuml.me/diagram/nofunky;dir:TB/class/[CodeSystem],[ProcedureConcept],[NamedThing],[DiagnosisConcept],[CodeSystem]<code%20system%200..1-%20[Concept&#124;mappings:CrossReference%20*;id(i):uriorcurie;name(i):string;description(i):string%20%3F;depicted_by(i):ImageURL%20%3F],[Concept]^-[ProcedureConcept],[Concept]^-[DiagnosisConcept],[NamedThing]^-[Concept])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - A generic grouping for any identifiable entity

## Children

 * [DiagnosisConcept](DiagnosisConcept.md)
 * [ProcedureConcept](ProcedureConcept.md)

## Referenced by Class


## Attributes


### Own

 * [➞code system](concept__code_system.md)  <sub>0..1</sub>
     * Range: [CodeSystem](CodeSystem.md)
 * [➞mappings](concept__mappings.md)  <sub>0..\*</sub>
     * Range: [CrossReference](types/CrossReference.md)

### Inherited from NamedThing:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [name](name.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [depicted_by](depicted_by.md)  <sub>0..1</sub>
     * Range: [ImageURL](types/ImageURL.md)
