
# Class: thing with taxon


A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms; genes, their products and other molecular entities; body parts; biological processes

URI: [biolink:ThingWithTaxon](https://w3id.org/biolink/vocab/ThingWithTaxon)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon]<in%20taxon%200..*-%20[ThingWithTaxon],[NucleicAcidEntity]uses%20-.->[ThingWithTaxon],[GenomicBackgroundExposure]uses%20-.->[ThingWithTaxon],[BiologicalEntity]uses%20-.->[ThingWithTaxon],[OrganismTaxon],[NucleicAcidEntity],[GenomicBackgroundExposure],[BiologicalEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon]<in%20taxon%200..*-%20[ThingWithTaxon],[NucleicAcidEntity]uses%20-.->[ThingWithTaxon],[GenomicBackgroundExposure]uses%20-.->[ThingWithTaxon],[BiologicalEntity]uses%20-.->[ThingWithTaxon],[OrganismTaxon],[NucleicAcidEntity],[GenomicBackgroundExposure],[BiologicalEntity])

## Mixin for

 * [BiologicalEntity](BiologicalEntity.md) (mixin) 
 * [GenomicBackgroundExposure](GenomicBackgroundExposure.md) (mixin)  - A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing an outcome.
 * [NucleicAcidEntity](NucleicAcidEntity.md) (mixin)  - A nucleic acid entity is a molecular entity characterized by availability in gene databases of nucleotide-based sequence representations of its precise sequence; for convenience of representation, partial sequences of various kinds are included.

## Referenced by Class

 *  **[OrganismTaxon](OrganismTaxon.md)** *[taxon of](taxon_of.md)*  <sub>0..\*</sub>  **[ThingWithTaxon](ThingWithTaxon.md)**

## Attributes


### Own

 * [in taxon](in_taxon.md)  <sub>0..\*</sub>
     * Description: connects an entity to its taxonomic classification. Only certain kinds of entities can be taxonomically classified; see 'thing with taxon'
     * Range: [OrganismTaxon](OrganismTaxon.md)
     * in subsets: (translator_minimal)
