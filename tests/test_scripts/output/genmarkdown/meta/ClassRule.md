
# Class: class_rule


A rule that applies to instances of a class

URI: [linkml:ClassRule](https://w3id.org/linkml/ClassRule)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[Extension],[Extensible],[Example],[CommonMetadata],[AnonymousClassExpression]<elseconditions%200..1-++[ClassRule&#124;bidirectional:boolean%20%3F;open_world:boolean%20%3F;rank:integer%20%3F;deactivated:boolean%20%3F;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*],[AnonymousClassExpression]<postconditions%200..1-++[ClassRule],[AnonymousClassExpression]<preconditions%200..1-++[ClassRule],[ClassDefinition]++-%20rules%200..*>[ClassRule],[ClassDefinition]++-%20rules(i)%200..*>[ClassRule],[ClassRule]uses%20-.->[Extensible],[ClassRule]uses%20-.->[Annotatable],[ClassRule]uses%20-.->[CommonMetadata],[ClassLevelRule]^-[ClassRule],[ClassLevelRule],[ClassDefinition],[AnonymousClassExpression],[Annotation],[Annotatable],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[Extension],[Extensible],[Example],[CommonMetadata],[AnonymousClassExpression]<elseconditions%200..1-++[ClassRule&#124;bidirectional:boolean%20%3F;open_world:boolean%20%3F;rank:integer%20%3F;deactivated:boolean%20%3F;description:string%20%3F;title:string%20%3F;deprecated:string%20%3F;todos:string%20*;notes:string%20*;comments:string%20*;from_schema:uri%20%3F;imported_from:string%20%3F;source:uriorcurie%20%3F;in_language:string%20%3F;see_also:uriorcurie%20*;deprecated_element_has_exact_replacement:uriorcurie%20%3F;deprecated_element_has_possible_replacement:uriorcurie%20%3F;aliases:string%20*;mappings:uriorcurie%20*;exact_mappings:uriorcurie%20*;close_mappings:uriorcurie%20*;related_mappings:uriorcurie%20*;narrow_mappings:uriorcurie%20*;broad_mappings:uriorcurie%20*],[AnonymousClassExpression]<postconditions%200..1-++[ClassRule],[AnonymousClassExpression]<preconditions%200..1-++[ClassRule],[ClassDefinition]++-%20rules%200..*>[ClassRule],[ClassDefinition]++-%20rules(i)%200..*>[ClassRule],[ClassRule]uses%20-.->[Extensible],[ClassRule]uses%20-.->[Annotatable],[ClassRule]uses%20-.->[CommonMetadata],[ClassLevelRule]^-[ClassRule],[ClassLevelRule],[ClassDefinition],[AnonymousClassExpression],[Annotation],[Annotatable],[AltDescription])

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
     * Range: [Boolean](types/Boolean.md)
 * [open_world](open_world.md)  <sub>0..1</sub>
     * Description: if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these
     * Range: [Boolean](types/Boolean.md)
 * [rank](rank.md)  <sub>0..1</sub>
     * Description: the relative order in which the element occurs, lower values are given precedence
     * Range: [Integer](types/Integer.md)
     * in subsets: (basic)
 * [deactivated](deactivated.md)  <sub>0..1</sub>
     * Description: a deactivated rule is not executed by the rules engine
     * Range: [Boolean](types/Boolean.md)

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
     * Range: [String](types/String.md)
     * in subsets: (basic)

### Mixed in from common_metadata:

 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Range: [AltDescription](AltDescription.md)
     * in subsets: (basic)

### Mixed in from common_metadata:

 * [title](title.md)  <sub>0..1</sub>
     * Description: the official title of the element
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)

### Mixed in from common_metadata:

 * [deprecated](deprecated.md)  <sub>0..1</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](types/String.md)
     * in subsets: (basic)

### Mixed in from common_metadata:

 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issue that needs resolution
     * Range: [String](types/String.md)
     * in subsets: (basic)

### Mixed in from common_metadata:

 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)

### Mixed in from common_metadata:

 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended for external consumption
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)

### Mixed in from common_metadata:

 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (owl,basic)

### Mixed in from common_metadata:

 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * Range: [SubsetDefinition](SubsetDefinition.md)
     * in subsets: (basic)

### Mixed in from common_metadata:

 * [from_schema](from_schema.md)  <sub>0..1</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](types/Uri.md)

### Mixed in from common_metadata:

 * [imported_from](imported_from.md)  <sub>0..1</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](types/String.md)

### Mixed in from common_metadata:

 * [source](source.md)  <sub>0..1</sub>
     * Description: A related resource from which the element is derived.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)

### Mixed in from common_metadata:

 * [in_language](in_language.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

### Mixed in from common_metadata:

 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: a reference
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (owl,basic)

### Mixed in from common_metadata:

 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
     * in subsets: (basic)

### Mixed in from common_metadata:

 * [structured_aliases](structured_aliases.md)  <sub>0..\*</sub>
     * Description: A list of structured_alias objects.
     * Range: [StructuredAlias](StructuredAlias.md)

### Mixed in from common_metadata:

 * [mappings](mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [exact mappings](exact_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have identical meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [close mappings](close_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have close meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [related mappings](related_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have related meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [narrow mappings](narrow_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have narrower meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

### Mixed in from common_metadata:

 * [broad mappings](broad_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have broader meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | if rule |
| **Close Mappings:** | | sh:TripleRule |
|  | | swrl:Imp |

