
# Class: enum_definition


an element whose instances must be drawn from a specified set of permissible values

URI: [linkml:EnumDefinition](https://w3id.org/linkml/EnumDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[SchemaDefinition],[ReachabilityQuery],[PermissibleValue],[MatchQuery],[LocalName],[Extension],[Example],[EnumExpression],[SchemaDefinition]++-%20enums%200..*>[EnumDefinition&#124;enum_uri:uriorcurie%20%3F;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;concepts:uriorcurie%20*;abstract(i):boolean%20%3F;mixin(i):boolean%20%3F;values_from(i):uriorcurie%20*;string_serialization(i):string%20%3F;name(i):string;id_prefixes(i):ncname%20*;id_prefixes_are_closed(i):boolean%20%3F;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;implements(i):uriorcurie%20*;instantiates(i):uriorcurie%20*;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;contributors(i):uriorcurie%20*;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;rank(i):integer%20%3F;categories(i):uriorcurie%20*;keywords(i):string%20*],[EnumExpression]-%20inherits%200..*>[EnumDefinition],[EnumDefinition]uses%20-.->[EnumExpression],[Definition]^-[EnumDefinition],[Definition],[AnonymousEnumExpression],[Annotation],[AltDescription])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubsetDefinition],[StructuredAlias],[SchemaDefinition],[ReachabilityQuery],[PermissibleValue],[MatchQuery],[LocalName],[Extension],[Example],[EnumExpression],[SchemaDefinition]++-%20enums%200..*>[EnumDefinition&#124;enum_uri:uriorcurie%20%3F;code_set:uriorcurie%20%3F;code_set_tag:string%20%3F;code_set_version:string%20%3F;pv_formula:pv_formula_options%20%3F;concepts:uriorcurie%20*;abstract(i):boolean%20%3F;mixin(i):boolean%20%3F;values_from(i):uriorcurie%20*;string_serialization(i):string%20%3F;name(i):string;id_prefixes(i):ncname%20*;id_prefixes_are_closed(i):boolean%20%3F;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;implements(i):uriorcurie%20*;instantiates(i):uriorcurie%20*;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;contributors(i):uriorcurie%20*;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;rank(i):integer%20%3F;categories(i):uriorcurie%20*;keywords(i):string%20*],[EnumExpression]-%20inherits%200..*>[EnumDefinition],[EnumDefinition]uses%20-.->[EnumExpression],[Definition]^-[EnumDefinition],[Definition],[AnonymousEnumExpression],[Annotation],[AltDescription])

## Parents

 *  is_a: [Definition](Definition.md) - abstract base class for core metaclasses

## Uses Mixin

 *  mixin: [EnumExpression](EnumExpression.md) - An expression that constrains the range of a slot

## Referenced by Class

 *  **[SchemaDefinition](SchemaDefinition.md)** *[enums](enums.md)*  <sub>0..\*</sub>  **[EnumDefinition](EnumDefinition.md)**
 *  **[EnumExpression](EnumExpression.md)** *[inherits](inherits.md)*  <sub>0..\*</sub>  **[EnumDefinition](EnumDefinition.md)**

## Attributes


### Own

 * [enum_uri](enum_uri.md)  <sub>0..1</sub>
     * Description: URI of the enum that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Inherited from definition:

 * [name](name.md)  <sub>1..1</sub>
     * Description: the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,OwlProfile,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile)
 * [id_prefixes](id_prefixes.md)  <sub>0..\*</sub>
     * Description: An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [id_prefixes_are_closed](id_prefixes_are_closed.md)  <sub>0..1</sub>
     * Description: If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.
     * Range: [Boolean](types/Boolean.md)
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
 * [instantiates](instantiates.md)  <sub>0..\*</sub>
     * Description: An element in another schema which this element instantiates.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [is_a](is_a.md)  <sub>0..1</sub>
     * Description: A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded
     * Range: [Definition](Definition.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [abstract](abstract.md)  <sub>0..1</sub>
     * Description: Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile)
 * [mixin](mixin.md)  <sub>0..1</sub>
     * Description: Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile)
 * [mixins](mixins.md)  <sub>0..\*</sub>
     * Description: A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.
     * Range: [Definition](Definition.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [apply_to](apply_to.md)  <sub>0..\*</sub>
     * Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * Range: [Definition](Definition.md)
 * [values_from](values_from.md)  <sub>0..\*</sub>
     * Description: The identifier of a "value set" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [string_serialization](string_serialization.md)  <sub>0..1</sub>
     * Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [code_set](code_set.md)  <sub>0..1</sub>
     * Description: the identifier of an enumeration code set.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from enum_expression:

 * [code_set_tag](code_set_tag.md)  <sub>0..1</sub>
     * Description: the version tag of the enumeration code set
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from enum_expression:

 * [code_set_version](code_set_version.md)  <sub>0..1</sub>
     * Description: the version identifier of the enumeration code set
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)

### Mixed in from enum_expression:

 * [pv_formula](pv_formula.md)  <sub>0..1</sub>
     * Description: Defines the specific formula to be used to generate the permissible values.
     * Range: [pv_formula_options](pv_formula_options.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from enum_expression:

 * [permissible_values](permissible_values.md)  <sub>0..\*</sub>
     * Description: A list of possible values for a slot range
     * Range: [PermissibleValue](PermissibleValue.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from enum_expression:

 * [include](include.md)  <sub>0..\*</sub>
     * Description: An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set
     * Range: [AnonymousEnumExpression](AnonymousEnumExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [minus](minus.md)  <sub>0..\*</sub>
     * Description: An enum expression that yields a list of permissible values that are to be subtracted from the enum
     * Range: [AnonymousEnumExpression](AnonymousEnumExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [inherits](inherits.md)  <sub>0..\*</sub>
     * Description: An enum definition that is used as the basis to create a new enum
     * Range: [EnumDefinition](EnumDefinition.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [reachable_from](reachable_from.md)  <sub>0..1</sub>
     * Description: Specifies a query for obtaining a list of permissible values based on graph reachability
     * Range: [ReachabilityQuery](ReachabilityQuery.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [matches](matches.md)  <sub>0..1</sub>
     * Description: Specifies a match query that is used to calculate the list of permissible values
     * Range: [MatchQuery](MatchQuery.md)
     * in subsets: (SpecificationSubset)

### Mixed in from enum_expression:

 * [concepts](concepts.md)  <sub>0..\*</sub>
     * Description: A list of identifiers that are used to construct a set of permissible values
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | enum |
|  | | enumeration |
|  | | semantic enumeration |
|  | | value set |
|  | | term set |
|  | | concept set |
|  | | code set |
|  | | Terminology Value Set |
|  | | answer list |
|  | | value domain |
| **In Subsets:** | | SpecificationSubset |
|  | | BasicSubset |
|  | | RelationalModelProfile |
|  | | ObjectOrientedProfile |
|  | | OwlProfile |
| **Exact Mappings:** | | qb:HierarchicalCodeList |
|  | | NCIT:C113497 |
|  | | cdisc:ValueDomain |
| **Close Mappings:** | | skos:ConceptScheme |

