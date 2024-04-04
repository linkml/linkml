
# Class: match_query


A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that  matches on properties of the external concepts.

URI: [linkml:MatchQuery](https://w3id.org/linkml/MatchQuery)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[EnumExpression]++-%20matches%200..1>[MatchQuery&#124;identifier_pattern:string%20%3F;source_ontology:uriorcurie%20%3F],[EnumExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[EnumExpression]++-%20matches%200..1>[MatchQuery&#124;identifier_pattern:string%20%3F;source_ontology:uriorcurie%20%3F],[EnumExpression])

## Referenced by Class

 *  **[EnumExpression](EnumExpression.md)** *[matches](matches.md)*  <sub>0..1</sub>  **[MatchQuery](MatchQuery.md)**

## Attributes


### Own

 * [identifier_pattern](identifier_pattern.md)  <sub>0..1</sub>
     * Description: A regular expression that is used to obtain a set of identifiers from a source_ontology to construct a set of permissible values
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)
 * [source_ontology](source_ontology.md)  <sub>0..1</sub>
     * Description: An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | SpecificationSubset |

