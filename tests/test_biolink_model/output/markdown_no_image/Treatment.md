
# Class: Treatment


A treatment is targeted at a disease or phenotype and may involve multiple drug 'exposures', medical devices and/or procedures

URI: [biolink:Treatment](https://w3id.org/biolink/vocab/Treatment)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Procedure]<has%20procedure%200..*-%20[Treatment&#124;timepoint:time_type%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Device]<has%20device%200..*-%20[Treatment],[Drug]<has%20drug%200..*-%20[Treatment],[SequenceVariantModulatesTreatmentAssociation]-%20object%201..1>[Treatment],[Treatment]uses%20-.->[ExposureEvent],[NamedThing]^-[Treatment],[SequenceVariantModulatesTreatmentAssociation],[Procedure],[NamedThing],[ExposureEvent],[Drug],[DiseaseOrPhenotypicFeature],[Device],[Attribute],[Agent])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Uses Mixins

 *  mixin: [ExposureEvent](ExposureEvent.md) - A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more phenotypic features of that organism, potentially mediated by genes

## Referenced by class

 *  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)** *[approved for treatment by](approved_for_treatment_by.md)*  <sub>0..*</sub>  **[Treatment](Treatment.md)**
 *  **[SequenceVariantModulatesTreatmentAssociation](SequenceVariantModulatesTreatmentAssociation.md)** *[sequence variant modulates treatment association➞object](sequence_variant_modulates_treatment_association_object.md)*  <sub>REQ</sub>  **[Treatment](Treatment.md)**
 *  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)** *[treated by](treated_by.md)*  <sub>0..*</sub>  **[Treatment](Treatment.md)**

## Attributes


### Own

 * [has device](has_device.md)  <sub>0..*</sub>
     * Description: connects an entity to one or more (medical) devices
     * range: [Device](Device.md)
 * [has drug](has_drug.md)  <sub>0..*</sub>
     * Description: connects an entity to one or more drugs
     * range: [Drug](Drug.md)
 * [has procedure](has_procedure.md)  <sub>0..*</sub>
     * Description: connects an entity to one or more (medical) procedures
     * range: [Procedure](Procedure.md)

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

### Mixed in from exposure event:

 * [timepoint](timepoint.md)  <sub>OPT</sub>
     * Description: a point in time
     * range: [TimeType](types/TimeType.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | medical action |
|  | | medical intervention |
| **Exact Mappings:** | | OGMS:0000090 |
|  | | SIO:001398 |

