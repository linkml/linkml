
# Class: gene grouping mixin


any grouping of multiple genes or gene products

URI: [biolink:GeneGroupingMixin](https://w3id.org/biolink/vocab/GeneGroupingMixin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Gene]<has%20gene%20or%20gene%20product%200..*-%20[GeneGroupingMixin],[GenomicBackgroundExposure]uses%20-.->[GeneGroupingMixin],[GeneFamily]uses%20-.->[GeneGroupingMixin],[DrugToGeneInteractionExposure]uses%20-.->[GeneGroupingMixin],[GenomicBackgroundExposure],[GeneFamily],[Gene],[DrugToGeneInteractionExposure])](https://yuml.me/diagram/nofunky;dir:TB/class/[Gene]<has%20gene%20or%20gene%20product%200..*-%20[GeneGroupingMixin],[GenomicBackgroundExposure]uses%20-.->[GeneGroupingMixin],[GeneFamily]uses%20-.->[GeneGroupingMixin],[DrugToGeneInteractionExposure]uses%20-.->[GeneGroupingMixin],[GenomicBackgroundExposure],[GeneFamily],[Gene],[DrugToGeneInteractionExposure])

## Mixin for

 * [DrugToGeneInteractionExposure](DrugToGeneInteractionExposure.md) (mixin)  - drug to gene interaction exposure is a drug exposure is where the interactions of the drug with specific genes are known to constitute an 'exposure' to the organism, leading to or influencing an outcome.
 * [GeneFamily](GeneFamily.md) (mixin)  - any grouping of multiple genes or gene products related by common descent
 * [GenomicBackgroundExposure](GenomicBackgroundExposure.md) (mixin)  - A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing an outcome.

## Referenced by Class


## Attributes


### Own

 * [has gene or gene product](has_gene_or_gene_product.md)  <sub>0..\*</sub>
     * Description: connects an entity with one or more gene or gene products
     * Range: [Gene](Gene.md)
