
# Class: named thing


a databased entity or concept/class

URI: [biolink:NamedThing](https://w3id.org/biolink/vocab/NamedThing)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[VariantToDiseaseAssociation],[Treatment],[Procedure],[PlanetaryEntity],[PhysicalEntity],[Phenomenon],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxon],[Occurrent],[NamedThing]<category%201..*-%20[NamedThing&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GenotypeToDiseaseAssociation]-%20object%201..1>[NamedThing],[GenotypeToDiseaseAssociation]-%20subject%201..1>[NamedThing],[BiologicalProcessOrActivity]-%20has%20input%200..*>[NamedThing],[BiologicalProcessOrActivity]-%20has%20output%200..*>[NamedThing],[Attribute]-%20has%20qualitative%20value%200..1>[NamedThing],[MacromolecularMachineToEntityAssociationMixin]-%20subject%201..1>[NamedThing],[MaterialSampleDerivationAssociation]-%20object%201..1>[NamedThing],[ModelToDiseaseAssociationMixin]-%20subject%201..1>[NamedThing],[Association]-%20object%201..1>[NamedThing],[OrganismTaxonToEnvironmentAssociation]-%20object%201..1>[NamedThing],[Association]-%20subject%201..1>[NamedThing],[VariantToDiseaseAssociation]-%20object%201..1>[NamedThing],[VariantToDiseaseAssociation]-%20subject%201..1>[NamedThing],[NamedThing]^-[Treatment],[NamedThing]^-[Procedure],[NamedThing]^-[PlanetaryEntity],[NamedThing]^-[PhysicalEntity],[NamedThing]^-[Phenomenon],[NamedThing]^-[OrganismTaxon],[NamedThing]^-[InformationContentEntity],[NamedThing]^-[Device],[NamedThing]^-[ClinicalEntity],[NamedThing]^-[BiologicalEntity],[NamedThing]^-[AdministrativeEntity],[NamedThing]^-[Activity],[Entity]^-[NamedThing],[ModelToDiseaseAssociationMixin],[MaterialSampleDerivationAssociation],[MacromolecularMachineToEntityAssociationMixin],[InformationContentEntity],[GenotypeToDiseaseAssociation],[Entity],[Device],[ClinicalEntity],[BiologicalProcessOrActivity],[BiologicalEntity],[Attribute],[Association],[Agent],[AdministrativeEntity],[Activity])](https://yuml.me/diagram/nofunky;dir:TB/class/[VariantToDiseaseAssociation],[Treatment],[Procedure],[PlanetaryEntity],[PhysicalEntity],[Phenomenon],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxon],[Occurrent],[NamedThing]<category%201..*-%20[NamedThing&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[GenotypeToDiseaseAssociation]-%20object%201..1>[NamedThing],[GenotypeToDiseaseAssociation]-%20subject%201..1>[NamedThing],[BiologicalProcessOrActivity]-%20has%20input%200..*>[NamedThing],[BiologicalProcessOrActivity]-%20has%20output%200..*>[NamedThing],[Attribute]-%20has%20qualitative%20value%200..1>[NamedThing],[MacromolecularMachineToEntityAssociationMixin]-%20subject%201..1>[NamedThing],[MaterialSampleDerivationAssociation]-%20object%201..1>[NamedThing],[ModelToDiseaseAssociationMixin]-%20subject%201..1>[NamedThing],[Association]-%20object%201..1>[NamedThing],[OrganismTaxonToEnvironmentAssociation]-%20object%201..1>[NamedThing],[Association]-%20subject%201..1>[NamedThing],[VariantToDiseaseAssociation]-%20object%201..1>[NamedThing],[VariantToDiseaseAssociation]-%20subject%201..1>[NamedThing],[NamedThing]^-[Treatment],[NamedThing]^-[Procedure],[NamedThing]^-[PlanetaryEntity],[NamedThing]^-[PhysicalEntity],[NamedThing]^-[Phenomenon],[NamedThing]^-[OrganismTaxon],[NamedThing]^-[InformationContentEntity],[NamedThing]^-[Device],[NamedThing]^-[ClinicalEntity],[NamedThing]^-[BiologicalEntity],[NamedThing]^-[AdministrativeEntity],[NamedThing]^-[Activity],[Entity]^-[NamedThing],[ModelToDiseaseAssociationMixin],[MaterialSampleDerivationAssociation],[MacromolecularMachineToEntityAssociationMixin],[InformationContentEntity],[GenotypeToDiseaseAssociation],[Entity],[Device],[ClinicalEntity],[BiologicalProcessOrActivity],[BiologicalEntity],[Attribute],[Association],[Agent],[AdministrativeEntity],[Activity])

## Parents

 *  is_a: [Entity](Entity.md) - Root Biolink Model class for all things and informational relationships, real or imagined.

## Children

 * [Activity](Activity.md) - An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.
 * [AdministrativeEntity](AdministrativeEntity.md)
 * [BiologicalEntity](BiologicalEntity.md)
 * [ClinicalEntity](ClinicalEntity.md) - Any entity or process that exists in the clinical domain and outside the biological realm. Diseases are placed under biological entities
 * [Device](Device.md) - A thing made or adapted for a particular purpose, especially a piece of mechanical or electronic equipment
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
 *  **[NamedThing](NamedThing.md)** *[affects expression in](affects_expression_in.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[affects risk for](affects_risk_for.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[broad match](broad_match.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[caused by](caused_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[causes](causes.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[chemically similar to](chemically_similar_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[close match](close_match.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[coexists with](coexists_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[colocalizes with](colocalizes_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[contributes to](contributes_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[correlated with](correlated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[derives from](derives_from.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[derives into](derives_into.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[develops from](develops_from.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[disease has basis in](disease_has_basis_in.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[disrupted by](disrupted_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[disrupts](disrupts.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[exact match](exact_match.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[filler](filler.md)*  <sub>0..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[genetic association](genetic_association.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[GenotypeToDiseaseAssociation](GenotypeToDiseaseAssociation.md)** *[genotype to disease association➞object](genotype_to_disease_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[GenotypeToDiseaseAssociation](GenotypeToDiseaseAssociation.md)** *[genotype to disease association➞subject](genotype_to_disease_association_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has completed](has_completed.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has decreased amount](has_decreased_amount.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has increased amount](has_increased_amount.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Occurrent](Occurrent.md)** *[has input](has_input.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has not completed](has_not_completed.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Occurrent](Occurrent.md)** *[has output](has_output.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has part](has_part.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Occurrent](Occurrent.md)** *[has participant](has_participant.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Attribute](Attribute.md)** *[has qualitative value](has_qualitative_value.md)*  <sub>0..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[has variant part](has_variant_part.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[homologous to](homologous_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[in linkage disequilibrium with](in_linkage_disequilibrium_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[interacts with](interacts_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[lacks part](lacks_part.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[located in](located_in.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[location of](location_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[MacromolecularMachineToEntityAssociationMixin](MacromolecularMachineToEntityAssociationMixin.md)** *[macromolecular machine to entity association mixin➞subject](macromolecular_machine_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[MaterialSampleDerivationAssociation](MaterialSampleDerivationAssociation.md)** *[material sample derivation association➞object](material_sample_derivation_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[model of](model_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[ModelToDiseaseAssociationMixin](ModelToDiseaseAssociationMixin.md)** *[model to disease association mixin➞subject](model_to_disease_association_mixin_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[named thing➞category](named_thing_category.md)*  <sub>1..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[narrow match](narrow_match.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[negatively correlated with](negatively_correlated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Association](Association.md)** *[object](object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[occurs in](occurs_in.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[opposite of](opposite_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[OrganismTaxonToEnvironmentAssociation](OrganismTaxonToEnvironmentAssociation.md)** *[organism taxon to environment association➞object](organism_taxon_to_environment_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[orthologous to](orthologous_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[overlaps](overlaps.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[paralogous to](paralogous_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[part of](part_of.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[physically interacts with](physically_interacts_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[positively correlated with](positively_correlated_with.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[predisposes](predisposes.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[prevented by](prevented_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[prevents](prevents.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[produced by](produced_by.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[produces](produces.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[related condition](related_condition.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[related to](related_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[same as](same_as.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[similar to](similar_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**
 *  **[Association](Association.md)** *[subject](subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[VariantToDiseaseAssociation](VariantToDiseaseAssociation.md)** *[variant to disease association➞object](variant_to_disease_association_object.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[VariantToDiseaseAssociation](VariantToDiseaseAssociation.md)** *[variant to disease association➞subject](variant_to_disease_association_subject.md)*  <sub>1..1</sub>  **[NamedThing](NamedThing.md)**
 *  **[NamedThing](NamedThing.md)** *[xenologous to](xenologous_to.md)*  <sub>0..\*</sub>  **[NamedThing](NamedThing.md)**

## Attributes


### Own

 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [NamedThing](NamedThing.md)
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

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | BFO:0000001 |
|  | | WIKIDATA:Q35120 |
|  | | UMLSSG:OBJC |
|  | | UMLSSC:T071 |
|  | | UMLSST:enty |

