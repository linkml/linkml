
# Class: gene product mixin


The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.

URI: [biolink:GeneProductMixin](https://w3id.org/biolink/vocab/GeneProductMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[GeneToGeneProductRelationship],[GeneToGeneProductRelationship]++-%20object%201..1>[GeneProductMixin&#124;synonym:label_type%20*;xref:iri_type%20*;name(i):symbol_type%20%3F],[Protein]uses%20-.->[GeneProductMixin],[RNAProduct]uses%20-.->[GeneProductMixin],[GeneProductMixin]^-[GeneProductIsoformMixin],[GeneOrGeneProduct]^-[GeneProductMixin],[Protein],[GeneProductIsoformMixin],[GeneOrGeneProduct],[Gene],[RNAProduct])](https://yuml.me/diagram/nofunky;dir:TB/class/[GeneToGeneProductRelationship],[GeneToGeneProductRelationship]++-%20object%201..1>[GeneProductMixin&#124;synonym:label_type%20*;xref:iri_type%20*;name(i):symbol_type%20%3F],[Protein]uses%20-.->[GeneProductMixin],[RNAProduct]uses%20-.->[GeneProductMixin],[GeneProductMixin]^-[GeneProductIsoformMixin],[GeneOrGeneProduct]^-[GeneProductMixin],[Protein],[GeneProductIsoformMixin],[GeneOrGeneProduct],[Gene],[RNAProduct])

## Identifier prefixes

 * UniProtKB
 * gtpo
 * PR

## Parents

 *  is_a: [GeneOrGeneProduct](GeneOrGeneProduct.md) - A union of gene loci or gene products. Frequently an identifier for one will be used as proxy for another

## Children

 * [GeneProductIsoformMixin](GeneProductIsoformMixin.md) - This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene product is intended to represent a specific isoform rather than a canonical or reference or generic product. The designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.

## Mixin for

 * [RNAProduct](RNAProduct.md) (mixin) 
 * [Protein](Protein.md) (mixin)  - A gene product that is composed of a chain of amino acid sequences and is produced by ribosome-mediated translation of mRNA

## Referenced by Class

 *  **[GeneToGeneProductRelationship](GeneToGeneProductRelationship.md)** *[gene to gene product relationship➞object](gene_to_gene_product_relationship_object.md)*  <sub>1..1</sub>  **[GeneProductMixin](GeneProductMixin.md)**
 *  **[Gene](Gene.md)** *[has gene product](has_gene_product.md)*  <sub>0..\*</sub>  **[GeneProductMixin](GeneProductMixin.md)**

## Attributes


### Own

 * [synonym](synonym.md)  <sub>0..\*</sub>
     * Description: Alternate human-readable names for a thing
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [xref](xref.md)  <sub>0..\*</sub>
     * Description: Alternate CURIEs for a thing
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal)

### Inherited from gene or gene product:

 * [macromolecular machine mixin➞name](macromolecular_machine_mixin_name.md)  <sub>0..1</sub>
     * Description: genes are typically designated by a short symbol and a full name. We map the symbol to the default display name and use an additional slot for full name
     * Range: [SymbolType](types/SymbolType.md)
     * in subsets: (translator_minimal,samples)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | WIKIDATA:Q424689 |
|  | | GENO:0000907 |
|  | | NCIT:C26548 |

