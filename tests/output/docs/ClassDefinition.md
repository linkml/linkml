
# Class: class_definition


an element whose instances are complex objects that may have slot-value assignments

URI: [linkml:ClassDefinition](https://w3id.org/linkml/ClassDefinition)


[![img](images/ClassDefinition.svg)](images/ClassDefinition.svg)

## Parents

 *  is_a: [Definition](Definition.md) - abstract base class for core metaclasses

## Uses Mixin

 *  mixin: [ClassExpression](ClassExpression.md) - A boolean expression that can be used to dynamically determine membership of a class

## Referenced by Class

 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞apply_to](class_definition_apply_to.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞disjoint_with](class_definition_disjoint_with.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞is_a](class_definition_is_a.md)*  <sub>0..1</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞mixins](class_definition_mixins.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[class_definition➞union_of](class_definition_union_of.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[classes](classes.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[domain](domain.md)*  <sub>0..1</sub>  **[ClassDefinition](ClassDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[domain_of](domain_of.md)*  <sub>0..\*</sub>  **[ClassDefinition](ClassDefinition.md)**

## Attributes


### Own

 * [slots](slots.md)  <sub>0..\*</sub>
     * Description: collection of slot names that are applicable to a class
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [slot_usage](slot_usage.md)  <sub>0..\*</sub>
     * Description: the refinement of a slot in the context of the containing class definition.
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [attributes](attributes.md)  <sub>0..\*</sub>
     * Description: Inline definition of slots
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile,OwlProfile)
 * [class_uri](class_uri.md)  <sub>0..1</sub>
     * Description: URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [subclass_of](subclass_of.md)  <sub>0..1</sub>
     * Description: DEPRECATED -- rdfs:subClassOf to be emitted in OWL generation
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [class_definition➞union_of](class_definition_union_of.md)  <sub>0..\*</sub>
     * Description: indicates that the domain element consists exactly of the members of the element in the range.
     * Range: [ClassDefinition](ClassDefinition.md)
     * in subsets: (SpecificationSubset,OwlProfile)
 * [defining_slots](defining_slots.md)  <sub>0..\*</sub>
     * Description: The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom
     * Range: [SlotDefinition](SlotDefinition.md)
 * [tree_root](tree_root.md)  <sub>0..1</sub>
     * Description: Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [unique_keys](unique_keys.md)  <sub>0..\*</sub>
     * Description: A collection of named unique keys for this class. Unique keys may be singular or compound.
     * Range: [UniqueKey](UniqueKey.md)
     * in subsets: (SpecificationSubset,BasicSubset,RelationalModelProfile)
 * [class_definition➞rules](class_definition_rules.md)  <sub>0..\*</sub>
     * Description: the collection of rules that apply to all members of this class
     * Range: [ClassRule](ClassRule.md)
     * in subsets: (SpecificationSubset)
 * [classification_rules](classification_rules.md)  <sub>0..\*</sub>
     * Description: The collection of classification rules that apply to all members of this class. Classification rules allow for automatically assigning the instantiated type of an instance.
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)
 * [slot_names_unique](slot_names_unique.md)  <sub>0..1</sub>
     * Description: if true then induced/mangled slot names are not created for class_usage and attributes
     * Range: [Boolean](types/Boolean.md)
 * [represents_relationship](represents_relationship.md)  <sub>0..1</sub>
     * Description: true if this class represents a relationship rather than an entity
     * Range: [Boolean](types/Boolean.md)
 * [class_definition➞disjoint_with](class_definition_disjoint_with.md)  <sub>0..\*</sub>
     * Description: Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
     * Range: [ClassDefinition](ClassDefinition.md)
     * in subsets: (SpecificationSubset)
 * [children_are_mutually_disjoint](children_are_mutually_disjoint.md)  <sub>0..1</sub>
     * Description: If true then all direct is_a children are mutually disjoint and share no instances in common
     * Range: [Boolean](types/Boolean.md)
 * [class_definition➞is_a](class_definition_is_a.md)  <sub>0..1</sub>
     * Description: A primary parent class from which inheritable metaslots are propagated
     * Range: [ClassDefinition](ClassDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [class_definition➞mixins](class_definition_mixins.md)  <sub>0..\*</sub>
     * Description: A collection of secondary parent mixin classes from which inheritable metaslots are propagated
     * Range: [ClassDefinition](ClassDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [class_definition➞apply_to](class_definition_apply_to.md)  <sub>0..\*</sub>
     * Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * Range: [ClassDefinition](ClassDefinition.md)

### Inherited from definition:

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,OwlProfile,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [definition_uri](definition_uri.md)  <sub>0..1</sub>
     * Description: The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [local_names](local_names.md)  <sub>0..\*</sub>
     * Range: [LocalName](LocalName.md)
 * [conforms_to](conforms_to.md)  <sub>0..1</sub>
     * Description: An established standard to which the element conforms.
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
 * [implements](implements.md)  <sub>0..\*</sub>
     * Description: An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [abstract](abstract.md)  <sub>0..1</sub>
     * Description: Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile)
 * [mixin](mixin.md)  <sub>0..1</sub>
     * Description: Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile)
 * [values_from](values_from.md)  <sub>0..\*</sub>
     * Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hiearchy into an enumerated list of possible values in every serialization of the model.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [string_serialization](string_serialization.md)  <sub>0..1</sub>
     * Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from class_expression:

 * [class_expression➞any_of](class_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from class_expression:

 * [class_expression➞exactly_one_of](class_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from class_expression:

 * [class_expression➞none_of](class_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from class_expression:

 * [class_expression➞all_of](class_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from class_expression:

 * [slot_conditions](slot_conditions.md)  <sub>0..\*</sub>
     * Description: expresses constraints on a group of slots for a class expression
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | table |
|  | | record |
|  | | template |
|  | | message |
|  | | observation |
| **In Subsets:** | | SpecificationSubset |
|  | | MinimalSubset |
|  | | BasicSubset |
|  | | RelationalModelProfile |
|  | | ObjectOrientedProfile |
|  | | OwlProfile |
| **Close Mappings:** | | owl:Class |

