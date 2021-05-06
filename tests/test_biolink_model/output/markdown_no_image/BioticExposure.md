
# Class: BioticExposure


An external biotic exposure is an intake of (sometimes pathological) biological organisms (including viruses).

URI: [biolink:BioticExposure](https://w3id.org/biolink/vocab/BioticExposure)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[TaxonomicRank],[OrganismTaxon],[ExposureEvent],[BioticExposure&#124;timepoint:time_type%20%3F]uses%20-.->[ExposureEvent],[OrganismTaxon]^-[BioticExposure])

## Parents

 *  is_a: [OrganismTaxon](OrganismTaxon.md) - A classification of a set of organisms. Example instances: NCBITaxon:9606 (Homo sapiens), NCBITaxon:2 (Bacteria). Can also be used to represent strains or subspecies.

## Uses Mixins

 *  mixin: [ExposureEvent](ExposureEvent.md) - A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more phenotypic features of that organism, potentially mediated by genes

## Attributes


### Inherited from organism taxon:

 * [organism taxon➞has taxonomic rank](organism_taxon_has_taxonomic_rank.md)  <sub>OPT</sub>
     * range: [TaxonomicRank](TaxonomicRank.md)
 * [organism taxon➞subclass of](organism_taxon_subclass_of.md)  <sub>0..*</sub>
     * Description: subclass of holds between two taxa, e.g. human subclass of mammal
     * range: [OrganismTaxon](OrganismTaxon.md)

### Mixed in from exposure event:

 * [timepoint](timepoint.md)  <sub>OPT</sub>
     * Description: a point in time
     * range: [TimeType](types/TimeType.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | viral exposure |
|  | | bacterial exposure |

