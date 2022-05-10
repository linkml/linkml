
# Class: class_definition


the definition of a class or interface

URI: [linkml:ClassDefinition](https://w3id.org/linkml/ClassDefinition)


[![img](images/ClassDefinition.svg)](images/ClassDefinition.svg)

## Parents

 *  is_a: [Definition](Definition.md) - base class for definitions

## Uses Mixin

 *  mixin: [ClassExpression](ClassExpression.md) - A boolean expression that can be used to dynamically determine membership of a class

## Referenced by Class

 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞apply_to](class_definition_apply_to.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞disjoint_with](class_definition_disjoint_with.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
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
     * in subsets: (basic)
 * [slot_usage](slot_usage.md)  <sub>0..\*</sub>
     * Description: the redefinition of a slot in the context of the containing class definition.
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (basic)
 * [attributes](attributes.md)  <sub>0..\*</sub>
     * Description: Inline definition of slots
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (minimal,basic,relational_model,object_oriented)
 * [class_uri](class_uri.md)  <sub>0..1</sub>
     * Description: URI of the class in an RDF environment
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)
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
     * in subsets: (basic)
 * [unique_keys](unique_keys.md)  <sub>0..\*</sub>
     * Description: Set of unique keys for this slot
     * Range: [UniqueKey](UniqueKey.md)
     * in subsets: (basic,relational_model)
 * [class_definition➞rules](class_definition_rules.md)  <sub>0..\*</sub>
     * Description: the collection of rules that apply to all members of this class
     * Range: [ClassRule](ClassRule.md)
 * [classification_rules](classification_rules.md)  <sub>0..\*</sub>
     * Description: the collection of classification rules that apply to all members of this class
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
 * [slot_names_unique](slot_names_unique.md)  <sub>0..1</sub>
     * Description: if true then induced/mangled slot names are not created for class_usage and attributes
     * Range: [Boolean](types/Boolean.md)
 * [represents_relationship](represents_relationship.md)  <sub>0..1</sub>
     * Description: true if this class represents a relationship rather than an entity
     * Range: [Boolean](types/Boolean.md)
 * [class_definition➞disjoint_with](class_definition_disjoint_with.md)  <sub>0..\*</sub>
     * Description: Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
     * Range: [ClassDefinition](ClassDefinition.md)
 * [children_are_mutually_disjoint](children_are_mutually_disjoint.md)  <sub>0..1</sub>
     * Description: If true then all direct is_a children are mutually disjoint and share no instances in common
     * Range: [Boolean](types/Boolean.md)
 * [class_definition➞is_a](class_definition_is_a.md)  <sub>0..1</sub>
     * Description: specifies single-inheritance between classes or slots. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * Range: [ClassDefinition](ClassDefinition.md)
     * in subsets: (basic,object_oriented)
 * [class_definition➞mixins](class_definition_mixins.md)  <sub>0..\*</sub>
     * Description: List of definitions to be mixed in. Targets may be any definition of the same type
     * Range: [ClassDefinition](ClassDefinition.md)
     * in subsets: (basic,object_oriented)
 * [class_definition➞apply_to](class_definition_apply_to.md)  <sub>0..\*</sub>
     * Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * Range: [ClassDefinition](ClassDefinition.md)

### Inherited from definition:

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](types/String.md)
     * in subsets: (owl,minimal,basic,relational_model,object_oriented)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: the identifier of this class or slot must begin with the URIs referenced by this prefix
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (basic)
 * [definition_uri](definition_uri.md)  <sub>0..1</sub>
     * Description: the "native" URI of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [conforms_to](conforms_to.md)  <sub>0..1</sub>
     * Description: An established standard to which the element conforms.
     * Range: [String](types/String.md)
     * in subsets: (owl,basic)
 * [abstract](abstract.md)  <sub>0..1</sub>
     * Description: an abstract class is a high level class or slot that is typically used to group common slots together and cannot be directly instantiated.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (basic,object_oriented)
 * [mixin](mixin.md)  <sub>0..1</sub>
     * Description: this slot or class can only be used as a mixin.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (basic,object_oriented)
 * [values_from](values_from.md)  <sub>0..\*</sub>
     * Description: the identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [created_by](created_by.md)  <sub>0..1</sub>
     * Description: agent that created the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)
 * [created_on](created_on.md)  <sub>0..1</sub>
     * Description: time at which the element was created
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (basic)
 * [last_updated_on](last_updated_on.md)  <sub>0..1</sub>
     * Description: time at which the element was last updated
     * Range: [Datetime](types/Datetime.md)
     * in subsets: (basic)
 * [modified_by](modified_by.md)  <sub>0..1</sub>
     * Description: agent that modified the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (basic)
 * [status](status.md)  <sub>0..1</sub>
     * Description: status of the element
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * Example: bibo:draft None
     * in subsets: (basic)
 * [string_serialization](string_serialization.md)  <sub>0..1</sub>
     * Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
     * Range: [String](types/String.md)

### Mixed in from class_expression:

 * [class_expression➞any_of](class_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)

### Mixed in from class_expression:

 * [class_expression➞exactly_one_of](class_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)

### Mixed in from class_expression:

 * [class_expression➞none_of](class_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)

### Mixed in from class_expression:

 * [class_expression➞all_of](class_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)

### Mixed in from class_expression:

 * [slot_conditions](slot_conditions.md)  <sub>0..\*</sub>
     * Description: the redefinition of a slot in the context of the containing class definition.
     * Range: [SlotDefinition](SlotDefinition.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | table |
|  | | record |
|  | | template |
|  | | message |
|  | | observation |
| **In Subsets:** | | minimal |
|  | | basic |
|  | | relational_model |
|  | | object_oriented |
| **Close Mappings:** | | owl:Class |

