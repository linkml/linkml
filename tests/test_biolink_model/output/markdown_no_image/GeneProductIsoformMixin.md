
# Class: GeneProductIsoformMixin


This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene product is intended to represent a specific isoform rather than a canonical or reference or generic product. The designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.

URI: [biolink:GeneProductIsoformMixin](https://w3id.org/biolink/vocab/GeneProductIsoformMixin)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[GeneProductMixin],[ProteinIsoform]uses%20-.->[GeneProductIsoformMixin&#124;synonym(i):label_type%20*;xref(i):iri_type%20*;name(i):symbol_type%20%3F],[RNAProductIsoform]uses%20-.->[GeneProductIsoformMixin],[GeneProductMixin]^-[GeneProductIsoformMixin],[ProteinIsoform],[RNAProductIsoform])

## Parents

 *  is_a: [GeneProductMixin](GeneProductMixin.md) - The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.

## Mixin for

 * [RNAProductIsoform](RNAProductIsoform.md) (mixin)  - Represents a protein that is a specific isoform of the canonical or reference RNA
 * [ProteinIsoform](ProteinIsoform.md) (mixin)  - Represents a protein that is a specific isoform of the canonical or reference protein. See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4114032/

## Referenced by class


## Attributes


### Inherited from gene product mixin:

 * [macromolecular machine mixin➞name](macromolecular_machine_mixin_name.md)  <sub>OPT</sub>
     * Description: genes are typically designated by a short symbol and a full name. We map the symbol to the default display name and use an additional slot for full name
     * range: [SymbolType](types/SymbolType.md)
 * [synonym](synonym.md)  <sub>0..*</sub>
     * Description: Alternate human-readable names for a thing
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [xref](xref.md)  <sub>0..*</sub>
     * Description: Alternate CURIEs for a thing
     * range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal)
