
# Class: MacromolecularMachineToEntityAssociationMixin


an association which has a macromolecular machine mixin as a subject

URI: [biolink:MacromolecularMachineToEntityAssociationMixin](https://w3id.org/biolink/vocab/MacromolecularMachineToEntityAssociationMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing],[NamedThing]<subject%201..1-%20[MacromolecularMachineToEntityAssociationMixin],[MacromolecularMachineToMolecularActivityAssociation]uses%20-.->[MacromolecularMachineToEntityAssociationMixin],[MacromolecularMachineToCellularComponentAssociation]uses%20-.->[MacromolecularMachineToEntityAssociationMixin],[MacromolecularMachineToBiologicalProcessAssociation]uses%20-.->[MacromolecularMachineToEntityAssociationMixin],[MacromolecularMachineToMolecularActivityAssociation],[MacromolecularMachineToCellularComponentAssociation],[MacromolecularMachineToBiologicalProcessAssociation])

## Mixin for

 * [MacromolecularMachineToBiologicalProcessAssociation](MacromolecularMachineToBiologicalProcessAssociation.md) (mixin)  - A functional association between a macromolecular machine (gene, gene product or complex) and a biological process or pathway (as represented in the GO biological process branch), where the entity carries out some part of the process, regulates it, or acts upstream of it.
 * [MacromolecularMachineToCellularComponentAssociation](MacromolecularMachineToCellularComponentAssociation.md) (mixin)  - A functional association between a macromolecular machine (gene, gene product or complex) and a cellular component (as represented in the GO cellular component branch), where the entity carries out its function in the cellular component.
 * [MacromolecularMachineToMolecularActivityAssociation](MacromolecularMachineToMolecularActivityAssociation.md) (mixin)  - A functional association between a macromolecular machine (gene, gene product or complex) and a molecular activity (as represented in the GO molecular function branch), where the entity carries out the activity, or contributes to its execution.

## Referenced by class


## Attributes


### Own

 * [macromolecular machine to entity association mixin➞subject](macromolecular_machine_to_entity_association_mixin_subject.md)  <sub>REQ</sub>
     * range: [NamedThing](NamedThing.md)
