
# Class: PopulationToPopulationAssociation


An association between a two populations

URI: [biolink:PopulationToPopulationAssociation](https://w3id.org/biolink/vocab/PopulationToPopulationAssociation)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[PopulationOfIndividualOrganisms]<object%201..1-%20[PopulationToPopulationAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[PopulationOfIndividualOrganisms]<subject%201..1-%20[PopulationToPopulationAssociation],[Association]^-[PopulationToPopulationAssociation],[PopulationOfIndividualOrganisms],[OntologyClass],[Attribute],[Association],[Agent])

## Parents

 *  is_a: [Association](Association.md) - A typed association between two entities, supported by evidence

## Referenced by class


## Attributes


### Own

 * [population to population association➞object](population_to_population_association_object.md)  <sub>REQ</sub>
     * Description: the population that form the object of the association
     * range: [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md)
 * [population to population association➞predicate](population_to_population_association_predicate.md)  <sub>REQ</sub>
     * Description: A relationship type that holds between the subject and object populations. Standard mereological relations can be used. E.g. subject part-of object, subject overlaps object. Derivation relationships can also be used
     * range: [PredicateType](types/PredicateType.md)
 * [population to population association➞subject](population_to_population_association_subject.md)  <sub>REQ</sub>
     * Description: the population that form the subject of the association
     * range: [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md)

### Inherited from association:

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
