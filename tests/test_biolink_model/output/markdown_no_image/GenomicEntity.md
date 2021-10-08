
# Class: genomic entity


an entity that can either be directly located on a genome (gene, transcript, exon, regulatory region) or is encoded in a genome (protein)

URI: [biolink:GenomicEntity](https://w3id.org/biolink/vocab/GenomicEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Transcript],[SequenceVariant],[SequenceFeatureRelationship],[ReagentTargetedGene],[Protein],[OrganismTaxon],[NamedThing],[MolecularEntity],[Haplotype],[Genotype],[GenomicSequenceLocalization],[GenomicSequenceLocalization]-%20object%201..1>[GenomicEntity&#124;has_biological_sequence:biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GenomicSequenceLocalization]-%20subject%201..1>[GenomicEntity],[SequenceFeatureRelationship]-%20object%201..1>[GenomicEntity],[SequenceFeatureRelationship]-%20subject%201..1>[GenomicEntity],[GenomicEntity]^-[Transcript],[GenomicEntity]^-[SequenceVariant],[GenomicEntity]^-[ReagentTargetedGene],[GenomicEntity]^-[Protein],[GenomicEntity]^-[Haplotype],[GenomicEntity]^-[Genotype],[GenomicEntity]^-[GenomicBackgroundExposure],[GenomicEntity]^-[Genome],[GenomicEntity]^-[Gene],[GenomicEntity]^-[Exon],[GenomicEntity]^-[CodingSequence],[MolecularEntity]^-[GenomicEntity],[GenomicBackgroundExposure],[Genome],[Gene],[Exon],[CodingSequence],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[Transcript],[SequenceVariant],[SequenceFeatureRelationship],[ReagentTargetedGene],[Protein],[OrganismTaxon],[NamedThing],[MolecularEntity],[Haplotype],[Genotype],[GenomicSequenceLocalization],[GenomicSequenceLocalization]-%20object%201..1>[GenomicEntity&#124;has_biological_sequence:biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GenomicSequenceLocalization]-%20subject%201..1>[GenomicEntity],[SequenceFeatureRelationship]-%20object%201..1>[GenomicEntity],[SequenceFeatureRelationship]-%20subject%201..1>[GenomicEntity],[GenomicEntity]^-[Transcript],[GenomicEntity]^-[SequenceVariant],[GenomicEntity]^-[ReagentTargetedGene],[GenomicEntity]^-[Protein],[GenomicEntity]^-[Haplotype],[GenomicEntity]^-[Genotype],[GenomicEntity]^-[GenomicBackgroundExposure],[GenomicEntity]^-[Genome],[GenomicEntity]^-[Gene],[GenomicEntity]^-[Exon],[GenomicEntity]^-[CodingSequence],[MolecularEntity]^-[GenomicEntity],[GenomicBackgroundExposure],[Genome],[Gene],[Exon],[CodingSequence],[Attribute],[Agent])

## Parents

 *  is_a: [MolecularEntity](MolecularEntity.md) - A gene, gene product, small molecule or macromolecule (including protein complex)"

## Children

 * [CodingSequence](CodingSequence.md)
 * [Exon](Exon.md) - A region of the transcript sequence within a gene which is not removed from the primary RNA transcript by RNA splicing.
 * [Gene](Gene.md) - A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.
 * [Genome](Genome.md) - A genome is the sum of genetic material within a cell or virion.
 * [GenomicBackgroundExposure](GenomicBackgroundExposure.md) - A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing an outcome.
 * [Genotype](Genotype.md) - An information content entity that describes a genome by specifying the total variation in genomic sequence and/or gene expression, relative to some established background
 * [Haplotype](Haplotype.md) - A set of zero or more Alleles on a single instance of a Sequence[VMC]
 * [Protein](Protein.md) - A gene product that is composed of a chain of amino acid sequences and is produced by ribosome-mediated translation of mRNA
 * [ReagentTargetedGene](ReagentTargetedGene.md) - A gene altered in its expression level in the context of some experiment as a result of being targeted by gene-knockdown reagent(s) such as a morpholino or RNAi.
 * [SequenceVariant](SequenceVariant.md) - An allele that varies in its sequence from what is considered the reference allele at that locus.
 * [Transcript](Transcript.md) - An RNA synthesized on a DNA or RNA template by an RNA polymerase.

## Referenced by Class

 *  **[MolecularEntity](MolecularEntity.md)** *[affects expression of](affects_expression_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects mutation rate of](affects_mutation_rate_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases expression of](decreases_expression_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases mutation rate of](decreases_mutation_rate_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[GenomicSequenceLocalization](GenomicSequenceLocalization.md)** *[genomic sequence localization➞object](genomic_sequence_localization_object.md)*  <sub>1..1</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[GenomicSequenceLocalization](GenomicSequenceLocalization.md)** *[genomic sequence localization➞subject](genomic_sequence_localization_subject.md)*  <sub>1..1</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has sequence location](has_sequence_location.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases expression of](increases_expression_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases mutation rate of](increases_mutation_rate_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[is sequence variant of](is_sequence_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceFeatureRelationship](SequenceFeatureRelationship.md)** *[sequence feature relationship➞object](sequence_feature_relationship_object.md)*  <sub>1..1</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceFeatureRelationship](SequenceFeatureRelationship.md)** *[sequence feature relationship➞subject](sequence_feature_relationship_subject.md)*  <sub>1..1</sub>  **[GenomicEntity](GenomicEntity.md)**

## Attributes


### Own

 * [has biological sequence](has_biological_sequence.md)  <sub>0..1</sub>
     * Description: connects a genomic feature to its sequence
     * Range: [BiologicalSequence](types/BiologicalSequence.md)

### Inherited from molecular entity:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [type](type.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [name](name.md)  <sub>0..1</sub>
     * Description: A human-readable name for an attribute or entity.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a human-readable description of an entity
     * Range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [source](source.md)  <sub>0..1</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * Range: [Agent](Agent.md)
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | sequence feature |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | UMLSSG:GENE |
|  | | SO:0000110 |
|  | | GENO:0000897 |
| **Narrow Mappings:** | | UMLSSC:T028 |
|  | | UMLSST:gngm |
|  | | UMLSSC:T086 |
|  | | UMLSST:nusq |

