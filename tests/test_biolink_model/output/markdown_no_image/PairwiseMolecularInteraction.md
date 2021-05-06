
# Class: PairwiseMolecularInteraction


An interaction at the molecular level between two physical entities

URI: [biolink:PairwiseMolecularInteraction](https://w3id.org/biolink/vocab/PairwiseMolecularInteraction)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[MolecularEntity]<object%201..1-%20[PairwiseMolecularInteraction&#124;id:string;predicate:predicate_type;relation:uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[MolecularEntity]<subject%201..1-%20[PairwiseMolecularInteraction],[OntologyClass]<interacting%20molecules%20category%200..1-++[PairwiseMolecularInteraction],[PairwiseGeneToGeneInteraction]^-[PairwiseMolecularInteraction],[PairwiseGeneToGeneInteraction],[OntologyClass],[MolecularEntity],[Attribute],[Agent])

## Parents

 *  is_a: [PairwiseGeneToGeneInteraction](PairwiseGeneToGeneInteraction.md) - An interaction between two genes or two gene products. May be physical (e.g. protein binding) or genetic (between genes). May be symmetric (e.g. protein interaction) or directed (e.g. phosphorylation)

## Referenced by class


## Attributes


### Own

 * [interacting molecules category](interacting_molecules_category.md)  <sub>OPT</sub>
     * range: [OntologyClass](OntologyClass.md)
     * Example: MI:1048 smallmolecule-protein
 * [pairwise molecular interaction➞id](pairwise_molecular_interaction_id.md)  <sub>REQ</sub>
     * Description: identifier for the interaction. This may come from an interaction database such as IMEX.
     * range: [String](types/String.md)
     * Example:    
 * [pairwise molecular interaction➞object](pairwise_molecular_interaction_object.md)  <sub>REQ</sub>
     * range: [MolecularEntity](MolecularEntity.md)
 * [pairwise molecular interaction➞predicate](pairwise_molecular_interaction_predicate.md)  <sub>REQ</sub>
     * range: [PredicateType](types/PredicateType.md)
 * [pairwise molecular interaction➞relation](pairwise_molecular_interaction_relation.md)  <sub>REQ</sub>
     * Description: interaction relationship type
     * range: [Uriorcurie](types/Uriorcurie.md)
     * Example:    
 * [pairwise molecular interaction➞subject](pairwise_molecular_interaction_subject.md)  <sub>REQ</sub>
     * range: [MolecularEntity](MolecularEntity.md)

### Inherited from pairwise gene to gene interaction:

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
