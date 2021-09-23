
# Class: genotype to genotype part association


Any association between one genotype and a genotypic entity that is a sub-component of it

URI: [biolink:GenotypeToGenotypePartAssociation](https://w3id.org/biolink/vocab/GenotypeToGenotypePartAssociation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[Genotype]<object%201..1-%20[GenotypeToGenotypePartAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Genotype]<subject%201..1-%20[GenotypeToGenotypePartAssociation],[Association]^-[GenotypeToGenotypePartAssociation],[Genotype],[Attribute],[Association],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[Genotype]<object%201..1-%20[GenotypeToGenotypePartAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Genotype]<subject%201..1-%20[GenotypeToGenotypePartAssociation],[Association]^-[GenotypeToGenotypePartAssociation],[Genotype],[Attribute],[Association],[Agent])

## Parents

 *  is_a: [Association](Association.md) - A typed association between two entities, supported by evidence

## Referenced by Class


## Attributes


### Own

 * [genotype to genotype part association➞predicate](genotype_to_genotype_part_association_predicate.md)  <sub>1..1</sub>
     * Range: [PredicateType](types/PredicateType.md)
 * [genotype to genotype part association➞subject](genotype_to_genotype_part_association_subject.md)  <sub>1..1</sub>
     * Description: parent genotype
     * Range: [Genotype](Genotype.md)
 * [genotype to genotype part association➞object](genotype_to_genotype_part_association_object.md)  <sub>1..1</sub>
     * Description: child genotype
     * Range: [Genotype](Genotype.md)

### Inherited from association:

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
