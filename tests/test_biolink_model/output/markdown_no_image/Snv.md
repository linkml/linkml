
# Class: snv


SNVs are single nucleotide positions in genomic DNA at which different sequence alternatives exist

URI: [biolink:Snv](https://w3id.org/biolink/vocab/Snv)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SequenceVariant]^-[Snv&#124;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[SequenceVariant],[OrganismTaxon],[NamedThing],[Gene],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[SequenceVariant]^-[Snv&#124;has_biological_sequence(i):biological_sequence%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[SequenceVariant],[OrganismTaxon],[NamedThing],[Gene],[Attribute],[Agent])

## Parents

 *  is_a: [SequenceVariant](SequenceVariant.md) - An allele that varies in its sequence from what is considered the reference allele at that locus.

## Attributes


### Inherited from sequence variant:

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
 * [sequence variant➞has gene](sequence_variant_has_gene.md)  <sub>0..\*</sub>
     * Description: Each allele can be associated with any number of genes
     * Range: [Gene](Gene.md)
 * [sequence variant➞has biological sequence](sequence_variant_has_biological_sequence.md)  <sub>0..1</sub>
     * Description: The state of the sequence w.r.t a reference sequence
     * Range: [BiologicalSequence](types/BiologicalSequence.md)
 * [sequence variant➞id](sequence_variant_id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * Example: ZFIN:ZDB-ALT-980203-1091 ti282a allele from ZFIN
     * Example: ClinVarVariant:17681 NM_007294.3(BRCA1):c.2521C>T (p.Arg841Trp)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | single nucleotide variant |
|  | | single nucleotide polymorphism |
|  | | snp |
| **Exact Mappings:** | | SO:0001483 |

