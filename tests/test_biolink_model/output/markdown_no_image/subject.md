
# Slot: subject


connects an association to the subject of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.

URI: [biolink:subject](https://w3id.org/biolink/vocab/subject)


## Domain and Range

[Association](Association.md) &#8594;  <sub>1..1</sub> [NamedThing](NamedThing.md)

## Parents

 *  is_a: [association slot](association_slot.md)

## Children

 *  [anatomical entity to anatomical entity association➞subject](anatomical_entity_to_anatomical_entity_association_subject.md)
 *  [behavior to behavioral feature association➞subject](behavior_to_behavioral_feature_association_subject.md)
 *  [case to entity association mixin➞subject](case_to_entity_association_mixin_subject.md)
 *  [cell line to disease or phenotypic feature association➞subject](cell_line_to_disease_or_phenotypic_feature_association_subject.md)
 *  [cell line to entity association mixin➞subject](cell_line_to_entity_association_mixin_subject.md)
 *  [chemical to chemical derivation association➞subject](chemical_to_chemical_derivation_association_subject.md)
 *  [contributor association➞subject](contributor_association_subject.md)
 *  [disease or phenotypic feature to entity association mixin➞subject](disease_or_phenotypic_feature_to_entity_association_mixin_subject.md)
 *  [disease to entity association mixin➞subject](disease_to_entity_association_mixin_subject.md)
 *  [exposure event to entity association mixin➞subject](exposure_event_to_entity_association_mixin_subject.md)
 *  [exposure event to phenotypic feature association➞subject](exposure_event_to_phenotypic_feature_association_subject.md)
 *  [functional association➞subject](functional_association_subject.md)
 *  [gene regulatory relationship➞subject](gene_regulatory_relationship_subject.md)
 *  [gene to disease association➞subject](gene_to_disease_association_subject.md)
 *  [gene to entity association mixin➞subject](gene_to_entity_association_mixin_subject.md)
 *  [gene to expression site association➞subject](gene_to_expression_site_association_subject.md)
 *  [gene to gene association➞subject](gene_to_gene_association_subject.md)
 *  [gene to phenotypic feature association➞subject](gene_to_phenotypic_feature_association_subject.md)
 *  [genomic sequence localization➞subject](genomic_sequence_localization_subject.md)
 *  [genotype to disease association➞subject](genotype_to_disease_association_subject.md)
 *  [genotype to entity association mixin➞subject](genotype_to_entity_association_mixin_subject.md)
 *  [genotype to gene association➞subject](genotype_to_gene_association_subject.md)
 *  [genotype to genotype part association➞subject](genotype_to_genotype_part_association_subject.md)
 *  [genotype to phenotypic feature association➞subject](genotype_to_phenotypic_feature_association_subject.md)
 *  [genotype to variant association➞subject](genotype_to_variant_association_subject.md)
 *  [macromolecular machine to entity association mixin➞subject](macromolecular_machine_to_entity_association_mixin_subject.md)
 *  [material sample derivation association➞subject](material_sample_derivation_association_subject.md)
 *  [material sample to entity association mixin➞subject](material_sample_to_entity_association_mixin_subject.md)
 *  [model to disease association mixin➞subject](model_to_disease_association_mixin_subject.md)
 *  [molecular entity to entity association mixin➞subject](molecular_entity_to_entity_association_mixin_subject.md)
 *  [organism taxon to entity association➞subject](organism_taxon_to_entity_association_subject.md)
 *  [organism taxon to environment association➞subject](organism_taxon_to_environment_association_subject.md)
 *  [organism taxon to organism taxon association➞subject](organism_taxon_to_organism_taxon_association_subject.md)
 *  [organismal entity as a model of disease association➞subject](organismal_entity_as_a_model_of_disease_association_subject.md)
 *  [population to population association➞subject](population_to_population_association_subject.md)
 *  [sequence feature relationship➞subject](sequence_feature_relationship_subject.md)
 *  [sequence variant modulates treatment association➞subject](sequence_variant_modulates_treatment_association_subject.md)
 *  [variant to disease association➞subject](variant_to_disease_association_subject.md)
 *  [variant to entity association mixin➞subject](variant_to_entity_association_mixin_subject.md)
 *  [variant to phenotypic feature association➞subject](variant_to_phenotypic_feature_association_subject.md)
 *  [variant to population association➞subject](variant_to_population_association_subject.md)

## Used by

 * [Association](Association.md)
 * [CaseToPhenotypicFeatureAssociation](CaseToPhenotypicFeatureAssociation.md)
 * [ChemicalToChemicalAssociation](ChemicalToChemicalAssociation.md)
 * [ChemicalToDiseaseOrPhenotypicFeatureAssociation](ChemicalToDiseaseOrPhenotypicFeatureAssociation.md)
 * [ChemicalToGeneAssociation](ChemicalToGeneAssociation.md)
 * [ChemicalToPathwayAssociation](ChemicalToPathwayAssociation.md)
 * [DiseaseOrPhenotypicFeatureAssociationToLocationAssociation](DiseaseOrPhenotypicFeatureAssociationToLocationAssociation.md)
 * [DiseaseOrPhenotypicFeatureToLocationAssociation](DiseaseOrPhenotypicFeatureToLocationAssociation.md)
 * [DiseaseToExposureEventAssociation](DiseaseToExposureEventAssociation.md)
 * [DiseaseToPhenotypicFeatureAssociation](DiseaseToPhenotypicFeatureAssociation.md)
 * [DrugToGeneAssociation](DrugToGeneAssociation.md)
 * [ExposureEventToOutcomeAssociation](ExposureEventToOutcomeAssociation.md)
 * [MaterialSampleToDiseaseOrPhenotypicFeatureAssociation](MaterialSampleToDiseaseOrPhenotypicFeatureAssociation.md)
 * [SequenceAssociation](SequenceAssociation.md)
 * [VariantToGeneAssociation](VariantToGeneAssociation.md)
 * [VariantToGeneExpressionAssociation](VariantToGeneExpressionAssociation.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Local names:** | | annotation subject (ga4gh) |
|  | | node with outgoing relationship (neo4j) |
| **Mappings:** | | rdf:subject |
| **Exact Mappings:** | | owl:annotatedSource |
|  | | OBAN:association_has_subject |

