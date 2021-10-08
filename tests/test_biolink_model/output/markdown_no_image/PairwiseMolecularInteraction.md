
# Class: pairwise molecular interaction


An interaction at the molecular level between two physical entities

URI: [biolink:PairwiseMolecularInteraction](https://w3id.org/biolink/vocab/PairwiseMolecularInteraction)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[MolecularEntity]<object%201..1-%20[PairwiseMolecularInteraction&#124;id:string;predicate:predicate_type;relation:uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[MolecularEntity]<subject%201..1-%20[PairwiseMolecularInteraction],[OntologyClass]<interacting%20molecules%20category%200..1-++[PairwiseMolecularInteraction],[PairwiseGeneToGeneInteraction]^-[PairwiseMolecularInteraction],[PairwiseGeneToGeneInteraction],[OntologyClass],[MolecularEntity],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[MolecularEntity]<object%201..1-%20[PairwiseMolecularInteraction&#124;id:string;predicate:predicate_type;relation:uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[MolecularEntity]<subject%201..1-%20[PairwiseMolecularInteraction],[OntologyClass]<interacting%20molecules%20category%200..1-++[PairwiseMolecularInteraction],[PairwiseGeneToGeneInteraction]^-[PairwiseMolecularInteraction],[PairwiseGeneToGeneInteraction],[OntologyClass],[MolecularEntity],[Attribute],[Agent])

## Parents

 *  is_a: [PairwiseGeneToGeneInteraction](PairwiseGeneToGeneInteraction.md) - An interaction between two genes or two gene products. May be physical (e.g. protein binding) or genetic (between genes). May be symmetric (e.g. protein interaction) or directed (e.g. phosphorylation)

## Referenced by Class


## Attributes


### Own

 * [interacting molecules category](interacting_molecules_category.md)  <sub>0..1</sub>
     * Range: [OntologyClass](OntologyClass.md)
     * Example: MI:1048 smallmolecule-protein
 * [pairwise molecular interaction➞subject](pairwise_molecular_interaction_subject.md)  <sub>1..1</sub>
     * Description: connects an association to the subject of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
     * Range: [MolecularEntity](MolecularEntity.md)
 * [pairwise molecular interaction➞id](pairwise_molecular_interaction_id.md)  <sub>1..1</sub>
     * Description: identifier for the interaction. This may come from an interaction database such as IMEX.
     * Range: [String](types/String.md)
     * Example: WB:WBInteraction000538741 None
     * in subsets: (translator_minimal)
 * [pairwise molecular interaction➞predicate](pairwise_molecular_interaction_predicate.md)  <sub>1..1</sub>
     * Description: A high-level grouping for the relationship type. AKA minimal predicate. This is analogous to category for nodes.
     * Range: [PredicateType](types/PredicateType.md)
 * [pairwise molecular interaction➞relation](pairwise_molecular_interaction_relation.md)  <sub>1..1</sub>
     * Description: interaction relationship type
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * Example: RO:0002447 the subject molecular phosphorylates the object molecule
 * [pairwise molecular interaction➞object](pairwise_molecular_interaction_object.md)  <sub>1..1</sub>
     * Description: connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
     * Range: [MolecularEntity](MolecularEntity.md)

### Inherited from pairwise gene to gene interaction:

 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
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
 * [negated](negated.md)  <sub>0..1</sub>
     * Description: if set to true, then the association is negated i.e. is not true
     * Range: [Boolean](types/Boolean.md)
 * [qualifiers](qualifiers.md)  <sub>0..\*</sub>
     * Description: connects an association to qualifiers that modify or qualify the meaning of that association
     * Range: [OntologyClass](OntologyClass.md)
 * [publications](publications.md)  <sub>0..\*</sub>
     * Description: connects an association to publications supporting the association
     * Range: [Publication](Publication.md)
 * [association➞type](association_type.md)  <sub>0..1</sub>
     * Description: rdf:type of biolink:Association should be fixed at rdf:Statement
     * Range: [String](types/String.md)
 * [association➞category](association_category.md)  <sub>0..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [CategoryType](types/CategoryType.md)
     * in subsets: (translator_minimal)
