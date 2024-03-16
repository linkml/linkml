
# Class: gene product isoform mixin


This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene product is intended to represent a specific isoform rather than a canonical or reference or generic product. The designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.

URI: [biolink:GeneProductIsoformMixin](https://w3id.org/biolink/vocab/GeneProductIsoformMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[GeneProductMixin],[ProteinIsoform]uses%20-.->[GeneProductIsoformMixin&#124;synonym(i):label_type%20*;xref(i):uriorcurie%20*;name(i):symbol_type%20%3F],[PosttranslationalModification]uses%20-.->[GeneProductIsoformMixin],[NucleosomeModification]uses%20-.->[GeneProductIsoformMixin],[RNAProductIsoform]uses%20-.->[GeneProductIsoformMixin],[GeneProductMixin]^-[GeneProductIsoformMixin],[ProteinIsoform],[PosttranslationalModification],[NucleosomeModification],[RNAProductIsoform])](https://yuml.me/diagram/nofunky;dir:TB/class/[GeneProductMixin],[ProteinIsoform]uses%20-.->[GeneProductIsoformMixin&#124;synonym(i):label_type%20*;xref(i):uriorcurie%20*;name(i):symbol_type%20%3F],[PosttranslationalModification]uses%20-.->[GeneProductIsoformMixin],[NucleosomeModification]uses%20-.->[GeneProductIsoformMixin],[RNAProductIsoform]uses%20-.->[GeneProductIsoformMixin],[GeneProductMixin]^-[GeneProductIsoformMixin],[ProteinIsoform],[PosttranslationalModification],[NucleosomeModification],[RNAProductIsoform])

## Parents

 *  is_a: [GeneProductMixin](GeneProductMixin.md) - The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA molecules.

## Mixin for

 * [RNAProductIsoform](RNAProductIsoform.md) (mixin)  - Represents a protein that is a specific isoform of the canonical or reference RNA
 * [NucleosomeModification](NucleosomeModification.md) (mixin)  - A chemical modification of a histone protein within a nucleosome octomer or a substitution of a histone with a variant histone isoform. e.g. Histone 4 Lysine 20 methylation (H4K20me), histone variant H2AZ substituting H2A.
 * [PosttranslationalModification](PosttranslationalModification.md) (mixin)  - A chemical modification of a polypeptide or protein that occurs after translation.  e.g. polypeptide cleavage to form separate proteins, methylation or acetylation of histone tail amino acids,  protein ubiquitination.
 * [ProteinIsoform](ProteinIsoform.md) (mixin)  - Represents a protein that is a specific isoform of the canonical or reference protein. See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4114032/

## Referenced by Class


## Attributes


### Inherited from gene product mixin:

 * [macromolecular machine mixin➞name](macromolecular_machine_mixin_name.md)  <sub>0..1</sub>
     * Description: genes are typically designated by a short symbol and a full name. We map the symbol to the default display name and use an additional slot for full name
     * Range: [SymbolType](types/SymbolType.md)
     * in subsets: (translator_minimal,samples)
 * [synonym](synonym.md)  <sub>0..\*</sub>
     * Description: Alternate human-readable names for a thing
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [xref](xref.md)  <sub>0..\*</sub>
     * Description: Alternate CURIEs for a thing
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (translator_minimal)
