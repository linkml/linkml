
# Class: slot_definition


the definition of a property or a slot

URI: [linkml:SlotDefinition](https://w3id.org/linkml/SlotDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[UniqueKey],[SubsetDefinition],[SlotDefinition]<apply_to%200..*-%20[SlotDefinition&#124;singular_name:string%20%3F;slot_uri:uriorcurie%20%3F;multivalued:boolean%20%3F;inherited:boolean%20%3F;readonly:string%20%3F;ifabsent:string%20%3F;required:boolean%20%3F;recommended:boolean%20%3F;inlined:boolean%20%3F;inlined_as_list:boolean%20%3F;key:boolean%20%3F;identifier:boolean%20%3F;designates_type:boolean%20%3F;alias:string%20%3F;symmetric:boolean%20%3F;is_class_field:boolean%20%3F;role:string%20%3F;is_usage_slot:boolean%20%3F;usage_slot_name:string%20%3F;minimum_value:integer%20%3F;maximum_value:integer%20%3F;pattern:string%20%3F;abstract(i):boolean%20%3F;mixin(i):boolean%20%3F;values_from(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;string_serialization(i):string%20%3F;name(i):string;title(i):string%20%3F;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[SlotDefinition]<mixins%200..*-%20[SlotDefinition],[SlotDefinition]<is_a%200..1-%20[SlotDefinition],[SlotDefinition]<inverse%200..1-%20[SlotDefinition],[SlotDefinition]<subproperty_of%200..1-%20[SlotDefinition],[ClassDefinition]<domain_of%200..*-%20[SlotDefinition],[Definition]<owner%200..1-%20[SlotDefinition],[Element]<range%200..1-%20[SlotDefinition],[ClassDefinition]<domain%200..1-%20[SlotDefinition],[ClassDefinition]++-%20attributes%200..*>[SlotDefinition],[ClassDefinition]-%20defining_slots%200..*>[SlotDefinition],[SchemaDefinition]++-%20slots%200..*>[SlotDefinition],[ClassDefinition]++-%20slot_usage%200..*>[SlotDefinition],[ClassDefinition]-%20slots%200..*>[SlotDefinition],[UniqueKey]-%20unique_key_slots%201..*>[SlotDefinition],[Definition]^-[SlotDefinition],[SchemaDefinition],[LocalName],[Extension],[Example],[Element],[Definition],[ClassDefinition],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[UniqueKey],[SubsetDefinition],[SlotDefinition]<apply_to%200..*-%20[SlotDefinition&#124;singular_name:string%20%3F;slot_uri:uriorcurie%20%3F;multivalued:boolean%20%3F;inherited:boolean%20%3F;readonly:string%20%3F;ifabsent:string%20%3F;required:boolean%20%3F;recommended:boolean%20%3F;inlined:boolean%20%3F;inlined_as_list:boolean%20%3F;key:boolean%20%3F;identifier:boolean%20%3F;designates_type:boolean%20%3F;alias:string%20%3F;symmetric:boolean%20%3F;is_class_field:boolean%20%3F;role:string%20%3F;is_usage_slot:boolean%20%3F;usage_slot_name:string%20%3F;minimum_value:integer%20%3F;maximum_value:integer%20%3F;pattern:string%20%3F;abstract(i):boolean%20%3F;mixin(i):boolean%20%3F;values_from(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;string_serialization(i):string%20%3F;name(i):string;title(i):string%20%3F;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;description(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F],[SlotDefinition]<mixins%200..*-%20[SlotDefinition],[SlotDefinition]<is_a%200..1-%20[SlotDefinition],[SlotDefinition]<inverse%200..1-%20[SlotDefinition],[SlotDefinition]<subproperty_of%200..1-%20[SlotDefinition],[ClassDefinition]<domain_of%200..*-%20[SlotDefinition],[Definition]<owner%200..1-%20[SlotDefinition],[Element]<range%200..1-%20[SlotDefinition],[ClassDefinition]<domain%200..1-%20[SlotDefinition],[ClassDefinition]++-%20attributes%200..*>[SlotDefinition],[ClassDefinition]-%20defining_slots%200..*>[SlotDefinition],[SchemaDefinition]++-%20slots%200..*>[SlotDefinition],[ClassDefinition]++-%20slot_usage%200..*>[SlotDefinition],[ClassDefinition]-%20slots%200..*>[SlotDefinition],[UniqueKey]-%20unique_key_slots%201..*>[SlotDefinition],[Definition]^-[SlotDefinition],[SchemaDefinition],[LocalName],[Extension],[Example],[Element],[Definition],[ClassDefinition],[Annotation],[AltDescription])

## Parents

 *  is_a: [Definition](Definition.md) - base class for definitions

## Referenced by Class

 *  **[ClassDefinition](ClassDefinition.md)** *[attributes](attributes.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[defining_slots](defining_slots.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[inverse](inverse.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞apply_to](slot_definition_apply_to.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞is_a](slot_definition_is_a.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞mixins](slot_definition_mixins.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[schema_definition➞slots](slot_definitions.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[slot_usage](slot_usage.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[slots](slots.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[subproperty_of](subproperty_of.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[UniqueKey](UniqueKey.md)** *[unique_key_slots](unique_key_slots.md)*  <sub>1..\*</sub>  **[SlotDefinition](SlotDefinition.md)**

## Attributes


### Own

 * [singular_name](singular_name.md)  <sub>0..1</sub>
     * Description: a name that is used in the singular form
     * Range: [String](types/String.md)
 * [domain](domain.md)  <sub>0..1</sub>
     * Description: defines the type of the subject of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts that X is an instance of C1

     * Range: [ClassDefinition](ClassDefinition.md)
 * [range](range.md)  <sub>0..1</sub>
     * Description: defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2

     * Range: [Element](Element.md)
 * [slot_uri](slot_uri.md)  <sub>0..1</sub>
     * Description: predicate of this slot for semantic web application
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [multivalued](multivalued.md)  <sub>0..1</sub>
     * Description: true means that slot can have more than one value
     * Range: [Boolean](types/Boolean.md)
 * [inherited](inherited.md)  <sub>0..1</sub>
     * Description: true means that the *value* of a slot is inherited by subclasses
     * Range: [Boolean](types/Boolean.md)
 * [readonly](readonly.md)  <sub>0..1</sub>
     * Description: If present, slot is read only.  Text explains why
     * Range: [String](types/String.md)
 * [ifabsent](ifabsent.md)  <sub>0..1</sub>
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
     * Range: [String](types/String.md)
 * [required](required.md)  <sub>0..1</sub>
     * Description: true means that the slot must be present in the loaded definition
     * Range: [Boolean](types/Boolean.md)
 * [recommended](recommended.md)  <sub>0..1</sub>
     * Description: true means that the slot should be present in the loaded definition, but this is not required
     * Range: [Boolean](types/Boolean.md)
 * [inlined](inlined.md)  <sub>0..1</sub>
     * Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
     * Range: [Boolean](types/Boolean.md)
 * [inlined_as_list](inlined_as_list.md)  <sub>0..1</sub>
     * Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
     * Range: [Boolean](types/Boolean.md)
 * [key](key.md)  <sub>0..1</sub>
     * Description: True means that the key slot(s) uniquely identify the container.
     * Range: [Boolean](types/Boolean.md)
 * [identifier](identifier.md)  <sub>0..1</sub>
     * Description: True means that the key slot(s) uniquely identify the container. There can be at most one identifier or key per container
     * Range: [Boolean](types/Boolean.md)
 * [designates_type](designates_type.md)  <sub>0..1</sub>
     * Description: True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition
     * Range: [Boolean](types/Boolean.md)
 * [alias](alias.md)  <sub>0..1</sub>
     * Description: the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
     * Range: [String](types/String.md)
 * [owner](owner.md)  <sub>0..1</sub>
     * Description: the "owner" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot
     * Range: [Definition](Definition.md)
 * [domain_of](domain_of.md)  <sub>0..\*</sub>
     * Description: the class(es) that reference the slot in a "slots" or "slot_usage" context
     * Range: [ClassDefinition](ClassDefinition.md)
 * [subproperty_of](subproperty_of.md)  <sub>0..1</sub>
     * Description: Ontology property which this slot is a subproperty of
     * Range: [SlotDefinition](SlotDefinition.md)
 * [symmetric](symmetric.md)  <sub>0..1</sub>
     * Description: True means that any instance of  d s r implies that there is also an instance of r s d
     * Range: [Boolean](types/Boolean.md)
 * [inverse](inverse.md)  <sub>0..1</sub>
     * Description: indicates that any instance of d s r implies that there is also an instance of r s' d
     * Range: [SlotDefinition](SlotDefinition.md)
 * [is_class_field](is_class_field.md)  <sub>0..1</sub>
     * Description: indicates that any instance, i,  the domain of this slot will include an assert of i s range
     * Range: [Boolean](types/Boolean.md)
 * [role](role.md)  <sub>0..1</sub>
     * Description: the role played by the slot range
     * Range: [String](types/String.md)
 * [is_usage_slot](is_usage_slot.md)  <sub>0..1</sub>
     * Description: True means that this slot was defined in a slot_usage situation
     * Range: [Boolean](types/Boolean.md)
 * [usage_slot_name](usage_slot_name.md)  <sub>0..1</sub>
     * Description: The name of the slot referenced in the slot_usage
     * Range: [String](types/String.md)
 * [minimum_value](minimum_value.md)  <sub>0..1</sub>
     * Description: for slots with ranges of type number, the value must be equal to or higher than this
     * Range: [Integer](types/Integer.md)
 * [maximum_value](maximum_value.md)  <sub>0..1</sub>
     * Description: for slots with ranges of type number, the value must be equal to or lowe than this
     * Range: [Integer](types/Integer.md)
 * [pattern](pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to this regular expression
     * Range: [String](types/String.md)
 * [slot_definition➞is_a](slot_definition_is_a.md)  <sub>0..1</sub>
     * Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * Range: [SlotDefinition](SlotDefinition.md)
 * [slot_definition➞mixins](slot_definition_mixins.md)  <sub>0..\*</sub>
     * Description: List of definitions to be mixed in. Targets may be any definition of the same type
     * Range: [SlotDefinition](SlotDefinition.md)
 * [slot_definition➞apply_to](slot_definition_apply_to.md)  <sub>0..\*</sub>
     * Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * Range: [SlotDefinition](SlotDefinition.md)

### Inherited from definition:

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [title](title.md)  <sub>0..1</sub>
     * Description: the official title of the element
     * Range: [String](types/String.md)
     * in subsets: (owl)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
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
 * [string_serialization](string_serialization.md)  <sub>0..1</sub>
     * Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | slot |
|  | | field |
|  | | property |
|  | | attribute |
|  | | column |
|  | | variable |
| **Close Mappings:** | | rdf:Property |

