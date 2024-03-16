
# Class: sequence variant


A sequence_variant is a non exact copy of a sequence_feature or genome exhibiting one or more sequence_alteration.

URI: [biolink:SequenceVariant](https://w3id.org/biolink/vocab/SequenceVariant)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[VariantToPopulationAssociation],[VariantToPhenotypicFeatureAssociation],[VariantToEntityAssociationMixin],[VariantAsAModelOfDiseaseAssociation],[Snv],[SequenceVariantModulatesTreatmentAssociation],[Gene]<has%20gene%200..*-%20[SequenceVariant&#124;has_biological_sequence:biological_sequence%20%3F;id:string;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[GenotypeToVariantAssociation]-%20object%201..1>[SequenceVariant],[SequenceVariantModulatesTreatmentAssociation]-%20subject%201..1>[SequenceVariant],[VariantAsAModelOfDiseaseAssociation]-%20subject%201..1>[SequenceVariant],[VariantToEntityAssociationMixin]-%20subject%201..1>[SequenceVariant],[VariantToPhenotypicFeatureAssociation]-%20subject%201..1>[SequenceVariant],[VariantToPopulationAssociation]-%20subject%201..1>[SequenceVariant],[SequenceVariant]uses%20-.->[GenomicEntity],[SequenceVariant]uses%20-.->[PhysicalEssence],[SequenceVariant]uses%20-.->[OntologyClass],[SequenceVariant]^-[Snv],[BiologicalEntity]^-[SequenceVariant],[PhysicalEssence],[OrganismTaxon],[OntologyClass],[GenotypeToVariantAssociation],[GenomicEntity],[Gene],[BiologicalEntity],[Attribute],[Association])](https://yuml.me/diagram/nofunky;dir:TB/class/[VariantToPopulationAssociation],[VariantToPhenotypicFeatureAssociation],[VariantToEntityAssociationMixin],[VariantAsAModelOfDiseaseAssociation],[Snv],[SequenceVariantModulatesTreatmentAssociation],[Gene]<has%20gene%200..*-%20[SequenceVariant&#124;has_biological_sequence:biological_sequence%20%3F;id:string;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[GenotypeToVariantAssociation]-%20object%201..1>[SequenceVariant],[SequenceVariantModulatesTreatmentAssociation]-%20subject%201..1>[SequenceVariant],[VariantAsAModelOfDiseaseAssociation]-%20subject%201..1>[SequenceVariant],[VariantToEntityAssociationMixin]-%20subject%201..1>[SequenceVariant],[VariantToPhenotypicFeatureAssociation]-%20subject%201..1>[SequenceVariant],[VariantToPopulationAssociation]-%20subject%201..1>[SequenceVariant],[SequenceVariant]uses%20-.->[GenomicEntity],[SequenceVariant]uses%20-.->[PhysicalEssence],[SequenceVariant]uses%20-.->[OntologyClass],[SequenceVariant]^-[Snv],[BiologicalEntity]^-[SequenceVariant],[PhysicalEssence],[OrganismTaxon],[OntologyClass],[GenotypeToVariantAssociation],[GenomicEntity],[Gene],[BiologicalEntity],[Attribute],[Association])

## Identifier prefixes

 * CAID
 * CLINVAR
 * WIKIDATA
 * DBSNP
 * MGI
 * ZFIN
 * FB
 * RGD
 * AGRKB
 * SPDI
 * WB
 * WormBase

## Parents

 *  is_a: [BiologicalEntity](BiologicalEntity.md)

## Uses Mixin

 *  mixin: [GenomicEntity](GenomicEntity.md)
 *  mixin: [PhysicalEssence](PhysicalEssence.md) - Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.
 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [Snv](Snv.md) - SNVs are single nucleotide positions in genomic DNA at which different sequence alternatives exist

## Referenced by Class

 *  **[GenotypeToVariantAssociation](GenotypeToVariantAssociation.md)** *[genotype to variant association➞object](genotype_to_variant_association_object.md)*  <sub>1..1</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has frameshift variant](has_frameshift_variant.md)*  <sub>0..\*</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has missense variant](has_missense_variant.md)*  <sub>0..\*</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has nearby variant](has_nearby_variant.md)*  <sub>0..\*</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has non coding variant](has_non_coding_variant.md)*  <sub>0..\*</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has nonsense variant](has_nonsense_variant.md)*  <sub>0..\*</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has sequence variant](has_sequence_variant.md)*  <sub>0..\*</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has splice site variant](has_splice_site_variant.md)*  <sub>0..\*</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[GenomicEntity](GenomicEntity.md)** *[has synonymous variant](has_synonymous_variant.md)*  <sub>0..\*</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[SequenceVariantModulatesTreatmentAssociation](SequenceVariantModulatesTreatmentAssociation.md)** *[sequence variant modulates treatment association➞subject](sequence_variant_modulates_treatment_association_subject.md)*  <sub>1..1</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[Association](Association.md)** *[sequence variant qualifier](sequence_variant_qualifier.md)*  <sub>0..1</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[VariantAsAModelOfDiseaseAssociation](VariantAsAModelOfDiseaseAssociation.md)** *[variant as a model of disease association➞subject](variant_as_a_model_of_disease_association_subject.md)*  <sub>1..1</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[VariantToEntityAssociationMixin](VariantToEntityAssociationMixin.md)** *[variant to entity association mixin➞subject](variant_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[VariantToPhenotypicFeatureAssociation](VariantToPhenotypicFeatureAssociation.md)** *[variant to phenotypic feature association➞subject](variant_to_phenotypic_feature_association_subject.md)*  <sub>1..1</sub>  **[SequenceVariant](SequenceVariant.md)**
 *  **[VariantToPopulationAssociation](VariantToPopulationAssociation.md)** *[variant to population association➞subject](variant_to_population_association_subject.md)*  <sub>1..1</sub>  **[SequenceVariant](SequenceVariant.md)**

## Attributes


### Own

 * [sequence variant➞has gene](sequence_variant_has_gene.md)  <sub>0..\*</sub>
     * Description: Each allele can be associated with any number of genes
     * Range: [Gene](Gene.md)
 * [sequence variant➞has biological sequence](sequence_variant_has_biological_sequence.md)  <sub>0..1</sub>
     * Description: The state of the sequence w.r.t a reference sequence
     * Range: [BiologicalSequence](types/BiologicalSequence.md)
 * [sequence variant➞id](sequence_variant_id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * Example: ZFIN:ZDB-ALT-980203-1091 ti282a allele from ZFIN
     * Example: CLINVAR:17681 NM_007294.3(BRCA1):c.2521C>T (p.Arg841Trp)
     * in subsets: (translator_minimal)

### Inherited from biological entity:

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
| **Aliases:** | | allele |
| **Local names:** | | allele (agr) |
| **Alt Descriptions:** | | An entity that describes a single affected, endogenous allele. These can be of any type that matches that definition (AGR) |
|  | | A contiguous change at a Location (VMC) |
| **Comments:** | | This class is for modeling the specific state at a locus. A single DBSNP rs ID could correspond to more than one sequence variants (e.g CIViC:1252 and CIViC:1253, two distinct BRCA2 alleles for rs28897743) |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | WIKIDATA:Q15304597 |
| **Close Mappings:** | | dcid:Allele |
|  | | SO:0001060 |
|  | | VMC:Allele |
|  | | GENO:0000002 |
|  | | SIO:010277 |
|  | | SO:0001060 |

