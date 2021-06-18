
# Slot: object


connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.

URI: [biolink:object](https://w3id.org/biolink/vocab/object)


## Domain and Range

[Association](Association.md) &#8594;  <sub>1..1</sub> [NamedThing](NamedThing.md)

## Parents

 *  is_a: [association slot](association_slot.md)

## Children

 *  [anatomical entity to anatomical entity association➞object](anatomical_entity_to_anatomical_entity_association_object.md)
 *  [behavior to behavioral feature association➞object](behavior_to_behavioral_feature_association_object.md)
 *  [chemical to chemical association➞object](chemical_to_chemical_association_object.md)
 *  [chemical to disease or phenotypic feature association➞object](chemical_to_disease_or_phenotypic_feature_association_object.md)
 *  [chemical to gene association➞object](chemical_to_gene_association_object.md)
 *  [chemical to pathway association➞object](chemical_to_pathway_association_object.md)
 *  [contributor association➞object](contributor_association_object.md)
 *  [disease or phenotypic feature association to location association➞object](disease_or_phenotypic_feature_association_to_location_association_object.md)
 *  [disease or phenotypic feature to location association➞object](disease_or_phenotypic_feature_to_location_association_object.md)
 *  [drug to gene association➞object](drug_to_gene_association_object.md)
 *  [entity to disease association mixin➞object](entity_to_disease_association_mixin_object.md)
 *  [entity to disease or phenotypic feature association mixin➞object](entity_to_disease_or_phenotypic_feature_association_mixin_object.md)
 *  [entity to exposure event association mixin➞object](entity_to_exposure_event_association_mixin_object.md)
 *  [entity to outcome association mixin➞object](entity_to_outcome_association_mixin_object.md)
 *  [entity to phenotypic feature association mixin➞object](entity_to_phenotypic_feature_association_mixin_object.md)
 *  [functional association➞object](functional_association_object.md)
 *  [gene regulatory relationship➞object](gene_regulatory_relationship_object.md)
 *  [gene to expression site association➞object](gene_to_expression_site_association_object.md)
 *  [gene to gene association➞object](gene_to_gene_association_object.md)
 *  [genomic sequence localization➞object](genomic_sequence_localization_object.md)
 *  [genotype to disease association➞object](genotype_to_disease_association_object.md)
 *  [genotype to gene association➞object](genotype_to_gene_association_object.md)
 *  [genotype to genotype part association➞object](genotype_to_genotype_part_association_object.md)
 *  [genotype to variant association➞object](genotype_to_variant_association_object.md)
 *  [material sample derivation association➞object](material_sample_derivation_association_object.md)
 *  [organism taxon to environment association➞object](organism_taxon_to_environment_association_object.md)
 *  [organism taxon to organism taxon association➞object](organism_taxon_to_organism_taxon_association_object.md)
 *  [population to population association➞object](population_to_population_association_object.md)
 *  [sequence feature relationship➞object](sequence_feature_relationship_object.md)
 *  [sequence variant modulates treatment association➞object](sequence_variant_modulates_treatment_association_object.md)
 *  [variant to disease association➞object](variant_to_disease_association_object.md)
 *  [variant to gene association➞object](variant_to_gene_association_object.md)
 *  [variant to population association➞object](variant_to_population_association_object.md)

## Used by

 * [Association](Association.md)
 * [CaseToPhenotypicFeatureAssociation](CaseToPhenotypicFeatureAssociation.md)
 * [CellLineAsAModelOfDiseaseAssociation](CellLineAsAModelOfDiseaseAssociation.md)
 * [CellLineToDiseaseOrPhenotypicFeatureAssociation](CellLineToDiseaseOrPhenotypicFeatureAssociation.md)
 * [DiseaseToExposureEventAssociation](DiseaseToExposureEventAssociation.md)
 * [DiseaseToPhenotypicFeatureAssociation](DiseaseToPhenotypicFeatureAssociation.md)
 * [ExposureEventToOutcomeAssociation](ExposureEventToOutcomeAssociation.md)
 * [ExposureEventToPhenotypicFeatureAssociation](ExposureEventToPhenotypicFeatureAssociation.md)
 * [GeneAsAModelOfDiseaseAssociation](GeneAsAModelOfDiseaseAssociation.md)
 * [GeneHasVariantThatContributesToDiseaseAssociation](GeneHasVariantThatContributesToDiseaseAssociation.md)
 * [GeneToDiseaseAssociation](GeneToDiseaseAssociation.md)
 * [GeneToPhenotypicFeatureAssociation](GeneToPhenotypicFeatureAssociation.md)
 * [GenotypeToPhenotypicFeatureAssociation](GenotypeToPhenotypicFeatureAssociation.md)
 * [MaterialSampleToDiseaseOrPhenotypicFeatureAssociation](MaterialSampleToDiseaseOrPhenotypicFeatureAssociation.md)
 * [OrganismalEntityAsAModelOfDiseaseAssociation](OrganismalEntityAsAModelOfDiseaseAssociation.md)
 * [SequenceAssociation](SequenceAssociation.md)
 * [VariantToPhenotypicFeatureAssociation](VariantToPhenotypicFeatureAssociation.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | descriptor (ga4gh) |
|  | | node with incoming relationship (neo4j) |
| **Mappings:** | | rdf:object |
| **Exact Mappings:** | | owl:annotatedTarget |
|  | | OBAN:association_has_object |

