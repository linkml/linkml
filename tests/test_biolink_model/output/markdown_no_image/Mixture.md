
# Class: mixture


The physical combination of two or more molecular entities in which the identities are retained and are mixed in the form of solutions, suspensions and colloids.

URI: [biolink:Mixture](https://w3id.org/biolink/vocab/Mixture)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ChemicalSubstance]<has%20constituent%200..*-%20[Mixture],[ProcessedMaterial]uses%20-.->[Mixture],[Food]uses%20-.->[Mixture],[Drug]uses%20-.->[Mixture],[ComplexChemicalExposure]uses%20-.->[Mixture],[ProcessedMaterial],[Food],[Drug],[ComplexChemicalExposure],[ChemicalSubstance])](https://yuml.me/diagram/nofunky;dir:TB/class/[ChemicalSubstance]<has%20constituent%200..*-%20[Mixture],[ProcessedMaterial]uses%20-.->[Mixture],[Food]uses%20-.->[Mixture],[Drug]uses%20-.->[Mixture],[ComplexChemicalExposure]uses%20-.->[Mixture],[ProcessedMaterial],[Food],[Drug],[ComplexChemicalExposure],[ChemicalSubstance])

## Mixin for

 * [ComplexChemicalExposure](ComplexChemicalExposure.md) (mixin)  - A complex chemical exposure is an intake of a chemical mixture (e.g. gasoline), other than a drug.
 * [Drug](Drug.md) (mixin)  - A substance intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease
 * [Food](Food.md) (mixin)  - A substance consumed by a living organism as a source of nutrition
 * [ProcessedMaterial](ProcessedMaterial.md) (mixin)  - A chemical substance (often a mixture) processed for consumption for nutritional, medical or technical use.

## Referenced by Class


## Attributes


### Own

 * [has constituent](has_constituent.md)  <sub>0..\*</sub>
     * Description: one or more chemical substances within a mixture
     * Range: [ChemicalSubstance](ChemicalSubstance.md)
