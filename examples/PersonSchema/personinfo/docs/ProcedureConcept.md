
# Class: ProcedureConcept



URI: [personinfo:ProcedureConcept](https://w3id.org/linkml/examples/personinfo/ProcedureConcept)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[CodeSystem],[MedicalEvent]++-%20procedure%200..1>[ProcedureConcept&#124;mappings(i):CrossReference%20*;id(i):uriorcurie;name(i):string;description(i):string%20%3F;depicted_by(i):ImageURL%20%3F],[ProcedureConcept]^-[OperationProcedureConcept],[ProcedureConcept]^-[ImagingProcedureConcept],[Concept]^-[ProcedureConcept],[OperationProcedureConcept],[MedicalEvent],[ImagingProcedureConcept],[Concept])](https://yuml.me/diagram/nofunky;dir:TB/class/[CodeSystem],[MedicalEvent]++-%20procedure%200..1>[ProcedureConcept&#124;mappings(i):CrossReference%20*;id(i):uriorcurie;name(i):string;description(i):string%20%3F;depicted_by(i):ImageURL%20%3F],[ProcedureConcept]^-[OperationProcedureConcept],[ProcedureConcept]^-[ImagingProcedureConcept],[Concept]^-[ProcedureConcept],[OperationProcedureConcept],[MedicalEvent],[ImagingProcedureConcept],[Concept])

## Parents

 *  is_a: [Concept](Concept.md)

## Children

 * [ImagingProcedureConcept](ImagingProcedureConcept.md)
 * [OperationProcedureConcept](OperationProcedureConcept.md)

## Referenced by Class

 *  **None** *[procedure](procedure.md)*  <sub>0..1</sub>  **[ProcedureConcept](ProcedureConcept.md)**

## Attributes


### Inherited from Concept:

 * [id](id.md)  <sub>1..1</sub>
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [name](name.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [depicted_by](depicted_by.md)  <sub>0..1</sub>
     * Range: [ImageURL](types/ImageURL.md)
 * [➞code system](concept__code_system.md)  <sub>0..1</sub>
     * Range: [CodeSystem](CodeSystem.md)
 * [➞mappings](concept__mappings.md)  <sub>0..\*</sub>
     * Range: [CrossReference](types/CrossReference.md)
