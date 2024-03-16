
# Class: disease or phenotypic feature


Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.  Please see definitions of phenotypic feature and disease in this model for their independent descriptions.  This class is helpful to enforce domains and ranges   that may involve either a disease or a phenotypic feature.

URI: [biolink:DiseaseOrPhenotypicFeature](https://w3id.org/biolink/vocab/DiseaseOrPhenotypicFeature)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PhenotypicFeature],[OrganismTaxon],[NamedThing],[GeneticInheritance],[Gene],[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[Drug],[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[CellLineToDiseaseOrPhenotypicFeatureAssociation]-%20subject%201..1>[DiseaseOrPhenotypicFeature&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[ChemicalToDiseaseOrPhenotypicFeatureAssociation]-%20object%201..1>[DiseaseOrPhenotypicFeature],[DiseaseOrPhenotypicFeatureToEntityAssociationMixin]-%20subject%201..1>[DiseaseOrPhenotypicFeature],[EntityToDiseaseOrPhenotypicFeatureAssociationMixin]-%20object%201..1>[DiseaseOrPhenotypicFeature],[GeneExpressionMixin]-%20phenotypic%20state%200..1>[DiseaseOrPhenotypicFeature],[DiseaseOrPhenotypicFeature]^-[PhenotypicFeature],[DiseaseOrPhenotypicFeature]^-[Disease],[BiologicalEntity]^-[DiseaseOrPhenotypicFeature],[GeneExpressionMixin],[Disease],[ChemicalToDiseaseOrPhenotypicFeatureAssociation],[ChemicalOrDrugOrTreatment],[ChemicalEntityOrGeneOrGeneProduct],[CellLineToDiseaseOrPhenotypicFeatureAssociation],[BiologicalEntity],[Attribute],[Association])](https://yuml.me/diagram/nofunky;dir:TB/class/[PhenotypicFeature],[OrganismTaxon],[NamedThing],[GeneticInheritance],[Gene],[EntityToDiseaseOrPhenotypicFeatureAssociationMixin],[Drug],[DiseaseOrPhenotypicFeatureToEntityAssociationMixin],[CellLineToDiseaseOrPhenotypicFeatureAssociation]-%20subject%201..1>[DiseaseOrPhenotypicFeature&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[ChemicalToDiseaseOrPhenotypicFeatureAssociation]-%20object%201..1>[DiseaseOrPhenotypicFeature],[DiseaseOrPhenotypicFeatureToEntityAssociationMixin]-%20subject%201..1>[DiseaseOrPhenotypicFeature],[EntityToDiseaseOrPhenotypicFeatureAssociationMixin]-%20object%201..1>[DiseaseOrPhenotypicFeature],[GeneExpressionMixin]-%20phenotypic%20state%200..1>[DiseaseOrPhenotypicFeature],[DiseaseOrPhenotypicFeature]^-[PhenotypicFeature],[DiseaseOrPhenotypicFeature]^-[Disease],[BiologicalEntity]^-[DiseaseOrPhenotypicFeature],[GeneExpressionMixin],[Disease],[ChemicalToDiseaseOrPhenotypicFeatureAssociation],[ChemicalOrDrugOrTreatment],[ChemicalEntityOrGeneOrGeneProduct],[CellLineToDiseaseOrPhenotypicFeatureAssociation],[BiologicalEntity],[Attribute],[Association])

## Parents

 *  is_a: [BiologicalEntity](BiologicalEntity.md)

## Children

 * [Disease](Disease.md) - A disorder of structure or function, especially one that produces specific  signs, phenotypes or symptoms or that affects a specific location and is not simply a  direct result of physical injury.  A disposition to undergo pathological processes that exists in an  organism because of one or more disorders in that organism.
 * [PhenotypicFeature](PhenotypicFeature.md) - A combination of entity and quality that makes up a phenotyping statement. An observable characteristic of an  individual resulting from the interaction of its genotype with its molecular and physical environment.

## Referenced by Class

 *  **[NamedThing](NamedThing.md)** *[ameliorates](ameliorates.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[NamedThing](NamedThing.md)** *[animal model available from](animal_model_available_from.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[ChemicalEntityOrGeneOrGeneProduct](ChemicalEntityOrGeneOrGeneProduct.md)** *[biomarker for](biomarker_for.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[CellLineToDiseaseOrPhenotypicFeatureAssociation](CellLineToDiseaseOrPhenotypicFeatureAssociation.md)** *[cell line to disease or phenotypic feature association➞subject](cell_line_to_disease_or_phenotypic_feature_association_subject.md)*  <sub>1..1</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[ChemicalToDiseaseOrPhenotypicFeatureAssociation](ChemicalToDiseaseOrPhenotypicFeatureAssociation.md)** *[chemical to disease or phenotypic feature association➞object](chemical_to_disease_or_phenotypic_feature_association_object.md)*  <sub>1..1</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Gene](Gene.md)** *[condition associated with gene](condition_associated_with_gene.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Drug](Drug.md)** *[contraindicated for](contraindicated_for.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[ChemicalOrDrugOrTreatment](ChemicalOrDrugOrTreatment.md)** *[diagnoses](diagnoses.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[DiseaseOrPhenotypicFeatureToEntityAssociationMixin](DiseaseOrPhenotypicFeatureToEntityAssociationMixin.md)** *[disease or phenotypic feature to entity association mixin➞subject](disease_or_phenotypic_feature_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[EntityToDiseaseOrPhenotypicFeatureAssociationMixin](EntityToDiseaseOrPhenotypicFeatureAssociationMixin.md)** *[entity to disease or phenotypic feature association mixin➞object](entity_to_disease_or_phenotypic_feature_association_mixin_object.md)*  <sub>1..1</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[BiologicalEntity](BiologicalEntity.md)** *[exacerbates](exacerbates.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[ChemicalOrDrugOrTreatment](ChemicalOrDrugOrTreatment.md)** *[has adverse event](has_adverse_event.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[ChemicalOrDrugOrTreatment](ChemicalOrDrugOrTreatment.md)** *[has side effect](has_side_effect.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[GeneticInheritance](GeneticInheritance.md)** *[mode of inheritance of](mode_of_inheritance_of.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[Association](Association.md)** *[phenotypic state](phenotypic_state.md)*  <sub>0..1</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**
 *  **[ChemicalOrDrugOrTreatment](ChemicalOrDrugOrTreatment.md)** *[treats](treats.md)*  <sub>0..\*</sub>  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)**

## Attributes


### Inherited from biological entity:

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

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | phenome |
| **Narrow Mappings:** | | STY:T033 |

