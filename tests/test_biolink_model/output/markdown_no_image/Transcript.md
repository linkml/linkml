
# Class: transcript


An RNA synthesized on a DNA or RNA template by an RNA polymerase.

URI: [biolink:Transcript](https://w3id.org/biolink/vocab/Transcript)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TranscriptToGeneRelationship],[ExonToTranscriptRelationship]-%20object%201..1>[Transcript&#124;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[TranscriptToGeneRelationship]-%20subject%201..1>[Transcript],[Transcript]^-[RNAProduct],[GenomicEntity]^-[Transcript],[Protein],[OrganismTaxon],[NamedThing],[MolecularEntity],[GenomicEntity],[Gene],[ExonToTranscriptRelationship],[Attribute],[Agent],[RNAProduct])](https://yuml.me/diagram/nofunky;dir:TB/class/[TranscriptToGeneRelationship],[ExonToTranscriptRelationship]-%20object%201..1>[Transcript&#124;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[TranscriptToGeneRelationship]-%20subject%201..1>[Transcript],[Transcript]^-[RNAProduct],[GenomicEntity]^-[Transcript],[Protein],[OrganismTaxon],[NamedThing],[MolecularEntity],[GenomicEntity],[Gene],[ExonToTranscriptRelationship],[Attribute],[Agent],[RNAProduct])

## Identifier prefixes

 * ENSEMBL
 * FB

## Parents

 *  is_a: [GenomicEntity](GenomicEntity.md) - an entity that can either be directly located on a genome (gene, transcript, exon, regulatory region) or is encoded in a genome (protein)

## Children

 * [RNAProduct](RNAProduct.md)

## Referenced by Class

 *  **[MolecularEntity](MolecularEntity.md)** *[affects splicing of](affects_splicing_of.md)*  <sub>0..\*</sub>  **[Transcript](Transcript.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases splicing of](decreases_splicing_of.md)*  <sub>0..\*</sub>  **[Transcript](Transcript.md)**
 *  **[ExonToTranscriptRelationship](ExonToTranscriptRelationship.md)** *[exon to transcript relationship➞object](exon_to_transcript_relationship_object.md)*  <sub>1..1</sub>  **[Transcript](Transcript.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases splicing of](increases_splicing_of.md)*  <sub>0..\*</sub>  **[Transcript](Transcript.md)**
 *  **[Gene](Gene.md)** *[transcribed to](transcribed_to.md)*  <sub>0..\*</sub>  **[Transcript](Transcript.md)**
 *  **[TranscriptToGeneRelationship](TranscriptToGeneRelationship.md)** *[transcript to gene relationship➞subject](transcript_to_gene_relationship_subject.md)*  <sub>1..1</sub>  **[Transcript](Transcript.md)**
 *  **[Protein](Protein.md)** *[translation of](translation_of.md)*  <sub>0..\*</sub>  **[Transcript](Transcript.md)**

## Attributes


### Inherited from genomic entity:

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
     * Range: [NamedThing](NamedThing.md)
 * [has biological sequence](has_biological_sequence.md)  <sub>0..1</sub>
     * Description: connects a genomic feature to its sequence
     * Range: [BiologicalSequence](types/BiologicalSequence.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | SO:0000673 |
|  | | SIO:010450 |
|  | | WIKIDATA:Q7243183 |

