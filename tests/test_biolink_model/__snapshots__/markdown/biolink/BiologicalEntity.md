
# Class: biological entity




URI: [biolink:BiologicalEntity](https://w3id.org/biolink/vocab/BiologicalEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[SequenceVariant],[ReagentTargetedGene],[ProteinFamily],[ProteinDomain],[PosttranslationalModification],[Polypeptide],[PhenotypicFeature],[OrganismalEntity],[OrganismTaxon],[NucleosomeModification],[NucleicAcidSequenceMotif],[NamedThing],[MacromolecularComplex],[Haplotype],[Genotype],[Genome],[GeneticInheritance],[GeneFamily],[Gene],[DiseaseOrPhenotypicFeature],[BiologicalProcessOrActivity],[BiologicalEntity&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F]uses%20-.->[ThingWithTaxon],[BiologicalEntity]^-[SequenceVariant],[BiologicalEntity]^-[ReagentTargetedGene],[BiologicalEntity]^-[ProteinFamily],[BiologicalEntity]^-[ProteinDomain],[BiologicalEntity]^-[PosttranslationalModification],[BiologicalEntity]^-[Polypeptide],[BiologicalEntity]^-[OrganismalEntity],[BiologicalEntity]^-[NucleosomeModification],[BiologicalEntity]^-[NucleicAcidSequenceMotif],[BiologicalEntity]^-[MacromolecularComplex],[BiologicalEntity]^-[Haplotype],[BiologicalEntity]^-[Genotype],[BiologicalEntity]^-[Genome],[BiologicalEntity]^-[GeneticInheritance],[BiologicalEntity]^-[GeneFamily],[BiologicalEntity]^-[Gene],[BiologicalEntity]^-[DiseaseOrPhenotypicFeature],[BiologicalEntity]^-[BiologicalProcessOrActivity],[NamedThing]^-[BiologicalEntity],[Attribute])](https://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[SequenceVariant],[ReagentTargetedGene],[ProteinFamily],[ProteinDomain],[PosttranslationalModification],[Polypeptide],[PhenotypicFeature],[OrganismalEntity],[OrganismTaxon],[NucleosomeModification],[NucleicAcidSequenceMotif],[NamedThing],[MacromolecularComplex],[Haplotype],[Genotype],[Genome],[GeneticInheritance],[GeneFamily],[Gene],[DiseaseOrPhenotypicFeature],[BiologicalProcessOrActivity],[BiologicalEntity&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F]uses%20-.->[ThingWithTaxon],[BiologicalEntity]^-[SequenceVariant],[BiologicalEntity]^-[ReagentTargetedGene],[BiologicalEntity]^-[ProteinFamily],[BiologicalEntity]^-[ProteinDomain],[BiologicalEntity]^-[PosttranslationalModification],[BiologicalEntity]^-[Polypeptide],[BiologicalEntity]^-[OrganismalEntity],[BiologicalEntity]^-[NucleosomeModification],[BiologicalEntity]^-[NucleicAcidSequenceMotif],[BiologicalEntity]^-[MacromolecularComplex],[BiologicalEntity]^-[Haplotype],[BiologicalEntity]^-[Genotype],[BiologicalEntity]^-[Genome],[BiologicalEntity]^-[GeneticInheritance],[BiologicalEntity]^-[GeneFamily],[BiologicalEntity]^-[Gene],[BiologicalEntity]^-[DiseaseOrPhenotypicFeature],[BiologicalEntity]^-[BiologicalProcessOrActivity],[NamedThing]^-[BiologicalEntity],[Attribute])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Uses Mixin

 *  mixin: [ThingWithTaxon](ThingWithTaxon.md) - A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms; genes, their products and other molecular entities; body parts; biological processes

## Children

 * [BiologicalProcessOrActivity](BiologicalProcessOrActivity.md) - Either an individual molecular activity, or a collection of causally connected molecular activities in a biological system.
 * [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md) - Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.  Please see definitions of phenotypic feature and disease in this model for their independent descriptions.  This class is helpful to enforce domains and ranges   that may involve either a disease or a phenotypic feature.
 * [Gene](Gene.md) - A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.
 * [GeneFamily](GeneFamily.md) - any grouping of multiple genes or gene products related by common descent
 * [GeneticInheritance](GeneticInheritance.md) - The pattern or 'mode' in which a particular genetic trait or disorder is passed from one generation to the next, e.g. autosomal dominant, autosomal recessive, etc.
 * [Genome](Genome.md) - A genome is the sum of genetic material within a cell or virion.
 * [Genotype](Genotype.md) - An information content entity that describes a genome by specifying the total variation in genomic sequence and/or gene expression, relative to some established background
 * [Haplotype](Haplotype.md) - A set of zero or more Alleles on a single instance of a Sequence[VMC]
 * [MacromolecularComplex](MacromolecularComplex.md) - A stable assembly of two or more macromolecules, i.e. proteins, nucleic acids, carbohydrates or lipids, in which at least one component is a protein and the constituent parts function together.
 * [NucleicAcidSequenceMotif](NucleicAcidSequenceMotif.md) - A linear nucleotide sequence pattern that is widespread and has, or is conjectured to have, a biological significance. e.g. the TATA box promoter motif, transcription factor binding consensus sequences.
 * [NucleosomeModification](NucleosomeModification.md) - A chemical modification of a histone protein within a nucleosome octomer or a substitution of a histone with a variant histone isoform. e.g. Histone 4 Lysine 20 methylation (H4K20me), histone variant H2AZ substituting H2A.
 * [OrganismalEntity](OrganismalEntity.md) - A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding chemical entities
 * [Polypeptide](Polypeptide.md) - A polypeptide is a molecular entity characterized by availability in protein databases of amino-acid-based sequence representations of its precise primary structure; for convenience of representation, partial sequences of various kinds are included, even if they do not represent a physical molecule.
 * [PosttranslationalModification](PosttranslationalModification.md) - A chemical modification of a polypeptide or protein that occurs after translation.  e.g. polypeptide cleavage to form separate proteins, methylation or acetylation of histone tail amino acids,  protein ubiquitination.
 * [ProteinDomain](ProteinDomain.md) - A conserved part of protein sequence and (tertiary) structure that can evolve, function, and exist independently of the rest of the protein chain. Protein domains maintain their structure and function independently of the proteins in which they are found. e.g. an SH3 domain.
 * [ProteinFamily](ProteinFamily.md)
 * [ReagentTargetedGene](ReagentTargetedGene.md) - A gene altered in its expression level in the context of some experiment as a result of being targeted by gene-knockdown reagent(s) such as a morpholino or RNAi.
 * [SequenceVariant](SequenceVariant.md) - A sequence_variant is a non exact copy of a sequence_feature or genome exhibiting one or more sequence_alteration.

## Referenced by Class

 *  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)** *[is exacerbated by](is_exacerbated_by.md)*  <sub>0..\*</sub>  **[BiologicalEntity](BiologicalEntity.md)**
 *  **[PhenotypicFeature](PhenotypicFeature.md)** *[phenotype of](phenotype_of.md)*  <sub>0..\*</sub>  **[BiologicalEntity](BiologicalEntity.md)**

## Attributes


### Inherited from named thing:

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
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: The value in this node property represents the knowledge provider that created or assembled the node and all of its attributes.  Used internally to represent how a particular node made its way into a knowledge provider or graph.
     * Range: [String](types/String.md)
 * [xref](xref.md)  <sub>0..\*</sub>
     * Description: Alternate CURIEs for a thing
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (translator_minimal)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [CategoryType](types/CategoryType.md)
     * in subsets: (translator_minimal)

### Mixed in from thing with taxon:

 * [in taxon](in_taxon.md)  <sub>0..\*</sub>
     * Description: connects an entity to its taxonomic classification. Only certain kinds of entities can be taxonomically classified; see 'thing with taxon'
     * Range: [OrganismTaxon](OrganismTaxon.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | bioentity |
| **Narrow Mappings:** | | WIKIDATA:Q28845870 |
|  | | STY:T050 |
|  | | SIO:010046 |

