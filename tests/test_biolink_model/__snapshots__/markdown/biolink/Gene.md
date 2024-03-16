
# Class: gene


A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.

URI: [biolink:Gene](https://w3id.org/biolink/vocab/Gene)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[VariantToGeneAssociation],[TranscriptToGeneRelationship],[Transcript],[SequenceVariant],[PhysicalEssence],[OrganismTaxon],[OntologyClass],[NamedThing],[GenotypeToGeneAssociation],[GenomicEntity],[GeneToGoTermAssociation],[GeneToGeneProductRelationship],[GeneToGeneFamilyAssociation],[GeneProductMixin],[GeneOrGeneProduct],[GeneToGeneFamilyAssociation]-%20subject%201..1>[Gene&#124;symbol:string%20%3F;synonym:label_type%20*;has_biological_sequence:biological_sequence%20%3F;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[GeneToGeneProductRelationship]-%20subject%201..1>[Gene],[GeneToGoTermAssociation]-%20subject%201..1>[Gene],[GenotypeToGeneAssociation]-%20object%201..1>[Gene],[SequenceVariant]-%20has%20gene(i)%200..*>[Gene],[GeneGroupingMixin]-%20has%20gene%20or%20gene%20product%200..*>[Gene],[SequenceVariant]-%20has%20gene%200..*>[Gene],[TranscriptToGeneRelationship]-%20object%201..1>[Gene],[VariantToGeneAssociation]-%20object%201..1>[Gene],[Gene]uses%20-.->[GeneOrGeneProduct],[Gene]uses%20-.->[GenomicEntity],[Gene]uses%20-.->[ChemicalEntityOrGeneOrGeneProduct],[Gene]uses%20-.->[PhysicalEssence],[Gene]uses%20-.->[OntologyClass],[BiologicalEntity]^-[Gene],[GeneGroupingMixin],[DiseaseOrPhenotypicFeature],[Disease],[ChemicalEntityOrGeneOrGeneProduct],[BiologicalEntity],[Attribute])](https://yuml.me/diagram/nofunky;dir:TB/class/[VariantToGeneAssociation],[TranscriptToGeneRelationship],[Transcript],[SequenceVariant],[PhysicalEssence],[OrganismTaxon],[OntologyClass],[NamedThing],[GenotypeToGeneAssociation],[GenomicEntity],[GeneToGoTermAssociation],[GeneToGeneProductRelationship],[GeneToGeneFamilyAssociation],[GeneProductMixin],[GeneOrGeneProduct],[GeneToGeneFamilyAssociation]-%20subject%201..1>[Gene&#124;symbol:string%20%3F;synonym:label_type%20*;has_biological_sequence:biological_sequence%20%3F;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[GeneToGeneProductRelationship]-%20subject%201..1>[Gene],[GeneToGoTermAssociation]-%20subject%201..1>[Gene],[GenotypeToGeneAssociation]-%20object%201..1>[Gene],[SequenceVariant]-%20has%20gene(i)%200..*>[Gene],[GeneGroupingMixin]-%20has%20gene%20or%20gene%20product%200..*>[Gene],[SequenceVariant]-%20has%20gene%200..*>[Gene],[TranscriptToGeneRelationship]-%20object%201..1>[Gene],[VariantToGeneAssociation]-%20object%201..1>[Gene],[Gene]uses%20-.->[GeneOrGeneProduct],[Gene]uses%20-.->[GenomicEntity],[Gene]uses%20-.->[ChemicalEntityOrGeneOrGeneProduct],[Gene]uses%20-.->[PhysicalEssence],[Gene]uses%20-.->[OntologyClass],[BiologicalEntity]^-[Gene],[GeneGroupingMixin],[DiseaseOrPhenotypicFeature],[Disease],[ChemicalEntityOrGeneOrGeneProduct],[BiologicalEntity],[Attribute])

## Identifier prefixes

 * NCBIGene
 * ENSEMBL
 * HGNC
 * MGI
 * ZFIN
 * dictyBase
 * WB
 * WormBase
 * FB
 * RGD
 * SGD
 * PomBase
 * OMIM
 * KEGG.GENE
 * UMLS
 * Xenbase
 * AspGD

## Parents

 *  is_a: [BiologicalEntity](BiologicalEntity.md)

## Uses Mixin

 *  mixin: [GeneOrGeneProduct](GeneOrGeneProduct.md) - A union of gene loci or gene products. Frequently an identifier for one will be used as proxy for another
 *  mixin: [GenomicEntity](GenomicEntity.md)
 *  mixin: [ChemicalEntityOrGeneOrGeneProduct](ChemicalEntityOrGeneOrGeneProduct.md) - A union of chemical entities and children, and gene or gene product. This mixin is helpful to use when searching across chemical entities that must include genes and their children as chemical entities.
 *  mixin: [PhysicalEssence](PhysicalEssence.md) - Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.
 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Referenced by Class

 *  **[DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)** *[gene associated with condition](gene_associated_with_condition.md)*  <sub>0..\*</sub>  **[Gene](Gene.md)**
 *  **[GeneProductMixin](GeneProductMixin.md)** *[gene product of](gene_product_of.md)*  <sub>0..\*</sub>  **[Gene](Gene.md)**
 *  **[GeneToGeneFamilyAssociation](GeneToGeneFamilyAssociation.md)** *[gene to gene family association➞subject](gene_to_gene_family_association_subject.md)*  <sub>1..1</sub>  **[Gene](Gene.md)**
 *  **[GeneToGeneProductRelationship](GeneToGeneProductRelationship.md)** *[gene to gene product relationship➞subject](gene_to_gene_product_relationship_subject.md)*  <sub>1..1</sub>  **[Gene](Gene.md)**
 *  **[GeneToGoTermAssociation](GeneToGoTermAssociation.md)** *[gene to go term association➞subject](gene_to_go_term_association_subject.md)*  <sub>1..1</sub>  **[Gene](Gene.md)**
 *  **[Gene](Gene.md)** *[genetically interacts with](genetically_interacts_with.md)*  <sub>0..\*</sub>  **[Gene](Gene.md)**
 *  **[GenotypeToGeneAssociation](GenotypeToGeneAssociation.md)** *[genotype to gene association➞object](genotype_to_gene_association_object.md)*  <sub>1..1</sub>  **[Gene](Gene.md)**
 *  **[NamedThing](NamedThing.md)** *[has gene](has_gene.md)*  <sub>0..\*</sub>  **[Gene](Gene.md)**
 *  **[NamedThing](NamedThing.md)** *[has gene or gene product](has_gene_or_gene_product.md)*  <sub>0..\*</sub>  **[Gene](Gene.md)**
 *  **[Disease](Disease.md)** *[has target](has_target.md)*  <sub>0..\*</sub>  **[Gene](Gene.md)**
 *  **[SequenceVariant](SequenceVariant.md)** *[sequence variant➞has gene](sequence_variant_has_gene.md)*  <sub>0..\*</sub>  **[Gene](Gene.md)**
 *  **[Transcript](Transcript.md)** *[transcribed from](transcribed_from.md)*  <sub>0..\*</sub>  **[Gene](Gene.md)**
 *  **[TranscriptToGeneRelationship](TranscriptToGeneRelationship.md)** *[transcript to gene relationship➞object](transcript_to_gene_relationship_object.md)*  <sub>1..1</sub>  **[Gene](Gene.md)**
 *  **[VariantToGeneAssociation](VariantToGeneAssociation.md)** *[variant to gene association➞object](variant_to_gene_association_object.md)*  <sub>1..1</sub>  **[Gene](Gene.md)**

## Attributes


### Own

 * [symbol](symbol.md)  <sub>0..1</sub>
     * Description: Symbol for a particular thing
     * Range: [String](types/String.md)
 * [synonym](synonym.md)  <sub>0..\*</sub>
     * Description: Alternate human-readable names for a thing
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [xref](xref.md)  <sub>0..\*</sub>
     * Description: Alternate CURIEs for a thing
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (translator_minimal)

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
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [CategoryType](types/CategoryType.md)
     * in subsets: (translator_minimal)

### Mixed in from genomic entity:

 * [has biological sequence](has_biological_sequence.md)  <sub>0..1</sub>
     * Description: connects a genomic feature to its sequence
     * Range: [BiologicalSequence](types/BiologicalSequence.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | translator_minimal |
|  | | model_organism_database |
| **Exact Mappings:** | | SO:0000704 |
|  | | SIO:010035 |
|  | | WIKIDATA:Q7187 |
|  | | dcid:Gene |
| **Narrow Mappings:** | | bioschemas:gene |
| **Broad Mappings:** | | NCIT:C45822 |

