
# Class: protein isoform


Represents a protein that is a specific isoform of the canonical or reference protein. See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4114032/

URI: [biolink:ProteinIsoform](https://w3id.org/biolink/vocab/ProteinIsoform)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ProteinIsoform&#124;synonym(i):label_type%20*;xref(i):iri_type%20*;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[GeneProductIsoformMixin],[Protein]^-[ProteinIsoform],[Protein],[OrganismTaxon],[NamedThing],[GeneProductIsoformMixin],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[ProteinIsoform&#124;synonym(i):label_type%20*;xref(i):iri_type%20*;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[GeneProductIsoformMixin],[Protein]^-[ProteinIsoform],[Protein],[OrganismTaxon],[NamedThing],[GeneProductIsoformMixin],[Attribute],[Agent])

## Identifier prefixes

 * UniProtKB
 * UNIPROT.ISOFORM
 * PR
 * ENSEMBL

## Parents

 *  is_a: [Protein](Protein.md) - A gene product that is composed of a chain of amino acid sequences and is produced by ribosome-mediated translation of mRNA

## Uses Mixin

 *  mixin: [GeneProductIsoformMixin](GeneProductIsoformMixin.md) - This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene product is intended to represent a specific isoform rather than a canonical or reference or generic product. The designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.

## Attributes


### Inherited from protein:

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
| **Aliases:** | | proteoform |

