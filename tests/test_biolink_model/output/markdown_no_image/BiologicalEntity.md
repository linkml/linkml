
# Class: BiologicalEntity




URI: [biolink:BiologicalEntity](https://w3id.org/biolink/vocab/BiologicalEntity)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[OrganismalEntity],[NamedThing],[MolecularEntity],[EpidemiologicalOutcome],[DiseaseOrPhenotypicFeature],[BiologicalProcessOrActivity],[BiologicalEntity&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]^-[OrganismalEntity],[BiologicalEntity]^-[MolecularEntity],[BiologicalEntity]^-[EpidemiologicalOutcome],[BiologicalEntity]^-[DiseaseOrPhenotypicFeature],[BiologicalEntity]^-[BiologicalProcessOrActivity],[NamedThing]^-[BiologicalEntity],[Attribute],[Agent])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Children

 * [BiologicalProcessOrActivity](BiologicalProcessOrActivity.md) - Either an individual molecular activity, or a collection of causally connected molecular activities in a biological system.
 * [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md) - Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.
 * [EpidemiologicalOutcome](EpidemiologicalOutcome.md) - An epidemiological outcome, such as societal disease burden, resulting from an exposure event.
 * [MolecularEntity](MolecularEntity.md) - A gene, gene product, small molecule or macromolecule (including protein complex)"
 * [OrganismalEntity](OrganismalEntity.md) - A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding molecular entities

## Referenced by class


## Attributes


### Inherited from named thing:

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

## Other properties

|  |  |  |
| --- | --- | --- |
| **Narrow Mappings:** | | WIKIDATA:Q28845870 |
|  | | UMLSSC:T050 |
|  | | UMLSST:emod |
|  | | SIO:010046 |

