
# Class: definition


base class for definitions

URI: [linkml:Definition](https://w3id.org/linkml/Definition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[SlotDefinition],[LocalName],[Extension],[Example],[Element],[Definition]<apply_to%200..*-%20[Definition&#124;abstract:boolean%20%3F;mixin:boolean%20%3F;values_from:uriorcurie%20*;created_by:uriorcurie%20%3F;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;string_serialization:string%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;rank(i):integer%20%3F],[Definition]<mixins%200..*-%20[Definition],[Definition]<is_a%200..1-%20[Definition],[SlotDefinition]-%20disjoint_with(i)%200..*>[Definition],[ClassDefinition]-%20disjoint_with(i)%200..*>[Definition],[SlotDefinition]-%20owner%200..1>[Definition],[Definition]^-[SlotDefinition],[Definition]^-[ClassDefinition],[Element]^-[Definition],[ClassDefinition],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[SlotDefinition],[LocalName],[Extension],[Example],[Element],[Definition]<apply_to%200..*-%20[Definition&#124;abstract:boolean%20%3F;mixin:boolean%20%3F;values_from:uriorcurie%20*;created_by:uriorcurie%20%3F;created_on:datetime%20%3F;last_updated_on:datetime%20%3F;modified_by:uriorcurie%20%3F;status:uriorcurie%20%3F;string_serialization:string%20%3F;name(i):string;id_prefixes(i):ncname%20*;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;rank(i):integer%20%3F],[Definition]<mixins%200..*-%20[Definition],[Definition]<is_a%200..1-%20[Definition],[SlotDefinition]-%20disjoint_with(i)%200..*>[Definition],[ClassDefinition]-%20disjoint_with(i)%200..*>[Definition],[SlotDefinition]-%20owner%200..1>[Definition],[Definition]^-[SlotDefinition],[Definition]^-[ClassDefinition],[Element]^-[Definition],[ClassDefinition],[Annotation],[AltDescription])

## Parents

 *  is_a: [Element](Element.md) - a named element in the model

## Children

 * [ClassDefinition](ClassDefinition.md) - the definition of a class or interface
 * [SlotDefinition](SlotDefinition.md) - the definition of a property or a slot

## Referenced by Class

 *  **[Definition](Definition.md)** *[apply_to](apply_to.md)*  <sub>0..\*</sub>  **[Definition](Definition.md)**
 *  **[Definition](Definition.md)** *[disjoint_with](disjoint_with.md)*  <sub>0..\*</sub>  **[Definition](Definition.md)**
 *  **[Definition](Definition.md)** *[is_a](is_a.md)*  <sub>0..1</sub>  **[Definition](Definition.md)**
 *  **[Definition](Definition.md)** *[mixins](mixins.md)*  <sub>0..\*</sub>  **[Definition](Definition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[owner](owner.md)*  <sub>0..1</sub>  **[Definition](Definition.md)**

## Attributes


### Own

 * [is_a](is_a.md)  <sub>0..1</sub>
     * Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * Range: [Definition](Definition.md)
     * in subsets: (basic,object_oriented)
 * [abstract](abstract.md)  <sub>0..1</sub>
     * Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
     * Range: [Boolean](Boolean.md)
     * in subsets: (basic,object_oriented)
 * [mixin](mixin.md)  <sub>0..1</sub>
     * Description: this slot or class can only be used as a mixin.
     * Range: [Boolean](Boolean.md)
     * in subsets: (basic,object_oriented)
 * [mixins](mixins.md)  <sub>0..\*</sub>
     * Description: List of definitions to be mixed in. Targets may be any definition of the same type
     * Range: [Definition](Definition.md)
     * in subsets: (basic,object_oriented)
 * [apply_to](apply_to.md)  <sub>0..\*</sub>
     * Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * Range: [Definition](Definition.md)
 * [values_from](values_from.md)  <sub>0..\*</sub>
     * Description: the identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot
     * Range: [Uriorcurie](Uriorcurie.md)
 * [created_by](created_by.md)  <sub>0..1</sub>
     * Description: agent that created the element
     * Range: [Uriorcurie](Uriorcurie.md)
     * in subsets: (basic)
 * [created_on](created_on.md)  <sub>0..1</sub>
     * Description: time at which the element was created
     * Range: [Datetime](Datetime.md)
     * in subsets: (basic)
 * [last_updated_on](last_updated_on.md)  <sub>0..1</sub>
     * Description: time at which the element was last updated
     * Range: [Datetime](Datetime.md)
     * in subsets: (basic)
 * [modified_by](modified_by.md)  <sub>0..1</sub>
     * Description: agent that modified the element
     * Range: [Uriorcurie](Uriorcurie.md)
     * in subsets: (basic)
 * [status](status.md)  <sub>0..1</sub>
     * Description: status of the element
     * Range: [Uriorcurie](Uriorcurie.md)
     * Example: bibo:draft None
     * in subsets: (basic)
 * [string_serialization](string_serialization.md)  <sub>0..1</sub>
     * Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
     * Range: [String](String.md)

### Inherited from element:

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](String.md)
     * in subsets: (owl,minimal,basic,relational_model,object_oriented)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
     * Range: [Ncname](Ncname.md)
     * in subsets: (basic)
 * [definition_uri](definition_uri.md)  <sub>0..1</sub>
     * Description: the "native" URI of the element
     * Range: [Uriorcurie](Uriorcurie.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [conforms_to](conforms_to.md)  <sub>0..1</sub>
     * Description: An established standard to which the element conforms.
     * Range: [String](String.md)
     * in subsets: (owl,basic)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | basic |
| **See also:** | | [https://en.wikipedia.org/wiki/Data_element_definition](https://en.wikipedia.org/wiki/Data_element_definition) |

