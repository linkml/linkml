
# Class: DiseaseOrPhenotypicFeature


Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.

URI: [biolink:DiseaseOrPhenotypicFeature](https://w3id.org/biolink/vocab/DiseaseOrPhenotypicFeature)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Treatment],[ThingWithTaxon],[PhenotypicFeature],[OrganismTaxon],[NamedThing],[MolecularEntity],[Gene],[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[Drug],[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[DiseaseOrPhenotypicFeatureOutcome],[DiseaseOrPhenotypicFeatureExposure],[CellLineToDiseaseOrPhenotypicFeatureAssociation]-%20subject%201..1>[DiseaseOrPhenotypicFeature&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[ChemicalToDiseaseOrPhenotypicFeatureAssociation]-%20object%201..1>[DiseaseOrPhenotypicFeature],[DiseaseOrPhenotypicFeatureToEntityAssociationMixin]-%20subject%201..1>[DiseaseOrPhenotypicFeature],[EntityToDiseaseOrPhenotypicFeatureAssociationMixin]-%20object%201..1>[DiseaseOrPhenotypicFeature],[GeneExpressionMixin]-%20phenotypic%20state%200..1>[DiseaseOrPhenotypicFeature],[DiseaseOrPhenotypicFeature]uses%20-.->[ThingWithTaxon],[DiseaseOrPhenotypicFeature]^-[PhenotypicFeature],[DiseaseOrPhenotypicFeature]^-[DiseaseOrPhenotypicFeatureOutcome],[DiseaseOrPhenotypicFeature]^-[DiseaseOrPhenotypicFeatureExposure],[DiseaseOrPhenotypicFeature]^-[Disease],[BiologicalEntity]^-[DiseaseOrPhenotypicFeature],[GeneExpressionMixin],[Disease],[ChemicalToDiseaseOrPhenotypicFeatureAssociation],[CellLineToDiseaseOrPhenotypicFeatureAssociation],[BiologicalEntity],[Attribute],[Association],[Agent])

## Parents

 *  is_a: [BiologicalEntity](BiologicalEntity.md)

## Uses Mixins

 *  mixin: [ThingWithTaxon](ThingWithTaxon.md) - A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms; genes, their products and other molecular entities; body parts; biological processes

## Children

 * [Disease](Disease.md)
 * [DiseaseOrPhenotypicFeatureExposure](DiseaseOrPhenotypicFeatureExposure.md) - A disease or phenotypic feature state, when viewed as an exposure, represents an precondition, leading to or influencing an outcome, e.g. HIV predisposing an individual to infections; a relative deficiency of skin pigmentation predisposing an individual to skin cancer.
 * [DiseaseOrPhenotypicFeatureOutcome](DiseaseOrPhenotypicFeatureOutcome.md) - Physiological outcomes resulting from an exposure event which is the manifestation of a disease or other characteristic phenotype.
 * [PhenotypicFeature](PhenotypicFeature.md)

## Referenced by class

 *  **[BiologicalEntity](BiologicalEntity.md)** *[ameliorates](ameliorates.md)*  <sub>0..*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Treatment](Treatment.md)** *[approved to treat](approved_to_treat.md)*  <sub>0..*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[biomarker for](biomarker_for.md)*  <sub>0..*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Drug](Drug.md)** *[causes adverse event](causes_adverse_event.md)*  <sub>0..*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[CellLineToDiseaseOrPhenotypicFeatureAssociation](CellLineToDiseaseOrPhenotypicFeatureAssociation.md)** *[cell line to disease or phenotypic feature association➞subject](cell_line_to_disease_or_phenotypic_feature_association_subject.md)*  <sub>REQ</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[ChemicalToDiseaseOrPhenotypicFeatureAssociation](ChemicalToDiseaseOrPhenotypicFeatureAssociation.md)** *[chemical to disease or phenotypic feature association➞object](chemical_to_disease_or_phenotypic_feature_association_object.md)*  <sub>REQ</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Drug](Drug.md)** *[contraindicated for](contraindicated_for.md)*  <sub>0..*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[DiseaseOrPhenotypicFeatureToEntityAssociationMixin](DiseaseOrPhenotypicFeatureToEntityAssociationMixin.md)** *[disease or phenotypic feature to entity association mixin➞subject](disease_or_phenotypic_feature_to_entity_association_mixin_subject.md)*  <sub>REQ</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[EntityToDiseaseOrPhenotypicFeatureAssociationMixin](EntityToDiseaseOrPhenotypicFeatureAssociationMixin.md)** *[entity to disease or phenotypic feature association mixin➞object](entity_to_disease_or_phenotypic_feature_association_mixin_object.md)*  <sub>REQ</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[BiologicalEntity](BiologicalEntity.md)** *[exacerbates](exacerbates.md)*  <sub>0..*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Gene](Gene.md)** *[gene associated with condition](gene_associated_with_condition.md)*  <sub>0..*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Association](Association.md)** *[phenotypic state](phenotypic_state.md)*  <sub>OPT</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Treatment](Treatment.md)** *[treats](treats.md)*  <sub>0..*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**

## Attributes


### Inherited from biological entity:

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

### Mixed in from thing with taxon:

 * [in taxon](in_taxon.md)  <sub>0..*</sub>
     * Description: connects an entity to its taxonomic classification. Only certain kinds of entities can be taxonomically classified; see 'thing with taxon'
     * range: [OrganismTaxon](OrganismTaxon.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | phenome |
| **Narrow Mappings:** | | UMLSSC:T033 |
|  | | UMLSST:fndg |

