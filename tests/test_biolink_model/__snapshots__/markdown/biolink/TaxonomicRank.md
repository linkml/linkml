
# Class: taxonomic rank


A descriptor for the rank within a taxonomic classification. Example instance: TAXRANK:0000017 (kingdom)

URI: [biolink:TaxonomicRank](https://w3id.org/biolink/vocab/TaxonomicRank)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon]-%20has%20taxonomic%20rank%200..1>[TaxonomicRank&#124;id(i):string],[OntologyClass]^-[TaxonomicRank],[OrganismTaxon],[OntologyClass],[NamedThing])](https://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon]-%20has%20taxonomic%20rank%200..1>[TaxonomicRank&#124;id(i):string],[OntologyClass]^-[TaxonomicRank],[OrganismTaxon],[OntologyClass],[NamedThing])

## Identifier prefixes

 * TAXRANK

## Parents

 *  is_a: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Referenced by Class

 *  **[NamedThing](NamedThing.md)** *[has taxonomic rank](has_taxonomic_rank.md)*  <sub>0..1</sub>  **[TaxonomicRank](TaxonomicRank.md)**
 *  **[OrganismTaxon](OrganismTaxon.md)** *[organism taxon➞has taxonomic rank](organism_taxon_has_taxonomic_rank.md)*  <sub>0..1</sub>  **[TaxonomicRank](TaxonomicRank.md)**

## Attributes


### Inherited from ontology class:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | WIKIDATA:Q427626 |

