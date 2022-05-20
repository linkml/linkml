
# Class: information content entity


a piece of information that typically describes some topic of discourse or is used as support.

URI: [biolink:InformationContentEntity](https://w3id.org/biolink/vocab/InformationContentEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[NamedThing],[ContributorAssociation]-%20subject%201..1>[InformationContentEntity&#124;license:string%20%3F;rights:string%20%3F;format:string%20%3F;creation_date:date%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[InformationContentEntity]^-[Publication],[InformationContentEntity]^-[EvidenceType],[InformationContentEntity]^-[DatasetVersion],[InformationContentEntity]^-[DatasetSummary],[InformationContentEntity]^-[DatasetDistribution],[InformationContentEntity]^-[Dataset],[InformationContentEntity]^-[ConfidenceLevel],[NamedThing]^-[InformationContentEntity],[EvidenceType],[DatasetVersion],[DatasetSummary],[DatasetDistribution],[Dataset],[ContributorAssociation],[ConfidenceLevel],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[NamedThing],[ContributorAssociation]-%20subject%201..1>[InformationContentEntity&#124;license:string%20%3F;rights:string%20%3F;format:string%20%3F;creation_date:date%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[InformationContentEntity]^-[Publication],[InformationContentEntity]^-[EvidenceType],[InformationContentEntity]^-[DatasetVersion],[InformationContentEntity]^-[DatasetSummary],[InformationContentEntity]^-[DatasetDistribution],[InformationContentEntity]^-[Dataset],[InformationContentEntity]^-[ConfidenceLevel],[NamedThing]^-[InformationContentEntity],[EvidenceType],[DatasetVersion],[DatasetSummary],[DatasetDistribution],[Dataset],[ContributorAssociation],[ConfidenceLevel],[Attribute],[Agent])

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

## Referenced by Class

 *  **[ContributorAssociation](ContributorAssociation.md)** *[contributor association➞subject](contributor_association_subject.md)*  <sub>1..1</sub>  **[InformationContentEntity](InformationContentEntity.md)**

## Attributes


### Own

 * [license](license.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [rights](rights.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [format](format.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [creation date](creation_date.md)  <sub>0..1</sub>
     * Description: date on which an entity was created. This can be applied to nodes or edges
     * Range: [Date](types/Date.md)

### Inherited from named thing:

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
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)

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

