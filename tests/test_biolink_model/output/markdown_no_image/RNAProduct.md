
# Class: RNA product




URI: [biolink:RNAProduct](https://w3id.org/biolink/vocab/RNAProduct)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Transcript],[OrganismTaxon],[NoncodingRNAProduct],[NamedThing],[GeneProductMixin],[Attribute],[Agent],[RNAProductIsoform],[RNAProduct&#124;synonym:label_type%20*;xref:iri_type%20*;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[GeneProductMixin],[RNAProduct]^-[NoncodingRNAProduct],[RNAProduct]^-[RNAProductIsoform],[Transcript]^-[RNAProduct])](https://yuml.me/diagram/nofunky;dir:TB/class/[Transcript],[OrganismTaxon],[NoncodingRNAProduct],[NamedThing],[GeneProductMixin],[Attribute],[Agent],[RNAProductIsoform],[RNAProduct&#124;synonym:label_type%20*;xref:iri_type%20*;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[GeneProductMixin],[RNAProduct]^-[NoncodingRNAProduct],[RNAProduct]^-[RNAProductIsoform],[Transcript]^-[RNAProduct])

## Identifier prefixes

 * RNACENTRAL

## Parents

 *  is_a: [Transcript](Transcript.md) - An RNA synthesized on a DNA or RNA template by an RNA polymerase.

## Uses Mixin

 *  mixin: [GeneProductMixin](GeneProductMixin.md) - The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.

## Children

 * [RNAProductIsoform](RNAProductIsoform.md) - Represents a protein that is a specific isoform of the canonical or reference RNA
 * [NoncodingRNAProduct](NoncodingRNAProduct.md)

## Referenced by Class


## Attributes


### Inherited from transcript:

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

### Mixed in from gene product mixin:

 * [synonym](synonym.md)  <sub>0..\*</sub>
     * Description: Alternate human-readable names for a thing
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)

### Mixed in from gene product mixin:

 * [xref](xref.md)  <sub>0..\*</sub>
     * Description: Alternate CURIEs for a thing
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | CHEBI:33697 |
|  | | WIKIDATA:Q11053 |

