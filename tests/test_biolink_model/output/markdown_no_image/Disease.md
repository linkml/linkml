
# Class: Disease




URI: [biolink:Disease](https://w3id.org/biolink/vocab/Disease)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon],[NamedThing],[EntityToDiseaseAssociationMixin],[DiseaseToEntityAssociationMixin],[DiseaseOrPhenotypicFeature],[DiseaseToEntityAssociationMixin]-%20subject%201..1>[Disease&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[EntityToDiseaseAssociationMixin]-%20object%201..1>[Disease],[DiseaseOrPhenotypicFeature]^-[Disease],[Attribute],[Agent])

## Identifier prefixes

 * MONDO
 * DOID
 * OMIM
 * ORPHANET
 * EFO
 * UMLS
 * MESH
 * MEDDRA
 * NCIT
 * SNOMEDCT
 * medgen
 * ICD10
 * ICD9
 * ICD0
 * KEGG.DISEASE
 * HP
 * MP

## Parents

 *  is_a: [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md) - Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.

## Referenced by class

 *  **[DiseaseToEntityAssociationMixin](DiseaseToEntityAssociationMixin.md)** *[disease to entity association mixin➞subject](disease_to_entity_association_mixin_subject.md)*  <sub>REQ</sub>  **[Disease](Disease.md)**
 *  **[EntityToDiseaseAssociationMixin](EntityToDiseaseAssociationMixin.md)** *[entity to disease association mixin➞object](entity_to_disease_association_mixin_object.md)*  <sub>REQ</sub>  **[Disease](Disease.md)**
 *  **[NamedThing](NamedThing.md)** *[manifestation of](manifestation_of.md)*  <sub>0..*</sub>  **[Disease](Disease.md)**

## Attributes


### Inherited from disease or phenotypic feature:

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
| **Aliases:** | | condition |
|  | | disorder |
|  | | medical condition |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | MONDO:0000001 |
|  | | DOID:4 |
|  | | NCIT:C2991 |
|  | | WIKIDATA:Q12136 |
|  | | SIO:010299 |
|  | | UMLSSG:DISO |
|  | | UMLSSC:T047 |
|  | | UMLSST:dsyn |
| **Narrow Mappings:** | | UMLSSC:T019 |
|  | | UMLSST:cgab |
|  | | UMLSSC:T020 |
|  | | UMLSST:acab |
|  | | UMLSSC:T037 |
|  | | UMLSST:inpo |
|  | | UMLSSC:T046 |
|  | | UMLSST:patf |
|  | | UMLSSC:T048 |
|  | | UMLSST:mobd |
|  | | UMLSSC:T049 |
|  | | UMLSST:comd |
|  | | UMLSSC:T190 |
|  | | UMLSST:anab |
|  | | UMLSSC:T191 |
|  | | UMLSST:neop |

