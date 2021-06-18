
# Class: ClassDefinition


the definition of a class or interface

URI: [linkml:ClassDefinition](https://w3id.org/linkml/ClassDefinition)


[![img](images/ClassDefinition.svg)](images/ClassDefinition.svg)

## Parents

 *  is_a: [Definition](Definition.md) - base class for definitions

## Referenced by class

 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞apply_to](class_definition_apply_to.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞is_a](class_definition_is_a.md)*  <sub>0..1</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞mixins](class_definition_mixins.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[classes](classes.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[domain](domain.md)*  <sub>0..1</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[domain_of](domain_of.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[union_of](union_of.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**

## Attributes


### Own

 * [slots](slots.md)  <sub>0..\*</sub>
     * Description: list of slot names that are applicable to a class
     * Range: [SlotDefinition](SlotDefinition.md)
 * [slot_usage](slot_usage.md)  <sub>0..\*</sub>
     * Description: the redefinition of a slot in the context of the containing class definition.
     * Range: [SlotDefinition](SlotDefinition.md)
 * [attributes](attributes.md)  <sub>0..\*</sub>
     * Description: Inline definition of slots
     * Range: [SlotDefinition](SlotDefinition.md)
 * [class_uri](class_uri.md)  <sub>0..1</sub>
     * Description: URI of the class in an RDF environment
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [subclass_of](subclass_of.md)  <sub>0..1</sub>
     * Description: rdfs:subClassOf to be emitted in OWL generation
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [union_of](union_of.md)  <sub>0..\*</sub>
     * Description: indicates that the domain class consists exactly of the members of the classes in the range
     * Range: [ClassDefinition](ClassDefinition.md)
 * [defining_slots](defining_slots.md)  <sub>0..\*</sub>
     * Description: The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom
     * Range: [SlotDefinition](SlotDefinition.md)
 * [tree_root](tree_root.md)  <sub>0..1</sub>
     * Description: indicator that this is the root class in tree structures
     * Range: [Boolean](types/Boolean.md)
 * [class_definition➞is_a](class_definition_is_a.md)  <sub>0..1</sub>
     * Range: [ClassDefinition](ClassDefinition.md)
 * [class_definition➞mixins](class_definition_mixins.md)  <sub>0..\*</sub>
     * Range: [ClassDefinition](ClassDefinition.md)
 * [class_definition➞apply_to](class_definition_apply_to.md)  <sub>0..\*</sub>
     * Range: [ClassDefinition](ClassDefinition.md)

### Inherited from definition:

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with one of the URIs referenced by this prefix
     * Range: [Ncname](types/Ncname.md)
 * [definition_uri](definition_uri.md)  <sub>0..1</sub>
     * Description: the "native" URI of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [mappings](mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a description of the element's purpose and use
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Range: [AltDescription](AltDescription.md)
 * [deprecated](deprecated.md)  <sub>0..1</sub>
     * Description: Description of why and when this element will no longer be used
     * Range: [String](types/String.md)
 * [todos](todos.md)  <sub>0..\*</sub>
     * Description: Outstanding issue that needs resolution
     * Range: [String](types/String.md)
 * [notes](notes.md)  <sub>0..\*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [comments](comments.md)  <sub>0..\*</sub>
     * Description: notes and comments about an element intended for external consumption
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [examples](examples.md)  <sub>0..\*</sub>
     * Description: example usages of an element
     * Range: [Example](Example.md)
     * in subsets: (owl)
 * [in_subset](in_subset.md)  <sub>0..\*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * Range: [SubsetDefinition](SubsetDefinition.md)
 * [from_schema](from_schema.md)  <sub>0..1</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](types/Uri.md)
 * [imported_from](imported_from.md)  <sub>0..1</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * Range: [String](types/String.md)
 * [see_also](see_also.md)  <sub>0..\*</sub>
     * Description: a reference
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (owl)
 * [exact mappings](exact_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have identical meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [close mappings](close_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have close meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [related mappings](related_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have related meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [narrow mappings](narrow_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have narrower meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [broad mappings](broad_mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have broader meaning.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>0..1</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [abstract](abstract.md)  <sub>0..1</sub>
     * Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
     * Range: [Boolean](types/Boolean.md)
 * [mixin](mixin.md)  <sub>0..1</sub>
     * Description: this slot or class can only be used as a mixin.
     * Range: [Boolean](types/Boolean.md)
 * [values_from](values_from.md)  <sub>0..\*</sub>
     * Description: the identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [created_by](created_by.md)  <sub>0..1</sub>
     * Description: agent that created the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [created_on](created_on.md)  <sub>0..1</sub>
     * Description: time at which the element was created
     * Range: [Datetime](types/Datetime.md)
 * [last_updated_on](last_updated_on.md)  <sub>0..1</sub>
     * Description: time at which the element was last updated
     * Range: [Datetime](types/Datetime.md)
 * [modified_by](modified_by.md)  <sub>0..1</sub>
     * Description: agent that modified the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [status](status.md)  <sub>0..1</sub>
     * Description: status of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * Example: bibo:draft None

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | table |
|  | | record |
|  | | template |

