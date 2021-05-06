
# Class: InformationContentEntity


a piece of information that typically describes some topic of discourse or is used as support.

URI: [biolink:InformationContentEntity](https://w3id.org/biolink/vocab/InformationContentEntity)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[NamedThing],[ContributorAssociation]-%20subject%201..1>[InformationContentEntity&#124;license:string%20%3F;rights:string%20%3F;format:string%20%3F;creation_date:date%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[InformationContentEntity]^-[Publication],[InformationContentEntity]^-[EvidenceType],[InformationContentEntity]^-[DatasetVersion],[InformationContentEntity]^-[DatasetSummary],[InformationContentEntity]^-[DatasetDistribution],[InformationContentEntity]^-[Dataset],[InformationContentEntity]^-[ConfidenceLevel],[NamedThing]^-[InformationContentEntity],[EvidenceType],[DatasetVersion],[DatasetSummary],[DatasetDistribution],[Dataset],[ContributorAssociation],[ConfidenceLevel],[Attribute],[Agent])

## Identifier prefixes

 * doi

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Children

 * [ConfidenceLevel](ConfidenceLevel.md) - Level of confidence in a statement
 * [Dataset](Dataset.md) - an item that refers to a collection of data from a data source.
 * [DatasetDistribution](DatasetDistribution.md) - an item that holds distribution level information about a dataset.
 * [DatasetSummary](DatasetSummary.md) - an item that holds summary level information about a dataset.
 * [DatasetVersion](DatasetVersion.md) - an item that holds version level information about a dataset.
 * [EvidenceType](EvidenceType.md) - Class of evidence that supports an association
 * [Publication](Publication.md) - Any published piece of information. Can refer to a whole publication, its encompassing publication (i.e. journal or book) or to a part of a publication, if of significant knowledge scope (e.g. a figure, figure legend, or section highlighted by NLP). The scope is intended to be general and include information published on the web, as well as printed materials, either directly or in one of the Publication Biolink category subclasses.

## Referenced by class

 *  **[ContributorAssociation](ContributorAssociation.md)** *[contributor association➞subject](contributor_association_subject.md)*  <sub>REQ</sub>  **[InformationContentEntity](InformationContentEntity.md)**

## Attributes


### Own

 * [creation date](creation_date.md)  <sub>OPT</sub>
     * Description: date on which an entity was created. This can be applied to nodes or edges
     * range: [Date](types/Date.md)
 * [format](format.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [license](license.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [rights](rights.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

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
| **Aliases:** | | information |
|  | | information artefact |
|  | | information entity |
| **Exact Mappings:** | | IAO:0000030 |
| **Narrow Mappings:** | | UMLSSG:CONC |
|  | | UMLSSC:T077 |
|  | | UMLSST:cnce |
|  | | UMLSSC:T078 |
|  | | UMLSST:idcn |
|  | | UMLSSC:T079 |
|  | | UMLSST:tmco |
|  | | UMLSSC:T080 |
|  | | UMLSST:qlco |
|  | | UMLSSC:T081 |
|  | | UMLSST:qnco |
|  | | UMLSSC:T082 |
|  | | UMLSST:spco |
|  | | UMLSSC:T089 |
|  | | UMLSST:rnlw |
|  | | UMLSSC:T102 |
|  | | UMLSST:grpa |
|  | | UMLSSC:T169 |
|  | | UMLSST:ftcn |
|  | | UMLSSC:T171 |
|  | | UMLSST:lang |
|  | | UMLSSC:T185 |
|  | | UMLSST:clas |

