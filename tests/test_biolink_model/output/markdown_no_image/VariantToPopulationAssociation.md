
# Class: variant to population association


An association between a variant and a population, where the variant has particular frequency in the population

URI: [biolink:VariantToPopulationAssociation](https://w3id.org/biolink/vocab/VariantToPopulationAssociation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PopulationOfIndividualOrganisms]<object%201..1-%20[VariantToPopulationAssociation&#124;has_quotient:double%20%3F;has_count:integer%20%3F;has_total:integer%20%3F;has_percentage:double%20%3F;frequency_qualifier:frequency_value%20%3F;predicate(i):predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[SequenceVariant]<subject%201..1-%20[VariantToPopulationAssociation],[VariantToPopulationAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPopulationAssociation]uses%20-.->[FrequencyQuantifier],[VariantToPopulationAssociation]uses%20-.->[FrequencyQualifierMixin],[Association]^-[VariantToPopulationAssociation],[VariantToEntityAssociationMixin],[SequenceVariant],[Publication],[PopulationOfIndividualOrganisms],[OntologyClass],[FrequencyQuantifier],[FrequencyQualifierMixin],[Attribute],[Association],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[PopulationOfIndividualOrganisms]<object%201..1-%20[VariantToPopulationAssociation&#124;has_quotient:double%20%3F;has_count:integer%20%3F;has_total:integer%20%3F;has_percentage:double%20%3F;frequency_qualifier:frequency_value%20%3F;predicate(i):predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[SequenceVariant]<subject%201..1-%20[VariantToPopulationAssociation],[VariantToPopulationAssociation]uses%20-.->[VariantToEntityAssociationMixin],[VariantToPopulationAssociation]uses%20-.->[FrequencyQuantifier],[VariantToPopulationAssociation]uses%20-.->[FrequencyQualifierMixin],[Association]^-[VariantToPopulationAssociation],[VariantToEntityAssociationMixin],[SequenceVariant],[Publication],[PopulationOfIndividualOrganisms],[OntologyClass],[FrequencyQuantifier],[FrequencyQualifierMixin],[Attribute],[Association],[Agent])

## Parents

 *  is_a: [Association](Association.md) - A typed association between two entities, supported by evidence

## Uses Mixin

 *  mixin: [VariantToEntityAssociationMixin](VariantToEntityAssociationMixin.md)
 *  mixin: [FrequencyQuantifier](FrequencyQuantifier.md)
 *  mixin: [FrequencyQualifierMixin](FrequencyQualifierMixin.md) - Qualifier for frequency type associations

## Referenced by Class


## Attributes


### Own

 * [variant to population association➞subject](variant_to_population_association_subject.md)  <sub>1..1</sub>
     * Description: an allele that has a certain frequency in a given population
     * Range: [SequenceVariant](SequenceVariant.md)
     * Example: NC_000017.11:g.43051071A>T 17:41203088 A/C in gnomad
 * [variant to population association➞object](variant_to_population_association_object.md)  <sub>1..1</sub>
     * Description: the population that is observed to have the frequency
     * Range: [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md)
     * Example: HANCESTRO:0010 African
 * [variant to population association➞has quotient](variant_to_population_association_has_quotient.md)  <sub>0..1</sub>
     * Description: frequency of allele in population, expressed as a number with allele divided by number in reference population, aka allele frequency
     * Range: [Double](types/Double.md)
     * Example: 0.0001666 None
 * [variant to population association➞has count](variant_to_population_association_has_count.md)  <sub>0..1</sub>
     * Description: number in object population that carry a particular allele, aka allele count
     * Range: [Integer](types/Integer.md)
     * Example: 4 4 individuals in gnomad set
 * [variant to population association➞has total](variant_to_population_association_has_total.md)  <sub>0..1</sub>
     * Description: number all populations that carry a particular allele, aka allele number
     * Range: [Integer](types/Integer.md)
     * Example: 24014 24014 individuals in gnomad set

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
 * [predicate](predicate.md)  <sub>1..1</sub>
     * Description: A high-level grouping for the relationship type. AKA minimal predicate. This is analogous to category for nodes.
     * Range: [PredicateType](types/PredicateType.md)
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
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [CategoryType](types/CategoryType.md)
     * in subsets: (translator_minimal)

### Mixed in from frequency quantifier:

 * [has percentage](has_percentage.md)  <sub>0..1</sub>
     * Description: equivalent to has quotient multiplied by 100
     * Range: [Double](types/Double.md)

### Mixed in from frequency qualifier mixin:

 * [frequency qualifier](frequency_qualifier.md)  <sub>0..1</sub>
     * Description: a qualifier used in a phenotypic association to state how frequent the phenotype is observed in the subject
     * Range: [FrequencyValue](types/FrequencyValue.md)
