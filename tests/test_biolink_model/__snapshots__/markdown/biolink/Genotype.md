
# Class: genotype


An information content entity that describes a genome by specifying the total variation in genomic sequence and/or gene expression, relative to some established background

URI: [biolink:Genotype](https://w3id.org/biolink/vocab/Genotype)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Zygosity],[PhysicalEssence],[OrganismTaxon],[OntologyClass],[GenotypeToVariantAssociation],[GenotypeToPhenotypicFeatureAssociation],[GenotypeToGenotypePartAssociation],[GenotypeToGeneAssociation],[GenotypeToEntityAssociationMixin],[GenotypeAsAModelOfDiseaseAssociation],[Zygosity]<has%20zygosity%200..1-%20[Genotype&#124;has_biological_sequence:biological_sequence%20%3F;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[GenotypeAsAModelOfDiseaseAssociation]-%20subject%201..1>[Genotype],[GenotypeToEntityAssociationMixin]-%20subject%201..1>[Genotype],[GenotypeToGeneAssociation]-%20subject%201..1>[Genotype],[GenotypeToGenotypePartAssociation]-%20object%201..1>[Genotype],[GenotypeToGenotypePartAssociation]-%20subject%201..1>[Genotype],[GenotypeToPhenotypicFeatureAssociation]-%20subject%201..1>[Genotype],[GenotypeToVariantAssociation]-%20subject%201..1>[Genotype],[Genotype]uses%20-.->[PhysicalEssence],[Genotype]uses%20-.->[GenomicEntity],[Genotype]uses%20-.->[OntologyClass],[BiologicalEntity]^-[Genotype],[GenomicEntity],[BiologicalEntity],[Attribute])](https://yuml.me/diagram/nofunky;dir:TB/class/[Zygosity],[PhysicalEssence],[OrganismTaxon],[OntologyClass],[GenotypeToVariantAssociation],[GenotypeToPhenotypicFeatureAssociation],[GenotypeToGenotypePartAssociation],[GenotypeToGeneAssociation],[GenotypeToEntityAssociationMixin],[GenotypeAsAModelOfDiseaseAssociation],[Zygosity]<has%20zygosity%200..1-%20[Genotype&#124;has_biological_sequence:biological_sequence%20%3F;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[GenotypeAsAModelOfDiseaseAssociation]-%20subject%201..1>[Genotype],[GenotypeToEntityAssociationMixin]-%20subject%201..1>[Genotype],[GenotypeToGeneAssociation]-%20subject%201..1>[Genotype],[GenotypeToGenotypePartAssociation]-%20object%201..1>[Genotype],[GenotypeToGenotypePartAssociation]-%20subject%201..1>[Genotype],[GenotypeToPhenotypicFeatureAssociation]-%20subject%201..1>[Genotype],[GenotypeToVariantAssociation]-%20subject%201..1>[Genotype],[Genotype]uses%20-.->[PhysicalEssence],[Genotype]uses%20-.->[GenomicEntity],[Genotype]uses%20-.->[OntologyClass],[BiologicalEntity]^-[Genotype],[GenomicEntity],[BiologicalEntity],[Attribute])

## Identifier prefixes

 * ZFIN
 * FB

## Parents

 *  is_a: [BiologicalEntity](BiologicalEntity.md)

## Uses Mixin

 *  mixin: [PhysicalEssence](PhysicalEssence.md) - Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.
 *  mixin: [GenomicEntity](GenomicEntity.md)
 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Referenced by Class

 *  **[GenotypeAsAModelOfDiseaseAssociation](GenotypeAsAModelOfDiseaseAssociation.md)** *[genotype as a model of disease association➞subject](genotype_as_a_model_of_disease_association_subject.md)*  <sub>1..1</sub>  **[Genotype](Genotype.md)**
 *  **[GenotypeToEntityAssociationMixin](GenotypeToEntityAssociationMixin.md)** *[genotype to entity association mixin➞subject](genotype_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[Genotype](Genotype.md)**
 *  **[GenotypeToGeneAssociation](GenotypeToGeneAssociation.md)** *[genotype to gene association➞subject](genotype_to_gene_association_subject.md)*  <sub>1..1</sub>  **[Genotype](Genotype.md)**
 *  **[GenotypeToGenotypePartAssociation](GenotypeToGenotypePartAssociation.md)** *[genotype to genotype part association➞object](genotype_to_genotype_part_association_object.md)*  <sub>1..1</sub>  **[Genotype](Genotype.md)**
 *  **[GenotypeToGenotypePartAssociation](GenotypeToGenotypePartAssociation.md)** *[genotype to genotype part association➞subject](genotype_to_genotype_part_association_subject.md)*  <sub>1..1</sub>  **[Genotype](Genotype.md)**
 *  **[GenotypeToPhenotypicFeatureAssociation](GenotypeToPhenotypicFeatureAssociation.md)** *[genotype to phenotypic feature association➞subject](genotype_to_phenotypic_feature_association_subject.md)*  <sub>1..1</sub>  **[Genotype](Genotype.md)**
 *  **[GenotypeToVariantAssociation](GenotypeToVariantAssociation.md)** *[genotype to variant association➞subject](genotype_to_variant_association_subject.md)*  <sub>1..1</sub>  **[Genotype](Genotype.md)**

## Attributes


### Own

 * [has zygosity](has_zygosity.md)  <sub>0..1</sub>
     * Range: [Zygosity](Zygosity.md)

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

### Mixed in from genomic entity:

 * [has biological sequence](has_biological_sequence.md)  <sub>0..1</sub>
     * Description: connects a genomic feature to its sequence
     * Range: [BiologicalSequence](types/BiologicalSequence.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | Consider renaming as genotypic entity |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | GENO:0000536 |
|  | | SIO:001079 |

