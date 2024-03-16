
# Class: disease


A disorder of structure or function, especially one that produces specific  signs, phenotypes or symptoms or that affects a specific location and is not simply a  direct result of physical injury.  A disposition to undergo pathological processes that exists in an  organism because of one or more disorders in that organism.

URI: [biolink:Disease](https://w3id.org/biolink/vocab/Disease)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon],[NamedThing],[GeneToDiseaseAssociation],[GeneHasVariantThatContributesToDiseaseAssociation],[Gene],[EntityToDiseaseAssociationMixin],[DiseaseToPhenotypicFeatureAssociation],[DiseaseToEntityAssociationMixin],[DiseaseOrPhenotypicFeature],[DiseaseToEntityAssociationMixin]-%20subject%201..1>[Disease&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[DiseaseToPhenotypicFeatureAssociation]-%20subject%201..1>[Disease],[EntityToDiseaseAssociationMixin]-%20object%201..1>[Disease],[GeneHasVariantThatContributesToDiseaseAssociation]-%20object%201..1>[Disease],[GeneToDiseaseAssociation]-%20object%201..1>[Disease],[DiseaseOrPhenotypicFeature]^-[Disease],[Attribute])](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon],[NamedThing],[GeneToDiseaseAssociation],[GeneHasVariantThatContributesToDiseaseAssociation],[Gene],[EntityToDiseaseAssociationMixin],[DiseaseToPhenotypicFeatureAssociation],[DiseaseToEntityAssociationMixin],[DiseaseOrPhenotypicFeature],[DiseaseToEntityAssociationMixin]-%20subject%201..1>[Disease&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[DiseaseToPhenotypicFeatureAssociation]-%20subject%201..1>[Disease],[EntityToDiseaseAssociationMixin]-%20object%201..1>[Disease],[GeneHasVariantThatContributesToDiseaseAssociation]-%20object%201..1>[Disease],[GeneToDiseaseAssociation]-%20object%201..1>[Disease],[DiseaseOrPhenotypicFeature]^-[Disease],[Attribute])

## Identifier prefixes

 * MONDO
 * DOID
 * OMIM
 * OMIM.PS
 * orphanet
 * EFO
 * UMLS
 * MESH
 * MEDDRA
 * NCIT
 * SNOMEDCT
 * medgen
 * ICD10
 * ICD9
 * KEGG.DISEASE
 * HP
 * MP

## Parents

 *  is_a: [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md) - Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these as distinct, others such as MESH conflate.  Please see definitions of phenotypic feature and disease in this model for their independent descriptions.  This class is helpful to enforce domains and ranges   that may involve either a disease or a phenotypic feature.

## Referenced by Class

 *  **[DiseaseToEntityAssociationMixin](DiseaseToEntityAssociationMixin.md)** *[disease to entity association mixin➞subject](disease_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[Disease](Disease.md)**
 *  **[DiseaseToPhenotypicFeatureAssociation](DiseaseToPhenotypicFeatureAssociation.md)** *[disease to phenotypic feature association➞subject](disease_to_phenotypic_feature_association_subject.md)*  <sub>1..1</sub>  **[Disease](Disease.md)**
 *  **[EntityToDiseaseAssociationMixin](EntityToDiseaseAssociationMixin.md)** *[entity to disease association mixin➞object](entity_to_disease_association_mixin_object.md)*  <sub>1..1</sub>  **[Disease](Disease.md)**
 *  **[GeneHasVariantThatContributesToDiseaseAssociation](GeneHasVariantThatContributesToDiseaseAssociation.md)** *[gene has variant that contributes to disease association➞object](gene_has_variant_that_contributes_to_disease_association_object.md)*  <sub>1..1</sub>  **[Disease](Disease.md)**
 *  **[GeneToDiseaseAssociation](GeneToDiseaseAssociation.md)** *[gene to disease association➞object](gene_to_disease_association_object.md)*  <sub>1..1</sub>  **[Disease](Disease.md)**
 *  **[NamedThing](NamedThing.md)** *[manifestation of](manifestation_of.md)*  <sub>0..\*</sub>  **[Disease](Disease.md)**
 *  **[Gene](Gene.md)** *[target for](target_for.md)*  <sub>0..\*</sub>  **[Disease](Disease.md)**

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
| **Aliases:** | | condition |
|  | | disorder |
|  | | medical condition |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | MONDO:0000001 |
|  | | DOID:4 |
|  | | NCIT:C2991 |
|  | | WIKIDATA:Q12136 |
|  | | SIO:010299 |
|  | | UMLSSG:DISO |
|  | | STY:T047 |
|  | | dcid:Disease |
| **Narrow Mappings:** | | STY:T019 |
|  | | STY:T020 |
|  | | STY:T048 |
|  | | STY:T049 |
|  | | STY:T190 |
|  | | STY:T191 |
|  | | MONDO:0042489 |

