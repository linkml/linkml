
# Class: SlotDefinition


the definition of a property or a slot

URI: [linkml:SlotDefinition](https://w3id.org/linkml/SlotDefinition)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[SlotDefinition]<apply_to%200..*-%20[SlotDefinition&#124;singular_name:string%20%3F;slot_uri:uriorcurie%20%3F;multivalued:boolean%20%3F;inherited:boolean%20%3F;readonly:string%20%3F;ifabsent:string%20%3F;required:boolean%20%3F;inlined:boolean%20%3F;inlined_as_list:boolean%20%3F;key:boolean%20%3F;identifier:boolean%20%3F;alias:string%20%3F;symmetric:boolean%20%3F;is_class_field:boolean%20%3F;role:string%20%3F;is_usage_slot:boolean%20%3F;usage_slot_name:string%20%3F;minimum_value:integer%20%3F;maximum_value:integer%20%3F;pattern:string%20%3F;string_serialization:string%20%3F;abstract(i):boolean%20%3F;mixin(i):boolean%20%3F;values_from(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[SlotDefinition]<mixins%200..*-%20[SlotDefinition],[SlotDefinition]<is_a%200..1-%20[SlotDefinition],[SlotDefinition]<inverse%200..1-%20[SlotDefinition],[SlotDefinition]<subproperty_of%200..1-%20[SlotDefinition],[ClassDefinition]<domain_of%200..*-%20[SlotDefinition],[Definition]<owner%200..1-%20[SlotDefinition],[Element]<range%200..1-%20[SlotDefinition],[ClassDefinition]<domain%200..1-%20[SlotDefinition],[ClassDefinition]++-%20attributes%200..*>[SlotDefinition],[ClassDefinition]-%20defining_slots%200..*>[SlotDefinition],[SchemaDefinition]++-%20slots%200..*>[SlotDefinition],[ClassDefinition]++-%20slot_usage%200..*>[SlotDefinition],[ClassDefinition]-%20slots%200..*>[SlotDefinition],[Definition]^-[SlotDefinition],[SchemaDefinition],[LocalName],[Extension],[Example],[Element],[Definition],[ClassDefinition],[Annotation],[AltDescription])

## Parents

 *  is_a: [Definition](Definition.md) - base class for definitions

## Referenced by class

 *  **[ClassDefinition](ClassDefinition.md)** *[attributes](attributes.md)*  <sub>0..*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[defining_slots](defining_slots.md)*  <sub>0..*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[inverse](inverse.md)*  <sub>OPT</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞apply_to](slot_definition_apply_to.md)*  <sub>0..*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞is_a](slot_definition_is_a.md)*  <sub>OPT</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞mixins](slot_definition_mixins.md)*  <sub>0..*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[schema_definition➞slots](slot_definitions.md)*  <sub>0..*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[slot_usage](slot_usage.md)*  <sub>0..*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[slots](slots.md)*  <sub>0..*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[subproperty_of](subproperty_of.md)*  <sub>OPT</sub>  **[SlotDefinition](SlotDefinition.md)**

## Attributes


### Own

 * [alias](alias.md)  <sub>OPT</sub>
     * Description: the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
     * range: [String](types/String.md)
 * [domain](domain.md)  <sub>OPT</sub>
     * Description: defines the type of the subject of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts that X is an instance of C1

     * range: [ClassDefinition](ClassDefinition.md)
 * [domain_of](domain_of.md)  <sub>0..*</sub>
     * Description: the class(es) that reference the slot in a "slots" or "slot_usage" context
     * range: [ClassDefinition](ClassDefinition.md)
 * [identifier](identifier.md)  <sub>OPT</sub>
     * Description: True means that the key slot(s) uniquely identify the container. There can be at most one identifier or key per container
     * range: [Boolean](types/Boolean.md)
 * [ifabsent](ifabsent.md)  <sub>OPT</sub>
     * Description: function that provides a default value for the slot.  Possible values for this slot are defined in biolink.utils.ifabsent_functions.default_library:
  * [Tt]rue -- boolean True
  * [Ff]alse -- boolean False
  * int(value) -- integer value
  * str(value) -- string value
  * default_range -- schema default range
  * bnode -- blank node identifier
  * slot_uri -- URI for the slot
  * class_curie -- CURIE for the containing class
  * class_uri -- URI for the containing class
     * range: [String](types/String.md)
 * [inherited](inherited.md)  <sub>OPT</sub>
     * Description: true means that the *value* of a slot is inherited by subclasses
     * range: [Boolean](types/Boolean.md)
 * [inlined](inlined.md)  <sub>OPT</sub>
     * Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
     * range: [Boolean](types/Boolean.md)
 * [inlined_as_list](inlined_as_list.md)  <sub>OPT</sub>
     * Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
     * range: [Boolean](types/Boolean.md)
 * [inverse](inverse.md)  <sub>OPT</sub>
     * Description: indicates that any instance of d s r implies that there is also an instance of r s' d
     * range: [SlotDefinition](SlotDefinition.md)
 * [is_class_field](is_class_field.md)  <sub>OPT</sub>
     * Description: indicates that any instance, i,  the domain of this slot will include an assert of i s range
     * range: [Boolean](types/Boolean.md)
 * [is_usage_slot](is_usage_slot.md)  <sub>OPT</sub>
     * Description: True means that this slot was defined in a slot_usage situation
     * range: [Boolean](types/Boolean.md)
 * [key](key.md)  <sub>OPT</sub>
     * Description: True means that the key slot(s) uniquely identify the container. In future releases, it will be possible for there to be compound keys, where several slots combine to produce a unique identifier
     * range: [Boolean](types/Boolean.md)
 * [maximum_value](maximum_value.md)  <sub>OPT</sub>
     * Description: for slots with ranges of type number, the value must be equal to or lowe than this
     * range: [Integer](types/Integer.md)
 * [minimum_value](minimum_value.md)  <sub>OPT</sub>
     * Description: for slots with ranges of type number, the value must be equal to or higher than this
     * range: [Integer](types/Integer.md)
 * [multivalued](multivalued.md)  <sub>OPT</sub>
     * Description: true means that slot can have more than one value
     * range: [Boolean](types/Boolean.md)
 * [owner](owner.md)  <sub>OPT</sub>
     * Description: the "owner" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot
     * range: [Definition](Definition.md)
 * [pattern](pattern.md)  <sub>OPT</sub>
     * Description: the string value of the slot must conform to this regular expression
     * range: [String](types/String.md)
 * [range](range.md)  <sub>OPT</sub>
     * Description: defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2

     * range: [Element](Element.md)
 * [readonly](readonly.md)  <sub>OPT</sub>
     * Description: If present, slot is read only.  Text explains why
     * range: [String](types/String.md)
 * [required](required.md)  <sub>OPT</sub>
     * Description: true means that the slot must be present in the loaded definition
     * range: [Boolean](types/Boolean.md)
 * [role](role.md)  <sub>OPT</sub>
     * Description: the role played by the slot range
     * range: [String](types/String.md)
 * [singular_name](singular_name.md)  <sub>OPT</sub>
     * Description: a name that is used in the singular form
     * range: [String](types/String.md)
 * [slot_definition➞apply_to](slot_definition_apply_to.md)  <sub>0..*</sub>
     * range: [SlotDefinition](SlotDefinition.md)
 * [slot_definition➞is_a](slot_definition_is_a.md)  <sub>OPT</sub>
     * range: [SlotDefinition](SlotDefinition.md)
 * [slot_definition➞mixins](slot_definition_mixins.md)  <sub>0..*</sub>
     * range: [SlotDefinition](SlotDefinition.md)
 * [slot_uri](slot_uri.md)  <sub>OPT</sub>
     * Description: predicate of this slot for semantic web application
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [string_serialization](string_serialization.md)  <sub>OPT</sub>
     * Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
     * range: [String](types/String.md)
 * [subproperty_of](subproperty_of.md)  <sub>OPT</sub>
     * Description: Ontology property which this slot is a subproperty of
     * range: [SlotDefinition](SlotDefinition.md)
 * [symmetric](symmetric.md)  <sub>OPT</sub>
     * Description: True means that any instance of  d s r implies that there is also an instance of r s d
     * range: [Boolean](types/Boolean.md)
 * [usage_slot_name](usage_slot_name.md)  <sub>OPT</sub>
     * Description: The name of the slot referenced in the slot_usage
     * range: [String](types/String.md)

### Inherited from definition:

 * [abstract](abstract.md)  <sub>OPT</sub>
     * Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
     * range: [Boolean](types/Boolean.md)
 * [aliases](aliases.md)  <sub>0..*</sub>
     * range: [String](types/String.md)
 * [alt_descriptions](alt_descriptions.md)  <sub>0..*</sub>
     * range: [AltDescription](AltDescription.md)
 * [broad mappings](broad_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have broader meaning.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [close mappings](close_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have close meaning.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [comments](comments.md)  <sub>0..*</sub>
     * Description: notes and comments about an element intended for external consumption
     * range: [String](types/String.md)
     * in subsets: (owl)
 * [created_by](created_by.md)  <sub>OPT</sub>
     * Description: agent that created the element
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [created_on](created_on.md)  <sub>OPT</sub>
     * Description: time at which the element was created
     * range: [Datetime](types/Datetime.md)
 * [definition_uri](definition_uri.md)  <sub>OPT</sub>
     * Description: the "native" URI of the element
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated](deprecated.md)  <sub>OPT</sub>
     * Description: Description of why and when this element will no longer be used
     * range: [String](types/String.md)
 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be automatically replaced by this uri or curie
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md)  <sub>OPT</sub>
     * Description: When an element is deprecated, it can be potentially replaced by this uri or curie
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a description of the element's purpose and use
     * range: [String](types/String.md)
     * in subsets: (owl)
 * [exact mappings](exact_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have identical meaning.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [examples](examples.md)  <sub>0..*</sub>
     * Description: example usages of an element
     * range: [Example](Example.md)
     * in subsets: (owl)
 * [from_schema](from_schema.md)  <sub>OPT</sub>
     * Description: id of the schema that defined the element
     * range: [Uri](types/Uri.md)
 * [id_prefixes](id_prefixes.md)  <sub>0..*</sub>
     * Description: the identifier of this class or slot must begin with one of the URIs referenced by this prefix
     * range: [Ncname](types/Ncname.md)
 * [imported_from](imported_from.md)  <sub>OPT</sub>
     * Description: the imports entry that this element was derived from.  Empty means primary source
     * range: [String](types/String.md)
 * [in_subset](in_subset.md)  <sub>0..*</sub>
     * Description: used to indicate membership of a term in a defined subset of terms used for a particular domain or application (e.g. the translator_minimal subset holding the minimal set of predicates used in a translator knowledge graph)
     * range: [SubsetDefinition](SubsetDefinition.md)
 * [last_updated_on](last_updated_on.md)  <sub>OPT</sub>
     * Description: time at which the element was last updated
     * range: [Datetime](types/Datetime.md)
 * [local_names](local_names.md)  <sub>0..*</sub>
     * range: [LocalName](LocalName.md)
 * [mappings](mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [mixin](mixin.md)  <sub>OPT</sub>
     * Description: this slot or class can only be used as a mixin -- equivalent to abstract
     * range: [Boolean](types/Boolean.md)
 * [modified_by](modified_by.md)  <sub>OPT</sub>
     * Description: agent that modified the element
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [name](name.md)  <sub>REQ</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * range: [String](types/String.md)
     * in subsets: (owl)
 * [narrow mappings](narrow_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have narrower meaning.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [notes](notes.md)  <sub>0..*</sub>
     * Description: editorial notes about an element intended for internal consumption
     * range: [String](types/String.md)
     * in subsets: (owl)
 * [related mappings](related_mappings.md)  <sub>0..*</sub>
     * Description: A list of terms from different schemas or terminology systems that have related meaning.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [see_also](see_also.md)  <sub>0..*</sub>
     * Description: a reference
     * range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (owl)
 * [status](status.md)  <sub>OPT</sub>
     * Description: status of the element
     * range: [Uriorcurie](types/Uriorcurie.md)
     * Example: bibo:draft None
 * [todos](todos.md)  <sub>0..*</sub>
     * Description: Outstanding issue that needs resolution
     * range: [String](types/String.md)
 * [values_from](values_from.md)  <sub>0..*</sub>
     * Description: the identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot
     * range: [Uriorcurie](types/Uriorcurie.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | slot |
|  | | field |
|  | | property |
|  | | attribute |

