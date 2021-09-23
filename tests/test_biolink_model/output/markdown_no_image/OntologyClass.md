
# Class: ontology class


a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

URI: [biolink:OntologyClass](https://w3id.org/biolink/vocab/OntologyClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[UnclassifiedOntologyClass],[TaxonomicRank],[RelationshipType],[ClinicalMeasurement]++-%20has%20attribute%20type%201..1>[OntologyClass],[ContributorAssociation]++-%20qualifiers%200..*>[OntologyClass],[GeneExpressionMixin]++-%20quantifier%20qualifier%200..1>[OntologyClass],[GeneToExpressionSiteAssociation]++-%20quantifier%20qualifier%200..1>[OntologyClass],[Attribute]++-%20has%20attribute%20type%201..1>[OntologyClass],[PairwiseMolecularInteraction]++-%20interacting%20molecules%20category%200..1>[OntologyClass],[Association]++-%20qualifiers%200..*>[OntologyClass],[GeneExpressionMixin]++-%20quantifier%20qualifier(i)%200..1>[OntologyClass],[GeneToExpressionSiteAssociation]++-%20quantifier%20qualifier(i)%200..1>[OntologyClass],[ProcessedMaterial]uses%20-.->[OntologyClass],[PhysiologicalProcess]uses%20-.->[OntologyClass],[Pathway]uses%20-.->[OntologyClass],[MolecularEntity]uses%20-.->[OntologyClass],[MolecularActivity]uses%20-.->[OntologyClass],[Drug]uses%20-.->[OntologyClass],[ChemicalSubstance]uses%20-.->[OntologyClass],[BiologicalProcessOrActivity]uses%20-.->[OntologyClass],[BiologicalProcess]uses%20-.->[OntologyClass],[Behavior]uses%20-.->[OntologyClass],[Attribute]uses%20-.->[OntologyClass],[OntologyClass]^-[UnclassifiedOntologyClass],[OntologyClass]^-[TaxonomicRank],[OntologyClass]^-[RelationshipType],[OntologyClass]^-[GeneOntologyClass],[ProcessedMaterial],[PhysiologicalProcess],[Pathway],[PairwiseMolecularInteraction],[NamedThing],[MolecularEntity],[MolecularActivity],[GeneToExpressionSiteAssociation],[GeneOntologyClass],[GeneExpressionMixin],[Drug],[ContributorAssociation],[ClinicalMeasurement],[ChemicalSubstance],[BiologicalProcessOrActivity],[BiologicalProcess],[Behavior],[Attribute],[Association])](https://yuml.me/diagram/nofunky;dir:TB/class/[UnclassifiedOntologyClass],[TaxonomicRank],[RelationshipType],[ClinicalMeasurement]++-%20has%20attribute%20type%201..1>[OntologyClass],[ContributorAssociation]++-%20qualifiers%200..*>[OntologyClass],[GeneExpressionMixin]++-%20quantifier%20qualifier%200..1>[OntologyClass],[GeneToExpressionSiteAssociation]++-%20quantifier%20qualifier%200..1>[OntologyClass],[Attribute]++-%20has%20attribute%20type%201..1>[OntologyClass],[PairwiseMolecularInteraction]++-%20interacting%20molecules%20category%200..1>[OntologyClass],[Association]++-%20qualifiers%200..*>[OntologyClass],[GeneExpressionMixin]++-%20quantifier%20qualifier(i)%200..1>[OntologyClass],[GeneToExpressionSiteAssociation]++-%20quantifier%20qualifier(i)%200..1>[OntologyClass],[ProcessedMaterial]uses%20-.->[OntologyClass],[PhysiologicalProcess]uses%20-.->[OntologyClass],[Pathway]uses%20-.->[OntologyClass],[MolecularEntity]uses%20-.->[OntologyClass],[MolecularActivity]uses%20-.->[OntologyClass],[Drug]uses%20-.->[OntologyClass],[ChemicalSubstance]uses%20-.->[OntologyClass],[BiologicalProcessOrActivity]uses%20-.->[OntologyClass],[BiologicalProcess]uses%20-.->[OntologyClass],[Behavior]uses%20-.->[OntologyClass],[Attribute]uses%20-.->[OntologyClass],[OntologyClass]^-[UnclassifiedOntologyClass],[OntologyClass]^-[TaxonomicRank],[OntologyClass]^-[RelationshipType],[OntologyClass]^-[GeneOntologyClass],[ProcessedMaterial],[PhysiologicalProcess],[Pathway],[PairwiseMolecularInteraction],[NamedThing],[MolecularEntity],[MolecularActivity],[GeneToExpressionSiteAssociation],[GeneOntologyClass],[GeneExpressionMixin],[Drug],[ContributorAssociation],[ClinicalMeasurement],[ChemicalSubstance],[BiologicalProcessOrActivity],[BiologicalProcess],[Behavior],[Attribute],[Association])

## Identifier prefixes

 * MESH
 * UMLS
 * KEGG.BRITE

## Children

 * [GeneOntologyClass](GeneOntologyClass.md) - an ontology class that describes a functional aspect of a gene, gene prodoct or complex
 * [RelationshipType](RelationshipType.md) - An OWL property used as an edge label
 * [TaxonomicRank](TaxonomicRank.md) - A descriptor for the rank within a taxonomic classification. Example instance: TAXRANK:0000017 (kingdom)
 * [UnclassifiedOntologyClass](UnclassifiedOntologyClass.md) - this is used for nodes that are taken from an ontology but are not typed using an existing biolink class

## Mixin for

 * [Attribute](Attribute.md) (mixin)  - A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age, crispiness. An environmental sample may have attributes such as depth, lat, long, material.
 * [Behavior](Behavior.md) (mixin) 
 * [BiologicalProcess](BiologicalProcess.md) (mixin)  - One or more causally connected executions of molecular functions
 * [BiologicalProcessOrActivity](BiologicalProcessOrActivity.md) (mixin)  - Either an individual molecular activity, or a collection of causally connected molecular activities in a biological system.
 * [ChemicalSubstance](ChemicalSubstance.md) (mixin)  - May be a chemical entity or a formulation with a chemical entity as active ingredient, or a complex material with multiple chemical entities as part
 * [Drug](Drug.md) (mixin)  - A substance intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease
 * [MolecularActivity](MolecularActivity.md) (mixin)  - An execution of a molecular function carried out by a gene product or macromolecular complex.
 * [MolecularEntity](MolecularEntity.md) (mixin)  - A gene, gene product, small molecule or macromolecule (including protein complex)"
 * [Pathway](Pathway.md) (mixin) 
 * [PhysiologicalProcess](PhysiologicalProcess.md) (mixin) 
 * [ProcessedMaterial](ProcessedMaterial.md) (mixin)  - A chemical substance (often a mixture) processed for consumption for nutritional, medical or technical use.

## Referenced by Class

 *  **[ClinicalMeasurement](ClinicalMeasurement.md)** *[clinical measurement➞has attribute type](clinical_measurement_has_attribute_type.md)*  <sub>1..1</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[ContributorAssociation](ContributorAssociation.md)** *[contributor association➞qualifiers](contributor_association_qualifiers.md)*  <sub>0..\*</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[GeneExpressionMixin](GeneExpressionMixin.md)** *[gene expression mixin➞quantifier qualifier](gene_expression_mixin_quantifier_qualifier.md)*  <sub>0..1</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[GeneToExpressionSiteAssociation](GeneToExpressionSiteAssociation.md)** *[gene to expression site association➞quantifier qualifier](gene_to_expression_site_association_quantifier_qualifier.md)*  <sub>0..1</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[Attribute](Attribute.md)** *[has attribute type](has_attribute_type.md)*  <sub>1..1</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[NamedThing](NamedThing.md)** *[has molecular consequence](has_molecular_consequence.md)*  <sub>0..\*</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[NamedThing](NamedThing.md)** *[has topic](has_topic.md)*  <sub>0..1</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[Association](Association.md)** *[interacting molecules category](interacting_molecules_category.md)*  <sub>0..1</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[Association](Association.md)** *[qualifiers](qualifiers.md)*  <sub>0..\*</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[Association](Association.md)** *[quantifier qualifier](quantifier_qualifier.md)*  <sub>0..1</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[OntologyClass](OntologyClass.md)** *[subclass of](subclass_of.md)*  <sub>0..\*</sub>  **[OntologyClass](OntologyClass.md)**
 *  **[OntologyClass](OntologyClass.md)** *[superclass of](superclass_of.md)*  <sub>0..\*</sub>  **[OntologyClass](OntologyClass.md)**

## Attributes


## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | This is modeled as a mixin. 'ontology class' should not be the primary type of a node in the KG. Instead you should use an informative bioloink category, such as AnatomicalEntity (for Uberon classes), ChemicalSubstance (for CHEBI or CHEMBL), etc |
|  | | Note that formally this is a metaclass. Instances of this class are instances in the graph, but can be the object of 'type' edges. For example, if we had a node in the graph representing a specific brain of a specific patient (e.g brain001), this could have  a category of bl:Sample, and by typed more specifically with an ontology class UBERON:nnn, which has as category bl:AnatomicalEntity |
| **Examples:** | | Example(value='UBERON:0000955', description="the class 'brain' from the Uberon anatomy ontology") |
| **See also:** | | https://github.com/biolink/biolink-model/issues/486 |
| **Exact Mappings:** | | owl:Class |
|  | | schema:Class |

