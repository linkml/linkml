
# Class: exposure event


A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more phenotypic features of that organism, potentially mediated by genes

URI: [biolink:ExposureEvent](https://w3id.org/biolink/vocab/ExposureEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyClass],[ExposureEventToPhenotypicFeatureAssociation],[EntityToExposureEventAssociationMixin]-%20object%201..1>[ExposureEvent&#124;timepoint:time_type%20%3F;id(i):string],[ExposureEventToPhenotypicFeatureAssociation]-%20subject%201..1>[ExposureEvent],[Treatment]uses%20-.->[ExposureEvent],[SocioeconomicExposure]uses%20-.->[ExposureEvent],[PathologicalProcessExposure]uses%20-.->[ExposureEvent],[PathologicalAnatomicalExposure]uses%20-.->[ExposureEvent],[GeographicExposure]uses%20-.->[ExposureEvent],[GenomicBackgroundExposure]uses%20-.->[ExposureEvent],[EnvironmentalExposure]uses%20-.->[ExposureEvent],[DrugExposure]uses%20-.->[ExposureEvent],[DiseaseOrPhenotypicFeatureExposure]uses%20-.->[ExposureEvent],[ChemicalExposure]uses%20-.->[ExposureEvent],[BioticExposure]uses%20-.->[ExposureEvent],[BehavioralExposure]uses%20-.->[ExposureEvent],[OntologyClass]^-[ExposureEvent],[Treatment],[SocioeconomicExposure],[PathologicalProcessExposure],[PathologicalAnatomicalExposure],[GeographicExposure],[GenomicBackgroundExposure],[EnvironmentalExposure],[EntityToExposureEventAssociationMixin],[DrugExposure],[DiseaseOrPhenotypicFeatureExposure],[ChemicalExposure],[BioticExposure],[BehavioralExposure])](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyClass],[ExposureEventToPhenotypicFeatureAssociation],[EntityToExposureEventAssociationMixin]-%20object%201..1>[ExposureEvent&#124;timepoint:time_type%20%3F;id(i):string],[ExposureEventToPhenotypicFeatureAssociation]-%20subject%201..1>[ExposureEvent],[Treatment]uses%20-.->[ExposureEvent],[SocioeconomicExposure]uses%20-.->[ExposureEvent],[PathologicalProcessExposure]uses%20-.->[ExposureEvent],[PathologicalAnatomicalExposure]uses%20-.->[ExposureEvent],[GeographicExposure]uses%20-.->[ExposureEvent],[GenomicBackgroundExposure]uses%20-.->[ExposureEvent],[EnvironmentalExposure]uses%20-.->[ExposureEvent],[DrugExposure]uses%20-.->[ExposureEvent],[DiseaseOrPhenotypicFeatureExposure]uses%20-.->[ExposureEvent],[ChemicalExposure]uses%20-.->[ExposureEvent],[BioticExposure]uses%20-.->[ExposureEvent],[BehavioralExposure]uses%20-.->[ExposureEvent],[OntologyClass]^-[ExposureEvent],[Treatment],[SocioeconomicExposure],[PathologicalProcessExposure],[PathologicalAnatomicalExposure],[GeographicExposure],[GenomicBackgroundExposure],[EnvironmentalExposure],[EntityToExposureEventAssociationMixin],[DrugExposure],[DiseaseOrPhenotypicFeatureExposure],[ChemicalExposure],[BioticExposure],[BehavioralExposure])

## Parents

 *  is_a: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Mixin for

 * [BehavioralExposure](BehavioralExposure.md) (mixin)  - A behavioral exposure is a factor relating to behavior impacting an individual.
 * [BioticExposure](BioticExposure.md) (mixin)  - An external biotic exposure is an intake of (sometimes pathological) biological organisms (including viruses).
 * [ChemicalExposure](ChemicalExposure.md) (mixin)  - A chemical exposure is an intake of a particular chemical entity.
 * [DiseaseOrPhenotypicFeatureExposure](DiseaseOrPhenotypicFeatureExposure.md) (mixin)  - A disease or phenotypic feature state, when viewed as an exposure, represents an precondition, leading to or influencing an outcome, e.g. HIV predisposing an individual to infections; a relative deficiency of skin pigmentation predisposing an individual to skin cancer.
 * [DrugExposure](DrugExposure.md) (mixin)  - A drug exposure is an intake of a particular drug.
 * [EnvironmentalExposure](EnvironmentalExposure.md) (mixin)  - A environmental exposure is a factor relating to abiotic processes in the environment including sunlight (UV-B), atmospheric (heat, cold, general pollution) and water-born contaminants.
 * [GenomicBackgroundExposure](GenomicBackgroundExposure.md) (mixin)  - A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing an outcome.
 * [GeographicExposure](GeographicExposure.md) (mixin)  - A geographic exposure is a factor relating to geographic proximity to some impactful entity.
 * [PathologicalAnatomicalExposure](PathologicalAnatomicalExposure.md) (mixin)  - An abnormal anatomical structure, when viewed as an exposure, representing an precondition, leading to or influencing an outcome, e.g. thrombosis leading to an ischemic disease outcome.
 * [PathologicalProcessExposure](PathologicalProcessExposure.md) (mixin)  - A pathological process, when viewed as an exposure, representing a precondition, leading to or influencing an outcome, e.g. autoimmunity leading to disease.
 * [SocioeconomicExposure](SocioeconomicExposure.md) (mixin)  - A socioeconomic exposure is a factor relating to social and financial status of an affected individual (e.g. poverty).
 * [Treatment](Treatment.md) (mixin)  - A treatment is targeted at a disease or phenotype and may involve multiple drug 'exposures', medical devices and/or procedures

## Referenced by Class

 *  **[EntityToExposureEventAssociationMixin](EntityToExposureEventAssociationMixin.md)** *[entity to exposure event association mixin➞object](entity_to_exposure_event_association_mixin_object.md)*  <sub>1..1</sub>  **[ExposureEvent](ExposureEvent.md)**
 *  **[ExposureEventToPhenotypicFeatureAssociation](ExposureEventToPhenotypicFeatureAssociation.md)** *[exposure event to phenotypic feature association➞subject](exposure_event_to_phenotypic_feature_association_subject.md)*  <sub>1..1</sub>  **[ExposureEvent](ExposureEvent.md)**

## Attributes


### Own

 * [timepoint](timepoint.md)  <sub>0..1</sub>
     * Description: a point in time
     * Range: [TimeType](types/TimeType.md)

### Inherited from ontology class:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | exposure |
|  | | experimental condition |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | XCO:0000000 |

