
# Class: ExposureEventToOutcomeAssociation


An association between an exposure event and an outcome.

URI: [biolink:ExposureEventToOutcomeAssociation](https://w3id.org/biolink/vocab/ExposureEventToOutcomeAssociation)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[PopulationOfIndividualOrganisms],[OntologyClass],[NamedThing],[PopulationOfIndividualOrganisms]<has%20population%20context%200..1-%20[ExposureEventToOutcomeAssociation&#124;has_temporal_context:time_type%20%3F;predicate(i):predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[ExposureEventToOutcomeAssociation]uses%20-.->[ExposureEventToEntityAssociationMixin],[ExposureEventToOutcomeAssociation]uses%20-.->[EntityToOutcomeAssociationMixin],[Association]^-[ExposureEventToOutcomeAssociation],[ExposureEventToEntityAssociationMixin],[EntityToOutcomeAssociationMixin],[Attribute],[Association],[Agent])

## Parents

 *  is_a: [Association](Association.md) - A typed association between two entities, supported by evidence

## Uses Mixins

 *  mixin: [ExposureEventToEntityAssociationMixin](ExposureEventToEntityAssociationMixin.md) - An association between some exposure event and some entity.
 *  mixin: [EntityToOutcomeAssociationMixin](EntityToOutcomeAssociationMixin.md) - An association between some entity and an outcome

## Attributes


### Own

 * [has population context](has_population_context.md)  <sub>OPT</sub>
     * Description: a biological population (general, study, cohort, etc.) with a specific set of characteristics to constrain an association.
     * range: [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md)
 * [has temporal context](has_temporal_context.md)  <sub>OPT</sub>
     * Description: a constraint of time placed upon the truth value of an association.
     * range: [TimeType](types/TimeType.md)

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
 * [object](object.md)  <sub>REQ</sub>
     * Description: connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
     * range: [NamedThing](NamedThing.md)
 * [predicate](predicate.md)  <sub>REQ</sub>
     * Description: A high-level grouping for the relationship type. AKA minimal predicate. This is analogous to category for nodes.
     * range: [PredicateType](types/PredicateType.md)
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
 * [subject](subject.md)  <sub>REQ</sub>
     * Description: connects an association to the subject of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.
     * range: [NamedThing](NamedThing.md)
