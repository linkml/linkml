
# Class: class_rule


A rule that applies to instances of a class

URI: [linkml:ClassRule](https://w3id.org/linkml/ClassRule)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[Extension],[Extensible],[Example],[CommonMetadata],[AnonymousClassExpression]<elseconditions%200..1-++[ClassRule&#124;bidirectional:boolean%20%3F;open_world:boolean%20%3F;precedence:integer%20%3F;deactivated:boolean%20%3F;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F],[AnonymousClassExpression]<postconditions%200..1-++[ClassRule],[AnonymousClassExpression]<preconditions%200..1-++[ClassRule],[ClassDefinition]++-%20rules%200..*>[ClassRule],[ClassDefinition]++-%20rules(i)%200..*>[ClassRule],[ClassRule]uses%20-.->[Extensible],[ClassRule]uses%20-.->[Annotatable],[ClassRule]uses%20-.->[CommonMetadata],[ClassLevelRule]^-[ClassRule],[ClassLevelRule],[ClassDefinition],[AnonymousClassExpression],[Annotation],[Annotatable],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[Extension],[Extensible],[Example],[CommonMetadata],[AnonymousClassExpression]<elseconditions%200..1-++[ClassRule&#124;bidirectional:boolean%20%3F;open_world:boolean%20%3F;precedence:integer%20%3F;deactivated:boolean%20%3F;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F],[AnonymousClassExpression]<postconditions%200..1-++[ClassRule],[AnonymousClassExpression]<preconditions%200..1-++[ClassRule],[ClassDefinition]++-%20rules%200..*>[ClassRule],[ClassDefinition]++-%20rules(i)%200..*>[ClassRule],[ClassRule]uses%20-.->[Extensible],[ClassRule]uses%20-.->[Annotatable],[ClassRule]uses%20-.->[CommonMetadata],[ClassLevelRule]^-[ClassRule],[ClassLevelRule],[ClassDefinition],[AnonymousClassExpression],[Annotation],[Annotatable],[AltDescription])

## Parents

 *  is_a: [ClassLevelRule](ClassLevelRule.md) - A rule that is applied to classes

## Uses Mixin

 *  mixin: [Extensible](Extensible.md) - mixin for classes that support extension
 *  mixin: [Annotatable](Annotatable.md) - mixin for classes that support annotations
 *  mixin: [CommonMetadata](CommonMetadata.md) - Generic metadata shared across definitions

## Referenced by Class

 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞rules](class_definition_rules.md)*  <sub>0..\*</sub>  **[ClassRule](ClassRule.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[rules](rules.md)*  <sub>0..\*</sub>  **[ClassRule](ClassRule.md)**

## Attributes


### Own

 * [preconditions](preconditions.md)  <sub>0..1</sub>
     * Description: an expression that must hold in order for the rule to be applicable to an instance
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
 * [postconditions](postconditions.md)  <sub>0..1</sub>
     * Description: an expression that must hold for an instance of the class, if the preconditions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
 * [elseconditions](elseconditions.md)  <sub>0..1</sub>
     * Description: an expression that must hold for an instance of the class, if the preconditions no not hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
 * [bidirectional](bidirectional.md)  <sub>0..1</sub>
     * Description: in addition to preconditions entailing postconditions, the postconditions entail the preconditions
     * Range: [Boolean](Boolean.md)
 * [open_world](open_world.md)  <sub>0..1</sub>
     * Description: if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these
     * Range: [Boolean](Boolean.md)
 * [precedence](precedence.md)  <sub>0..1</sub>
     * Description: the relative order in which the rule is applied
     * Range: [Integer](Integer.md)
 * [deactivated](deactivated.md)  <sub>0..1</sub>
     * Description: a deactivated rule is not executed by the rules engine
     * Range: [Boolean](Boolean.md)

### Mixed in from extensible:

 * [extensions](extensions.md)  <sub>0..\*</sub>
     * Description: a tag/text tuple attached to an arbitrary element
     * Range: [Extension](Extension.md)

### Mixed in from annotatable:

 * [annotations](annotations.md)  <sub>0..\*</sub>
     * Description: a collection of tag/text tuples with the semantics of OWL Annotation
     * Range: [Annotation](Annotation.md)

### Mixed in from common_metadata:

 * [description](description.md)  <sub>0..1</sub>
     * Description: a description of the element's purpose and use
     * Range: [String](String.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Range: [AltDescription](AltDescription.md)

### Mixed in from common_metadata:

 * [title](title.md)  <sub>0..1</sub>
     * Description: the official title of the element
     * Range: [String](String.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [deprecated](deprecated.md)  <sub>0..1</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](String.md)

### Mixed in from common_metadata:

 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issue that needs resolution
     * Range: [String](String.md)

### Mixed in from common_metadata:

 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * Range: [String](String.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended for external consumption
     * Range: [String](String.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * Range: [SubsetDefinition](SubsetDefinition.md)

### Mixed in from common_metadata:

 * [from_schema](from_schema.md)  <sub>0..1</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](Uri.md)

### Mixed in from common_metadata:

 * [imported_from](imported_from.md)  <sub>0..1</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](String.md)

### Mixed in from common_metadata:

 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: a reference
     * Range: [Uriorcurie](Uriorcurie.md)
     * in subsets: (owl)

### Mixed in from common_metadata:

 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](Uriorcurie.md)

### Mixed in from common_metadata:

 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](Uriorcurie.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | if rule |
| **Close Mappings:** | | sh:TripleRule |
|  | | swrl:Imp |

