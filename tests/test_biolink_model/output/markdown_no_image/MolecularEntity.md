
# Class: molecular entity


A gene, gene product, small molecule or macromolecule (including protein complex)"

URI: [biolink:MolecularEntity](https://w3id.org/biolink/vocab/MolecularEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[PhysicalEssence],[PairwiseMolecularInteraction],[OrganismTaxon],[OntologyClass],[NamedThing],[MolecularEntityToEntityAssociationMixin],[GeneToGoTermAssociation]-%20subject%201..1>[MolecularEntity&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[MolecularEntityToEntityAssociationMixin]-%20subject%201..1>[MolecularEntity],[PairwiseMolecularInteraction]-%20object%201..1>[MolecularEntity],[PairwiseMolecularInteraction]-%20subject%201..1>[MolecularEntity],[MolecularEntity]uses%20-.->[ThingWithTaxon],[MolecularEntity]uses%20-.->[PhysicalEssence],[MolecularEntity]uses%20-.->[OntologyClass],[MolecularEntity]^-[GenomicEntity],[MolecularEntity]^-[GeneFamily],[MolecularEntity]^-[Food],[MolecularEntity]^-[Drug],[MolecularEntity]^-[ChemicalSubstance],[BiologicalEntity]^-[MolecularEntity],[GenomicEntity],[GeneToGoTermAssociation],[GeneFamily],[Food],[Drug],[DiseaseOrPhenotypicFeature],[ChemicalSubstance],[BiologicalEntity],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[PhysicalEssence],[PairwiseMolecularInteraction],[OrganismTaxon],[OntologyClass],[NamedThing],[MolecularEntityToEntityAssociationMixin],[GeneToGoTermAssociation]-%20subject%201..1>[MolecularEntity&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[MolecularEntityToEntityAssociationMixin]-%20subject%201..1>[MolecularEntity],[PairwiseMolecularInteraction]-%20object%201..1>[MolecularEntity],[PairwiseMolecularInteraction]-%20subject%201..1>[MolecularEntity],[MolecularEntity]uses%20-.->[ThingWithTaxon],[MolecularEntity]uses%20-.->[PhysicalEssence],[MolecularEntity]uses%20-.->[OntologyClass],[MolecularEntity]^-[GenomicEntity],[MolecularEntity]^-[GeneFamily],[MolecularEntity]^-[Food],[MolecularEntity]^-[Drug],[MolecularEntity]^-[ChemicalSubstance],[BiologicalEntity]^-[MolecularEntity],[GenomicEntity],[GeneToGoTermAssociation],[GeneFamily],[Food],[Drug],[DiseaseOrPhenotypicFeature],[ChemicalSubstance],[BiologicalEntity],[Attribute],[Agent])

## Parents

 *  is_a: [BiologicalEntity](BiologicalEntity.md)

## Uses Mixin

 *  mixin: [ThingWithTaxon](ThingWithTaxon.md) - A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms; genes, their products and other molecular entities; body parts; biological processes
 *  mixin: [PhysicalEssence](PhysicalEssence.md) - Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.
 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [ChemicalSubstance](ChemicalSubstance.md) - May be a chemical entity or a formulation with a chemical entity as active ingredient, or a complex material with multiple chemical entities as part
 * [Drug](Drug.md) - A substance intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease
 * [Food](Food.md) - A substance consumed by a living organism as a source of nutrition
 * [GeneFamily](GeneFamily.md) - any grouping of multiple genes or gene products related by common descent
 * [GenomicEntity](GenomicEntity.md) - an entity that can either be directly located on a genome (gene, transcript, exon, regulatory region) or is encoded in a genome (protein)

## Referenced by Class

 *  **[MolecularEntity](MolecularEntity.md)** *[affects abundance of](affects_abundance_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects activity of](affects_activity_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects degradation of](affects_degradation_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects folding of](affects_folding_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects localization of](affects_localization_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects metabolic processing of](affects_metabolic_processing_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects molecular modification of](affects_molecular_modification_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects response to](affects_response_to.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects secretion of](affects_secretion_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects stability of](affects_stability_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects synthesis of](affects_synthesis_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects transport of](affects_transport_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[affects uptake of](affects_uptake_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases abundance of](decreases_abundance_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases activity of](decreases_activity_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases degradation of](decreases_degradation_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases folding of](decreases_folding_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases localization of](decreases_localization_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases metabolic processing of](decreases_metabolic_processing_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases molecular interaction](decreases_molecular_interaction.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases molecular modification of](decreases_molecular_modification_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases response to](decreases_response_to.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases secretion of](decreases_secretion_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases stability of](decreases_stability_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases synthesis of](decreases_synthesis_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases transport of](decreases_transport_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[decreases uptake of](decreases_uptake_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[directly interacts with](directly_interacts_with.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[entity negatively regulated by entity](entity_negatively_regulated_by_entity.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[entity negatively regulates entity](entity_negatively_regulates_entity.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[entity positively regulated by entity](entity_positively_regulated_by_entity.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[entity positively regulates entity](entity_positively_regulates_entity.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[entity regulated by entity](entity_regulated_by_entity.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[entity regulates entity](entity_regulates_entity.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[GeneToGoTermAssociation](GeneToGoTermAssociation.md)** *[gene to go term association➞subject](gene_to_go_term_association_subject.md)*  <sub>1..1</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)** *[has biomarker](has_biomarker.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases abundance of](increases_abundance_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases activity of](increases_activity_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases degradation of](increases_degradation_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases folding of](increases_folding_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases localization of](increases_localization_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases metabolic processing of](increases_metabolic_processing_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases molecular interaction](increases_molecular_interaction.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases molecular modification of](increases_molecular_modification_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases response to](increases_response_to.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases secretion of](increases_secretion_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases stability of](increases_stability_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases synthesis of](increases_synthesis_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases transport of](increases_transport_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[increases uptake of](increases_uptake_of.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntityToEntityAssociationMixin](MolecularEntityToEntityAssociationMixin.md)** *[molecular entity to entity association mixin➞subject](molecular_entity_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[MolecularEntity](MolecularEntity.md)** *[molecularly interacts with](molecularly_interacts_with.md)*  <sub>0..\*</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[PairwiseMolecularInteraction](PairwiseMolecularInteraction.md)** *[pairwise molecular interaction➞object](pairwise_molecular_interaction_object.md)*  <sub>1..1</sub>  **[MolecularEntity](MolecularEntity.md)**
 *  **[PairwiseMolecularInteraction](PairwiseMolecularInteraction.md)** *[pairwise molecular interaction➞subject](pairwise_molecular_interaction_subject.md)*  <sub>1..1</sub>  **[MolecularEntity](MolecularEntity.md)**

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
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)

### Mixed in from thing with taxon:

 * [in taxon](in_taxon.md)  <sub>0..\*</sub>
     * Description: connects an entity to its taxonomic classification. Only certain kinds of entities can be taxonomically classified; see 'thing with taxon'
     * Range: [OrganismTaxon](OrganismTaxon.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | bioentity |
| **Exact Mappings:** | | CHEBI:24431 |
| **Narrow Mappings:** | | SIO:010341 |
|  | | WIKIDATA:Q43460564 |
|  | | UMLSSG:CHEM |
|  | | UMLSSC:T085 |
|  | | UMLSST:mosq |
|  | | UMLSSC:T123 |
|  | | UMLSST:bacs |
|  | | UMLSSC:T125 |
|  | | UMLSST:horm |
|  | | UMLSSC:T126 |
|  | | UMLSST:enzy |
|  | | UMLSSC:T129 |
|  | | UMLSST:imft |
|  | | UMLSSC:T192 |
|  | | UMLSST:rcpt |

