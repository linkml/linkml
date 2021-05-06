
# Class: Protein


A gene product that is composed of a chain of amino acid sequences and is produced by ribosome-mediated translation of mRNA

URI: [biolink:Protein](https://w3id.org/biolink/vocab/Protein)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[ProteinIsoform],[Protein&#124;synonym:label_type%20*;xref:iri_type%20*;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[GeneProductMixin],[Protein]^-[ProteinIsoform],[GenomicEntity]^-[Protein],[OrganismTaxon],[NamedThing],[GenomicEntity],[GeneProductMixin],[Attribute],[Agent])

## Identifier prefixes

 * UniProtKB
 * PR
 * ENSEMBL
 * FB

## Parents

 *  is_a: [GenomicEntity](GenomicEntity.md) - an entity that can either be directly located on a genome (gene, transcript, exon, regulatory region) or is encoded in a genome (protein)

## Uses Mixins

 *  mixin: [GeneProductMixin](GeneProductMixin.md) - The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.

## Children

 * [ProteinIsoform](ProteinIsoform.md) - Represents a protein that is a specific isoform of the canonical or reference protein. See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4114032/

## Referenced by class


## Attributes


### Inherited from genomic entity:

 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [has attribute](has_attribute.md)  <sub>0..*</sub>
     * Description: connects any entity to an attribute
     * range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [has biological sequence](has_biological_sequence.md)  <sub>OPT</sub>
     * Description: connects a genomic feature to its sequence
     * range: [BiologicalSequence](types/BiologicalSequence.md)
 * [id](id.md)  <sub>REQ</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>OPT</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [name](name.md)  <sub>OPT</sub>
     * Description: A human-readable name for an attribute or entity.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..*</sub>
     * range: [NamedThing](NamedThing.md)
 * [provided by](provided_by.md)  <sub>0..*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * range: [Agent](Agent.md)
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [type](type.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

### Mixed in from gene product mixin:

 * [synonym](synonym.md)  <sub>0..*</sub>
     * Description: Alternate human-readable names for a thing
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)

### Mixed in from gene product mixin:

 * [xref](xref.md)  <sub>0..*</sub>
     * Description: Alternate CURIEs for a thing
     * range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | polypeptide |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | PR:000000001 |
|  | | SIO:010043 |
|  | | WIKIDATA:Q8054 |
|  | | SO:0000104 |
|  | | UMLSSC:T087 |
|  | | UMLSST:amas |
| **Broad Mappings:** | | UMLSSC:T116 |
|  | | UMLSST:aapp |

