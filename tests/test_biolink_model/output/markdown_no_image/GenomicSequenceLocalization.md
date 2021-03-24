
# Class: GenomicSequenceLocalization


A relationship between a sequence feature and a genomic entity it is localized to. The reference entity may be a chromosome, chromosome region or information entity such as a contig.

URI: [biolink:GenomicSequenceLocalization](https://w3id.org/biolink/vocab/GenomicSequenceLocalization)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SequenceAssociation],[Publication],[OntologyClass],[GenomicEntity]<object%201..1-%20[GenomicSequenceLocalization&#124;start_interbase_coordinate:integer%20%3F;end_interbase_coordinate:integer%20%3F;genome_build:string%20%3F;strand:string%20%3F;phase:string%20%3F;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GenomicEntity]<subject%201..1-%20[GenomicSequenceLocalization],[SequenceAssociation]^-[GenomicSequenceLocalization],[GenomicEntity],[Attribute],[Agent])

## Parents

 *  is_a: [SequenceAssociation](SequenceAssociation.md) - An association between a sequence feature and a genomic entity it is localized to.

## Referenced by class


## Attributes


### Own

 * [end interbase coordinate](end_interbase_coordinate.md)  <sub>OPT</sub>
     * Description: The position at which the subject genomic entity ends on the chromosome or other entity to which it is located on.
     * range: [Integer](types/Integer.md)
 * [genome build](genome_build.md)  <sub>OPT</sub>
     * Description: The version of the genome on which a feature is located. For example, GRCh38 for Homo sapiens.
     * range: [String](types/String.md)
 * [genomic sequence localization➞object](genomic_sequence_localization_object.md)  <sub>REQ</sub>
     * range: [GenomicEntity](GenomicEntity.md)
 * [genomic sequence localization➞predicate](genomic_sequence_localization_predicate.md)  <sub>REQ</sub>
     * range: [PredicateType](types/PredicateType.md)
 * [genomic sequence localization➞subject](genomic_sequence_localization_subject.md)  <sub>REQ</sub>
     * range: [GenomicEntity](GenomicEntity.md)
 * [phase](phase.md)  <sub>OPT</sub>
     * Description: The phase for a coding sequence entity. For example, phase of a CDS as represented in a GFF3 with a value of 0, 1 or 2.
     * range: [String](types/String.md)
 * [start interbase coordinate](start_interbase_coordinate.md)  <sub>OPT</sub>
     * Description: The position at which the subject genomic entity starts on the chromosome or other entity to which it is located on.
     * range: [Integer](types/Integer.md)
 * [strand](strand.md)  <sub>OPT</sub>
     * Description: The strand on which a feature is located. Has a value of '+' (sense strand or forward strand) or '-' (anti-sense strand or reverse strand).
     * range: [String](types/String.md)

### Inherited from sequence association:

 * [association➞category](association_category.md)  <sub>0..*</sub>
     * range: [CategoryType](types/CategoryType.md)
 * [association➞type](association_type.md)  <sub>OPT</sub>
     * Description: rdf:type of biolink:Association should be fixed at rdf:Statement
     * range: [String](types/String.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [has attribute](has_attribute.md)  <sub>0..*</sub>
     * Description: connects any entity to an attribute
     * range: [Attribute](Attribute.md)
     * in subsets: (samples)
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
 * [negated](negated.md)  <sub>OPT</sub>
     * Description: if set to true, then the association is negated i.e. is not true
     * range: [Boolean](types/Boolean.md)
 * [provided by](provided_by.md)  <sub>0..*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * range: [Agent](Agent.md)
 * [publications](publications.md)  <sub>0..*</sub>
     * Description: connects an association to publications supporting the association
     * range: [Publication](Publication.md)
 * [qualifiers](qualifiers.md)  <sub>0..*</sub>
     * Description: connects an association to qualifiers that modify or qualify the meaning of that association
     * range: [OntologyClass](OntologyClass.md)
 * [relation](relation.md)  <sub>REQ</sub>
     * Description: The relation which describes an association between a subject and an object in a more granular manner. Usually this is a term from Relation Ontology, but it can be any edge CURIE.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
