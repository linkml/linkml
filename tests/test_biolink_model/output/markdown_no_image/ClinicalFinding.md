
# Class: clinical finding


this category is currently considered broad enough to tag clinical lab measurements and other biological attributes taken as 'clinical traits' with some statistical score, for example, a p value in genetic associations.

URI: [biolink:ClinicalFinding](https://w3id.org/biolink/vocab/ClinicalFinding)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PhenotypicFeature],[OrganismTaxon],[NamedThing],[ClinicalAttribute]<has%20attribute%200..*-++[ClinicalFinding&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[PhenotypicFeature]^-[ClinicalFinding],[ClinicalAttribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[PhenotypicFeature],[OrganismTaxon],[NamedThing],[ClinicalAttribute]<has%20attribute%200..*-++[ClinicalFinding&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[PhenotypicFeature]^-[ClinicalFinding],[ClinicalAttribute],[Agent])

## Identifier prefixes

 * LOINC
 * NCIT
 * EFO

## Parents

 *  is_a: [PhenotypicFeature](PhenotypicFeature.md)

## Referenced by Class


## Attributes


### Own

 * [clinical finding➞has attribute](clinical_finding_has_attribute.md)  <sub>0..\*</sub>
     * Range: [ClinicalAttribute](ClinicalAttribute.md)

### Inherited from phenotypic feature:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [type](type.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
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
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Range: [NamedThing](NamedThing.md)
