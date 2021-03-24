
# Class: GenotypeToPhenotypicFeatureAssociation


Any association between one genotype and a phenotypic feature, where having the genotype confers the phenotype, either in isolation or through environment

URI: [biolink:GenotypeToPhenotypicFeatureAssociation](https://w3id.org/biolink/vocab/GenotypeToPhenotypicFeatureAssociation)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SeverityValue],[Publication],[OntologyClass],[Onset],[NamedThing],[Genotype]<subject%201..1-%20[GenotypeToPhenotypicFeatureAssociation&#124;predicate:predicate_type;frequency_qualifier:frequency_value%20%3F;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GenotypeToPhenotypicFeatureAssociation]uses%20-.->[EntityToPhenotypicFeatureAssociationMixin],[GenotypeToPhenotypicFeatureAssociation]uses%20-.->[GenotypeToEntityAssociationMixin],[Association]^-[GenotypeToPhenotypicFeatureAssociation],[GenotypeToEntityAssociationMixin],[Genotype],[EntityToPhenotypicFeatureAssociationMixin],[BiologicalSex],[Attribute],[Association],[Agent])

## Parents

 *  is_a: [Association](Association.md) - A typed association between two entities, supported by evidence

## Uses Mixins

 *  mixin: [EntityToPhenotypicFeatureAssociationMixin](EntityToPhenotypicFeatureAssociationMixin.md)
 *  mixin: [GenotypeToEntityAssociationMixin](GenotypeToEntityAssociationMixin.md)

## Referenced by class


## Attributes


### Own

 * [genotype to phenotypic feature association➞predicate](genotype_to_phenotypic_feature_association_predicate.md)  <sub>REQ</sub>
     * range: [PredicateType](types/PredicateType.md)
 * [genotype to phenotypic feature association➞subject](genotype_to_phenotypic_feature_association_subject.md)  <sub>REQ</sub>
     * Description: genotype that is associated with the phenotypic feature
     * range: [Genotype](Genotype.md)

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

### Mixed in from frequency qualifier mixin:

 * [frequency qualifier](frequency_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state how frequent the phenotype is observed in the subject
     * range: [FrequencyValue](types/FrequencyValue.md)

### Mixed in from entity to feature or disease qualifiers mixin:

 * [onset qualifier](onset_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state when the phenotype appears is in the subject
     * range: [Onset](Onset.md)

### Mixed in from entity to feature or disease qualifiers mixin:

 * [severity qualifier](severity_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state how severe the phenotype is in the subject
     * range: [SeverityValue](SeverityValue.md)

### Mixed in from entity to phenotypic feature association mixin:

 * [sex qualifier](sex_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state whether the association is specific to a particular sex.
     * range: [BiologicalSex](BiologicalSex.md)
