
# Class: study population


A group of people banded together or treated as a group as participants in a research study.

URI: [biolink:StudyPopulation](https://w3id.org/biolink/vocab/StudyPopulation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[StudyPopulation&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]^-[Cohort],[PopulationOfIndividualOrganisms]^-[StudyPopulation],[PopulationOfIndividualOrganisms],[OrganismTaxon],[NamedThing],[Cohort],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[StudyPopulation&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]^-[Cohort],[PopulationOfIndividualOrganisms]^-[StudyPopulation],[PopulationOfIndividualOrganisms],[OrganismTaxon],[NamedThing],[Cohort],[Attribute],[Agent])

## Parents

 *  is_a: [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md) - A collection of individuals from the same taxonomic class distinguished by one or more characteristics.  Characteristics can include, but are not limited to, shared geographic location, genetics, phenotypes [Alliance for Genome Resources]

## Children

 * [Cohort](Cohort.md) - A group of people banded together or treated as a group who share common characteristics. A cohort 'study' is a particular form of longitudinal study that samples a cohort, performing a cross-section at intervals through time.

## Referenced by Class


## Attributes


### Inherited from population of individual organisms:

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
 * [organismal entity➞has attribute](organismal_entity_has_attribute.md)  <sub>0..\*</sub>
     * Description: may often be an organism attribute
     * Range: [Attribute](Attribute.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Close Mappings:** | | WIKIDATA:Q7229825 |

