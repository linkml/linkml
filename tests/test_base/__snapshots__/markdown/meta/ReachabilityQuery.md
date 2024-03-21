
# Class: reachability_query


A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a  set of source nodes to a set of descendants or ancestors over a set of relationship types.

URI: [linkml:ReachabilityQuery](https://w3id.org/linkml/ReachabilityQuery)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[EnumExpression]++-%20reachable_from%200..1>[ReachabilityQuery&#124;source_ontology:uriorcurie%20%3F;source_nodes:uriorcurie%20*;relationship_types:uriorcurie%20*;is_direct:boolean%20%3F;include_self:boolean%20%3F;traverse_up:boolean%20%3F],[EnumExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[EnumExpression]++-%20reachable_from%200..1>[ReachabilityQuery&#124;source_ontology:uriorcurie%20%3F;source_nodes:uriorcurie%20*;relationship_types:uriorcurie%20*;is_direct:boolean%20%3F;include_self:boolean%20%3F;traverse_up:boolean%20%3F],[EnumExpression])

## Referenced by Class

 *  **[EnumExpression](EnumExpression.md)** *[reachable_from](reachable_from.md)*  <sub>0..1</sub>  **[ReachabilityQuery](ReachabilityQuery.md)**

## Attributes


### Own

 * [source_ontology](source_ontology.md)  <sub>0..1</sub>
     * Description: An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset)
 * [source_nodes](source_nodes.md)  <sub>0..\*</sub>
     * Description: A list of nodes that are used in the reachability query
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset)
 * [relationship_types](relationship_types.md)  <sub>0..\*</sub>
     * Description: A list of relationship types (properties) that are used in a reachability query
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset)
 * [is_direct](is_direct.md)  <sub>0..1</sub>
     * Description: True if the reachability query should only include directly related nodes, if False then include also transitively connected
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [include_self](include_self.md)  <sub>0..1</sub>
     * Description: True if the query is reflexive
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [traverse_up](traverse_up.md)  <sub>0..1</sub>
     * Description: True if the direction of the reachability query is reversed and ancestors are retrieved
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | SpecificationSubset |

