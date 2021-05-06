
# Class: ClassDefinition


the definition of a class or interface

URI: [linkml:ClassDefinition](https://w3id.org/linkml/ClassDefinition)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[SlotDefinition],[SchemaDefinition],[LocalName],[Extension],[Example],[Definition],[ClassDefinition]<apply_to%200..*-%20[ClassDefinition&#124;class_uri:uriorcurie%20%3F;subclass_of:uriorcurie%20%3F;tree_root:boolean%20%3F;abstract(i):boolean%20%3F;mixin(i):boolean%20%3F;values_from(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[ClassDefinition]<mixins%200..*-%20[ClassDefinition],[ClassDefinition]<is_a%200..1-%20[ClassDefinition],[SlotDefinition]<defining_slots%200..*-%20[ClassDefinition],[ClassDefinition]<union_of%200..*-%20[ClassDefinition],[SlotDefinition]<attributes%200..*-++[ClassDefinition],[SlotDefinition]<slot_usage%200..*-++[ClassDefinition],[SlotDefinition]<slots%200..*-%20[ClassDefinition],[SchemaDefinition]++-%20classes%200..*>[ClassDefinition],[SlotDefinition]-%20domain%200..1>[ClassDefinition],[SlotDefinition]-%20domain_of%200..*>[ClassDefinition],[Definition]^-[ClassDefinition],[Annotation],[AltDescription])

## Parents

 *  is_a: [Definition](Definition.md) - base class for definitions

## Referenced by class

 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞apply_to](class_definition_apply_to.md)*  <sub>0..*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞is_a](class_definition_is_a.md)*  <sub>OPT</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞mixins](class_definition_mixins.md)*  <sub>0..*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[classes](classes.md)*  <sub>0..*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[domain](domain.md)*  <sub>OPT</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[domain_of](domain_of.md)*  <sub>0..*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[union_of](union_of.md)*  <sub>0..*</sub>  **[ClassDefinition](ClassDefinition.md)**

## Attributes


### Own

 * [attributes](attributes.md)  <sub>0..*</sub>
     * Description: Inline definition of slots
     * range: [SlotDefinition](SlotDefinition.md)
 * [class_definition➞apply_to](class_definition_apply_to.md)  <sub>0..*</sub>
     * range: [ClassDefinition](ClassDefinition.md)
 * [class_definition➞is_a](class_definition_is_a.md)  <sub>OPT</sub>
     * range: [ClassDefinition](ClassDefinition.md)
 * [class_definition➞mixins](class_definition_mixins.md)  <sub>0..*</sub>
     * range: [ClassDefinition](ClassDefinition.md)
 * [class_uri](class_uri.md)  <sub>OPT</sub>
     * Description: URI of the class in an RDF environment
     * range: [Uriorcurie](Uriorcurie.md)
 * [defining_slots](defining_slots.md)  <sub>0..*</sub>
     * Description: The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom
     * range: [SlotDefinition](SlotDefinition.md)
 * [slot_usage](slot_usage.md)  <sub>0..*</sub>
     * Description: the redefinition of a slot in the context of the containing class definition.
     * range: [SlotDefinition](SlotDefinition.md)
 * [slots](slots.md)  <sub>0..*</sub>
     * Description: list of slot names that are applicable to a class
     * range: [SlotDefinition](SlotDefinition.md)
 * [subclass_of](subclass_of.md)  <sub>OPT</sub>
     * Description: rdfs:subClassOf to be emitted in OWL generation
     * range: [Uriorcurie](Uriorcurie.md)
 * [tree_root](tree_root.md)  <sub>OPT</sub>
     * Description: indicator that this is the root class in tree structures
     * range: [Boolean](Boolean.md)
 * [union_of](union_of.md)  <sub>0..*</sub>
     * Description: indicates that the domain class consists exactly of the members of the classes in the range
     * range: [ClassDefinition](ClassDefinition.md)

### Inherited from definition:

 * [abstract](abstract.md)  <sub>OPT</sub>
     * Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
     * range: [Boolean](Boolean.md)
 * [aliases](aliases.md)  <sub>0..*</sub>
     * range: [String](String.md)
 * [alt_descriptions](alt_descriptions.md)  <sub>0..*</sub>
     * range: [AltDescription](AltDescription.md)
 * [broad mappings](broad_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have broader meaning.
     * range: [Uriorcurie](Uriorcurie.md)
 * [close mappings](close_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have close meaning.
     * range: [Uriorcurie](Uriorcurie.md)
 * [comments](comments.md)  <sub>0..*</sub>
     * Description: notes and comments about an element intended for external consumption
     * range: [String](String.md)
     * in subsets: (owl)
 * [created_by](created_by.md)  <sub>OPT</sub>
     * Description: agent that created the element
     * range: [Uriorcurie](Uriorcurie.md)
 * [created_on](created_on.md)  <sub>OPT</sub>
     * Description: time at which the element was created
     * range: [Datetime](Datetime.md)
 * [definition_uri](definition_uri.md)  <sub>OPT</sub>
     * Description: the "native" URI of the element
     * range: [Uriorcurie](Uriorcurie.md)
 * [deprecated](deprecated.md)  <sub>OPT</sub>
     * Description: Description of why and when this element will no longer be used
     * range: [String](String.md)
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * range: [Uriorcurie](Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * range: [Uriorcurie](Uriorcurie.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a description of the element's purpose and use
     * range: [String](String.md)
     * in subsets: (owl)
 * [exact mappings](exact_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have identical meaning.
     * range: [Uriorcurie](Uriorcurie.md)
 * [examples](examples.md)  <sub>0..*</sub>
     * Description: example usages of an element
     * range: [Example](Example.md)
     * in subsets: (owl)
 * [from_schema](from_schema.md)  <sub>OPT</sub>
     * Description: id of the schema that defined the element
     * range: [Uri](Uri.md)
 * [id_prefixes](id_prefixes.md)  <sub>0..*</sub>
     * Description: the identifier of this class or slot must begin with one of the URIs referenced by this prefix
     * range: [Ncname](Ncname.md)
 * [imported_from](imported_from.md)  <sub>OPT</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * range: [String](String.md)
 * [in_subset](in_subset.md)  <sub>0..*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * range: [SubsetDefinition](SubsetDefinition.md)
 * [last_updated_on](last_updated_on.md)  <sub>OPT</sub>
     * Description: time at which the element was last updated
     * range: [Datetime](Datetime.md)
 * [local_names](local_names.md)  <sub>0..*</sub>
     * range: [LocalName](LocalName.md)
 * [mappings](mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * range: [Uriorcurie](Uriorcurie.md)
 * [mixin](mixin.md)  <sub>OPT</sub>
     * Description: this slot or class can only be used as a mixin -- equivalent to abstract
     * range: [Boolean](Boolean.md)
 * [modified_by](modified_by.md)  <sub>OPT</sub>
     * Description: agent that modified the element
     * range: [Uriorcurie](Uriorcurie.md)
 * [name](name.md)  <sub>REQ</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * range: [String](String.md)
     * in subsets: (owl)
 * [narrow mappings](narrow_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have narrower meaning.
     * range: [Uriorcurie](Uriorcurie.md)
 * [notes](notes.md)  <sub>0..*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * range: [String](String.md)
     * in subsets: (owl)
 * [related mappings](related_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have related meaning.
     * range: [Uriorcurie](Uriorcurie.md)
 * [see_also](see_also.md)  <sub>0..*</sub>
     * Description: a reference
     * range: [Uriorcurie](Uriorcurie.md)
     * in subsets: (owl)
 * [status](status.md)  <sub>OPT</sub>
     * Description: status of the element
     * range: [Uriorcurie](Uriorcurie.md)
     * Example: bibo:draft None
 * [todos](todos.md)  <sub>0..*</sub>
     * Description: Outstanding issue that needs resolution
     * range: [String](String.md)
 * [values_from](values_from.md)  <sub>0..*</sub>
     * Description: the identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot
     * range: [Uriorcurie](Uriorcurie.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | table |
|  | | record |
|  | | template |

