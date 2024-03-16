
# Class: genomic entity




URI: [biolink:GenomicEntity](https://w3id.org/biolink/vocab/GenomicEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SequenceVariant],[SequenceVariant]uses%20-.->[GenomicEntity&#124;has_biological_sequence:biological_sequence%20%3F],[ReagentTargetedGene]uses%20-.->[GenomicEntity],[NucleosomeModification]uses%20-.->[GenomicEntity],[NucleicAcidEntity]uses%20-.->[GenomicEntity],[Haplotype]uses%20-.->[GenomicEntity],[Genotype]uses%20-.->[GenomicEntity],[GenomicBackgroundExposure]uses%20-.->[GenomicEntity],[Genome]uses%20-.->[GenomicEntity],[Gene]uses%20-.->[GenomicEntity],[ReagentTargetedGene],[NucleosomeModification],[NucleicAcidEntity],[Haplotype],[Genotype],[GenomicBackgroundExposure],[Genome],[Gene])](https://yuml.me/diagram/nofunky;dir:TB/class/[SequenceVariant],[SequenceVariant]uses%20-.->[GenomicEntity&#124;has_biological_sequence:biological_sequence%20%3F],[ReagentTargetedGene]uses%20-.->[GenomicEntity],[NucleosomeModification]uses%20-.->[GenomicEntity],[NucleicAcidEntity]uses%20-.->[GenomicEntity],[Haplotype]uses%20-.->[GenomicEntity],[Genotype]uses%20-.->[GenomicEntity],[GenomicBackgroundExposure]uses%20-.->[GenomicEntity],[Genome]uses%20-.->[GenomicEntity],[Gene]uses%20-.->[GenomicEntity],[ReagentTargetedGene],[NucleosomeModification],[NucleicAcidEntity],[Haplotype],[Genotype],[GenomicBackgroundExposure],[Genome],[Gene])

## Mixin for

 * [Gene](Gene.md) (mixin)  - A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.
 * [Genome](Genome.md) (mixin)  - A genome is the sum of genetic material within a cell or virion.
 * [GenomicBackgroundExposure](GenomicBackgroundExposure.md) (mixin)  - A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing an outcome.
 * [Genotype](Genotype.md) (mixin)  - An information content entity that describes a genome by specifying the total variation in genomic sequence and/or gene expression, relative to some established background
 * [Haplotype](Haplotype.md) (mixin)  - A set of zero or more Alleles on a single instance of a Sequence[VMC]
 * [NucleicAcidEntity](NucleicAcidEntity.md) (mixin)  - A nucleic acid entity is a molecular entity characterized by availability in gene databases of nucleotide-based sequence representations of its precise sequence; for convenience of representation, partial sequences of various kinds are included.
 * [NucleosomeModification](NucleosomeModification.md) (mixin)  - A chemical modification of a histone protein within a nucleosome octomer or a substitution of a histone with a variant histone isoform. e.g. Histone 4 Lysine 20 methylation (H4K20me), histone variant H2AZ substituting H2A.
 * [ReagentTargetedGene](ReagentTargetedGene.md) (mixin)  - A gene altered in its expression level in the context of some experiment as a result of being targeted by gene-knockdown reagent(s) such as a morpholino or RNAi.
 * [SequenceVariant](SequenceVariant.md) (mixin)  - A sequence_variant is a non exact copy of a sequence_feature or genome exhibiting one or more sequence_alteration.

## Referenced by Class

 *  **[SequenceVariant](SequenceVariant.md)** *[is frameshift variant of](is_frameshift_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[is missense variant of](is_missense_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[is nearby variant of](is_nearby_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[is non coding variant of](is_non_coding_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[is nonsense variant of](is_nonsense_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[is sequence variant of](is_sequence_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[is splice site variant of](is_splice_site_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[is synonymous variant of](is_synonymous_variant_of.md)*  <sub>0..\*</sub>  **[GenomicEntity](GenomicEntity.md)**

## Attributes


### Own

 * [has biological sequence](has_biological_sequence.md)  <sub>0..1</sub>
     * Description: connects a genomic feature to its sequence
     * Range: [BiologicalSequence](types/BiologicalSequence.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | translator_minimal |
| **Narrow Mappings:** | | STY:T028 |
|  | | GENO:0000897 |

