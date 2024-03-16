
# Class: predicate mapping


A deprecated predicate mapping object contains the deprecated predicate and an example of the rewiring that should be done to use a qualified statement in its place.

URI: [biolink:PredicateMapping](https://w3id.org/biolink/vocab/PredicateMapping)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing]<broad%20match%200..*-%20[PredicateMapping&#124;mapped_predicate:string%20%3F;subject_aspect_qualifier:string%20%3F;subject_direction_qualifier:string%20%3F;subject_form_or_variant_qualifier:string%20%3F;subject_part_qualifier:string%20%3F;subject_derivative_qualifier:string%20%3F;subject_context_qualifier:string%20%3F;predicate:predicate_type;qualified_predicate:string%20%3F;object_aspect_qualifier:string%20%3F;object_direction_qualifier:DirectionQualifierEnum%20%3F;object_form_or_variant_qualifier:string%20%3F;object_part_qualifier:string%20%3F;object_derivative_qualifier:string%20%3F;object_context_qualifier:string%20%3F;causal_mechanism_qualifier:string%20%3F;anatomical_context_qualifier:AnatomicalContextQualifierEnum%20%3F],[NamedThing]<narrow%20match%200..*-%20[PredicateMapping],[NamedThing]<exact%20match%200..*-%20[PredicateMapping],[OrganismTaxon]<species%20context%20qualifier%200..1-%20[PredicateMapping],[MappingCollection]++-%20predicate%20mappings%200..*>[PredicateMapping],[OrganismTaxon],[NamedThing],[MappingCollection])](https://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing]<broad%20match%200..*-%20[PredicateMapping&#124;mapped_predicate:string%20%3F;subject_aspect_qualifier:string%20%3F;subject_direction_qualifier:string%20%3F;subject_form_or_variant_qualifier:string%20%3F;subject_part_qualifier:string%20%3F;subject_derivative_qualifier:string%20%3F;subject_context_qualifier:string%20%3F;predicate:predicate_type;qualified_predicate:string%20%3F;object_aspect_qualifier:string%20%3F;object_direction_qualifier:DirectionQualifierEnum%20%3F;object_form_or_variant_qualifier:string%20%3F;object_part_qualifier:string%20%3F;object_derivative_qualifier:string%20%3F;object_context_qualifier:string%20%3F;causal_mechanism_qualifier:string%20%3F;anatomical_context_qualifier:AnatomicalContextQualifierEnum%20%3F],[NamedThing]<narrow%20match%200..*-%20[PredicateMapping],[NamedThing]<exact%20match%200..*-%20[PredicateMapping],[OrganismTaxon]<species%20context%20qualifier%200..1-%20[PredicateMapping],[MappingCollection]++-%20predicate%20mappings%200..*>[PredicateMapping],[OrganismTaxon],[NamedThing],[MappingCollection])

## Referenced by Class

 *  **None** *[predicate mappings](predicate_mappings.md)*  <sub>0..\*</sub>  **[PredicateMapping](PredicateMapping.md)**

## Attributes


### Own

 * [mapped predicate](mapped_predicate.md)  <sub>0..1</sub>
     * Description: The predicate that is being replaced by the fully qualified representation of predicate + subject and object  qualifiers.  Only to be used in test data and mapping data to help with the transition to the fully qualified predicate model. Not to be used in knowledge graphs.
     * Range: [String](types/String.md)
 * [subject aspect qualifier](subject_aspect_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [subject direction qualifier](subject_direction_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [subject form or variant qualifier](subject_form_or_variant_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [subject part qualifier](subject_part_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [subject derivative qualifier](subject_derivative_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [subject context qualifier](subject_context_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [predicate](predicate.md)  <sub>1..1</sub>
     * Description: A high-level grouping for the relationship type. AKA minimal predicate. This is analogous to category for nodes.
     * Range: [PredicateType](types/PredicateType.md)
 * [qualified predicate](qualified_predicate.md)  <sub>0..1</sub>
     * Description: Predicate to be used in an association when subject and object qualifiers are present and the full reading of the statement requires a qualification to the predicate in use in order to refine or  increase the specificity of the full statement reading.  This qualifier holds a relationship to be used instead of that  expressed by the primary predicate, in a ‘full statement’ reading of the association, where qualifier-based  semantics are included.  This is necessary only in cases where the primary predicate does not work in a  full statement reading.
     * Range: [String](types/String.md)
 * [object aspect qualifier](object_aspect_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [object direction qualifier](object_direction_qualifier.md)  <sub>0..1</sub>
     * Range: [DirectionQualifierEnum](DirectionQualifierEnum.md)
 * [object form or variant qualifier](object_form_or_variant_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [object part qualifier](object_part_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [object derivative qualifier](object_derivative_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [object context qualifier](object_context_qualifier.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [causal mechanism qualifier](causal_mechanism_qualifier.md)  <sub>0..1</sub>
     * Description: A statement qualifier representing a type of molecular control mechanism through which an effect of a chemical on a gene or gene product is mediated (e.g. 'agonism', 'inhibition', 'allosteric modulation', 'channel blocker')
     * Range: [String](types/String.md)
 * [anatomical context qualifier](anatomical_context_qualifier.md)  <sub>0..1</sub>
     * Description: A statement qualifier representing an anatomical location where an relationship expressed in an association took place (can be a tissue, cell type, or sub-cellular location).
     * Range: [AnatomicalContextQualifierEnum](AnatomicalContextQualifierEnum.md)
     * Example: blood None
     * Example: cerebral cortext None
 * [species context qualifier](species_context_qualifier.md)  <sub>0..1</sub>
     * Description: A statement qualifier representing a taxonomic category of species in which a relationship expressed in an association took place.
     * Range: [OrganismTaxon](OrganismTaxon.md)
     * Example: zebrafish None
     * Example: human None
 * [exact match](exact_match.md)  <sub>0..\*</sub>
     * Description: holds between two entities that have strictly equivalent meanings, with a high degree of confidence
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)
 * [narrow match](narrow_match.md)  <sub>0..\*</sub>
     * Description: a list of terms from different schemas or terminology systems that have a narrower, more specific meaning. Narrower terms are typically shown as children in a hierarchy or tree.
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)
 * [broad match](broad_match.md)  <sub>0..\*</sub>
     * Description: a list of terms from different schemas or terminology systems that have a broader, more general meaning. Broader terms are typically shown as parents in a hierarchy or tree.
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)
