
# Class: anatomical entity to anatomical entity ontogenic association


A relationship between two anatomical entities where the relationship is ontogenic, i.e. the two entities are related by development. A number of different relationship types can be used to specify the precise nature of the relationship.

URI: [biolink:AnatomicalEntityToAnatomicalEntityOntogenicAssociation](https://w3id.org/biolink/vocab/AnatomicalEntityToAnatomicalEntityOntogenicAssociation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[Attribute],[AnatomicalEntity]<object%201..1-%20[AnatomicalEntityToAnatomicalEntityOntogenicAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[AnatomicalEntity]<subject%201..1-%20[AnatomicalEntityToAnatomicalEntityOntogenicAssociation],[AnatomicalEntityToAnatomicalEntityAssociation]^-[AnatomicalEntityToAnatomicalEntityOntogenicAssociation],[AnatomicalEntityToAnatomicalEntityAssociation],[AnatomicalEntity],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[Attribute],[AnatomicalEntity]<object%201..1-%20[AnatomicalEntityToAnatomicalEntityOntogenicAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[AnatomicalEntity]<subject%201..1-%20[AnatomicalEntityToAnatomicalEntityOntogenicAssociation],[AnatomicalEntityToAnatomicalEntityAssociation]^-[AnatomicalEntityToAnatomicalEntityOntogenicAssociation],[AnatomicalEntityToAnatomicalEntityAssociation],[AnatomicalEntity],[Agent])

## Parents

 *  is_a: [AnatomicalEntityToAnatomicalEntityAssociation](AnatomicalEntityToAnatomicalEntityAssociation.md)

## Referenced by Class


## Attributes


### Own

 * [anatomical entity to anatomical entity ontogenic association➞subject](anatomical_entity_to_anatomical_entity_ontogenic_association_subject.md)  <sub>1..1</sub>
     * Description: the structure at a later time
     * Range: [AnatomicalEntity](AnatomicalEntity.md)
 * [anatomical entity to anatomical entity ontogenic association➞object](anatomical_entity_to_anatomical_entity_ontogenic_association_object.md)  <sub>1..1</sub>
     * Description: the structure at an earlier time
     * Range: [AnatomicalEntity](AnatomicalEntity.md)
 * [anatomical entity to anatomical entity ontogenic association➞predicate](anatomical_entity_to_anatomical_entity_ontogenic_association_predicate.md)  <sub>1..1</sub>
     * Range: [PredicateType](types/PredicateType.md)

### Inherited from anatomical entity to anatomical entity association:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
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
 * [relation](relation.md)  <sub>1..1</sub>
     * Description: The relation which describes an association between a subject and an object in a more granular manner. Usually this is a term from Relation Ontology, but it can be any edge CURIE.
     * Range: [Uriorcurie](types/Uriorcurie.md)
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
     * Range: [CategoryType](types/CategoryType.md)
