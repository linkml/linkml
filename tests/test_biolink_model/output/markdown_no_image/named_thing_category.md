
# Slot: category


Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}

URI: [biolink:named_thing_category](https://w3id.org/biolink/vocab/named_thing_category)


## Domain and Range

[NamedThing](NamedThing.md) &#8594;  <sub>1..\*</sub> [NamedThing](NamedThing.md)

## Parents

 *  is_a: [category](category.md)

## Children


## Used by

 * [RNAProduct](RNAProduct.md)
 * [RNAProductIsoform](RNAProductIsoform.md)
 * [Activity](Activity.md)
 * [AdministrativeEntity](AdministrativeEntity.md)
 * [Agent](Agent.md)
 * [AnatomicalEntity](AnatomicalEntity.md)
 * [Article](Article.md)
 * [Behavior](Behavior.md)
 * [BehavioralExposure](BehavioralExposure.md)
 * [BehavioralFeature](BehavioralFeature.md)
 * [BehavioralOutcome](BehavioralOutcome.md)
 * [BiologicalEntity](BiologicalEntity.md)
 * [BiologicalProcess](BiologicalProcess.md)
 * [BiologicalProcessOrActivity](BiologicalProcessOrActivity.md)
 * [BioticExposure](BioticExposure.md)
 * [Book](Book.md)
 * [BookChapter](BookChapter.md)
 * [Carbohydrate](Carbohydrate.md)
 * [Case](Case.md)
 * [Cell](Cell.md)
 * [CellLine](CellLine.md)
 * [CellularComponent](CellularComponent.md)
 * [ChemicalExposure](ChemicalExposure.md)
 * [ChemicalSubstance](ChemicalSubstance.md)
 * [ClinicalEntity](ClinicalEntity.md)
 * [ClinicalFinding](ClinicalFinding.md)
 * [ClinicalIntervention](ClinicalIntervention.md)
 * [ClinicalTrial](ClinicalTrial.md)
 * [CodingSequence](CodingSequence.md)
 * [Cohort](Cohort.md)
 * [ComplexChemicalExposure](ComplexChemicalExposure.md)
 * [ConfidenceLevel](ConfidenceLevel.md)
 * [Dataset](Dataset.md)
 * [DatasetDistribution](DatasetDistribution.md)
 * [DatasetSummary](DatasetSummary.md)
 * [DatasetVersion](DatasetVersion.md)
 * [Death](Death.md)
 * [Device](Device.md)
 * [Disease](Disease.md)
 * [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)
 * [DiseaseOrPhenotypicFeatureExposure](DiseaseOrPhenotypicFeatureExposure.md)
 * [DiseaseOrPhenotypicFeatureOutcome](DiseaseOrPhenotypicFeatureOutcome.md)
 * [Drug](Drug.md)
 * [DrugExposure](DrugExposure.md)
 * [DrugToGeneInteractionExposure](DrugToGeneInteractionExposure.md)
 * [EnvironmentalExposure](EnvironmentalExposure.md)
 * [EnvironmentalFeature](EnvironmentalFeature.md)
 * [EnvironmentalFoodContaminant](EnvironmentalFoodContaminant.md)
 * [EnvironmentalProcess](EnvironmentalProcess.md)
 * [EpidemiologicalOutcome](EpidemiologicalOutcome.md)
 * [EvidenceType](EvidenceType.md)
 * [Exon](Exon.md)
 * [Food](Food.md)
 * [FoodAdditive](FoodAdditive.md)
 * [FoodComponent](FoodComponent.md)
 * [Gene](Gene.md)
 * [GeneFamily](GeneFamily.md)
 * [Genome](Genome.md)
 * [GenomicBackgroundExposure](GenomicBackgroundExposure.md)
 * [GenomicEntity](GenomicEntity.md)
 * [Genotype](Genotype.md)
 * [GeographicExposure](GeographicExposure.md)
 * [GeographicLocation](GeographicLocation.md)
 * [GeographicLocationAtTime](GeographicLocationAtTime.md)
 * [GrossAnatomicalStructure](GrossAnatomicalStructure.md)
 * [Haplotype](Haplotype.md)
 * [Hospitalization](Hospitalization.md)
 * [HospitalizationOutcome](HospitalizationOutcome.md)
 * [IndividualOrganism](IndividualOrganism.md)
 * [InformationContentEntity](InformationContentEntity.md)
 * [LifeStage](LifeStage.md)
 * [Macronutrient](Macronutrient.md)
 * [MaterialSample](MaterialSample.md)
 * [Metabolite](Metabolite.md)
 * [MicroRNA](MicroRNA.md)
 * [Micronutrient](Micronutrient.md)
 * [MolecularActivity](MolecularActivity.md)
 * [MolecularEntity](MolecularEntity.md)
 * [MortalityOutcome](MortalityOutcome.md)
 * [NamedThing](NamedThing.md)
 * [NoncodingRNAProduct](NoncodingRNAProduct.md)
 * [Nutrient](Nutrient.md)
 * [OrganismTaxon](OrganismTaxon.md)
 * [OrganismalEntity](OrganismalEntity.md)
 * [PathologicalAnatomicalExposure](PathologicalAnatomicalExposure.md)
 * [PathologicalAnatomicalOutcome](PathologicalAnatomicalOutcome.md)
 * [PathologicalAnatomicalStructure](PathologicalAnatomicalStructure.md)
 * [PathologicalProcess](PathologicalProcess.md)
 * [PathologicalProcessExposure](PathologicalProcessExposure.md)
 * [PathologicalProcessOutcome](PathologicalProcessOutcome.md)
 * [Pathway](Pathway.md)
 * [Phenomenon](Phenomenon.md)
 * [PhenotypicFeature](PhenotypicFeature.md)
 * [PhysicalEntity](PhysicalEntity.md)
 * [PhysiologicalProcess](PhysiologicalProcess.md)
 * [PlanetaryEntity](PlanetaryEntity.md)
 * [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md)
 * [Procedure](Procedure.md)
 * [ProcessedMaterial](ProcessedMaterial.md)
 * [Protein](Protein.md)
 * [ProteinIsoform](ProteinIsoform.md)
 * [Publication](Publication.md)
 * [ReagentTargetedGene](ReagentTargetedGene.md)
 * [SequenceVariant](SequenceVariant.md)
 * [Serial](Serial.md)
 * [SiRNA](SiRNA.md)
 * [Snv](Snv.md)
 * [SocioeconomicExposure](SocioeconomicExposure.md)
 * [SocioeconomicOutcome](SocioeconomicOutcome.md)
 * [StudyPopulation](StudyPopulation.md)
 * [Transcript](Transcript.md)
 * [Treatment](Treatment.md)
 * [Vitamin](Vitamin.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | translator_minimal |

