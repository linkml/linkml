
# Class: DatasetVersion


an item that holds version level information about a dataset.

URI: [biolink:DatasetVersion](https://w3id.org/biolink/vocab/DatasetVersion)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing],[InformationContentEntity],[DatasetDistribution]<has%20distribution%200..1-%20[DatasetVersion&#124;ingest_date:string%20%3F;license(i):string%20%3F;rights(i):string%20%3F;format(i):string%20%3F;creation_date(i):date%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Dataset]<has%20dataset%200..1-%20[DatasetVersion],[InformationContentEntity]^-[DatasetVersion],[DatasetDistribution],[Dataset],[Attribute],[Agent])

## Parents

 *  is_a: [InformationContentEntity](InformationContentEntity.md) - a piece of information that typically describes some topic of discourse or is used as support.

## Referenced by class


## Attributes


### Own

 * [has dataset](has_dataset.md)  <sub>OPT</sub>
     * range: [Dataset](Dataset.md)
 * [has distribution](has_distribution.md)  <sub>OPT</sub>
     * range: [DatasetDistribution](DatasetDistribution.md)
 * [ingest date](ingest_date.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

### Inherited from information content entity:

 * [creation date](creation_date.md)  <sub>OPT</sub>
     * Description: date on which an entity was created. This can be applied to nodes or edges
     * range: [Date](types/Date.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [format](format.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
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
 * [license](license.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [name](name.md)  <sub>OPT</sub>
     * Description: A human-readable name for an attribute or entity.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..*</sub>
     * range: [NamedThing](NamedThing.md)
 * [provided by](provided_by.md)  <sub>0..*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * range: [Agent](Agent.md)
 * [rights](rights.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [type](type.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
