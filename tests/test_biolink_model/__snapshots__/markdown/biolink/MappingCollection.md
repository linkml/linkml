
# Class: mapping collection


A collection of deprecated mappings.

URI: [biolink:MappingCollection](https://w3id.org/biolink/vocab/MappingCollection)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PredicateMapping],[PredicateMapping]<predicate%20mappings%200..*-++[MappingCollection])](https://yuml.me/diagram/nofunky;dir:TB/class/[PredicateMapping],[PredicateMapping]<predicate%20mappings%200..*-++[MappingCollection])

## Attributes


### Own

 * [predicate mappings](predicate_mappings.md)  <sub>0..\*</sub>
     * Description: A collection of relationships that are not used in biolink, but have biolink patterns that can  be used to replace them.  This is a temporary slot to help with the transition to the fully qualified predicate model in Biolink3.
     * Range: [PredicateMapping](PredicateMapping.md)
