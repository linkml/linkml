
# Class: GenotypeToEntityAssociationMixin




URI: [biolink:GenotypeToEntityAssociationMixin](https://w3id.org/biolink/vocab/GenotypeToEntityAssociationMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Genotype]<subject%201..1-%20[GenotypeToEntityAssociationMixin],[GenotypeToPhenotypicFeatureAssociation]uses%20-.->[GenotypeToEntityAssociationMixin],[GenotypeToDiseaseAssociation]uses%20-.->[GenotypeToEntityAssociationMixin],[GenotypeToPhenotypicFeatureAssociation],[GenotypeToDiseaseAssociation],[Genotype])

## Mixin for

 * [GenotypeToDiseaseAssociation](GenotypeToDiseaseAssociation.md) (mixin) 
 * [GenotypeToPhenotypicFeatureAssociation](GenotypeToPhenotypicFeatureAssociation.md) (mixin)  - Any association between one genotype and a phenotypic feature, where having the genotype confers the phenotype, either in isolation or through environment

## Referenced by class


## Attributes


### Own

 * [genotype to entity association mixin➞subject](genotype_to_entity_association_mixin_subject.md)  <sub>REQ</sub>
     * Description: genotype that is the subject of the association
     * range: [Genotype](Genotype.md)
