
# Class: GeneToGeneProductRelationship


A gene is transcribed and potentially translated to a gene product

URI: [biolink:GeneToGeneProductRelationship](https://w3id.org/biolink/vocab/GeneToGeneProductRelationship)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SequenceFeatureRelationship],[Publication],[OntologyClass],[GeneProductMixin]<object%201..1-++[GeneToGeneProductRelationship&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Gene]<subject%201..1-%20[GeneToGeneProductRelationship],[SequenceFeatureRelationship]^-[GeneToGeneProductRelationship],[GeneProductMixin],[Gene],[Attribute],[Agent])

## Parents

 *  is_a: [SequenceFeatureRelationship](SequenceFeatureRelationship.md) - For example, a particular exon is part of a particular transcript or gene

## Referenced by class


## Attributes


### Own

 * [gene to gene product relationship➞object](gene_to_gene_product_relationship_object.md)  <sub>REQ</sub>
     * range: [GeneProductMixin](GeneProductMixin.md)
 * [gene to gene product relationship➞predicate](gene_to_gene_product_relationship_predicate.md)  <sub>REQ</sub>
     * range: [PredicateType](types/PredicateType.md)
 * [gene to gene product relationship➞subject](gene_to_gene_product_relationship_subject.md)  <sub>REQ</sub>
     * range: [Gene](Gene.md)

### Inherited from sequence feature relationship:

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
