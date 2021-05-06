
# Class: AnatomicalEntity


A subcellular location, cell type or gross anatomical part

URI: [biolink:AnatomicalEntity](https://w3id.org/biolink/vocab/AnatomicalEntity)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[PhysicalEssence],[PathologicalAnatomicalStructure],[OrganismalEntity],[OrganismTaxon],[NamedThing],[GrossAnatomicalStructure],[GeneToExpressionSiteAssociation],[GeneOrGeneProduct],[DiseaseOrPhenotypicFeatureToLocationAssociation],[DiseaseOrPhenotypicFeatureAssociationToLocationAssociation],[CellularComponent],[Cell],[Attribute],[Association],[AnatomicalEntityToAnatomicalEntityPartOfAssociation],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation],[AnatomicalEntityToAnatomicalEntityAssociation],[AnatomicalEntityToAnatomicalEntityAssociation]-%20object%201..1>[AnatomicalEntity&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[AnatomicalEntityToAnatomicalEntityAssociation]-%20subject%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation]-%20subject%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityPartOfAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityPartOfAssociation]-%20subject%201..1>[AnatomicalEntity],[DiseaseOrPhenotypicFeatureAssociationToLocationAssociation]-%20object%201..1>[AnatomicalEntity],[DiseaseOrPhenotypicFeatureToLocationAssociation]-%20object%201..1>[AnatomicalEntity],[GeneExpressionMixin]-%20expression%20site%200..1>[AnatomicalEntity],[GeneToExpressionSiteAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntity]uses%20-.->[ThingWithTaxon],[AnatomicalEntity]uses%20-.->[PhysicalEssence],[AnatomicalEntity]^-[PathologicalAnatomicalStructure],[AnatomicalEntity]^-[GrossAnatomicalStructure],[AnatomicalEntity]^-[CellularComponent],[AnatomicalEntity]^-[Cell],[OrganismalEntity]^-[AnatomicalEntity],[GeneExpressionMixin],[Agent])

## Identifier prefixes

 * UBERON
 * GO
 * CL
 * UMLS
 * MESH
 * NCIT

## Parents

 *  is_a: [OrganismalEntity](OrganismalEntity.md) - A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding molecular entities

## Uses Mixins

 *  mixin: [ThingWithTaxon](ThingWithTaxon.md) - A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms; genes, their products and other molecular entities; body parts; biological processes
 *  mixin: [PhysicalEssence](PhysicalEssence.md) - Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.

## Children

 * [Cell](Cell.md)
 * [CellularComponent](CellularComponent.md) - A location in or around a cell
 * [GrossAnatomicalStructure](GrossAnatomicalStructure.md)
 * [PathologicalAnatomicalStructure](PathologicalAnatomicalStructure.md) - An anatomical structure with the potential of have an abnormal or deleterious effect at the subcellular, cellular, multicellular, or organismal level.

## Referenced by class

 *  **[AnatomicalEntityToAnatomicalEntityAssociation](AnatomicalEntityToAnatomicalEntityAssociation.md)** *[anatomical entity to anatomical entity association➞object](anatomical_entity_to_anatomical_entity_association_object.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityAssociation](AnatomicalEntityToAnatomicalEntityAssociation.md)** *[anatomical entity to anatomical entity association➞subject](anatomical_entity_to_anatomical_entity_association_subject.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityOntogenicAssociation](AnatomicalEntityToAnatomicalEntityOntogenicAssociation.md)** *[anatomical entity to anatomical entity ontogenic association➞object](anatomical_entity_to_anatomical_entity_ontogenic_association_object.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityOntogenicAssociation](AnatomicalEntityToAnatomicalEntityOntogenicAssociation.md)** *[anatomical entity to anatomical entity ontogenic association➞subject](anatomical_entity_to_anatomical_entity_ontogenic_association_subject.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityPartOfAssociation](AnatomicalEntityToAnatomicalEntityPartOfAssociation.md)** *[anatomical entity to anatomical entity part of association➞object](anatomical_entity_to_anatomical_entity_part_of_association_object.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityPartOfAssociation](AnatomicalEntityToAnatomicalEntityPartOfAssociation.md)** *[anatomical entity to anatomical entity part of association➞subject](anatomical_entity_to_anatomical_entity_part_of_association_subject.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[DiseaseOrPhenotypicFeatureAssociationToLocationAssociation](DiseaseOrPhenotypicFeatureAssociationToLocationAssociation.md)** *[disease or phenotypic feature association to location association➞object](disease_or_phenotypic_feature_association_to_location_association_object.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[DiseaseOrPhenotypicFeatureToLocationAssociation](DiseaseOrPhenotypicFeatureToLocationAssociation.md)** *[disease or phenotypic feature to location association➞object](disease_or_phenotypic_feature_to_location_association_object.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[GeneOrGeneProduct](GeneOrGeneProduct.md)** *[expressed in](expressed_in.md)*  <sub>0..*</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[Association](Association.md)** *[expression site](expression_site.md)*  <sub>OPT</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[GeneToExpressionSiteAssociation](GeneToExpressionSiteAssociation.md)** *[gene to expression site association➞object](gene_to_expression_site_association_object.md)*  <sub>REQ</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**

## Attributes


### Inherited from organismal entity:

 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
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
 * [organismal entity➞has attribute](organismal_entity_has_attribute.md)  <sub>0..*</sub>
     * Description: may often be an organism attribute
     * range: [Attribute](Attribute.md)
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
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | UBERON:0001062 |
|  | | WIKIDATA:Q4936952 |
|  | | UMLSSG:ANAT |
| **Narrow Mappings:** | | UMLSSC:T022 |
|  | | UMLSST:bdsy |
|  | | UMLSSC:T029 |
|  | | UMLSST:blor |
|  | | UMLSSC:T030 |
|  | | UMLSST:bsoj |
|  | | UMLSSC:T031 |
|  | | UMLSST:bdsu |

