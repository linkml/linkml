
# Class: model to disease association mixin


This mixin is used for any association class for which the subject (source node) plays the role of a 'model', in that it recapitulates some features of the disease in a way that is useful for studying the disease outside a patient carrying the disease

URI: [biolink:ModelToDiseaseAssociationMixin](https://w3id.org/biolink/vocab/ModelToDiseaseAssociationMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing],[NamedThing]<subject%201..1-%20[ModelToDiseaseAssociationMixin&#124;predicate:predicate_type],[VariantAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[OrganismalEntityAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[GenotypeAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[GeneAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[CellLineAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[VariantAsAModelOfDiseaseAssociation],[OrganismalEntityAsAModelOfDiseaseAssociation],[GenotypeAsAModelOfDiseaseAssociation],[GeneAsAModelOfDiseaseAssociation],[CellLineAsAModelOfDiseaseAssociation])](https://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing],[NamedThing]<subject%201..1-%20[ModelToDiseaseAssociationMixin&#124;predicate:predicate_type],[VariantAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[OrganismalEntityAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[GenotypeAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[GeneAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[CellLineAsAModelOfDiseaseAssociation]uses%20-.->[ModelToDiseaseAssociationMixin],[VariantAsAModelOfDiseaseAssociation],[OrganismalEntityAsAModelOfDiseaseAssociation],[GenotypeAsAModelOfDiseaseAssociation],[GeneAsAModelOfDiseaseAssociation],[CellLineAsAModelOfDiseaseAssociation])

## Mixin for

 * [CellLineAsAModelOfDiseaseAssociation](CellLineAsAModelOfDiseaseAssociation.md) (mixin) 
 * [GeneAsAModelOfDiseaseAssociation](GeneAsAModelOfDiseaseAssociation.md) (mixin) 
 * [GenotypeAsAModelOfDiseaseAssociation](GenotypeAsAModelOfDiseaseAssociation.md) (mixin) 
 * [OrganismalEntityAsAModelOfDiseaseAssociation](OrganismalEntityAsAModelOfDiseaseAssociation.md) (mixin) 
 * [VariantAsAModelOfDiseaseAssociation](VariantAsAModelOfDiseaseAssociation.md) (mixin) 

## Referenced by Class


## Attributes


### Own

 * [model to disease association mixin➞subject](model_to_disease_association_mixin_subject.md)  <sub>1..1</sub>
     * Description: The entity that serves as the model of the disease. This may be an organism, a strain of organism, a genotype or variant that exhibits similar features, or a gene that when mutated exhibits features of the disease
     * Range: [NamedThing](NamedThing.md)
 * [model to disease association mixin➞predicate](model_to_disease_association_mixin_predicate.md)  <sub>1..1</sub>
     * Description: The relationship to the disease
     * Range: [PredicateType](types/PredicateType.md)
