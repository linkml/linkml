
# Class: named thing


a databased entity or concept/class

URI: [biolink:NamedThing](https://w3id.org/biolink/vocab/NamedThing)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[VariantToDiseaseAssociation],[Treatment],[Procedure],[PlanetaryEntity],[PhysicalEntity],[Phenomenon],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxon],[OntologyClass],[PredicateMapping]-%20broad%20match%200..*>[NamedThing&#124;provided_by:string%20*;xref:uriorcurie%20*;category:category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[ChemicalEntityAssessesNamedThingAssociation]-%20object%201..1>[NamedThing],[PredicateMapping]-%20exact%20match%200..*>[NamedThing],[GenotypeToDiseaseAssociation]-%20object%201..1>[NamedThing],[GenotypeToDiseaseAssociation]-%20subject%201..1>[NamedThing],[Attribute]-%20has%20qualitative%20value%200..1>[NamedThing],[InformationContentEntityToNamedThingAssociation]-%20object%201..1>[NamedThing],[InformationContentEntityToNamedThingAssociation]-%20subject%201..1>[NamedThing],[MacromolecularMachineToEntityAssociationMixin]-%20subject%201..1>[NamedThing],[MaterialSampleDerivationAssociation]-%20object%201..1>[NamedThing],[ModelToDiseaseAssociationMixin]-%20subject%201..1>[NamedThing],[PredicateMapping]-%20narrow%20match%200..*>[NamedThing],[Association]-%20object%201..1>[NamedThing],[OrganismTaxonToEnvironmentAssociation]-%20object%201..1>[NamedThing],[Association]-%20subject%201..1>[NamedThing],[VariantToDiseaseAssociation]-%20object%201..1>[NamedThing],[VariantToDiseaseAssociation]-%20subject%201..1>[NamedThing],[NamedThing]^-[Treatment],[NamedThing]^-[Procedure],[NamedThing]^-[PlanetaryEntity],[NamedThing]^-[PhysicalEntity],[NamedThing]^-[Phenomenon],[NamedThing]^-[OrganismTaxon],[NamedThing]^-[InformationContentEntity],[NamedThing]^-[Event],[NamedThing]^-[Device],[NamedThing]^-[ClinicalEntity],[NamedThing]^-[ChemicalEntity],[NamedThing]^-[BiologicalEntity],[NamedThing]^-[Attribute],[NamedThing]^-[AdministrativeEntity],[NamedThing]^-[Activity],[Entity]^-[NamedThing],[PredicateMapping],[ModelToDiseaseAssociationMixin],[MaterialSampleDerivationAssociation],[MacromolecularMachineToEntityAssociationMixin],[InformationContentEntityToNamedThingAssociation],[InformationContentEntity],[GenotypeToDiseaseAssociation],[Event],[Entity],[DiseaseOrPhenotypicFeature],[Disease],[Device],[ClinicalEntity],[ChemicalEntityAssessesNamedThingAssociation],[ChemicalEntity],[BiologicalEntity],[Attribute],[Association],[AdministrativeEntity],[Activity])](https://yuml.me/diagram/nofunky;dir:TB/class/[VariantToDiseaseAssociation],[Treatment],[Procedure],[PlanetaryEntity],[PhysicalEntity],[Phenomenon],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxon],[OntologyClass],[PredicateMapping]-%20broad%20match%200..*>[NamedThing&#124;provided_by:string%20*;xref:uriorcurie%20*;category:category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[ChemicalEntityAssessesNamedThingAssociation]-%20object%201..1>[NamedThing],[PredicateMapping]-%20exact%20match%200..*>[NamedThing],[GenotypeToDiseaseAssociation]-%20object%201..1>[NamedThing],[GenotypeToDiseaseAssociation]-%20subject%201..1>[NamedThing],[Attribute]-%20has%20qualitative%20value%200..1>[NamedThing],[InformationContentEntityToNamedThingAssociation]-%20object%201..1>[NamedThing],[InformationContentEntityToNamedThingAssociation]-%20subject%201..1>[NamedThing],[MacromolecularMachineToEntityAssociationMixin]-%20subject%201..1>[NamedThing],[MaterialSampleDerivationAssociation]-%20object%201..1>[NamedThing],[ModelToDiseaseAssociationMixin]-%20subject%201..1>[NamedThing],[PredicateMapping]-%20narrow%20match%200..*>[NamedThing],[Association]-%20object%201..1>[NamedThing],[OrganismTaxonToEnvironmentAssociation]-%20object%201..1>[NamedThing],[Association]-%20subject%201..1>[NamedThing],[VariantToDiseaseAssociation]-%20object%201..1>[NamedThing],[VariantToDiseaseAssociation]-%20subject%201..1>[NamedThing],[NamedThing]^-[Treatment],[NamedThing]^-[Procedure],[NamedThing]^-[PlanetaryEntity],[NamedThing]^-[PhysicalEntity],[NamedThing]^-[Phenomenon],[NamedThing]^-[OrganismTaxon],[NamedThing]^-[InformationContentEntity],[NamedThing]^-[Event],[NamedThing]^-[Device],[NamedThing]^-[ClinicalEntity],[NamedThing]^-[ChemicalEntity],[NamedThing]^-[BiologicalEntity],[NamedThing]^-[Attribute],[NamedThing]^-[AdministrativeEntity],[NamedThing]^-[Activity],[Entity]^-[NamedThing],[PredicateMapping],[ModelToDiseaseAssociationMixin],[MaterialSampleDerivationAssociation],[MacromolecularMachineToEntityAssociationMixin],[InformationContentEntityToNamedThingAssociation],[InformationContentEntity],[GenotypeToDiseaseAssociation],[Event],[Entity],[DiseaseOrPhenotypicFeature],[Disease],[Device],[ClinicalEntity],[ChemicalEntityAssessesNamedThingAssociation],[ChemicalEntity],[BiologicalEntity],[Attribute],[Association],[AdministrativeEntity],[Activity])

## Parents

 *  is_a: [Entity](Entity.md) - Root Biolink Model class for all things and informational relationships, real or imagined.

## Children

 * [Activity](Activity.md) - An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.
 * [AdministrativeEntity](AdministrativeEntity.md)
 * [Attribute](Attribute.md) - A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age, crispiness. An environmental sample may have attributes such as depth, lat, long, material.
 * [BiologicalEntity](BiologicalEntity.md)
 * [ChemicalEntity](ChemicalEntity.md) - A chemical entity is a physical entity that pertains to chemistry or biochemistry.
 * [ClinicalEntity](ClinicalEntity.md) - Any entity or process that exists in the clinical domain and outside the biological realm. Diseases are placed under biological entities
 * [Device](Device.md) - A thing made or adapted for a particular purpose, especially a piece of mechanical or electronic equipment
 * [Event](Event.md) - Something that happens at a given place and time.
 * [InformationContentEntity](InformationContentEntity.md) - a piece of information that typically describes some topic of discourse or is used as support.
 * [OrganismTaxon](OrganismTaxon.md) - A classification of a set of organisms. Example instances: NCBITaxon:9606 (Homo sapiens), NCBITaxon:2 (Bacteria). Can also be used to represent strains or subspecies.
 * [Phenomenon](Phenomenon.md) - a fact or situation that is observed to exist or happen, especially one whose cause or explanation is in question
 * [PhysicalEntity](PhysicalEntity.md) - An entity that has material reality (a.k.a. physical essence).
 * [PlanetaryEntity](PlanetaryEntity.md) - Any entity or process that exists at the level of the whole planet
 * [Procedure](Procedure.md) - A series of actions conducted in a certain order or manner
 * [Treatment](Treatment.md) - A treatment is targeted at a disease or phenotype and may involve multiple drug 'exposures', medical devices and/or procedures

## Referenced by Class

 *  **[NamedThing](NamedThing.md)** *[affected by](affected_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[affects](affects.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[affects risk for](affects_risk_for.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[amount or activity decreased by](amount_or_activity_decreased_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[amount or activity increased by](amount_or_activity_increased_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[assesses](assesses.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[associated with](associated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[associated with decreased likelihood of](associated_with_decreased_likelihood_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[associated with increased likelihood of](associated_with_increased_likelihood_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[associated with likelihood of](associated_with_likelihood_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[binds](binds.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[broad match](broad_match.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[caused by](caused_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[causes](causes.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[ChemicalEntityAssessesNamedThingAssociation](ChemicalEntityAssessesNamedThingAssociation.md)** *[chemical entity assesses named thing association➞object](chemical_entity_assesses_named_thing_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[chemically similar to](chemically_similar_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[close match](close_match.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[coexists with](coexists_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[colocalizes with](colocalizes_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[completed by](completed_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[composed primarily of](composed_primarily_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[contains process](contains_process.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[contributes to](contributes_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[contribution from](contribution_from.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[correlated with](correlated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[decreased amount in](decreased_amount_in.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[decreased likelihood associated with](decreased_likelihood_associated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[decreases amount or activity of](decreases_amount_or_activity_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[derives from](derives_from.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[derives into](derives_into.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[develops from](develops_from.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[develops into](develops_into.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[directly physically interacts with](directly_physically_interacts_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[disease has basis in](disease_has_basis_in.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[disease has location](disease_has_location.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[disrupted by](disrupted_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[disrupts](disrupts.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[exact match](exact_match.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[genetic association](genetic_association.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[GenotypeToDiseaseAssociation](GenotypeToDiseaseAssociation.md)** *[genotype to disease association➞object](genotype_to_disease_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[GenotypeToDiseaseAssociation](GenotypeToDiseaseAssociation.md)** *[genotype to disease association➞subject](genotype_to_disease_association_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has completed](has_completed.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has decreased amount](has_decreased_amount.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has increased amount](has_increased_amount.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Disease](Disease.md)** *[has manifestation](has_manifestation.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has member](has_member.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has not completed](has_not_completed.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has part](has_part.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has plasma membrane part](has_plasma_membrane_part.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has predisposing factor](has_predisposing_factor.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Attribute](Attribute.md)** *[has qualitative value](has_qualitative_value.md)*  <sub>0..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has variant part](has_variant_part.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[homologous to](homologous_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[in linkage disequilibrium with](in_linkage_disequilibrium_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[increased amount of](increased_amount_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[increased likelihood associated with](increased_likelihood_associated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[increases amount or activity of](increases_amount_or_activity_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[indirectly physically interacts with](indirectly_physically_interacts_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[InformationContentEntityToNamedThingAssociation](InformationContentEntityToNamedThingAssociation.md)** *[information content entity to named thing association➞object](information_content_entity_to_named_thing_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[InformationContentEntityToNamedThingAssociation](InformationContentEntityToNamedThingAssociation.md)** *[information content entity to named thing association➞subject](information_content_entity_to_named_thing_association_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[interacts with](interacts_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)** *[is ameliorated by](is_ameliorated_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[is assessed by](is_assessed_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[OntologyClass](OntologyClass.md)** *[is molecular consequence of](is_molecular_consequence_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[lacks part](lacks_part.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[likelihood associated with](likelihood_associated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[located in](located_in.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[location of](location_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[location of disease](location_of_disease.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[MacromolecularMachineToEntityAssociationMixin](MacromolecularMachineToEntityAssociationMixin.md)** *[macromolecular machine to entity association mixin➞subject](macromolecular_machine_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[MaterialSampleDerivationAssociation](MaterialSampleDerivationAssociation.md)** *[material sample derivation association➞object](material_sample_derivation_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[member of](member_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[mentioned by](mentioned_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[mentions](mentions.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[missing from](missing_from.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[model of](model_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[ModelToDiseaseAssociationMixin](ModelToDiseaseAssociationMixin.md)** *[model to disease association mixin➞subject](model_to_disease_association_mixin_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[models](models.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[narrow match](narrow_match.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[negatively correlated with](negatively_correlated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[not completed by](not_completed_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Association](Association.md)** *[object](object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[occurs in](occurs_in.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[occurs in disease](occurs_in_disease.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[occurs together in literature with](occurs_together_in_literature_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[opposite of](opposite_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[OrganismTaxonToEnvironmentAssociation](OrganismTaxonToEnvironmentAssociation.md)** *[organism taxon to environment association➞object](organism_taxon_to_environment_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[orthologous to](orthologous_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[overlaps](overlaps.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[paralogous to](paralogous_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[part of](part_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[physically interacts with](physically_interacts_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[plasma membrane part of](plasma_membrane_part_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[positively correlated with](positively_correlated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[predisposes](predisposes.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[prevented by](prevented_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[prevents](prevents.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[primarily composed of](primarily_composed_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[produced by](produced_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[produces](produces.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[related condition](related_condition.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[related to](related_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[related to at concept level](related_to_at_concept_level.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[related to at instance level](related_to_at_instance_level.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[ChemicalEntity](ChemicalEntity.md)** *[resistance associated with](resistance_associated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[risk affected by](risk_affected_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[same as](same_as.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[ChemicalEntity](ChemicalEntity.md)** *[sensitivity associated with](sensitivity_associated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[similar to](similar_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Association](Association.md)** *[subject](subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[variant part of](variant_part_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[VariantToDiseaseAssociation](VariantToDiseaseAssociation.md)** *[variant to disease association➞object](variant_to_disease_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[VariantToDiseaseAssociation](VariantToDiseaseAssociation.md)** *[variant to disease association➞subject](variant_to_disease_association_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[xenologous to](xenologous_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**

## Attributes


### Own

 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: The value in this node property represents the knowledge provider that created or assembled the node and all of its attributes.  Used internally to represent how a particular node made its way into a knowledge provider or graph.
     * Range: [String](types/String.md)
 * [xref](xref.md)  <sub>0..\*</sub>
     * Description: Alternate CURIEs for a thing
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (translator_minimal)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [CategoryType](types/CategoryType.md)
     * in subsets: (translator_minimal)

### Inherited from entity:

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
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | BFO:0000001 |
|  | | WIKIDATA:Q35120 |
|  | | UMLSSG:OBJC |
|  | | STY:T071 |
|  | | dcid:Thing |

