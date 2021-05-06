
# Class: VariantToPopulationAssociation


An association between a variant and a population, where the variant has particular frequency in the population

URI: [biolink:VariantToPopulationAssociation](https://w3id.org/biolink/vocab/VariantToPopulationAssociation)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[PopulationOfIndividualOrganisms]<object%201..1-%20[VariantToPopulationAssociation&#124;has_quotient:double%20%3F;has_count:integer%20%3F;has_total:integer%20%3F;has_percentage:double%20%3F;frequency_qualifier:frequency_value%20%3F;predicate(i):predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[SequenceVariant]<subject%201..1-%20[VariantToPopulationAssociation],[VariantToPopulationAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPopulationAssociation]uses%20-.->[FrequencyQuantifier],[VariantToPopulationAssociation]uses%20-.->[FrequencyQualifierMixin],[Association]^-[VariantToPopulationAssociation],[VariantToEntityAssociationMixin],[SequenceVariant],[Publication],[PopulationOfIndividualOrganisms],[OntologyClass],[FrequencyQuantifier],[FrequencyQualifierMixin],[Attribute],[Association],[Agent])

## Parents

 *  is_a: [Association](Association.md) - A typed association between two entities, supported by evidence

## Uses Mixins

 *  mixin: [VariantToEntityAssociationMixin](VariantToEntityAssociationMixin.md)
 *  mixin: [FrequencyQuantifier](FrequencyQuantifier.md)
 *  mixin: [FrequencyQualifierMixin](FrequencyQualifierMixin.md) - Qualifier for frequency type associations

## Referenced by class


## Attributes


### Own

 * [variant to population association➞has count](variant_to_population_association_has_count.md)  <sub>OPT</sub>
     * Description: number in object population that carry a particular allele, aka allele count
     * range: [Integer](types/Integer.md)
     * Example:    
 * [variant to population association➞has quotient](variant_to_population_association_has_quotient.md)  <sub>OPT</sub>
     * Description: frequency of allele in population, expressed as a number with allele divided by number in reference population, aka allele frequency
     * range: [Double](types/Double.md)
     * Example:    
 * [variant to population association➞has total](variant_to_population_association_has_total.md)  <sub>OPT</sub>
     * Description: number all populations that carry a particular allele, aka allele number
     * range: [Integer](types/Integer.md)
     * Example:    
 * [variant to population association➞object](variant_to_population_association_object.md)  <sub>REQ</sub>
     * Description: the population that is observed to have the frequency
     * range: [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md)
     * Example:    
 * [variant to population association➞subject](variant_to_population_association_subject.md)  <sub>REQ</sub>
     * Description: an allele that has a certain frequency in a given population
     * range: [SequenceVariant](SequenceVariant.md)
     * Example:    

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

### Mixed in from frequency qualifier mixin:

 * [frequency qualifier](frequency_qualifier.md)  <sub>OPT</sub>
     * Description: a qualifier used in a phenotypic association to state how frequent the phenotype is observed in the subject
     * range: [FrequencyValue](types/FrequencyValue.md)

### Mixed in from frequency quantifier:

 * [has percentage](has_percentage.md)  <sub>OPT</sub>
     * Description: equivalent to has quotient multiplied by 100
     * range: [Double](types/Double.md)
