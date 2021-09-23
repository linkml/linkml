
# Class: exposure event


A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more phenotypic features of that organism, potentially mediated by genes

URI: [biolink:ExposureEvent](https://w3id.org/biolink/vocab/ExposureEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ExposureEventToPhenotypicFeatureAssociation],[ExposureEventToEntityAssociationMixin],[EntityToExposureEventAssociationMixin]++-%20object%201..1>[ExposureEvent&#124;timepoint:time_type%20%3F],[ExposureEventToEntityAssociationMixin]++-%20subject%201..1>[ExposureEvent],[ExposureEventToPhenotypicFeatureAssociation]++-%20subject%201..1>[ExposureEvent],[Treatment]uses%20-.->[ExposureEvent],[SocioeconomicExposure]uses%20-.->[ExposureEvent],[PathologicalProcessExposure]uses%20-.->[ExposureEvent],[PathologicalAnatomicalExposure]uses%20-.->[ExposureEvent],[GeographicExposure]uses%20-.->[ExposureEvent],[GenomicBackgroundExposure]uses%20-.->[ExposureEvent],[EnvironmentalExposure]uses%20-.->[ExposureEvent],[DrugExposure]uses%20-.->[ExposureEvent],[DiseaseOrPhenotypicFeatureExposure]uses%20-.->[ExposureEvent],[ChemicalExposure]uses%20-.->[ExposureEvent],[BioticExposure]uses%20-.->[ExposureEvent],[BehavioralExposure]uses%20-.->[ExposureEvent],[Treatment],[SocioeconomicExposure],[PathologicalProcessExposure],[PathologicalAnatomicalExposure],[GeographicExposure],[GenomicBackgroundExposure],[EnvironmentalExposure],[EntityToExposureEventAssociationMixin],[DrugExposure],[DiseaseOrPhenotypicFeatureExposure],[ChemicalExposure],[BioticExposure],[BehavioralExposure])](https://yuml.me/diagram/nofunky;dir:TB/class/[ExposureEventToPhenotypicFeatureAssociation],[ExposureEventToEntityAssociationMixin],[EntityToExposureEventAssociationMixin]++-%20object%201..1>[ExposureEvent&#124;timepoint:time_type%20%3F],[ExposureEventToEntityAssociationMixin]++-%20subject%201..1>[ExposureEvent],[ExposureEventToPhenotypicFeatureAssociation]++-%20subject%201..1>[ExposureEvent],[Treatment]uses%20-.->[ExposureEvent],[SocioeconomicExposure]uses%20-.->[ExposureEvent],[PathologicalProcessExposure]uses%20-.->[ExposureEvent],[PathologicalAnatomicalExposure]uses%20-.->[ExposureEvent],[GeographicExposure]uses%20-.->[ExposureEvent],[GenomicBackgroundExposure]uses%20-.->[ExposureEvent],[EnvironmentalExposure]uses%20-.->[ExposureEvent],[DrugExposure]uses%20-.->[ExposureEvent],[DiseaseOrPhenotypicFeatureExposure]uses%20-.->[ExposureEvent],[ChemicalExposure]uses%20-.->[ExposureEvent],[BioticExposure]uses%20-.->[ExposureEvent],[BehavioralExposure]uses%20-.->[ExposureEvent],[Treatment],[SocioeconomicExposure],[PathologicalProcessExposure],[PathologicalAnatomicalExposure],[GeographicExposure],[GenomicBackgroundExposure],[EnvironmentalExposure],[EntityToExposureEventAssociationMixin],[DrugExposure],[DiseaseOrPhenotypicFeatureExposure],[ChemicalExposure],[BioticExposure],[BehavioralExposure])

## Mixin for

 * [BehavioralExposure](BehavioralExposure.md) (mixin)  - A behavioral exposure is a factor relating to behavior impacting an individual.
 * [BioticExposure](BioticExposure.md) (mixin)  - An external biotic exposure is an intake of (sometimes pathological) biological organisms (including viruses).
 * [ChemicalExposure](ChemicalExposure.md) (mixin)  - A chemical exposure is an intake of a particular chemical substance, other than a drug.
 * [DiseaseOrPhenotypicFeatureExposure](DiseaseOrPhenotypicFeatureExposure.md) (mixin)  - A disease or phenotypic feature state, when viewed as an exposure, represents an precondition, leading to or influencing an outcome, e.g. HIV predisposing an individual to infections; a relative deficiency of skin pigmentation predisposing an individual to skin cancer.
 * [DrugExposure](DrugExposure.md) (mixin)  - A drug exposure is an intake of a particular drug.
 * [EnvironmentalExposure](EnvironmentalExposure.md) (mixin)  - A environmental exposure is a factor relating to abiotic processes in the environment including sunlight (UV-B), atmospheric (heat, cold, general pollution) and water-born contaminants.
 * [GenomicBackgroundExposure](GenomicBackgroundExposure.md) (mixin)  - A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing an outcome.
 * [GeographicExposure](GeographicExposure.md) (mixin)  - A geographic exposure is a factor relating to geographic proximity to some impactful entity.
 * [PathologicalAnatomicalExposure](PathologicalAnatomicalExposure.md) (mixin)  - An abnormal anatomical structure, when viewed as an exposure, representing an precondition, leading to or influencing an outcome, e.g. thrombosis leading to an ischemic disease outcome.
 * [PathologicalProcessExposure](PathologicalProcessExposure.md) (mixin)  - A pathological process, when viewed as an exposure, representing an precondition, leading to or influencing an outcome, e.g. autoimmunity leading to disease.
 * [SocioeconomicExposure](SocioeconomicExposure.md) (mixin)  - A socioeconomic exposure is a factor relating to social and financial status of an affected individual (e.g. poverty).
 * [Treatment](Treatment.md) (mixin)  - A treatment is targeted at a disease or phenotype and may involve multiple drug 'exposures', medical devices and/or procedures

## Referenced by Class

 *  **[EntityToExposureEventAssociationMixin](EntityToExposureEventAssociationMixin.md)** *[entity to exposure event association mixin➞object](entity_to_exposure_event_association_mixin_object.md)*  <sub>1..1</sub>  **[ExposureEvent](ExposureEvent.md)**
 *  **[ExposureEventToEntityAssociationMixin](ExposureEventToEntityAssociationMixin.md)** *[exposure event to entity association mixin➞subject](exposure_event_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[ExposureEvent](ExposureEvent.md)**
 *  **[ExposureEventToPhenotypicFeatureAssociation](ExposureEventToPhenotypicFeatureAssociation.md)** *[exposure event to phenotypic feature association➞subject](exposure_event_to_phenotypic_feature_association_subject.md)*  <sub>1..1</sub>  **[ExposureEvent](ExposureEvent.md)**

## Attributes


### Own

 * [timepoint](timepoint.md)  <sub>0..1</sub>
     * Description: a point in time
     * Range: [TimeType](types/TimeType.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | exposure |
|  | | experimental condition |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | XCO:0000000 |
| **Broad Mappings:** | | UMLSSC:T051 |
|  | | UMLSST:evnt |

