
# Class: Definition


base class for definitions

URI: [linkml:Definition](https://w3id.org/linkml/Definition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[SlotDefinition],[LocalName],[Extension],[Example],[Element],[Definition]<apply_to%200..*-%20[Definition&#124;abstract:boolean%20%3F;mixin:boolean%20%3F;values_from:uriorcurie%20*;created_by:uriorcurie%20%3F;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[Definition]<mixins%200..*-%20[Definition],[Definition]<is_a%200..1-%20[Definition],[SlotDefinition]-%20owner%200..1>[Definition],[Definition]^-[SlotDefinition],[Definition]^-[ClassDefinition],[Element]^-[Definition],[ClassDefinition],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[SlotDefinition],[LocalName],[Extension],[Example],[Element],[Definition]<apply_to%200..*-%20[Definition&#124;abstract:boolean%20%3F;mixin:boolean%20%3F;values_from:uriorcurie%20*;created_by:uriorcurie%20%3F;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[Definition]<mixins%200..*-%20[Definition],[Definition]<is_a%200..1-%20[Definition],[SlotDefinition]-%20owner%200..1>[Definition],[Definition]^-[SlotDefinition],[Definition]^-[ClassDefinition],[Element]^-[Definition],[ClassDefinition],[Annotation],[AltDescription])

## Parents

 *  is_a: [Element](Element.md) - a named element in the model

## Children

 * [ClassDefinition](ClassDefinition.md) - the definition of a class or interface
 * [SlotDefinition](SlotDefinition.md) - the definition of a property or a slot

## Referenced by class

 *  **[Definition](Definition.md)** *[apply_to](apply_to.md)*  <sub>0..\*</sub>  **[Definition](Definition.md)**
 *  **[Definition](Definition.md)** *[is_a](is_a.md)*  <sub>OPT</sub>  **[Definition](Definition.md)**
 *  **[Definition](Definition.md)** *[mixins](mixins.md)*  <sub>0..\*</sub>  **[Definition](Definition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[owner](owner.md)*  <sub>OPT</sub>  **[Definition](Definition.md)**

## Attributes


### Own

 * [is_a](is_a.md)  <sub>OPT</sub>
     * Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * Range: [Definition](Definition.md)
 * [abstract](abstract.md)  <sub>OPT</sub>
     * Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
     * Range: [Boolean](types/Boolean.md)
 * [mixin](mixin.md)  <sub>OPT</sub>
     * Description: this slot or class can only be used as a mixin.
     * Range: [Boolean](types/Boolean.md)
 * [mixins](mixins.md)  <sub>0..\*</sub>
     * Description: List of definitions to be mixed in. Targets may be any definition of the same type
     * Range: [Definition](Definition.md)
 * [apply_to](apply_to.md)  <sub>0..\*</sub>
     * Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * Range: [Definition](Definition.md)
 * [values_from](values_from.md)  <sub>0..\*</sub>
     * Description: the identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [created_by](created_by.md)  <sub>OPT</sub>
     * Description: agent that created the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [created_on](created_on.md)  <sub>OPT</sub>
     * Description: time at which the element was created
     * Range: [Datetime](types/Datetime.md)
 * [last_updated_on](last_updated_on.md)  <sub>OPT</sub>
     * Description: time at which the element was last updated
     * Range: [Datetime](types/Datetime.md)
 * [modified_by](modified_by.md)  <sub>OPT</sub>
     * Description: agent that modified the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [status](status.md)  <sub>OPT</sub>
     * Description: status of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * Example: bibo:draft None

### Inherited from element:

 * [name](name.md)  <sub>REQ</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with one of the URIs referenced by this prefix
     * Range: [Ncname](types/Ncname.md)
 * [definition_uri](definition_uri.md)  <sub>OPT</sub>
     * Description: the "native" URI of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [aliases](aliases.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [mappings](mappings.md)  <sub>0..\*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a description of the element's purpose and use
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [alt_descriptions](alt_descriptions.md)  <sub>0..\*</sub>
     * Range: [AltDescription](AltDescription.md)
 * [deprecated](deprecated.md)  <sub>OPT</sub>
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
 * [from_schema](from_schema.md)  <sub>OPT</sub>
     * Description: id of the schema that defined the element
     * Range: [Uri](types/Uri.md)
 * [imported_from](imported_from.md)  <sub>OPT</sub>
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
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * Range: [Uriorcurie](types/Uriorcurie.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **See also:** | | https://en.wikipedia.org/wiki/Data_element_definition |

