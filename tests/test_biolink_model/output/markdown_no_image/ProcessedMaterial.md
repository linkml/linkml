
# Class: ProcessedMaterial


A chemical substance (often a mixture) processed for consumption for nutritional, medical or technical use.

URI: [biolink:ProcessedMaterial](https://w3id.org/biolink/vocab/ProcessedMaterial)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[ProcessedMaterial&#124;is_metabolite(i):boolean%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[Mixture],[ProcessedMaterial]uses%20-.->[OntologyClass],[ChemicalSubstance]^-[ProcessedMaterial],[OrganismTaxon],[OntologyClass],[NamedThing],[Mixture],[ChemicalSubstance],[Attribute],[Agent])

## Parents

 *  is_a: [ChemicalSubstance](ChemicalSubstance.md) - May be a chemical entity or a formulation with a chemical entity as active ingredient, or a complex material with multiple chemical entities as part

## Uses Mixins

 *  mixin: [Mixture](Mixture.md) - The physical combination of two or more molecular entities in which the identities are retained and are mixed in the form of solutions, suspensions and colloids.
 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Attributes


### Inherited from chemical substance:

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
 * [is metabolite](is_metabolite.md)  <sub>OPT</sub>
     * Description: indicates whether a chemical substance is a metabolite
     * range: [Boolean](types/Boolean.md)
 * [name](name.md)  <sub>OPT</sub>
     * Description: A human-readable name for an attribute or entity.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..*</sub>
     * range: [NamedThing](NamedThing.md)
 * [provided by](provided_by.md)  <sub>0..*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * range: [Agent](Agent.md)
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [type](type.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

### Mixed in from mixture:

 * [has constituent](has_constituent.md)  <sub>0..*</sub>
     * Description: one or more chemical substances within a mixture
     * range: [ChemicalSubstance](ChemicalSubstance.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | OBI:0000047 |

