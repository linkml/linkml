
# Biolink-Model schema


Entity and association taxonomy and datamodel for life-sciences data


### Classes

 * [Annotation](Annotation.md) - Biolink Model root class for entity annotations.
     * [Attribute](Attribute.md) - A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age, crispiness. An environmental sample may have attributes such as depth, lat, long, material.
         * [BiologicalSex](BiologicalSex.md)
             * [GenotypicSex](GenotypicSex.md) - An attribute corresponding to the genotypic sex of the individual, based upon genotypic composition of sex chromosomes.
             * [PhenotypicSex](PhenotypicSex.md) - An attribute corresponding to the phenotypic sex of the individual, based upon the reproductive organs present.
         * [ClinicalAttribute](ClinicalAttribute.md) - Attributes relating to a clinical manifestation
             * [ClinicalCourse](ClinicalCourse.md) - The course a disease typically takes from its onset, progression in time, and eventual resolution or death of the affected individual
                 * [Onset](Onset.md) - The age group in which (disease) symptom manifestations appear
             * [ClinicalMeasurement](ClinicalMeasurement.md) - A clinical measurement is a special kind of attribute which results from a laboratory observation from a subject individual or sample. Measurements can be connected to their subject by the 'has attribute' slot.
             * [ClinicalModifier](ClinicalModifier.md) - Used to characterize and specify the phenotypic abnormalities defined in the phenotypic abnormality sub-ontology, with respect to severity, laterality, and other aspects
         * [OrganismAttribute](OrganismAttribute.md) - describes a characteristic of an organismal entity.
             * [Inheritance](Inheritance.md) - The pattern or 'mode' in which a particular genetic trait or disorder is passed from one generation to the next, e.g. autosomal dominant, autosomal recessive, etc.
             * [PhenotypicQuality](PhenotypicQuality.md) - A property of a phenotype
         * [SeverityValue](SeverityValue.md) - describes the severity of a phenotypic feature or disease
         * [SocioeconomicAttribute](SocioeconomicAttribute.md) - Attributes relating to a socioeconomic manifestation
         * [Zygosity](Zygosity.md)
     * [QuantityValue](QuantityValue.md) - A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric value
 * [Entity](Entity.md) - Root Biolink Model class for all things and informational relationships, real or imagined.
     * [Association](Association.md) - A typed association between two entities, supported by evidence
         * [AnatomicalEntityToAnatomicalEntityAssociation](AnatomicalEntityToAnatomicalEntityAssociation.md)
             * [AnatomicalEntityToAnatomicalEntityOntogenicAssociation](AnatomicalEntityToAnatomicalEntityOntogenicAssociation.md) - A relationship between two anatomical entities where the relationship is ontogenic, i.e. the two entities are related by development. A number of different relationship types can be used to specify the precise nature of the relationship.
             * [AnatomicalEntityToAnatomicalEntityPartOfAssociation](AnatomicalEntityToAnatomicalEntityPartOfAssociation.md) - A relationship between two anatomical entities where the relationship is mereological, i.e the two entities are related by parthood. This includes relationships between cellular components and cells, between cells and tissues, tissues and whole organisms
         * [BehaviorToBehavioralFeatureAssociation](BehaviorToBehavioralFeatureAssociation.md) - An association between an aggregate behavior and a behavioral feature manifested by the individual exhibited or has exhibited the behavior.
         * [CaseToPhenotypicFeatureAssociation](CaseToPhenotypicFeatureAssociation.md) - An association between a case (e.g. individual patient) and a phenotypic feature in which the individual has or has had the phenotype.
         * [CellLineToDiseaseOrPhenotypicFeatureAssociation](CellLineToDiseaseOrPhenotypicFeatureAssociation.md) - An relationship between a cell line and a disease or a phenotype, where the cell line is derived from an individual with that disease or phenotype.
             * [CellLineAsAModelOfDiseaseAssociation](CellLineAsAModelOfDiseaseAssociation.md)
         * [ChemicalToChemicalAssociation](ChemicalToChemicalAssociation.md) - A relationship between two chemical entities. This can encompass actual interactions as well as temporal causal edges, e.g. one chemical converted to another.
             * [ChemicalToChemicalDerivationAssociation](ChemicalToChemicalDerivationAssociation.md) - A causal relationship between two chemical entities, where the subject represents the upstream entity and the object represents the downstream. For any such association there is an implicit reaction:
         * [ChemicalToDiseaseOrPhenotypicFeatureAssociation](ChemicalToDiseaseOrPhenotypicFeatureAssociation.md) - An interaction between a chemical entity and a phenotype or disease, where the presence of the chemical gives rise to or exacerbates the phenotype.
         * [ChemicalToGeneAssociation](ChemicalToGeneAssociation.md) - An interaction between a chemical entity and a gene or gene product.
         * [ChemicalToPathwayAssociation](ChemicalToPathwayAssociation.md) - An interaction between a chemical entity and a biological process or pathway.
         * [ContributorAssociation](ContributorAssociation.md) - Any association between an entity (such as a publication) and various agents that contribute to its realisation
         * [DiseaseOrPhenotypicFeatureAssociationToLocationAssociation](DiseaseOrPhenotypicFeatureAssociationToLocationAssociation.md)
         * [DiseaseOrPhenotypicFeatureToLocationAssociation](DiseaseOrPhenotypicFeatureToLocationAssociation.md) - An association between either a disease or a phenotypic feature and an anatomical entity, where the disease/feature manifests in that site.
         * [DiseaseToExposureEventAssociation](DiseaseToExposureEventAssociation.md) - An association between an exposure event and a disease.
         * [DiseaseToPhenotypicFeatureAssociation](DiseaseToPhenotypicFeatureAssociation.md) - An association between a disease and a phenotypic feature in which the phenotypic feature is associated with the disease in some way.
         * [DrugToGeneAssociation](DrugToGeneAssociation.md) - An interaction between a drug and a gene or gene product.
         * [ExposureEventToOutcomeAssociation](ExposureEventToOutcomeAssociation.md) - An association between an exposure event and an outcome.
         * [ExposureEventToPhenotypicFeatureAssociation](ExposureEventToPhenotypicFeatureAssociation.md) - Any association between an environment and a phenotypic feature, where being in the environment influences the phenotype.
         * [FunctionalAssociation](FunctionalAssociation.md) - An association between a macromolecular machine mixin (gene, gene product or complex of gene products) and either a molecular activity, a biological process or a cellular location in which a function is executed.
             * [GeneToGoTermAssociation](GeneToGoTermAssociation.md)
             * [MacromolecularMachineToBiologicalProcessAssociation](MacromolecularMachineToBiologicalProcessAssociation.md) - A functional association between a macromolecular machine (gene, gene product or complex) and a biological process or pathway (as represented in the GO biological process branch), where the entity carries out some part of the process, regulates it, or acts upstream of it.
             * [MacromolecularMachineToCellularComponentAssociation](MacromolecularMachineToCellularComponentAssociation.md) - A functional association between a macromolecular machine (gene, gene product or complex) and a cellular component (as represented in the GO cellular component branch), where the entity carries out its function in the cellular component.
             * [MacromolecularMachineToMolecularActivityAssociation](MacromolecularMachineToMolecularActivityAssociation.md) - A functional association between a macromolecular machine (gene, gene product or complex) and a molecular activity (as represented in the GO molecular function branch), where the entity carries out the activity, or contributes to its execution.
         * [GeneRegulatoryRelationship](GeneRegulatoryRelationship.md) - A regulatory relationship between two genes
         * [GeneToDiseaseAssociation](GeneToDiseaseAssociation.md)
             * [GeneAsAModelOfDiseaseAssociation](GeneAsAModelOfDiseaseAssociation.md)
             * [GeneHasVariantThatContributesToDiseaseAssociation](GeneHasVariantThatContributesToDiseaseAssociation.md)
         * [GeneToExpressionSiteAssociation](GeneToExpressionSiteAssociation.md) - An association between a gene and an expression site, possibly qualified by stage/timing info.
         * [GeneToGeneAssociation](GeneToGeneAssociation.md) - abstract parent class for different kinds of gene-gene or gene product to gene product relationships. Includes homology and interaction.
             * [GeneToGeneCoexpressionAssociation](GeneToGeneCoexpressionAssociation.md) - Indicates that two genes are co-expressed, generally under the same conditions.
             * [GeneToGeneHomologyAssociation](GeneToGeneHomologyAssociation.md) - A homology association between two genes. May be orthology (in which case the species of subject and object should differ) or paralogy (in which case the species may be the same)
             * [PairwiseGeneToGeneInteraction](PairwiseGeneToGeneInteraction.md) - An interaction between two genes or two gene products. May be physical (e.g. protein binding) or genetic (between genes). May be symmetric (e.g. protein interaction) or directed (e.g. phosphorylation)
                 * [PairwiseMolecularInteraction](PairwiseMolecularInteraction.md) - An interaction at the molecular level between two physical entities
         * [GeneToPhenotypicFeatureAssociation](GeneToPhenotypicFeatureAssociation.md)
         * [GenotypeToDiseaseAssociation](GenotypeToDiseaseAssociation.md)
             * [GenotypeAsAModelOfDiseaseAssociation](GenotypeAsAModelOfDiseaseAssociation.md)
         * [GenotypeToGeneAssociation](GenotypeToGeneAssociation.md) - Any association between a genotype and a gene. The genotype have have multiple variants in that gene or a single one. There is no assumption of cardinality
         * [GenotypeToGenotypePartAssociation](GenotypeToGenotypePartAssociation.md) - Any association between one genotype and a genotypic entity that is a sub-component of it
         * [GenotypeToPhenotypicFeatureAssociation](GenotypeToPhenotypicFeatureAssociation.md) - Any association between one genotype and a phenotypic feature, where having the genotype confers the phenotype, either in isolation or through environment
         * [GenotypeToVariantAssociation](GenotypeToVariantAssociation.md) - Any association between a genotype and a sequence variant.
         * [MaterialSampleDerivationAssociation](MaterialSampleDerivationAssociation.md) - An association between a material sample and the material entity from which it is derived.
         * [MaterialSampleToDiseaseOrPhenotypicFeatureAssociation](MaterialSampleToDiseaseOrPhenotypicFeatureAssociation.md) - An association between a material sample and a disease or phenotype.
         * [OrganismTaxonToEnvironmentAssociation](OrganismTaxonToEnvironmentAssociation.md)
         * [OrganismTaxonToOrganismTaxonAssociation](OrganismTaxonToOrganismTaxonAssociation.md) - A relationship between two organism taxon nodes
             * [OrganismTaxonToOrganismTaxonInteraction](OrganismTaxonToOrganismTaxonInteraction.md) - An interaction relationship between two taxa. This may be a symbiotic relationship (encompassing mutualism and parasitism), or it may be non-symbiotic. Example: plague transmitted_by flea; cattle domesticated_by Homo sapiens; plague infects Homo sapiens
             * [OrganismTaxonToOrganismTaxonSpecialization](OrganismTaxonToOrganismTaxonSpecialization.md) - A child-parent relationship between two taxa. For example: Homo sapiens subclass_of Homo
         * [OrganismalEntityAsAModelOfDiseaseAssociation](OrganismalEntityAsAModelOfDiseaseAssociation.md)
         * [PopulationToPopulationAssociation](PopulationToPopulationAssociation.md) - An association between a two populations
         * [SequenceAssociation](SequenceAssociation.md) - An association between a sequence feature and a genomic entity it is localized to.
             * [GenomicSequenceLocalization](GenomicSequenceLocalization.md) - A relationship between a sequence feature and a genomic entity it is localized to. The reference entity may be a chromosome, chromosome region or information entity such as a contig.
         * [SequenceFeatureRelationship](SequenceFeatureRelationship.md) - For example, a particular exon is part of a particular transcript or gene
             * [ExonToTranscriptRelationship](ExonToTranscriptRelationship.md) - A transcript is formed from multiple exons
             * [GeneToGeneProductRelationship](GeneToGeneProductRelationship.md) - A gene is transcribed and potentially translated to a gene product
             * [TranscriptToGeneRelationship](TranscriptToGeneRelationship.md) - A gene is a collection of transcripts
         * [SequenceVariantModulatesTreatmentAssociation](SequenceVariantModulatesTreatmentAssociation.md) - An association between a sequence variant and a treatment or health intervention. The treatment object itself encompasses both the disease and the drug used.
         * [VariantToDiseaseAssociation](VariantToDiseaseAssociation.md)
             * [VariantAsAModelOfDiseaseAssociation](VariantAsAModelOfDiseaseAssociation.md)
         * [VariantToGeneAssociation](VariantToGeneAssociation.md) - An association between a variant and a gene, where the variant has a genetic association with the gene (i.e. is in linkage disequilibrium)
             * [VariantToGeneExpressionAssociation](VariantToGeneExpressionAssociation.md) - An association between a variant and expression of a gene (i.e. e-QTL)
         * [VariantToPhenotypicFeatureAssociation](VariantToPhenotypicFeatureAssociation.md)
         * [VariantToPopulationAssociation](VariantToPopulationAssociation.md) - An association between a variant and a population, where the variant has particular frequency in the population
     * [NamedThing](NamedThing.md) - a databased entity or concept/class
         * [Activity](Activity.md) - An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.
         * [AdministrativeEntity](AdministrativeEntity.md)
             * [Agent](Agent.md) - person, group, organization or project that provides a piece of information (i.e. a knowledge association)
         * [BiologicalEntity](BiologicalEntity.md)
             * [BiologicalProcessOrActivity](BiologicalProcessOrActivity.md) - Either an individual molecular activity, or a collection of causally connected molecular activities in a biological system.
                 * [BiologicalProcess](BiologicalProcess.md) - One or more causally connected executions of molecular functions
                     * [Behavior](Behavior.md)
                         * [BehavioralExposure](BehavioralExposure.md) - A behavioral exposure is a factor relating to behavior impacting an individual.
                         * [BehavioralOutcome](BehavioralOutcome.md) - An outcome resulting from an exposure event which is the manifestation of human behavior.
                         * [SocioeconomicExposure](SocioeconomicExposure.md) - A socioeconomic exposure is a factor relating to social and financial status of an affected individual (e.g. poverty).
                         * [SocioeconomicOutcome](SocioeconomicOutcome.md) - An general social or economic outcome, such as healthcare costs, utilization, etc., resulting from an exposure event
                     * [Death](Death.md)
                         * [MortalityOutcome](MortalityOutcome.md) - An outcome of death from resulting from an exposure event.
                     * [PathologicalProcess](PathologicalProcess.md) - A biologic function or a process having an abnormal or deleterious effect at the subcellular, cellular, multicellular, or organismal level.
                         * [PathologicalProcessExposure](PathologicalProcessExposure.md) - A pathological process, when viewed as an exposure, representing an precondition, leading to or influencing an outcome, e.g. autoimmunity leading to disease.
                         * [PathologicalProcessOutcome](PathologicalProcessOutcome.md) - An outcome resulting from an exposure event which is the manifestation of a pathological process.
                     * [Pathway](Pathway.md)
                     * [PhysiologicalProcess](PhysiologicalProcess.md)
                 * [MolecularActivity](MolecularActivity.md) - An execution of a molecular function carried out by a gene product or macromolecular complex.
             * [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md) - Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.
                 * [Disease](Disease.md)
                 * [DiseaseOrPhenotypicFeatureExposure](DiseaseOrPhenotypicFeatureExposure.md) - A disease or phenotypic feature state, when viewed as an exposure, represents an precondition, leading to or influencing an outcome, e.g. HIV predisposing an individual to infections; a relative deficiency of skin pigmentation predisposing an individual to skin cancer.
                 * [DiseaseOrPhenotypicFeatureOutcome](DiseaseOrPhenotypicFeatureOutcome.md) - Physiological outcomes resulting from an exposure event which is the manifestation of a disease or other characteristic phenotype.
                 * [PhenotypicFeature](PhenotypicFeature.md)
                     * [BehavioralFeature](BehavioralFeature.md) - A phenotypic feature which is behavioral in nature.
                     * [ClinicalFinding](ClinicalFinding.md) - this category is currently considered broad enough to tag clinical lab measurements and other biological attributes taken as 'clinical traits' with some statistical score, for example, a p value in genetic associations.
             * [EpidemiologicalOutcome](EpidemiologicalOutcome.md) - An epidemiological outcome, such as societal disease burden, resulting from an exposure event.
             * [MolecularEntity](MolecularEntity.md) - A gene, gene product, small molecule or macromolecule (including protein complex)"
                 * [ChemicalSubstance](ChemicalSubstance.md) - May be a chemical entity or a formulation with a chemical entity as active ingredient, or a complex material with multiple chemical entities as part
                     * [Carbohydrate](Carbohydrate.md)
                     * [ChemicalExposure](ChemicalExposure.md) - A chemical exposure is an intake of a particular chemical substance, other than a drug.
                         * [ComplexChemicalExposure](ComplexChemicalExposure.md) - A complex chemical exposure is an intake of a chemical mixture (e.g. gasoline), other than a drug.
                     * [EnvironmentalFoodContaminant](EnvironmentalFoodContaminant.md)
                     * [FoodAdditive](FoodAdditive.md)
                     * [FoodComponent](FoodComponent.md)
                     * [Metabolite](Metabolite.md) - Any intermediate or product resulting from metabolism. Includes primary and secondary metabolites.
                     * [Nutrient](Nutrient.md)
                         * [Macronutrient](Macronutrient.md)
                         * [Micronutrient](Micronutrient.md)
                             * [Vitamin](Vitamin.md)
                     * [ProcessedMaterial](ProcessedMaterial.md) - A chemical substance (often a mixture) processed for consumption for nutritional, medical or technical use.
                 * [Drug](Drug.md) - A substance intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease
                     * [DrugExposure](DrugExposure.md) - A drug exposure is an intake of a particular drug.
                         * [DrugToGeneInteractionExposure](DrugToGeneInteractionExposure.md) - drug to gene interaction exposure is a drug exposure is where the interactions of the drug with specific genes are known to constitute an 'exposure' to the organism, leading to or influencing an outcome.
                 * [Food](Food.md) - A substance consumed by a living organism as a source of nutrition
                 * [GeneFamily](GeneFamily.md) - any grouping of multiple genes or gene products related by common descent
                 * [GenomicEntity](GenomicEntity.md) - an entity that can either be directly located on a genome (gene, transcript, exon, regulatory region) or is encoded in a genome (protein)
                     * [CodingSequence](CodingSequence.md)
                     * [Exon](Exon.md) - A region of the transcript sequence within a gene which is not removed from the primary RNA transcript by RNA splicing.
                     * [Gene](Gene.md) - A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.
                     * [Genome](Genome.md) - A genome is the sum of genetic material within a cell or virion.
                     * [GenomicBackgroundExposure](GenomicBackgroundExposure.md) - A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing an outcome.
                     * [Genotype](Genotype.md) - An information content entity that describes a genome by specifying the total variation in genomic sequence and/or gene expression, relative to some established background
                     * [Haplotype](Haplotype.md) - A set of zero or more Alleles on a single instance of a Sequence[VMC]
                     * [Protein](Protein.md) - A gene product that is composed of a chain of amino acid sequences and is produced by ribosome-mediated translation of mRNA
                         * [ProteinIsoform](ProteinIsoform.md) - Represents a protein that is a specific isoform of the canonical or reference protein. See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4114032/
                     * [ReagentTargetedGene](ReagentTargetedGene.md) - A gene altered in its expression level in the context of some experiment as a result of being targeted by gene-knockdown reagent(s) such as a morpholino or RNAi.
                     * [SequenceVariant](SequenceVariant.md) - An allele that varies in its sequence from what is considered the reference allele at that locus.
                         * [Snv](Snv.md) - SNVs are single nucleotide positions in genomic DNA at which different sequence alternatives exist
                     * [Transcript](Transcript.md) - An RNA synthesized on a DNA or RNA template by an RNA polymerase.
                         * [RNAProduct](RNAProduct.md)
                             * [RNAProductIsoform](RNAProductIsoform.md) - Represents a protein that is a specific isoform of the canonical or reference RNA
                             * [NoncodingRNAProduct](NoncodingRNAProduct.md)
                                 * [MicroRNA](MicroRNA.md)
                                 * [SiRNA](SiRNA.md) - A small RNA molecule that is the product of a longer exogenous or endogenous dsRNA, which is either a bimolecular duplex or very long hairpin, processed (via the Dicer pathway) such that numerous siRNAs accumulate from both strands of the dsRNA. SRNAs trigger the cleavage of their target molecules.
             * [OrganismalEntity](OrganismalEntity.md) - A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding molecular entities
                 * [AnatomicalEntity](AnatomicalEntity.md) - A subcellular location, cell type or gross anatomical part
                     * [Cell](Cell.md)
                     * [CellularComponent](CellularComponent.md) - A location in or around a cell
                     * [GrossAnatomicalStructure](GrossAnatomicalStructure.md)
                     * [PathologicalAnatomicalStructure](PathologicalAnatomicalStructure.md) - An anatomical structure with the potential of have an abnormal or deleterious effect at the subcellular, cellular, multicellular, or organismal level.
                         * [PathologicalAnatomicalExposure](PathologicalAnatomicalExposure.md) - An abnormal anatomical structure, when viewed as an exposure, representing an precondition, leading to or influencing an outcome, e.g. thrombosis leading to an ischemic disease outcome.
                         * [PathologicalAnatomicalOutcome](PathologicalAnatomicalOutcome.md) - An outcome resulting from an exposure event which is the manifestation of an abnormal anatomical structure.
                 * [CellLine](CellLine.md)
                 * [IndividualOrganism](IndividualOrganism.md) - An instance of an organism. For example, Richard Nixon, Charles Darwin, my pet cat. Example ID: ORCID:0000-0002-5355-2576
                     * [Case](Case.md) - An individual (human) organism that has a patient role in some clinical context.
                 * [LifeStage](LifeStage.md) - A stage of development or growth of an organism, including post-natal adult stages
                 * [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md) - A collection of individuals from the same taxonomic class distinguished by one or more characteristics.  Characteristics can include, but are not limited to, shared geographic location, genetics, phenotypes [Alliance for Genome Resources]
                     * [StudyPopulation](StudyPopulation.md) - A group of people banded together or treated as a group as participants in a research study.
                         * [Cohort](Cohort.md) - A group of people banded together or treated as a group who share common characteristics. A cohort 'study' is a particular form of longitudinal study that samples a cohort, performing a cross-section at intervals through time.
         * [ClinicalEntity](ClinicalEntity.md) - Any entity or process that exists in the clinical domain and outside the biological realm. Diseases are placed under biological entities
             * [ClinicalIntervention](ClinicalIntervention.md)
                 * [Hospitalization](Hospitalization.md)
                     * [HospitalizationOutcome](HospitalizationOutcome.md) - An outcome resulting from an exposure event which is the increased manifestation of acute (e.g. emergency room visit) or chronic (inpatient) hospitalization.
             * [ClinicalTrial](ClinicalTrial.md)
         * [Device](Device.md) - A thing made or adapted for a particular purpose, especially a piece of mechanical or electronic equipment
         * [InformationContentEntity](InformationContentEntity.md) - a piece of information that typically describes some topic of discourse or is used as support.
             * [ConfidenceLevel](ConfidenceLevel.md) - Level of confidence in a statement
             * [Dataset](Dataset.md) - an item that refers to a collection of data from a data source.
             * [DatasetDistribution](DatasetDistribution.md) - an item that holds distribution level information about a dataset.
             * [DatasetSummary](DatasetSummary.md) - an item that holds summary level information about a dataset.
             * [DatasetVersion](DatasetVersion.md) - an item that holds version level information about a dataset.
             * [EvidenceType](EvidenceType.md) - Class of evidence that supports an association
             * [Publication](Publication.md) - Any published piece of information. Can refer to a whole publication, its encompassing publication (i.e. journal or book) or to a part of a publication, if of significant knowledge scope (e.g. a figure, figure legend, or section highlighted by NLP). The scope is intended to be general and include information published on the web, as well as printed materials, either directly or in one of the Publication Biolink category subclasses.
                 * [Article](Article.md)
                 * [Book](Book.md) - This class may rarely be instantiated except if use cases of a given knowledge graph support its utility.
                 * [BookChapter](BookChapter.md)
                 * [Serial](Serial.md) - This class may rarely be instantiated except if use cases of a given knowledge graph support its utility.
         * [OrganismTaxon](OrganismTaxon.md) - A classification of a set of organisms. Example instances: NCBITaxon:9606 (Homo sapiens), NCBITaxon:2 (Bacteria). Can also be used to represent strains or subspecies.
             * [BioticExposure](BioticExposure.md) - An external biotic exposure is an intake of (sometimes pathological) biological organisms (including viruses).
         * [Phenomenon](Phenomenon.md) - a fact or situation that is observed to exist or happen, especially one whose cause or explanation is in question
         * [PhysicalEntity](PhysicalEntity.md) - An entity that has material reality (a.k.a. physical essence).
             * [MaterialSample](MaterialSample.md) - A sample is a limited quantity of something (e.g. an individual or set of individuals from a population, or a portion of a substance) to be used for testing, analysis, inspection, investigation, demonstration, or trial use. [SIO]
         * [PlanetaryEntity](PlanetaryEntity.md) - Any entity or process that exists at the level of the whole planet
             * [EnvironmentalFeature](EnvironmentalFeature.md)
             * [EnvironmentalProcess](EnvironmentalProcess.md)
                 * [EnvironmentalExposure](EnvironmentalExposure.md) - A environmental exposure is a factor relating to abiotic processes in the environment including sunlight (UV-B), atmospheric (heat, cold, general pollution) and water-born contaminants.
             * [GeographicLocation](GeographicLocation.md) - a location that can be described in lat/long coordinates
                 * [GeographicExposure](GeographicExposure.md) - A geographic exposure is a factor relating to geographic proximity to some impactful entity.
                 * [GeographicLocationAtTime](GeographicLocationAtTime.md) - a location that can be described in lat/long coordinates, for a particular time
         * [Procedure](Procedure.md) - A series of actions conducted in a certain order or manner
         * [Treatment](Treatment.md) - A treatment is targeted at a disease or phenotype and may involve multiple drug 'exposures', medical devices and/or procedures

### Mixins

 * [ActivityAndBehavior](ActivityAndBehavior.md) - Activity or behavior of any independent integral living, organization or mechanical actor in the world
 * [CaseToEntityAssociationMixin](CaseToEntityAssociationMixin.md) - An abstract association for use where the case is the subject
 * [CellLineToEntityAssociationMixin](CellLineToEntityAssociationMixin.md) - An relationship between a cell line and another entity
 * [ChemicalOrDrugOrTreatment](ChemicalOrDrugOrTreatment.md)
 * [ChemicalToEntityAssociationMixin](ChemicalToEntityAssociationMixin.md) - An interaction between a chemical entity and another entity
 * [DiseaseOrPhenotypicFeatureToEntityAssociationMixin](DiseaseOrPhenotypicFeatureToEntityAssociationMixin.md)
 * [DiseaseToEntityAssociationMixin](DiseaseToEntityAssociationMixin.md)
 * [DrugToEntityAssociationMixin](DrugToEntityAssociationMixin.md) - An interaction between a drug and another entity
 * [EntityToDiseaseAssociationMixin](EntityToDiseaseAssociationMixin.md) - mixin class for any association whose object (target node) is a disease
 * [EntityToDiseaseOrPhenotypicFeatureAssociationMixin](EntityToDiseaseOrPhenotypicFeatureAssociationMixin.md)
 * [EntityToExposureEventAssociationMixin](EntityToExposureEventAssociationMixin.md) - An association between some entity and an exposure event.
 * [EntityToFeatureOrDiseaseQualifiersMixin](EntityToFeatureOrDiseaseQualifiersMixin.md) - Qualifiers for entity to disease or phenotype associations.
     * [EntityToDiseaseAssociationMixin](EntityToDiseaseAssociationMixin.md) - mixin class for any association whose object (target node) is a disease
     * [EntityToPhenotypicFeatureAssociationMixin](EntityToPhenotypicFeatureAssociationMixin.md)
 * [EntityToOutcomeAssociationMixin](EntityToOutcomeAssociationMixin.md) - An association between some entity and an outcome
 * [EntityToPhenotypicFeatureAssociationMixin](EntityToPhenotypicFeatureAssociationMixin.md)
 * [ExposureEvent](ExposureEvent.md) - A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more phenotypic features of that organism, potentially mediated by genes
 * [ExposureEventToEntityAssociationMixin](ExposureEventToEntityAssociationMixin.md) - An association between some exposure event and some entity.
 * [FrequencyQualifierMixin](FrequencyQualifierMixin.md) - Qualifier for frequency type associations
     * [EntityToFeatureOrDiseaseQualifiersMixin](EntityToFeatureOrDiseaseQualifiersMixin.md) - Qualifiers for entity to disease or phenotype associations.
         * [EntityToDiseaseAssociationMixin](EntityToDiseaseAssociationMixin.md) - mixin class for any association whose object (target node) is a disease
         * [EntityToPhenotypicFeatureAssociationMixin](EntityToPhenotypicFeatureAssociationMixin.md)
 * [FrequencyQuantifier](FrequencyQuantifier.md)
 * [GeneExpressionMixin](GeneExpressionMixin.md) - Observed gene expression intensity, context (site, stage) and associated phenotypic status within which the expression occurs.
 * [GeneGroupingMixin](GeneGroupingMixin.md) - any grouping of multiple genes or gene products
 * [GeneOntologyClass](GeneOntologyClass.md) - an ontology class that describes a functional aspect of a gene, gene prodoct or complex
 * [GeneOrGeneProduct](GeneOrGeneProduct.md) - A union of gene loci or gene products. Frequently an identifier for one will be used as proxy for another
     * [GeneProductMixin](GeneProductMixin.md) - The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.
         * [GeneProductIsoformMixin](GeneProductIsoformMixin.md) - This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene product is intended to represent a specific isoform rather than a canonical or reference or generic product. The designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.
 * [GeneProductIsoformMixin](GeneProductIsoformMixin.md) - This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene product is intended to represent a specific isoform rather than a canonical or reference or generic product. The designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.
 * [GeneProductMixin](GeneProductMixin.md) - The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.
     * [GeneProductIsoformMixin](GeneProductIsoformMixin.md) - This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene product is intended to represent a specific isoform rather than a canonical or reference or generic product. The designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.
 * [GeneToEntityAssociationMixin](GeneToEntityAssociationMixin.md)
 * [GenotypeToEntityAssociationMixin](GenotypeToEntityAssociationMixin.md)
 * [MacromolecularComplexMixin](MacromolecularComplexMixin.md) - A stable assembly of two or more macromolecules, i.e. proteins, nucleic acids, carbohydrates or lipids, in which at least one component is a protein and the constituent parts function together.
 * [MacromolecularMachineMixin](MacromolecularMachineMixin.md) - A union of gene locus, gene product, and macromolecular complex mixin. These are the basic units of function in a cell. They either carry out individual biological activities, or they encode molecules which do this.
     * [GeneOrGeneProduct](GeneOrGeneProduct.md) - A union of gene loci or gene products. Frequently an identifier for one will be used as proxy for another
         * [GeneProductMixin](GeneProductMixin.md) - The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.
             * [GeneProductIsoformMixin](GeneProductIsoformMixin.md) - This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene product is intended to represent a specific isoform rather than a canonical or reference or generic product. The designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.
     * [MacromolecularComplexMixin](MacromolecularComplexMixin.md) - A stable assembly of two or more macromolecules, i.e. proteins, nucleic acids, carbohydrates or lipids, in which at least one component is a protein and the constituent parts function together.
 * [MacromolecularMachineToEntityAssociationMixin](MacromolecularMachineToEntityAssociationMixin.md) - an association which has a macromolecular machine mixin as a subject
 * [MaterialSampleToEntityAssociationMixin](MaterialSampleToEntityAssociationMixin.md) - An association between a material sample and something.
 * [Mixture](Mixture.md) - The physical combination of two or more molecular entities in which the identities are retained and are mixed in the form of solutions, suspensions and colloids.
 * [ModelToDiseaseAssociationMixin](ModelToDiseaseAssociationMixin.md) - This mixin is used for any association class for which the subject (source node) plays the role of a 'model', in that it recapitulates some features of the disease in a way that is useful for studying the disease outside a patient carrying the disease
 * [MolecularEntityToEntityAssociationMixin](MolecularEntityToEntityAssociationMixin.md) - An interaction between a molecular entity and another entity
     * [ChemicalToEntityAssociationMixin](ChemicalToEntityAssociationMixin.md) - An interaction between a chemical entity and another entity
     * [DrugToEntityAssociationMixin](DrugToEntityAssociationMixin.md) - An interaction between a drug and another entity
 * [Occurrent](Occurrent.md) - A processual entity.
     * [ActivityAndBehavior](ActivityAndBehavior.md) - Activity or behavior of any independent integral living, organization or mechanical actor in the world
 * [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.
     * [GeneOntologyClass](GeneOntologyClass.md) - an ontology class that describes a functional aspect of a gene, gene prodoct or complex
     * [RelationshipType](RelationshipType.md) - An OWL property used as an edge label
     * [TaxonomicRank](TaxonomicRank.md) - A descriptor for the rank within a taxonomic classification. Example instance: TAXRANK:0000017 (kingdom)
     * [UnclassifiedOntologyClass](UnclassifiedOntologyClass.md) - this is used for nodes that are taken from an ontology but are not typed using an existing biolink class
 * [OrganismTaxonToEntityAssociation](OrganismTaxonToEntityAssociation.md) - An association between an organism taxon and another entity
 * [Outcome](Outcome.md) - An entity that has the role of being the consequence of an exposure event. This is an abstract mixin grouping of various categories of possible biological or non-biological (e.g. clinical) outcomes.
 * [PathognomonicityQuantifier](PathognomonicityQuantifier.md) - A relationship quantifier between a variant or symptom and a disease, which is high when the presence of the feature implies the existence of the disease
 * [PathologicalEntityMixin](PathologicalEntityMixin.md) - A pathological (abnormal) structure or process.
 * [PhysicalEssence](PhysicalEssence.md) - Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.
 * [PhysicalEssenceOrOccurrent](PhysicalEssenceOrOccurrent.md) - Either a physical or processual entity.
     * [Occurrent](Occurrent.md) - A processual entity.
         * [ActivityAndBehavior](ActivityAndBehavior.md) - Activity or behavior of any independent integral living, organization or mechanical actor in the world
     * [PhysicalEssence](PhysicalEssence.md) - Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.
 * [RelationshipQuantifier](RelationshipQuantifier.md)
     * [FrequencyQuantifier](FrequencyQuantifier.md)
     * [SensitivityQuantifier](SensitivityQuantifier.md)
     * [SpecificityQuantifier](SpecificityQuantifier.md)
         * [PathognomonicityQuantifier](PathognomonicityQuantifier.md) - A relationship quantifier between a variant or symptom and a disease, which is high when the presence of the feature implies the existence of the disease
 * [SensitivityQuantifier](SensitivityQuantifier.md)
 * [SpecificityQuantifier](SpecificityQuantifier.md)
     * [PathognomonicityQuantifier](PathognomonicityQuantifier.md) - A relationship quantifier between a variant or symptom and a disease, which is high when the presence of the feature implies the existence of the disease
 * [SubjectOfInvestigation](SubjectOfInvestigation.md) - An entity that has the role of being studied in an investigation, study, or experiment
 * [ThingWithTaxon](ThingWithTaxon.md) - A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms; genes, their products and other molecular entities; body parts; biological processes
 * [UnclassifiedOntologyClass](UnclassifiedOntologyClass.md) - this is used for nodes that are taken from an ontology but are not typed using an existing biolink class
 * [VariantToEntityAssociationMixin](VariantToEntityAssociationMixin.md)

### Slots

 * [association slot](association_slot.md) - any slot that relates an association to another entity
     * [associated environmental context](associated_environmental_context.md) - An attribute that can be applied to an association where the association holds between two entities located or occurring in a particular environment. For example, two microbial taxa may interact in the context of a human gut; a disease may give rise to a particular phenotype in a particular environmental exposure.
         * [organism taxon to organism taxon interaction➞associated environmental context](organism_taxon_to_organism_taxon_interaction_associated_environmental_context.md) - the environment in which the two taxa interact
     * [association type](association_type.md) - connects an association to the category of association (e.g. gene to phenotype)
     * [association➞id](association_id.md) - A unique identifier for an association
     * [catalyst qualifier](catalyst_qualifier.md) - a qualifier that connects an association between two causally connected entities (for example, two chemical entities, or a chemical entity in that changes location) and the gene product, gene, or complex that enables or catalyzes the change.
         * [chemical to chemical derivation association➞catalyst qualifier](chemical_to_chemical_derivation_association_catalyst_qualifier.md) - this connects the derivation edge to the molecular entity that catalyzes the reaction that causes the subject chemical to transform into the object chemical.
     * [chi squared statistic](chi_squared_statistic.md) - represents the chi-squared statistic computed from observations
     * [clinical modifier qualifier](clinical_modifier_qualifier.md) - Used to characterize and specify the phenotypic abnormalities defined in the Phenotypic abnormality subontology, with respect to severity, laterality, age of onset, and other aspects
     * [edge label](edge_label.md)
     * [expression site](expression_site.md) - location in which gene or protein expression takes place. May be cell, tissue, or organ.
     * [frequency qualifier](frequency_qualifier.md) - a qualifier used in a phenotypic association to state how frequent the phenotype is observed in the subject
     * [has confidence level](has_confidence_level.md) - connects an association to a qualitative term denoting the level of confidence
     * [has evidence](has_evidence.md) - connects an association to an instance of supporting evidence
     * [has population context](has_population_context.md) - a biological population (general, study, cohort, etc.) with a specific set of characteristics to constrain an association.
     * [has temporal context](has_temporal_context.md) - a constraint of time placed upon the truth value of an association.
     * [interacting molecules category](interacting_molecules_category.md)
     * [logical interpretation](logical_interpretation.md)
     * [negated](negated.md) - if set to true, then the association is negated i.e. is not true
     * [object](object.md) - connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
         * [anatomical entity to anatomical entity association➞object](anatomical_entity_to_anatomical_entity_association_object.md)
             * [anatomical entity to anatomical entity ontogenic association➞object](anatomical_entity_to_anatomical_entity_ontogenic_association_object.md) - the structure at an earlier time
             * [anatomical entity to anatomical entity part of association➞object](anatomical_entity_to_anatomical_entity_part_of_association_object.md) - the whole
         * [behavior to behavioral feature association➞object](behavior_to_behavioral_feature_association_object.md) - behavioral feature that is the object of the association
         * [chemical to chemical association➞object](chemical_to_chemical_association_object.md) - the chemical element that is the target of the statement
             * [chemical to chemical derivation association➞object](chemical_to_chemical_derivation_association_object.md) - the downstream chemical entity
         * [chemical to disease or phenotypic feature association➞object](chemical_to_disease_or_phenotypic_feature_association_object.md) - the disease or phenotype that is affected by the chemical
         * [chemical to gene association➞object](chemical_to_gene_association_object.md) - the gene or gene product that is affected by the chemical.
         * [chemical to pathway association➞object](chemical_to_pathway_association_object.md) - the pathway that is affected by the chemical
         * [contributor association➞object](contributor_association_object.md) - agent helping to realise the given entity (e.g. such as a publication)
         * [disease or phenotypic feature association to location association➞object](disease_or_phenotypic_feature_association_to_location_association_object.md)
         * [disease or phenotypic feature to location association➞object](disease_or_phenotypic_feature_to_location_association_object.md) - anatomical entity in which the disease or feature is found.
         * [drug to gene association➞object](drug_to_gene_association_object.md) - the gene or gene product that is affected by the drug
         * [entity to disease association mixin➞object](entity_to_disease_association_mixin_object.md) - disease
         * [entity to disease or phenotypic feature association mixin➞object](entity_to_disease_or_phenotypic_feature_association_mixin_object.md) - disease or phenotype
         * [entity to exposure event association mixin➞object](entity_to_exposure_event_association_mixin_object.md)
         * [entity to outcome association mixin➞object](entity_to_outcome_association_mixin_object.md)
         * [entity to phenotypic feature association mixin➞object](entity_to_phenotypic_feature_association_mixin_object.md) - phenotypic class
         * [functional association➞object](functional_association_object.md) - class describing the activity, process or localization of the gene product
             * [gene to go term association➞object](gene_to_go_term_association_object.md)
             * [macromolecular machine to biological process association➞object](macromolecular_machine_to_biological_process_association_object.md) - connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
             * [macromolecular machine to cellular component association➞object](macromolecular_machine_to_cellular_component_association_object.md) - connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
             * [macromolecular machine to molecular activity association➞object](macromolecular_machine_to_molecular_activity_association_object.md) - connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
         * [gene regulatory relationship➞object](gene_regulatory_relationship_object.md)
         * [gene to expression site association➞object](gene_to_expression_site_association_object.md) - location in which the gene is expressed
         * [gene to gene association➞object](gene_to_gene_association_object.md) - the object gene in the association. If the relation is symmetric, subject vs object is arbitrary. We allow a gene product to stand as a proxy for the gene or vice versa.
             * [pairwise molecular interaction➞object](pairwise_molecular_interaction_object.md) - connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
         * [genomic sequence localization➞object](genomic_sequence_localization_object.md)
         * [genotype to disease association➞object](genotype_to_disease_association_object.md) - a disease that is associated with that genotype
         * [genotype to gene association➞object](genotype_to_gene_association_object.md) - gene implicated in genotype
         * [genotype to genotype part association➞object](genotype_to_genotype_part_association_object.md) - child genotype
         * [genotype to variant association➞object](genotype_to_variant_association_object.md) - gene implicated in genotype
         * [material sample derivation association➞object](material_sample_derivation_association_object.md) - the material entity the sample was derived from. This may be another material sample, or any other material entity, including for example an organism, a geographic feature, or some environmental material.
         * [organism taxon to environment association➞object](organism_taxon_to_environment_association_object.md) - the environment in which the organism occurs
         * [organism taxon to organism taxon association➞object](organism_taxon_to_organism_taxon_association_object.md)
             * [organism taxon to organism taxon interaction➞object](organism_taxon_to_organism_taxon_interaction_object.md) - the taxon that is the subject of the association
             * [organism taxon to organism taxon specialization➞object](organism_taxon_to_organism_taxon_specialization_object.md) - the more general taxon
         * [population to population association➞object](population_to_population_association_object.md) - the population that form the object of the association
         * [sequence feature relationship➞object](sequence_feature_relationship_object.md)
             * [exon to transcript relationship➞object](exon_to_transcript_relationship_object.md)
             * [gene to gene product relationship➞object](gene_to_gene_product_relationship_object.md)
             * [transcript to gene relationship➞object](transcript_to_gene_relationship_object.md)
         * [sequence variant modulates treatment association➞object](sequence_variant_modulates_treatment_association_object.md) - treatment whose efficacy is modulated by the subject variant
         * [variant to disease association➞object](variant_to_disease_association_object.md) - a disease that is associated with that variant
         * [variant to gene association➞object](variant_to_gene_association_object.md)
         * [variant to population association➞object](variant_to_population_association_object.md) - the population that is observed to have the frequency
     * [onset qualifier](onset_qualifier.md) - a qualifier used in a phenotypic association to state when the phenotype appears is in the subject
     * [p value](p_value.md) - A quantitative confidence value that represents the probability of obtaining a result at least as extreme as that actually obtained, assuming that the actual value was the result of chance alone.
     * [phenotypic state](phenotypic_state.md) - in experiments (e.g. gene expression) assaying diseased or unhealthy tissue, the phenotypic state can be put here, e.g. MONDO ID. For healthy tissues, use XXX.
     * [predicate](predicate.md) - A high-level grouping for the relationship type. AKA minimal predicate. This is analogous to category for nodes.
         * [anatomical entity to anatomical entity ontogenic association➞predicate](anatomical_entity_to_anatomical_entity_ontogenic_association_predicate.md)
         * [anatomical entity to anatomical entity part of association➞predicate](anatomical_entity_to_anatomical_entity_part_of_association_predicate.md)
         * [chemical to chemical derivation association➞predicate](chemical_to_chemical_derivation_association_predicate.md)
         * [contributor association➞predicate](contributor_association_predicate.md) - generally one of the predicate values 'provider', 'publisher', 'editor' or 'author'
         * [gene regulatory relationship➞predicate](gene_regulatory_relationship_predicate.md) - the direction is always from regulator to regulated
         * [gene to expression site association➞predicate](gene_to_expression_site_association_predicate.md) - expression relationship
         * [gene to gene coexpression association➞predicate](gene_to_gene_coexpression_association_predicate.md)
         * [gene to gene homology association➞predicate](gene_to_gene_homology_association_predicate.md) - homology relationship type
         * [gene to gene product relationship➞predicate](gene_to_gene_product_relationship_predicate.md)
         * [genomic sequence localization➞predicate](genomic_sequence_localization_predicate.md)
         * [genotype to disease association➞predicate](genotype_to_disease_association_predicate.md) - E.g. is pathogenic for
         * [genotype to gene association➞predicate](genotype_to_gene_association_predicate.md) - the relationship type used to connect genotype to gene
         * [genotype to genotype part association➞predicate](genotype_to_genotype_part_association_predicate.md)
         * [genotype to phenotypic feature association➞predicate](genotype_to_phenotypic_feature_association_predicate.md)
         * [genotype to variant association➞predicate](genotype_to_variant_association_predicate.md) - the relationship type used to connect genotype to gene
         * [material sample derivation association➞predicate](material_sample_derivation_association_predicate.md) - derivation relationship
         * [model to disease association mixin➞predicate](model_to_disease_association_mixin_predicate.md) - The relationship to the disease
         * [organism taxon to environment association➞predicate](organism_taxon_to_environment_association_predicate.md) - predicate describing the relationship between the taxon and the environment
         * [organism taxon to organism taxon interaction➞predicate](organism_taxon_to_organism_taxon_interaction_predicate.md)
         * [organism taxon to organism taxon specialization➞predicate](organism_taxon_to_organism_taxon_specialization_predicate.md)
         * [pairwise gene to gene interaction➞predicate](pairwise_gene_to_gene_interaction_predicate.md)
             * [pairwise molecular interaction➞predicate](pairwise_molecular_interaction_predicate.md)
         * [population to population association➞predicate](population_to_population_association_predicate.md) - A relationship type that holds between the subject and object populations. Standard mereological relations can be used. E.g. subject part-of object, subject overlaps object. Derivation relationships can also be used
         * [variant to disease association➞predicate](variant_to_disease_association_predicate.md) - E.g. is pathogenic for
         * [variant to gene association➞predicate](variant_to_gene_association_predicate.md)
             * [variant to gene expression association➞predicate](variant_to_gene_expression_association_predicate.md)
     * [provided by](provided_by.md) - connects an association to the agent (person, organization or group) that provided it
     * [publications](publications.md) - connects an association to publications supporting the association
     * [qualifiers](qualifiers.md) - connects an association to qualifiers that modify or qualify the meaning of that association
         * [contributor association➞qualifiers](contributor_association_qualifiers.md) - this field can be used to annotate special characteristics of an agent relationship, such as the fact that a given author agent of a publication is the 'corresponding author'
     * [quantifier qualifier](quantifier_qualifier.md) - A measurable quantity for the object of the association
         * [gene expression mixin➞quantifier qualifier](gene_expression_mixin_quantifier_qualifier.md) - Optional quantitative value indicating degree of expression.
         * [gene to expression site association➞quantifier qualifier](gene_to_expression_site_association_quantifier_qualifier.md) - can be used to indicate magnitude, or also ranking
     * [relation](relation.md) - The relation which describes an association between a subject and an object in a more granular manner. Usually this is a term from Relation Ontology, but it can be any edge CURIE.
         * [pairwise gene to gene interaction➞relation](pairwise_gene_to_gene_interaction_relation.md) - interaction relationship type
             * [pairwise molecular interaction➞relation](pairwise_molecular_interaction_relation.md)
     * [sequence localization attribute](sequence_localization_attribute.md) - An attribute that can be applied to a genome sequence localization edge. These edges connect a genomic entity such as an exon to an entity such as a chromosome. Edge properties are used to ascribe specific positional information and other metadata to the localization. In pragmatic terms this can be thought of as columns in a GFF3 line.
         * [genome build](genome_build.md) - The version of the genome on which a feature is located. For example, GRCh38 for Homo sapiens.
         * [interbase coordinate](interbase_coordinate.md) - A position in interbase coordinates. This is applied to a sequence localization edge.
             * [end interbase coordinate](end_interbase_coordinate.md) - The position at which the subject genomic entity ends on the chromosome or other entity to which it is located on.
             * [start interbase coordinate](start_interbase_coordinate.md) - The position at which the subject genomic entity starts on the chromosome or other entity to which it is located on.
         * [phase](phase.md) - The phase for a coding sequence entity. For example, phase of a CDS as represented in a GFF3 with a value of 0, 1 or 2.
         * [strand](strand.md) - The strand on which a feature is located. Has a value of '+' (sense strand or forward strand) or '-' (anti-sense strand or reverse strand).
     * [sequence variant qualifier](sequence_variant_qualifier.md) - a qualifier used in an association with the variant
     * [severity qualifier](severity_qualifier.md) - a qualifier used in a phenotypic association to state how severe the phenotype is in the subject
     * [sex qualifier](sex_qualifier.md) - a qualifier used in a phenotypic association to state whether the association is specific to a particular sex.
     * [stage qualifier](stage_qualifier.md) - stage during which gene or protein expression of takes place.
         * [gene to expression site association➞stage qualifier](gene_to_expression_site_association_stage_qualifier.md) - stage at which the gene is expressed in the site
     * [subject](subject.md) - connects an association to the subject of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
         * [anatomical entity to anatomical entity association➞subject](anatomical_entity_to_anatomical_entity_association_subject.md)
             * [anatomical entity to anatomical entity ontogenic association➞subject](anatomical_entity_to_anatomical_entity_ontogenic_association_subject.md) - the structure at a later time
             * [anatomical entity to anatomical entity part of association➞subject](anatomical_entity_to_anatomical_entity_part_of_association_subject.md) - the part
         * [behavior to behavioral feature association➞subject](behavior_to_behavioral_feature_association_subject.md) - behavior that is the subject of the association
         * [case to entity association mixin➞subject](case_to_entity_association_mixin_subject.md) - the case (e.g. patient) that has the property
         * [cell line to disease or phenotypic feature association➞subject](cell_line_to_disease_or_phenotypic_feature_association_subject.md)
             * [cell line as a model of disease association➞subject](cell_line_as_a_model_of_disease_association_subject.md) - A cell line derived from an organismal entity with a disease state that is used as a model of that disease.
         * [cell line to entity association mixin➞subject](cell_line_to_entity_association_mixin_subject.md)
         * [chemical to chemical derivation association➞subject](chemical_to_chemical_derivation_association_subject.md) - the upstream chemical entity
         * [contributor association➞subject](contributor_association_subject.md) - information content entity which an agent has helped realise
         * [disease or phenotypic feature to entity association mixin➞subject](disease_or_phenotypic_feature_to_entity_association_mixin_subject.md) - disease or phenotype
         * [disease to entity association mixin➞subject](disease_to_entity_association_mixin_subject.md) - disease class
         * [exposure event to entity association mixin➞subject](exposure_event_to_entity_association_mixin_subject.md)
         * [exposure event to phenotypic feature association➞subject](exposure_event_to_phenotypic_feature_association_subject.md)
         * [functional association➞subject](functional_association_subject.md) - gene, product or macromolecular complex mixin that has the function associated with the GO term
             * [gene to go term association➞subject](gene_to_go_term_association_subject.md) - gene, product or macromolecular complex that has the function associated with the GO term
         * [gene regulatory relationship➞subject](gene_regulatory_relationship_subject.md)
         * [gene to disease association➞subject](gene_to_disease_association_subject.md) - gene in which variation is correlated with the disease, may be protective or causative or associative, or as a model
             * [gene as a model of disease association➞subject](gene_as_a_model_of_disease_association_subject.md) - A gene that has a role in modeling the disease. This may be a model organism ortholog of a known disease gene, or it may be a gene whose mutants recapitulate core features of the disease.
             * [gene has variant that contributes to disease association➞subject](gene_has_variant_that_contributes_to_disease_association_subject.md) - A gene that has a role in modeling the disease. This may be a model organism ortholog of a known disease gene, or it may be a gene whose mutants recapitulate core features of the disease.
         * [gene to entity association mixin➞subject](gene_to_entity_association_mixin_subject.md) - gene that is the subject of the association
         * [gene to expression site association➞subject](gene_to_expression_site_association_subject.md) - gene in which variation is correlated with the phenotypic feature
         * [gene to gene association➞subject](gene_to_gene_association_subject.md) - the subject gene in the association. If the relation is symmetric, subject vs object is arbitrary. We allow a gene product to stand as a proxy for the gene or vice versa.
             * [pairwise molecular interaction➞subject](pairwise_molecular_interaction_subject.md) - connects an association to the subject of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
         * [gene to phenotypic feature association➞subject](gene_to_phenotypic_feature_association_subject.md) - gene in which variation is correlated with the phenotypic feature
         * [genomic sequence localization➞subject](genomic_sequence_localization_subject.md)
         * [genotype to disease association➞subject](genotype_to_disease_association_subject.md) - a genotype that is associated in some way with a disease state
             * [genotype as a model of disease association➞subject](genotype_as_a_model_of_disease_association_subject.md) - A genotype that has a role in modeling the disease.
         * [genotype to entity association mixin➞subject](genotype_to_entity_association_mixin_subject.md) - genotype that is the subject of the association
         * [genotype to gene association➞subject](genotype_to_gene_association_subject.md) - parent genotype
         * [genotype to genotype part association➞subject](genotype_to_genotype_part_association_subject.md) - parent genotype
         * [genotype to phenotypic feature association➞subject](genotype_to_phenotypic_feature_association_subject.md) - genotype that is associated with the phenotypic feature
         * [genotype to variant association➞subject](genotype_to_variant_association_subject.md) - parent genotype
         * [macromolecular machine to entity association mixin➞subject](macromolecular_machine_to_entity_association_mixin_subject.md)
         * [material sample derivation association➞subject](material_sample_derivation_association_subject.md) - the material sample being described
         * [material sample to entity association mixin➞subject](material_sample_to_entity_association_mixin_subject.md) - the material sample being described
         * [model to disease association mixin➞subject](model_to_disease_association_mixin_subject.md) - The entity that serves as the model of the disease. This may be an organism, a strain of organism, a genotype or variant that exhibits similar features, or a gene that when mutated exhibits features of the disease
         * [molecular entity to entity association mixin➞subject](molecular_entity_to_entity_association_mixin_subject.md) - the molecular entity that is an interactor
             * [chemical to entity association mixin➞subject](chemical_to_entity_association_mixin_subject.md) - the chemical substance or entity that is an interactor
             * [drug to entity association mixin➞subject](drug_to_entity_association_mixin_subject.md) - the drug that is an interactor
         * [organism taxon to entity association➞subject](organism_taxon_to_entity_association_subject.md) - organism taxon that is the subject of the association
         * [organism taxon to environment association➞subject](organism_taxon_to_environment_association_subject.md) - the taxon that is the subject of the association
         * [organism taxon to organism taxon association➞subject](organism_taxon_to_organism_taxon_association_subject.md)
             * [organism taxon to organism taxon interaction➞subject](organism_taxon_to_organism_taxon_interaction_subject.md) - the taxon that is the subject of the association
             * [organism taxon to organism taxon specialization➞subject](organism_taxon_to_organism_taxon_specialization_subject.md) - the more specific taxon
         * [organismal entity as a model of disease association➞subject](organismal_entity_as_a_model_of_disease_association_subject.md) - A organismal entity (strain, breed) with a predisposition to a disease, or bred/created specifically to model a disease.
         * [population to population association➞subject](population_to_population_association_subject.md) - the population that form the subject of the association
         * [sequence feature relationship➞subject](sequence_feature_relationship_subject.md)
             * [exon to transcript relationship➞subject](exon_to_transcript_relationship_subject.md)
             * [gene to gene product relationship➞subject](gene_to_gene_product_relationship_subject.md)
             * [transcript to gene relationship➞subject](transcript_to_gene_relationship_subject.md)
         * [sequence variant modulates treatment association➞subject](sequence_variant_modulates_treatment_association_subject.md) - variant that modulates the treatment of some disease
         * [variant to disease association➞subject](variant_to_disease_association_subject.md) - a sequence variant in which the allele state is associated in some way with the disease state
             * [variant as a model of disease association➞subject](variant_as_a_model_of_disease_association_subject.md) - A variant that has a role in modeling the disease.
         * [variant to entity association mixin➞subject](variant_to_entity_association_mixin_subject.md) - a sequence variant in which the allele state is associated with some other entity
         * [variant to phenotypic feature association➞subject](variant_to_phenotypic_feature_association_subject.md) - a sequence variant in which the allele state is associated in some way with the phenotype state
         * [variant to population association➞subject](variant_to_population_association_subject.md) - an allele that has a certain frequency in a given population
 * [biological role mixin](biological_role_mixin.md) - A role played by the molecular entity or part thereof within a biological context.
 * [chemical role mixin](chemical_role_mixin.md) - A role played by the molecular entity or part thereof within a chemical context.
 * [description](description.md) - a human-readable description of an entity
     * [entity to phenotypic feature association mixin➞description](entity_to_phenotypic_feature_association_mixin_description.md) - A description of specific aspects of this phenotype, not otherwise covered by the phenotype ontology class
 * [has attribute](has_attribute.md) - connects any entity to an attribute
     * [clinical finding➞has attribute](clinical_finding_has_attribute.md)
     * [organismal entity➞has attribute](organismal_entity_has_attribute.md) - may often be an organism attribute
     * [socioeconomic exposure➞has attribute](socioeconomic_exposure_has_attribute.md)
 * [has attribute type](has_attribute_type.md) - connects an attribute to a class that describes it
     * [clinical measurement➞has attribute type](clinical_measurement_has_attribute_type.md)
 * [has numeric value](has_numeric_value.md) - connects a quantity value to a number
 * [has qualitative value](has_qualitative_value.md) - connects an attribute to a value
 * [has quantitative value](has_quantitative_value.md) - connects an attribute to a value
 * [has taxonomic rank](has_taxonomic_rank.md)
     * [organism taxon➞has taxonomic rank](organism_taxon_has_taxonomic_rank.md)
 * [has unit](has_unit.md) - connects a quantity value to a unit
 * [id](id.md) - A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * [agent➞id](agent_id.md) - Different classes of agents have distinct preferred identifiers. For publishers, use the ISBN publisher code. See https://grp.isbn-international.org/ for publisher code lookups. For editors, authors and  individual providers, use the individual's ORCID if available; Otherwise, a ScopusID, ResearchID or Google Scholar ID ('GSID') may be used if the author ORCID is unknown. Institutional agents could be identified by an International Standard Name Identifier ('ISNI') code.
     * [pairwise molecular interaction➞id](pairwise_molecular_interaction_id.md) - identifier for the interaction. This may come from an interaction database such as IMEX.
     * [publication➞id](publication_id.md) - Different kinds of publication subtypes will have different preferred identifiers (curies when feasible). Precedence of identifiers for scientific articles is as follows: PMID if available; DOI if not; actual alternate CURIE otherwise. Enclosing publications (i.e. referenced by 'published in' node property) such as books and journals, should have industry-standard identifier such as from ISBN and ISSN.
         * [book➞id](book_id.md) - Books should have industry-standard identifier such as from ISBN.
         * [serial➞id](serial_id.md) - Serials (journals) should have industry-standard identifier such as from ISSN.
     * [sequence variant➞id](sequence_variant_id.md)
 * [iri](iri.md) - An IRI for an entity. This is determined by the id using expansion rules.
 * [name](name.md) - A human-readable name for an attribute or entity.
     * [agent➞name](agent_name.md) - it is recommended that an author's 'name' property be formatted as "surname, firstname initial."
     * [attribute➞name](attribute_name.md) - The human-readable 'attribute name' can be set to a string which reflects its context of interpretation, e.g. SEPIO evidence/provenance/confidence annotation or it can default to the name associated with the 'has attribute type' slot ontology term.
     * [macromolecular machine mixin➞name](macromolecular_machine_mixin_name.md) - genes are typically designated by a short symbol and a full name. We map the symbol to the default display name and use an additional slot for full name
     * [publication➞name](publication_name.md) - the 'title' of the publication is generally recorded in the 'name' property (inherited from NamedThing). The field name 'title' is now also tagged as an acceptable alias for the node property 'name' (just in case).
 * [node property](node_property.md) - A grouping for any property that holds between a node and a value
     * [address](address.md) - the particulars of the place where someone or an organization is situated.  For now, this slot is a simple text "blob" containing all relevant details of the given location for fitness of purpose. For the moment, this "address" can include other contact details such as email and phone number(?).
     * [affiliation](affiliation.md) - a professional relationship between one provider (often a person) within another provider (often an organization). Target provider identity should be specified by a CURIE. Providers may have multiple affiliations.
     * [aggregate statistic](aggregate_statistic.md)
         * [has count](has_count.md) - number of things with a particular property
             * [variant to population association➞has count](variant_to_population_association_has_count.md) - number in object population that carry a particular allele, aka allele count
         * [has percentage](has_percentage.md) - equivalent to has quotient multiplied by 100
         * [has quotient](has_quotient.md)
             * [variant to population association➞has quotient](variant_to_population_association_has_quotient.md) - frequency of allele in population, expressed as a number with allele divided by number in reference population, aka allele frequency
         * [has total](has_total.md) - total number of things in a particular reference set
             * [variant to population association➞has total](variant_to_population_association_has_total.md) - number all populations that carry a particular allele, aka allele number
     * [authors](authors.md) - connects an publication to the list of authors who contributed to the publication. This property should be a comma-delimited list of author names. It is recommended that an author's name be formatted as "surname, firstname initial.".   Note that this property is a node annotation expressing the citation list of authorship which might typically otherwise be more completely documented in biolink:PublicationToProviderAssociation defined edges which point to full details about an author and possibly, some qualifiers which clarify the specific status of a given author in the publication.
     * [chapter](chapter.md) - chapter of a book
     * [created_with](created_with.md)
     * [creation date](creation_date.md) - date on which an entity was created. This can be applied to nodes or edges
     * [dataset download url](dataset_download_url.md)
     * [distribution download url](distribution_download_url.md)
     * [download url](download_url.md)
     * [filler](filler.md) - The value in a property-value tuple
     * [format](format.md)
     * [full name](full_name.md) - a long-form human readable name for a thing
     * [has biological sequence](has_biological_sequence.md) - connects a genomic feature to its sequence
         * [sequence variant➞has biological sequence](sequence_variant_has_biological_sequence.md) - The state of the sequence w.r.t a reference sequence
     * [has chemical formula](has_chemical_formula.md) - description of chemical compound based on element symbols
     * [has constituent](has_constituent.md) - one or more chemical substances within a mixture
     * [has dataset](has_dataset.md)
     * [has device](has_device.md) - connects an entity to one or more (medical) devices
     * [has distribution](has_distribution.md)
     * [has drug](has_drug.md) - connects an entity to one or more drugs
     * [has gene or gene product](has_gene_or_gene_product.md) - connects an entity with one or more gene or gene products
         * [has gene](has_gene.md) - connects an entity associated with one or more genes
             * [sequence variant➞has gene](sequence_variant_has_gene.md) - Each allele can be associated with any number of genes
     * [has procedure](has_procedure.md) - connects an entity to one or more (medical) procedures
     * [has receptor](has_receptor.md) - the organism or organism part being exposed
     * [has route](has_route.md) - the process that results in the stressor coming into direct contact with the receptor
     * [has stressor](has_stressor.md) - the process or entity that the receptor is being exposed to
     * [has topic](has_topic.md) - Connects a node to a vocabulary term or ontology class that describes some aspect of the entity. In general specific characterization is preferred. See https://github.com/biolink/biolink-model/issues/238
     * [has zygosity](has_zygosity.md)
     * [ingest date](ingest_date.md)
     * [is metabolite](is_metabolite.md) - indicates whether a chemical substance is a metabolite
     * [iso abbreviation](iso_abbreviation.md) - Standard abbreviation for periodicals in the International Organization for Standardization (ISO) 4 system See https://www.issn.org/services/online-services/access-to-the-ltwa/. If the 'published in' property is set, then the iso abbreviation pertains to the broader publication context (the journal) within which the given publication node is embedded, not the publication itself.
         * [article➞iso abbreviation](article_iso_abbreviation.md) - Optional value, if used locally as a convenience, is set to the iso abbreviation of the 'published in' parent.
     * [issue](issue.md) - issue of a newspaper, a scientific journal or magazine for reference purpose
     * [keywords](keywords.md) - keywords tagging a publication
     * [latitude](latitude.md) - latitude
     * [license](license.md)
     * [longitude](longitude.md) - longitude
     * [mesh terms](mesh_terms.md) - mesh terms tagging a publication
     * [pages](pages.md) - page number of source referenced for statement or publication
         * [publication➞pages](publication_pages.md) - When a 2-tuple of page numbers are provided, they represent the start and end page of the publication within its parent publication context. For books, this may be set to the total number of pages of the book.
     * [published in](published_in.md) - CURIE identifier of a broader publication context within which the publication may be placed, e.g. a specified book or journal.
         * [article➞published in](article_published_in.md) - The enclosing parent serial containing the article should have industry-standard identifier from ISSN.
         * [book chapter➞published in](book_chapter_published_in.md) - The enclosing parent book containing the chapter should have industry-standard identifier from ISBN.
     * [retrieved on](retrieved_on.md)
     * [rights](rights.md)
     * [source logo](source_logo.md)
     * [source web page](source_web_page.md)
     * [summary](summary.md) - executive  summary of a publication
     * [symbol](symbol.md) - Symbol for a particular thing
     * [synonym](synonym.md) - Alternate human-readable names for a thing
     * [systematic synonym](systematic_synonym.md) - more commonly used for gene symbols in yeast
     * [timepoint](timepoint.md) - a point in time
     * [update date](update_date.md) - date on which an entity was updated. This can be applied to nodes or edges
     * [version](version.md)
     * [version of](version_of.md)
     * [volume](volume.md) - volume of a book or music release in a collection/series or a published collection of journal issues in a serial publication
     * [xref](xref.md) - Alternate CURIEs for a thing
 * [regulated by](regulated_by.md)
     * [negatively regulated by](negatively_regulated_by.md)
     * [positively regulated by](positively_regulated_by.md)
 * [regulates](regulates.md)
     * [negatively regulates](negatively_regulates.md)
     * [positively regulates](positively_regulates.md)
 * [related to](related_to.md) - A relationship that is asserted between two named things
     * [affected by](affected_by.md) - describes an entity of which the state or quality is affected by another existing entity.
         * [disrupted by](disrupted_by.md) - describes a relationship where the structure, function, or occurrence of one entity is degraded or interfered with by another.
         * [entity regulated by entity](entity_regulated_by_entity.md)
             * [entity negatively regulated by entity](entity_negatively_regulated_by_entity.md)
             * [entity positively regulated by entity](entity_positively_regulated_by_entity.md)
         * [process regulated by process](process_regulated_by_process.md)
             * [process negatively regulated by process](process_negatively_regulated_by_process.md)
             * [process positively regulated by process](process_positively_regulated_by_process.md)
     * [affects](affects.md) - describes an entity that has a direct affect on the state or quality of another existing entity. Use of the 'affects' predicate implies that the affected entity already exists, unlike predicates such as 'affects risk for' and 'prevents, where the outcome is something that may or may not come to be.
         * [affects abundance of](affects_abundance_of.md) - holds between two molecular entities where the action or effect of one changes the amount of the other within a system of interest
             * [decreases abundance of](decreases_abundance_of.md) - holds between two molecular entities where the action or effect of one decreases the amount of the other within a system of interest
             * [increases abundance of](increases_abundance_of.md) - holds between two molecular entities where the action or effect of one increases the amount of the other within a system of interest
         * [affects activity of](affects_activity_of.md) - holds between two molecular entities where the action or effect of one changes the activity of the other within a system of interest
             * [decreases activity of](decreases_activity_of.md) - holds between two molecular entities where the action or effect of one decreases the activity of the other within a system of interest
             * [increases activity of](increases_activity_of.md) - holds between two molecular entities where the action or effect of one increases the activity of the other within a system of interest
         * [affects degradation of](affects_degradation_of.md) - holds between two molecular entities where the action or effect of one impacts the rate of degradation of the other within a system of interest, where chemical degradation is defined act or process of simplifying or breaking down a molecule into smaller parts, either naturally or artificially (Oxford English Dictionary, UK, 1995)
             * [decreases degradation of](decreases_degradation_of.md) - holds between two molecular entities where the action or effect of one decreases the rate of degradation of the other within a system of interest
             * [increases degradation of](increases_degradation_of.md) - holds between two molecular entities where the action or effect of one increases the rate of degradation of the other within a system of interest
         * [affects expression in](affects_expression_in.md) - Holds between a variant and an anatomical entity where the expression of the variant is located in.
         * [affects expression of](affects_expression_of.md) - holds between two molecular entities where the action or effect of one changes the level of expression of the other within a system of interest
             * [decreases expression of](decreases_expression_of.md) - holds between two molecular entities where the action or effect of one decreases the level of expression of the other within a system of interest
             * [increases expression of](increases_expression_of.md) - holds between two molecular entities where the action or effect of one increases the level of expression of the other within a system of interest
         * [affects folding of](affects_folding_of.md) - holds between two molecular entities where the action or effect of one changes the rate or quality of folding of the other
             * [decreases folding of](decreases_folding_of.md) - holds between two molecular entities where the action or effect of one decreases the rate or quality of folding of the other
             * [increases folding of](increases_folding_of.md) - holds between two molecular entities where the action or effect of one increases the rate or quality of folding of the other
         * [affects localization of](affects_localization_of.md) - holds between two molecular entities where the action or effect of one changes the localization of the other within a system of interest
             * [decreases localization of](decreases_localization_of.md) - holds between two molecular entities where the action or effect of one decreases the proper localization of the other within a system of interest
             * [increases localization of](increases_localization_of.md) - holds between two molecular entities where the action or effect of one increases the proper localization of the other within a system of interest
         * [affects metabolic processing of](affects_metabolic_processing_of.md) - holds between two molecular entities where the action or effect of one impacts the metabolic processing of the other within a system of interest
             * [decreases metabolic processing of](decreases_metabolic_processing_of.md) - holds between two molecular entities where the action or effect of one decreases the rate of metabolic processing of the other within a system of interest
             * [increases metabolic processing of](increases_metabolic_processing_of.md) - holds between two molecular entities where the action or effect of one increases the rate of metabolic processing of the other within a system of interest
         * [affects molecular modification of](affects_molecular_modification_of.md) - holds between two molecular entities where the action or effect of one leads changes in the molecular modification(s) of the other (e.g. via post-translational modifications of proteins such as the addition of phosphoryl group, or via redox reaction that adds or subtracts electrons)
             * [decreases molecular modification of](decreases_molecular_modification_of.md) - holds between two molecular entities where the action or effect of one leads to decreased molecular modification(s) of the other (e.g. via post-translational modifications of proteins such as the addition of phosphoryl group, or via redox reaction that adds or subtracts electrons)
             * [increases molecular modification of](increases_molecular_modification_of.md) - holds between two molecular entities where the action or effect of one leads to increased molecular modification(s) of the other (e.g. via post-translational modifications of proteins such as the addition of phosphoryl group, or via redox reaction that adds or subtracts electrons)
         * [affects mutation rate of](affects_mutation_rate_of.md) - holds between a molecular entity and a genomic entity where the action or effect of the molecular entity impacts the rate of mutation of the genomic entity within a system of interest
             * [decreases mutation rate of](decreases_mutation_rate_of.md) - holds between a molecular entity and a genomic entity where the action or effect of the molecular entity decreases the rate of mutation of the genomic entity within a system of interest
             * [increases mutation rate of](increases_mutation_rate_of.md) - holds between a molecular entity and a genomic entity where the action or effect of the molecular entity increases the rate of mutation of the genomic entity within a system of interest
         * [affects response to](affects_response_to.md) - holds between two molecular entities where the action or effect of one impacts the susceptibility of a biological entity or system (e.g. an organism, cell, cellular component, macromolecular machine mixin, biological or pathological process) to the other
             * [decreases response to](decreases_response_to.md) - holds between two molecular entities where the action or effect of one decreases the susceptibility of a biological entity or system (e.g. an organism, cell, cellular component, macromolecular machine mixin, biological or pathological process) to the other
             * [increases response to](increases_response_to.md) - holds between two molecular entities where the action or effect of one increases the susceptibility of a biological entity or system (e.g. an organism, cell, cellular component, macromolecular machine mixin, biological or pathological process) to the other
         * [affects secretion of](affects_secretion_of.md) - holds between two molecular entities where the action or effect of one impacts the rate of secretion of the other out of a cell, gland, or organ
             * [decreases secretion of](decreases_secretion_of.md) - holds between two molecular entities where the action or effect of one decreases the rate of secretion of the other out of a cell, gland, or organ
             * [increases secretion of](increases_secretion_of.md) - holds between two molecular entities where the action or effect of one increases the rate of secretion of the other out of a cell, gland, or organ
         * [affects splicing of](affects_splicing_of.md) - holds between a molecular entity and an mRNA where the action or effect of the molecular entity impacts the splicing of the mRNA
             * [decreases splicing of](decreases_splicing_of.md) - holds between a molecular entity and an mRNA where the action or effect of the molecular entity decreases the proper splicing of the mRNA
             * [increases splicing of](increases_splicing_of.md) - holds between a molecular entity and an mRNA where the action or effect of the molecular entity increases the proper splicing of the mRNA
         * [affects stability of](affects_stability_of.md) - holds between two molecular entities where the action or effect of one impacts the stability of the other within a system of interest
             * [decreases stability of](decreases_stability_of.md) - holds between two molecular entities where the action or effect of one decreases the stability of the other within a system of interest
             * [increases stability of](increases_stability_of.md) - holds between two molecular entities where the action or effect of one increases the stability of the other within a system of interest
         * [affects synthesis of](affects_synthesis_of.md) - holds between two molecular entities where the action or effect of one impacts the rate of chemical synthesis of the other
             * [decreases synthesis of](decreases_synthesis_of.md) - holds between two molecular entities where the action or effect of one decreases the rate of chemical synthesis of the other
             * [increases synthesis of](increases_synthesis_of.md) - holds between two molecular entities where the action or effect of one increases the rate of chemical synthesis of the other
         * [affects transport of](affects_transport_of.md) - holds between two molecular entities where the action or effect of one impacts the rate of transport of the other across some boundary in a system of interest
             * [decreases transport of](decreases_transport_of.md) - holds between two molecular entities where the action or effect of one decreases the rate of transport of the other across some boundary in a system of interest
             * [increases transport of](increases_transport_of.md) - holds between two molecular entities where the action or effect of one increases the rate of transport of the other across some boundary in a system of interest
         * [affects uptake of](affects_uptake_of.md) - holds between two molecular entities where the action or effect of one impacts the rate of uptake of the other into of a cell, gland, or organ
             * [decreases uptake of](decreases_uptake_of.md) - holds between two molecular entities where the action or effect of one decreases the rate of uptake of the other into of a cell, gland, or organ
             * [increases uptake of](increases_uptake_of.md) - holds between two molecular entities where the action or effect of one increases the rate of uptake of the other into of a cell, gland, or organ
         * [ameliorates](ameliorates.md) - A relationship between an entity (e.g. a genotype, genetic variation, chemical, or environmental exposure) and a condition (a phenotype or disease), where the presence of the entity reduces or eliminates some or all aspects of the condition.
             * [treats](treats.md) - holds between a therapeutic procedure or chemical substance and a disease or phenotypic feature that it is used to treat
                 * [approved to treat](approved_to_treat.md) - holds between a therapeutic procedure or chemical substance and a disease or phenotypic feature for which it is approved for treatment to some level of clinical trial. Note that in terms of REPODB narrow mappings, terms containing 'suspended', 'terminated' or 'withdrawn' should be mapped onto associations using this term for which 'negated: true' is asserted.
         * [disrupts](disrupts.md) - describes a relationship where one entity degrades or interferes with the structure, function, or occurrence of another.
         * [entity regulates entity](entity_regulates_entity.md)
             * [entity negatively regulates entity](entity_negatively_regulates_entity.md)
             * [entity positively regulates entity](entity_positively_regulates_entity.md)
         * [exacerbates](exacerbates.md) - A relationship between an entity (e.g. a chemical, environmental exposure, or some form of genetic variation) and a condition (a phenotype or disease), where the presence of the entity worsens some or all aspects of the condition.
         * [process regulates process](process_regulates_process.md)
             * [process negatively regulates process](process_negatively_regulates_process.md)
             * [process positively regulates process](process_positively_regulates_process.md)
     * [affects risk for](affects_risk_for.md) - holds between two entities where exposure to one entity alters the chance of developing the other
         * [predisposes](predisposes.md) - holds between two entities where exposure to one entity increases the chance of developing the other
         * [prevents](prevents.md) - holds between an entity whose application or use reduces the likelihood of a potential outcome. Typically used to associate a chemical substance, exposure, activity, or medical intervention that can prevent the onset a disease or phenotypic feature.
     * [broad match](broad_match.md) - a list of terms from different schemas or terminology systems that have a broader, more general meaning. Broader terms are typically shown as parents in a hierarchy or tree.
     * [caused by](caused_by.md) - holds between two entities where the occurrence, existence, or activity of one is caused by the occurrence or generation of the other
     * [close match](close_match.md) - a list of terms from different schemas or terminology systems that have a semantically similar but not strictly equivalent, broader, or narrower meaning. Such terms often describe the same general concept from different ontological perspectives (e.g. drug as a type of chemical entity versus drug as a type of role borne by a chemical entity).
         * [exact match](exact_match.md) - holds between two entities that have strictly equivalent meanings, with a high degree of confidence
             * [same as](same_as.md) - holds between two entities that are considered equivalent to each other
     * [coexists with](coexists_with.md) - holds between two entities that are co-located in the same aggregate object, process, or spatio-temporal region
         * [colocalizes with](colocalizes_with.md) - holds between two entities that are observed to be located in the same place.
         * [in cell population with](in_cell_population_with.md) - holds between two genes or gene products that are expressed in the same cell type or population
         * [in complex with](in_complex_with.md) - holds between two genes or gene products that are part of (or code for products that are part of) in the same macromolecular complex mixin
         * [in pathway with](in_pathway_with.md) - holds between two genes or gene products that are part of in the same biological pathway
     * [contraindicated for](contraindicated_for.md) - Holds between a drug and a disease or phenotype, such that a person with that disease should not be treated with the drug.
     * [contributes to](contributes_to.md) - holds between two entities where the occurrence, existence, or activity of one causes or contributes to the occurrence or generation of the other
         * [causes](causes.md) - holds between two entities where the occurrence, existence, or activity of one causes the occurrence or generation of the other
             * [causes adverse event](causes_adverse_event.md) - holds between a drug and a disease or phenotype that can be caused by the drug
     * [contributor](contributor.md)
         * [author](author.md) - an instance of one (co-)creator primarily responsible for a written work
         * [editor](editor.md) - editor of a compiled work such as a book or a periodical (newspaper or an academic journal). Note that in the case of publications which have a containing "published in" node property, the editor association may not be attached directly to the embedded child publication, but only made in between the parent's publication node and the editorial agent of the encompassing publication (e.g. only from the Book referenced by the 'published_in' property of a book chapter Publication node).
         * [provider](provider.md) - person, group, organization or project that provides a piece of information (e.g. a knowledge association).
         * [publisher](publisher.md) - organization or person responsible for publishing books, periodicals, podcasts, games or software. Note that in the case of publications which have a containing "published in" node property, the publisher association may not be attached directly to the embedded child publication, but only made in between the parent's publication node and the publisher agent of the encompassing publication (e.g. only from the Journal referenced by the 'published_in' property of an journal article Publication node).
     * [correlated with](correlated_with.md) - holds between any two named thing entities. For example, correlated_with holds between a disease or phenotypic feature and a measurable molecular entity that is used as an indicator of the presence or state of the disease or feature.
         * [biomarker for](biomarker_for.md) - holds between a measurable molecular entity and a disease or phenotypic feature, where the entity is used as an indicator of the presence or state of the disease or feature.
         * [coexpressed with](coexpressed_with.md) - holds between any two genes or gene products, in which both are generally expressed within a single defined experimental context.
         * [has biomarker](has_biomarker.md) - holds between a disease or phenotypic feature and a measurable molecular entity that is used as an indicator of the presence or state of the disease or feature.
         * [negatively correlated with](negatively_correlated_with.md) - holds between any two named thing entities "correlated with" one another in a negative manner.
         * [positively correlated with](positively_correlated_with.md) - holds between any two named thing entities "correlated with" one another in a positive manner.
     * [derives from](derives_from.md) - holds between two distinct material entities, the new entity and the old entity, in which the new entity begins to exist when the old entity ceases to exist, and the new entity inherits the significant portion of the matter of the old entity
         * [is metabolite of](is_metabolite_of.md) - holds between two chemical substances in which the first one is derived from the second one as a product of metabolism
     * [derives into](derives_into.md) - holds between two distinct material entities, the old entity and the new entity, in which the new entity begins to exist when the old entity ceases to exist, and the new entity inherits the significant portion of the matter of the old entity
         * [has metabolite](has_metabolite.md) - holds between two chemical substances in which the second one is derived from the first one as a product of metabolism
     * [develops from](develops_from.md)
     * [disease has basis in](disease_has_basis_in.md) - A relation that holds between a disease and an entity where the state of the entity has contribution to the disease.
     * [expressed in](expressed_in.md) - holds between a gene or gene product and an anatomical entity in which it is expressed
     * [expresses](expresses.md) - holds between an anatomical entity and gene or gene product that is expressed there
     * [gene product of](gene_product_of.md) - definition x has gene product of y if and only if y is a gene (SO:0000704) that participates in some gene expression process (GO:0010467) where the output of thatf process is either y or something that is ribosomally translated from x
     * [genetic association](genetic_association.md) - Co-occurrence of a certain allele of a genetic marker and the phenotype of interest in the same individuals at above-chance level
         * [condition associated with gene](condition_associated_with_gene.md) - holds between a gene and a disease or phenotypic feature that may be influenced, contribute to, or be correlated with the gene or its alleles/products
         * [gene associated with condition](gene_associated_with_condition.md) - holds between a gene and a disease or phenotypic feature that the gene or its alleles/products may influence, contribute to, or correlate with
     * [has completed](has_completed.md) - holds between an entity and a process that the entity is capable of and has completed
     * [has decreased amount](has_decreased_amount.md)
     * [has gene product](has_gene_product.md) - holds between a gene and a transcribed and/or translated product generated from it
     * [has increased amount](has_increased_amount.md)
     * [has molecular consequence](has_molecular_consequence.md) - connects a sequence variant to a class describing the molecular consequence. E.g.  SO:0001583
     * [has not completed](has_not_completed.md) - holds between an entity and a process that the entity is capable of, but has not completed
     * [has participant](has_participant.md) - holds between a process and a continuant, where the continuant is somehow involved in the process
         * [enabled by](enabled_by.md) - holds between a process and a physical entity, where the physical entity executes the process
             * [molecular activity➞enabled by](molecular_activity_enabled_by.md) - The gene product, gene, or complex that catalyzes the reaction
         * [has input](has_input.md) - holds between a process and a continuant, where the continuant is an input into the process
             * [molecular activity➞has input](molecular_activity_has_input.md) - A chemical entity that is the input for the reaction
         * [has output](has_output.md) - holds between a process and a continuant, where the continuant is an output of the process
             * [molecular activity➞has output](molecular_activity_has_output.md) - A chemical entity that is the output for the reaction
     * [has phenotype](has_phenotype.md) - holds between a biological entity and a phenotype, where a phenotype is construed broadly as any kind of quality of an organism part, a collection of these qualities, or a change in quality or qualities (e.g. abnormally increased temperature).
     * [has sequence location](has_sequence_location.md) - holds between two genomic entities when the subject can be localized in sequence coordinates on the object. For example, between an exon and a chromosome/contig.
     * [in linkage disequilibrium with](in_linkage_disequilibrium_with.md) - holds between two sequence variants, the presence of which are correlated in a population
     * [in taxon](in_taxon.md) - connects an entity to its taxonomic classification. Only certain kinds of entities can be taxonomically classified; see 'thing with taxon'
     * [interacts with](interacts_with.md) - holds between any two entities that directly or indirectly interact with each other
         * [directly interacts with](directly_interacts_with.md) - Holds between molecular entities that physically and directly interact with each other
         * [genetically interacts with](genetically_interacts_with.md) - holds between two genes whose phenotypic effects are dependent on each other in some way - such that their combined phenotypic effects are the result of some interaction between the activity of their gene products. Examples include epistasis and synthetic lethality.
         * [physically interacts with](physically_interacts_with.md) - holds between two entities that make physical contact as part of some interaction
             * [molecularly interacts with](molecularly_interacts_with.md)
                 * [decreases molecular interaction](decreases_molecular_interaction.md) - indicates that the source decreases the molecular interaction between the target and some other molecular entity
                 * [increases molecular interaction](increases_molecular_interaction.md) - indicates that the source increases the molecular interaction between the target and some other molecular entity
     * [is sequence variant of](is_sequence_variant_of.md) - holds between a sequence variant and a genomic entity
         * [is frameshift variant of](is_frameshift_variant_of.md) - holds between a sequence variant and a gene, such the sequence variant causes a disruption of the translational reading frame, because the number of nucleotides inserted or deleted is not a multiple of three.
         * [is missense variant of](is_missense_variant_of.md) - holds between a gene  and a sequence variant, such the sequence variant results in a different amino acid sequence but where the length is preserved.
         * [is nearby variant of](is_nearby_variant_of.md) - holds between a sequence variant and a gene sequence that the variant is genomically close to.
         * [is non coding variant of](is_non_coding_variant_of.md) - holds between a sequence variant and a gene, where the variant does not affect the coding sequence
         * [is nonsense variant of](is_nonsense_variant_of.md) - holds between a sequence variant and a gene, such the sequence variant results in a premature stop codon
         * [is splice site variant of](is_splice_site_variant_of.md) - holds between a sequence variant and a gene, such the sequence variant is in the canonical splice site of one of the gene's exons.
         * [is synonymous variant of](is_synonymous_variant_of.md) - holds between a sequence variant and a gene, such the sequence variant is in the coding sequence of the gene, but results in the same amino acid sequence
     * [lacks part](lacks_part.md)
     * [located in](located_in.md) - holds between a material entity and a material entity or site within which it is located (but of which it is not considered a part)
     * [location of](location_of.md) - holds between material entity or site and a material entity that is located within it (but not considered a part of it)
     * [manifestation of](manifestation_of.md) - that part of a phenomenon which is directly observable or visibly expressed, or which gives evidence to the underlying process; used in SemMedDB for linking things like dysfunctions and processes to some disease or syndrome
     * [narrow match](narrow_match.md) - a list of terms from different schemas or terminology systems that have a narrower, more specific meaning. Narrower terms are typically shown as children in a hierarchy or tree.
     * [occurs in](occurs_in.md) - holds between a process and a material entity or site within which the process occurs
     * [opposite of](opposite_of.md) - x is the opposite of y if there exists some distance metric M, and there exists no z such as M(x,z) <= M(x,y) or M(y,z) <= M(y,x). (This description is from RO. Needs to be rephrased).
     * [overlaps](overlaps.md) - holds between entities that overlap in their extents (materials or processes)
         * [has part](has_part.md) - holds between wholes and their parts (material entities or processes)
             * [has active ingredient](has_active_ingredient.md) - holds between a drug and a chemical substance in which the latter is a part of the former, and is a biologically active component
             * [has excipient](has_excipient.md) - holds between a drug and a chemical substances in which the latter is a part of the former, and is a biologically inactive component
             * [has food component](has_food_component.md) - holds between food and one or more chemical substances composing it, irrespective of nutritional value (i.e. could also be a contaminant or additive)
                 * [has nutrient](has_nutrient.md) - one or more nutrients which are growth factors for a living organism
             * [has variant part](has_variant_part.md) - holds between a genomic entity and a genotypic entity that is a sub-component of it
         * [part of](part_of.md) - holds between parts and wholes (material entities or processes)
             * [food component of](food_component_of.md) - holds between a one or more chemical substances present in food, irrespective of nutritional value (i.e. could also be a contaminant or additive)
                 * [nutrient of](nutrient_of.md)
             * [is active ingredient of](is_active_ingredient_of.md) - holds between a chemical substance and a drug, in which the former is a part of the latter, and is a biologically active component
             * [is excipient of](is_excipient_of.md) - holds between a chemical substance and a drug in which the former is a part of the latter, and is a biologically inactive component
     * [participates in](participates_in.md) - holds between a continuant and a process, where the continuant is somehow involved in the process
         * [actively involved in](actively_involved_in.md) - holds between a continuant and a process or function, where the continuant actively contributes to part or all of the process or function it realizes
             * [capable of](capable_of.md) - holds between a physical entity and process or function, where the continuant alone has the ability to carry out the process or function.
         * [enables](enables.md) - holds between a physical entity and a process, where the physical entity executes the process
     * [phenotype of](phenotype_of.md) - holds between a phenotype and a biological entity, where a phenotype is construed broadly as any kind of quality of an organism part, a collection of these qualities, or a change in quality or qualities (e.g. abnormally increased temperature).
     * [prevented by](prevented_by.md) - holds between a potential outcome of which the likelihood was reduced by the application or use of an entity.
     * [produced by](produced_by.md)
     * [produces](produces.md) - holds between a material entity and a product that is generated through the intentional actions or functioning of the material entity
     * [related condition](related_condition.md)
     * [similar to](similar_to.md) - holds between an entity and some other entity with similar features.
         * [chemically similar to](chemically_similar_to.md) - holds between one chemical substances and another that it approximates for purposes of scientific study, in virtue of its exhibiting similar features of the studied entity.
         * [homologous to](homologous_to.md) - holds between two biological entities that have common evolutionary origin
             * [orthologous to](orthologous_to.md) - a homology relationship between entities (typically genes) that diverged after a speciation event.
             * [paralogous to](paralogous_to.md) - a homology relationship that holds between entities (typically genes) that diverged after a duplication event.
             * [xenologous to](xenologous_to.md) - a homology relationship characterized by an interspecies (horizontal) transfer since the common ancestor.
         * [model of](model_of.md) - holds between a thing and some other thing it approximates for purposes of scientific study, in virtue of its exhibiting similar features of the studied entity.
     * [subclass of](subclass_of.md) - holds between two classes where the domain class is a specialization of the range class
         * [organism taxon➞subclass of](organism_taxon_subclass_of.md) - subclass of holds between two taxa, e.g. human subclass of mammal
     * [superclass of](superclass_of.md) - holds between two classes where the domain class is a super class of the range class
     * [temporally related to](temporally_related_to.md) - holds between two entities with a temporal relationship
         * [preceded by](preceded_by.md) - holds between two processes, where the other is completed before the one begins
         * [precedes](precedes.md) - holds between two processes, where one completes before the other begins
     * [transcribed from](transcribed_from.md) - x is transcribed from y if and only if x is synthesized from template y
     * [transcribed to](transcribed_to.md) - inverse of transcribed from
     * [translates to](translates_to.md) - x (amino acid chain/polypeptide) is the ribosomal translation of y (transcript) if and only if a ribosome reads y (transcript) through a series of triplet codon-amino acid adaptor activities (GO:0030533) and produces x (amino acid chain/polypeptide)
     * [translation of](translation_of.md) - inverse of translates to
     * [treated by](treated_by.md) - holds between a disease or phenotypic feature and a therapeutic process or chemical substance that is used to treat the condition
         * [approved for treatment by](approved_for_treatment_by.md) - holds between a disease or phenotypic feature and a therapeutic process or chemical substance that is approved for treatment of the condition (or not, if negated) to some level of clinical trial
 * [source](source.md) - a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
 * [type](type.md)
     * [association➞type](association_type.md) - rdf:type of biolink:Association should be fixed at rdf:Statement
     * [category](category.md) - Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
         * [association➞category](association_category.md)
         * [named thing➞category](named_thing_category.md)
     * [publication➞type](publication_type.md) - Ontology term for publication type may be drawn from Dublin Core types (https://www.dublincore.org/specifications/dublin-core/dcmi-type-vocabulary/), FRBR-aligned Bibliographic Ontology (https://sparontologies.github.io/fabio/current/fabio.html), the MESH publication types (https://www.nlm.nih.gov/mesh/pubtypes.html), the Confederation of Open Access Repositories (COAR) Controlled Vocabulary for Resource Type Genres (http://vocabularies.coar-repositories.org/documentation/resource_types/), Wikidata (https://www.wikidata.org/wiki/Wikidata:Publication_types), or equivalent publication type ontology. When a given publication type ontology term is used within a given knowledge graph, then the CURIE identified term must be documented in the graph as a concept node of biolink:category biolink:OntologyClass.
         * [book➞type](book_type.md) - Should generally be set to an ontology class defined term for 'book'.
         * [serial➞type](serial_type.md) - Should generally be set to an ontology class defined term for 'serial' or 'journal'.

### Enums

 * [logical_interpretation_enum](logical_interpretation_enum.md)

### Subsets

 * [ModelOrganismDatabase](ModelOrganismDatabase.md) - Subset that is relevant for a typical Model Organism Database (MOD)
 * [Samples](Samples.md) - Sample/biosample datamodel
 * [Testing](Testing.md) - TBD
 * [TranslatorMinimal](TranslatorMinimal.md) - Minimum subset of translator work

### Types


#### Built in

 * **Bool**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [BiologicalSequence](types/BiologicalSequence.md)  ([String](types/String.md)) 
 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [CategoryType](types/CategoryType.md)  ([Uriorcurie](types/Uriorcurie.md))  - A primitive type in which the value denotes a class within the biolink model. The value must be a URI or a CURIE. In a Neo4j representation, the value should be the CURIE for the biolink class, for example biolink:Gene. For an RDF representation, the value should be a URI such as https://w3id.org/biolink/vocab/Gene
 * [ChemicalFormulaValue](types/ChemicalFormulaValue.md)  (**str**)  - A chemical formula
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [FrequencyValue](types/FrequencyValue.md)  ([String](types/String.md)) 
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [IriType](types/IriType.md)  ([Uriorcurie](types/Uriorcurie.md))  - An IRI
 * [LabelType](types/LabelType.md)  ([String](types/String.md))  - A string that provides a human-readable name for an entity
 * [NarrativeText](types/NarrativeText.md)  ([String](types/String.md))  - A string that provides a human-readable description of something
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [PercentageFrequencyValue](types/PercentageFrequencyValue.md)  ([Double](types/Double.md)) 
 * [PredicateType](types/PredicateType.md)  ([Uriorcurie](types/Uriorcurie.md))  - A CURIE from the biolink related_to hierarchy. For example, biolink:related_to, biolink:causes, biolink:treats.
 * [Quotient](types/Quotient.md)  ([Double](types/Double.md)) 
 * [String](types/String.md)  (**str**)  - A character string
 * [SymbolType](types/SymbolType.md)  ([String](types/String.md)) 
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [TimeType](types/TimeType.md)  ([Time](types/Time.md)) 
 * [Unit](types/Unit.md)  ([String](types/String.md)) 
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
