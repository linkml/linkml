
# Class: exon


A region of the transcript sequence within a gene which is not removed from the primary RNA transcript by RNA splicing.

URI: [biolink:Exon](https://w3id.org/biolink/vocab/Exon)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon],[NamedThing],[GenomicEntity],[ExonToTranscriptRelationship],[ExonToTranscriptRelationship]-%20subject%201..1>[Exon&#124;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GenomicEntity]^-[Exon],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon],[NamedThing],[GenomicEntity],[ExonToTranscriptRelationship],[ExonToTranscriptRelationship]-%20subject%201..1>[Exon&#124;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GenomicEntity]^-[Exon],[Attribute],[Agent])

## Parents

 *  is_a: [GenomicEntity](GenomicEntity.md) - an entity that can either be directly located on a genome (gene, transcript, exon, regulatory region) or is encoded in a genome (protein)

## Referenced by Class

 *  **[ExonToTranscriptRelationship](ExonToTranscriptRelationship.md)** *[exon to transcript relationship➞subject](exon_to_transcript_relationship_subject.md)*  <sub>1..1</sub>  **[Exon](Exon.md)**

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
| **Exact Mappings:** | | SO:0000147 |
|  | | SIO:010445 |
|  | | WIKIDATA:Q373027 |

