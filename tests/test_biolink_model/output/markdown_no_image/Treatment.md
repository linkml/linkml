
# Class: treatment


A treatment is targeted at a disease or phenotype and may involve multiple drug 'exposures', medical devices and/or procedures

URI: [biolink:Treatment](https://w3id.org/biolink/vocab/Treatment)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Procedure]<has%20procedure%200..*-%20[Treatment&#124;timepoint:time_type%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Device]<has%20device%200..*-%20[Treatment],[Drug]<has%20drug%200..*-%20[Treatment],[SequenceVariantModulatesTreatmentAssociation]-%20object%201..1>[Treatment],[Treatment]uses%20-.->[ExposureEvent],[Treatment]uses%20-.->[ChemicalOrDrugOrTreatment],[NamedThing]^-[Treatment],[SequenceVariantModulatesTreatmentAssociation],[Procedure],[NamedThing],[ExposureEvent],[Drug],[DiseaseOrPhenotypicFeature],[Device],[ChemicalOrDrugOrTreatment],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[Procedure]<has%20procedure%200..*-%20[Treatment&#124;timepoint:time_type%20%3F;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Device]<has%20device%200..*-%20[Treatment],[Drug]<has%20drug%200..*-%20[Treatment],[SequenceVariantModulatesTreatmentAssociation]-%20object%201..1>[Treatment],[Treatment]uses%20-.->[ExposureEvent],[Treatment]uses%20-.->[ChemicalOrDrugOrTreatment],[NamedThing]^-[Treatment],[SequenceVariantModulatesTreatmentAssociation],[Procedure],[NamedThing],[ExposureEvent],[Drug],[DiseaseOrPhenotypicFeature],[Device],[ChemicalOrDrugOrTreatment],[Attribute],[Agent])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Uses Mixin

 *  mixin: [ExposureEvent](ExposureEvent.md) - A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more phenotypic features of that organism, potentially mediated by genes
 *  mixin: [ChemicalOrDrugOrTreatment](ChemicalOrDrugOrTreatment.md)

## Referenced by Class

 *  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)** *[approved for treatment by](approved_for_treatment_by.md)*  <sub>0..\*</sub>  **[Treatment](Treatment.md)**
 *  **[SequenceVariantModulatesTreatmentAssociation](SequenceVariantModulatesTreatmentAssociation.md)** *[sequence variant modulates treatment association➞object](sequence_variant_modulates_treatment_association_object.md)*  <sub>1..1</sub>  **[Treatment](Treatment.md)**
 *  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)** *[treated by](treated_by.md)*  <sub>0..\*</sub>  **[Treatment](Treatment.md)**

## Attributes


### Own

 * [has drug](has_drug.md)  <sub>0..\*</sub>
     * Description: connects an entity to one or more drugs
     * Range: [Drug](Drug.md)
 * [has device](has_device.md)  <sub>0..\*</sub>
     * Description: connects an entity to one or more (medical) devices
     * Range: [Device](Device.md)
 * [has procedure](has_procedure.md)  <sub>0..\*</sub>
     * Description: connects an entity to one or more (medical) procedures
     * Range: [Procedure](Procedure.md)

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

### Mixed in from exposure event:

 * [timepoint](timepoint.md)  <sub>0..1</sub>
     * Description: a point in time
     * Range: [TimeType](types/TimeType.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | medical action |
|  | | medical intervention |
| **Exact Mappings:** | | OGMS:0000090 |
|  | | SIO:001398 |

