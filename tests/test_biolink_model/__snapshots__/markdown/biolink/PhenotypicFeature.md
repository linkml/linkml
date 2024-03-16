
# Class: phenotypic feature


A combination of entity and quality that makes up a phenotyping statement. An observable characteristic of an  individual resulting from the interaction of its genotype with its molecular and physical environment.

URI: [biolink:PhenotypicFeature](https://w3id.org/biolink/vocab/PhenotypicFeature)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[DiseaseToPhenotypicFeatureAssociation]-%20object%201..1>[PhenotypicFeature&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[EntityToPhenotypicFeatureAssociationMixin]-%20object%201..1>[PhenotypicFeature],[GeneToPhenotypicFeatureAssociation]-%20object%201..1>[PhenotypicFeature],[PhenotypicFeature]^-[ClinicalFinding],[PhenotypicFeature]^-[BehavioralFeature],[DiseaseOrPhenotypicFeature]^-[PhenotypicFeature],[OrganismTaxon],[GeneToPhenotypicFeatureAssociation],[EntityToPhenotypicFeatureAssociationMixin],[DiseaseToPhenotypicFeatureAssociation],[DiseaseOrPhenotypicFeature],[ClinicalFinding],[BiologicalEntity],[BehavioralFeature],[Attribute])](https://yuml.me/diagram/nofunky;dir:TB/class/[DiseaseToPhenotypicFeatureAssociation]-%20object%201..1>[PhenotypicFeature&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[EntityToPhenotypicFeatureAssociationMixin]-%20object%201..1>[PhenotypicFeature],[GeneToPhenotypicFeatureAssociation]-%20object%201..1>[PhenotypicFeature],[PhenotypicFeature]^-[ClinicalFinding],[PhenotypicFeature]^-[BehavioralFeature],[DiseaseOrPhenotypicFeature]^-[PhenotypicFeature],[OrganismTaxon],[GeneToPhenotypicFeatureAssociation],[EntityToPhenotypicFeatureAssociationMixin],[DiseaseToPhenotypicFeatureAssociation],[DiseaseOrPhenotypicFeature],[ClinicalFinding],[BiologicalEntity],[BehavioralFeature],[Attribute])

## Identifier prefixes

 * HP
 * EFO
 * NCIT
 * UMLS
 * MEDDRA
 * MP
 * ZP
 * UPHENO
 * APO
 * FBcv
 * WBPhenotype
 * SNOMEDCT
 * MESH
 * XPO
 * FYPO
 * TO

## Parents

 *  is_a: [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md) - Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.  Please see definitions of phenotypic feature and disease in this model for their independent descriptions.  This class is helpful to enforce domains and ranges   that may involve either a disease or a phenotypic feature.

## Children

 * [BehavioralFeature](BehavioralFeature.md) - A phenotypic feature which is behavioral in nature.
 * [ClinicalFinding](ClinicalFinding.md) - this category is currently considered broad enough to tag clinical lab measurements and other biological attributes taken as 'clinical traits' with some statistical score, for example, a p value in genetic associations.

## Referenced by Class

 *  **[DiseaseToPhenotypicFeatureAssociation](DiseaseToPhenotypicFeatureAssociation.md)** *[disease to phenotypic feature association➞object](disease_to_phenotypic_feature_association_object.md)*  <sub>1..1</sub>  **[PhenotypicFeature](PhenotypicFeature.md)**
 *  **[EntityToPhenotypicFeatureAssociationMixin](EntityToPhenotypicFeatureAssociationMixin.md)** *[entity to phenotypic feature association mixin➞object](entity_to_phenotypic_feature_association_mixin_object.md)*  <sub>1..1</sub>  **[PhenotypicFeature](PhenotypicFeature.md)**
 *  **[GeneToPhenotypicFeatureAssociation](GeneToPhenotypicFeatureAssociation.md)** *[gene to phenotypic feature association➞object](gene_to_phenotypic_feature_association_object.md)*  <sub>1..1</sub>  **[PhenotypicFeature](PhenotypicFeature.md)**
 *  **[BiologicalEntity](BiologicalEntity.md)** *[has phenotype](has_phenotype.md)*  <sub>0..\*</sub>  **[PhenotypicFeature](PhenotypicFeature.md)**

## Attributes


### Inherited from disease or phenotypic feature:

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
| **Aliases:** | | sign |
|  | | symptom |
|  | | phenotype |
|  | | trait |
|  | | endophenotype |
| **Examples:** | | Example(value='MP:0001262', description='decreased body weight', object=None) |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | UPHENO:0001001 |
|  | | SIO:010056 |
|  | | WIKIDATA:Q104053 |
|  | | UMLS:C4021819 |
|  | | NCIT:C16977 |
|  | | SNOMEDCT:8116006 |
|  | | MESH:D010641 |
| **Narrow Mappings:** | | STY:T184 |
|  | | WIKIDATA:Q169872 |
|  | | WIKIDATA:Q25203551 |
|  | | ZP:00000000 |
|  | | FBcv:0001347 |
|  | | HP:0000118 |
|  | | MP:0000001 |
|  | | WBPhenotype:0000886 |
|  | | XPO:00000000 |
|  | | FYPO:0000001 |
|  | | APO:0000017 |
|  | | TO:0000387 |
| **Broad Mappings:** | | BFO:0000019 |
|  | | PATO:0000001 |

