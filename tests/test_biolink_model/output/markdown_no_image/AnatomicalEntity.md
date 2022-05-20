
# Class: anatomical entity


A subcellular location, cell type or gross anatomical part

URI: [biolink:AnatomicalEntity](https://w3id.org/biolink/vocab/AnatomicalEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[PhysicalEssence],[PathologicalAnatomicalStructure],[OrganismalEntity],[OrganismTaxon],[NamedThing],[GrossAnatomicalStructure],[GeneToExpressionSiteAssociation],[GeneOrGeneProduct],[DiseaseOrPhenotypicFeatureToLocationAssociation],[DiseaseOrPhenotypicFeatureAssociationToLocationAssociation],[CellularComponent],[Cell],[Attribute],[Association],[AnatomicalEntityToAnatomicalEntityPartOfAssociation],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation],[AnatomicalEntityToAnatomicalEntityAssociation],[AnatomicalEntityToAnatomicalEntityAssociation]-%20object%201..1>[AnatomicalEntity&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[AnatomicalEntityToAnatomicalEntityAssociation]-%20subject%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation]-%20subject%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityPartOfAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityPartOfAssociation]-%20subject%201..1>[AnatomicalEntity],[DiseaseOrPhenotypicFeatureAssociationToLocationAssociation]-%20object%201..1>[AnatomicalEntity],[DiseaseOrPhenotypicFeatureToLocationAssociation]-%20object%201..1>[AnatomicalEntity],[GeneExpressionMixin]-%20expression%20site%200..1>[AnatomicalEntity],[GeneToExpressionSiteAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntity]uses%20-.->[ThingWithTaxon],[AnatomicalEntity]uses%20-.->[PhysicalEssence],[AnatomicalEntity]^-[PathologicalAnatomicalStructure],[AnatomicalEntity]^-[GrossAnatomicalStructure],[AnatomicalEntity]^-[CellularComponent],[AnatomicalEntity]^-[Cell],[OrganismalEntity]^-[AnatomicalEntity],[GeneExpressionMixin],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[PhysicalEssence],[PathologicalAnatomicalStructure],[OrganismalEntity],[OrganismTaxon],[NamedThing],[GrossAnatomicalStructure],[GeneToExpressionSiteAssociation],[GeneOrGeneProduct],[DiseaseOrPhenotypicFeatureToLocationAssociation],[DiseaseOrPhenotypicFeatureAssociationToLocationAssociation],[CellularComponent],[Cell],[Attribute],[Association],[AnatomicalEntityToAnatomicalEntityPartOfAssociation],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation],[AnatomicalEntityToAnatomicalEntityAssociation],[AnatomicalEntityToAnatomicalEntityAssociation]-%20object%201..1>[AnatomicalEntity&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[AnatomicalEntityToAnatomicalEntityAssociation]-%20subject%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityOntogenicAssociation]-%20subject%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityPartOfAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntityToAnatomicalEntityPartOfAssociation]-%20subject%201..1>[AnatomicalEntity],[DiseaseOrPhenotypicFeatureAssociationToLocationAssociation]-%20object%201..1>[AnatomicalEntity],[DiseaseOrPhenotypicFeatureToLocationAssociation]-%20object%201..1>[AnatomicalEntity],[GeneExpressionMixin]-%20expression%20site%200..1>[AnatomicalEntity],[GeneToExpressionSiteAssociation]-%20object%201..1>[AnatomicalEntity],[AnatomicalEntity]uses%20-.->[ThingWithTaxon],[AnatomicalEntity]uses%20-.->[PhysicalEssence],[AnatomicalEntity]^-[PathologicalAnatomicalStructure],[AnatomicalEntity]^-[GrossAnatomicalStructure],[AnatomicalEntity]^-[CellularComponent],[AnatomicalEntity]^-[Cell],[OrganismalEntity]^-[AnatomicalEntity],[GeneExpressionMixin],[Agent])

## Identifier prefixes

 * UBERON
 * GO
 * CL
 * UMLS
 * MESH
 * NCIT

## Parents

 *  is_a: [OrganismalEntity](OrganismalEntity.md) - A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding molecular entities

## Uses Mixin

 *  mixin: [ThingWithTaxon](ThingWithTaxon.md) - A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms; genes, their products and other molecular entities; body parts; biological processes
 *  mixin: [PhysicalEssence](PhysicalEssence.md) - Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.

## Children

 * [Cell](Cell.md)
 * [CellularComponent](CellularComponent.md) - A location in or around a cell
 * [GrossAnatomicalStructure](GrossAnatomicalStructure.md)
 * [PathologicalAnatomicalStructure](PathologicalAnatomicalStructure.md) - An anatomical structure with the potential of have an abnormal or deleterious effect at the subcellular, cellular, multicellular, or organismal level.

## Referenced by Class

 *  **[AnatomicalEntityToAnatomicalEntityAssociation](AnatomicalEntityToAnatomicalEntityAssociation.md)** *[anatomical entity to anatomical entity association➞object](anatomical_entity_to_anatomical_entity_association_object.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityAssociation](AnatomicalEntityToAnatomicalEntityAssociation.md)** *[anatomical entity to anatomical entity association➞subject](anatomical_entity_to_anatomical_entity_association_subject.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityOntogenicAssociation](AnatomicalEntityToAnatomicalEntityOntogenicAssociation.md)** *[anatomical entity to anatomical entity ontogenic association➞object](anatomical_entity_to_anatomical_entity_ontogenic_association_object.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityOntogenicAssociation](AnatomicalEntityToAnatomicalEntityOntogenicAssociation.md)** *[anatomical entity to anatomical entity ontogenic association➞subject](anatomical_entity_to_anatomical_entity_ontogenic_association_subject.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityPartOfAssociation](AnatomicalEntityToAnatomicalEntityPartOfAssociation.md)** *[anatomical entity to anatomical entity part of association➞object](anatomical_entity_to_anatomical_entity_part_of_association_object.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[AnatomicalEntityToAnatomicalEntityPartOfAssociation](AnatomicalEntityToAnatomicalEntityPartOfAssociation.md)** *[anatomical entity to anatomical entity part of association➞subject](anatomical_entity_to_anatomical_entity_part_of_association_subject.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[DiseaseOrPhenotypicFeatureAssociationToLocationAssociation](DiseaseOrPhenotypicFeatureAssociationToLocationAssociation.md)** *[disease or phenotypic feature association to location association➞object](disease_or_phenotypic_feature_association_to_location_association_object.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[DiseaseOrPhenotypicFeatureToLocationAssociation](DiseaseOrPhenotypicFeatureToLocationAssociation.md)** *[disease or phenotypic feature to location association➞object](disease_or_phenotypic_feature_to_location_association_object.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[GeneOrGeneProduct](GeneOrGeneProduct.md)** *[expressed in](expressed_in.md)*  <sub>0..\*</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[Association](Association.md)** *[expression site](expression_site.md)*  <sub>0..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**
 *  **[GeneToExpressionSiteAssociation](GeneToExpressionSiteAssociation.md)** *[gene to expression site association➞object](gene_to_expression_site_association_object.md)*  <sub>1..1</sub>  **[AnatomicalEntity](AnatomicalEntity.md)**

## Attributes


### Inherited from organismal entity:

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
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)
 * [organismal entity➞has attribute](organismal_entity_has_attribute.md)  <sub>0..\*</sub>
     * Description: may often be an organism attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)

### Mixed in from thing with taxon:

 * [in taxon](in_taxon.md)  <sub>0..\*</sub>
     * Description: connects an entity to its taxonomic classification. Only certain kinds of entities can be taxonomically classified; see 'thing with taxon'
     * Range: [OrganismTaxon](OrganismTaxon.md)
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

