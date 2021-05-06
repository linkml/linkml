
# Class: Snv


SNVs are single nucleotide positions in genomic DNA at which different sequence alternatives exist

URI: [biolink:Snv](https://w3id.org/biolink/vocab/Snv)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SequenceVariant]^-[Snv&#124;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[SequenceVariant],[OrganismTaxon],[NamedThing],[Gene],[Attribute],[Agent])

## Parents

 *  is_a: [SequenceVariant](SequenceVariant.md) - An allele that varies in its sequence from what is considered the reference allele at that locus.

## Attributes


### Inherited from sequence variant:

 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [has attribute](has_attribute.md)  <sub>0..*</sub>
     * Description: connects any entity to an attribute
     * range: [Attribute](Attribute.md)
     * in subsets: (samples)
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
 * [sequence variant➞has biological sequence](sequence_variant_has_biological_sequence.md)  <sub>OPT</sub>
     * Description: The state of the sequence w.r.t a reference sequence
     * range: [BiologicalSequence](types/BiologicalSequence.md)
 * [sequence variant➞has gene](sequence_variant_has_gene.md)  <sub>0..*</sub>
     * Description: Each allele can be associated with any number of genes
     * range: [Gene](Gene.md)
 * [sequence variant➞id](sequence_variant_id.md)  <sub>REQ</sub>
     * range: [String](types/String.md)
     * Example:    
     * Example:    
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [type](type.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | single nucleotide variant |
|  | | single nucleotide polymorphism |
|  | | snp |
| **Exact Mappings:** | | SO:0001483 |

