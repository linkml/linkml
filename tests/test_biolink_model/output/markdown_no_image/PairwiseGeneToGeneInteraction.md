
# Class: PairwiseGeneToGeneInteraction


An interaction between two genes or two gene products. May be physical (e.g. protein binding) or genetic (between genes). May be symmetric (e.g. protein interaction) or directed (e.g. phosphorylation)

URI: [biolink:PairwiseGeneToGeneInteraction](https://w3id.org/biolink/vocab/PairwiseGeneToGeneInteraction)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[PairwiseMolecularInteraction],[PairwiseGeneToGeneInteraction&#124;predicate:predicate_type;relation:uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]^-[PairwiseMolecularInteraction],[GeneToGeneAssociation]^-[PairwiseGeneToGeneInteraction],[OntologyClass],[GeneToGeneAssociation],[GeneOrGeneProduct],[Attribute],[Agent])

## Parents

 *  is_a: [GeneToGeneAssociation](GeneToGeneAssociation.md) - abstract parent class for different kinds of gene-gene or gene product to gene product relationships. Includes homology and interaction.

## Children

 * [PairwiseMolecularInteraction](PairwiseMolecularInteraction.md) - An interaction at the molecular level between two physical entities

## Referenced by class


## Attributes


### Own

 * [pairwise gene to gene interaction➞predicate](pairwise_gene_to_gene_interaction_predicate.md)  <sub>REQ</sub>
     * range: [PredicateType](types/PredicateType.md)
 * [pairwise gene to gene interaction➞relation](pairwise_gene_to_gene_interaction_relation.md)  <sub>REQ</sub>
     * Description: interaction relationship type
     * range: [Uriorcurie](types/Uriorcurie.md)

### Inherited from gene to gene association:

 * [association➞category](association_category.md)  <sub>0..*</sub>
     * range: [CategoryType](types/CategoryType.md)
 * [association➞type](association_type.md)  <sub>OPT</sub>
     * Description: rdf:type of biolink:Association should be fixed at rdf:Statement
     * range: [String](types/String.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [gene to gene association➞object](gene_to_gene_association_object.md)  <sub>REQ</sub>
     * Description: the object gene in the association. If the relation is symmetric, subject vs object is arbitrary. We allow a gene product to stand as a proxy for the gene or vice versa.
     * range: [GeneOrGeneProduct](GeneOrGeneProduct.md)
 * [gene to gene association➞subject](gene_to_gene_association_subject.md)  <sub>REQ</sub>
     * Description: the subject gene in the association. If the relation is symmetric, subject vs object is arbitrary. We allow a gene product to stand as a proxy for the gene or vice versa.
     * range: [GeneOrGeneProduct](GeneOrGeneProduct.md)
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
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
