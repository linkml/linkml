
# Class: slot_definition


an element that describes how instances are related to other instances

URI: [linkml:SlotDefinition](https://w3id.org/linkml/SlotDefinition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[UniqueKey],[SubsetDefinition],[StructuredAlias],[SlotExpression],[SlotDefinition]<apply_to%200..*-%20[SlotDefinition&#124;singular_name:string%20%3F;slot_uri:uriorcurie%20%3F;multivalued:boolean%20%3F;inherited:boolean%20%3F;readonly:string%20%3F;ifabsent:string%20%3F;list_elements_unique:boolean%20%3F;list_elements_ordered:boolean%20%3F;shared:boolean%20%3F;key:boolean%20%3F;identifier:boolean%20%3F;designates_type:boolean%20%3F;alias:string%20%3F;symmetric:boolean%20%3F;reflexive:boolean%20%3F;locally_reflexive:boolean%20%3F;irreflexive:boolean%20%3F;asymmetric:boolean%20%3F;transitive:boolean%20%3F;is_class_field:boolean%20%3F;role:string%20%3F;is_usage_slot:boolean%20%3F;usage_slot_name:string%20%3F;relational_role:relational_role_enum%20%3F;is_grouping_slot:boolean%20%3F;children_are_mutually_disjoint:boolean%20%3F;required:boolean%20%3F;recommended:boolean%20%3F;inlined:boolean%20%3F;inlined_as_list:boolean%20%3F;pattern:string%20%3F;implicit_prefix:string%20%3F;value_presence:presence_enum%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;equals_expression:string%20%3F;exact_cardinality:integer%20%3F;minimum_cardinality:integer%20%3F;maximum_cardinality:integer%20%3F;abstract(i):boolean%20%3F;mixin(i):boolean%20%3F;values_from(i):uriorcurie%20*;string_serialization(i):string%20%3F;name(i):string;id_prefixes(i):ncname%20*;id_prefixes_are_closed(i):boolean%20%3F;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;implements(i):uriorcurie%20*;instantiates(i):uriorcurie%20*;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;contributors(i):uriorcurie%20*;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;rank(i):integer%20%3F;categories(i):uriorcurie%20*;keywords(i):string%20*],[SlotDefinition]<mixins%200..*-%20[SlotDefinition],[SlotDefinition]<is_a%200..1-%20[SlotDefinition],[SlotDefinition]<union_of%200..*-%20[SlotDefinition],[SlotDefinition]<disjoint_with%200..*-%20[SlotDefinition],[PathExpression]<path_rule%200..1-++[SlotDefinition],[SlotDefinition]<slot_group%200..1-%20[SlotDefinition],[SlotDefinition]<reflexive_transitive_form_of%200..1-%20[SlotDefinition],[SlotDefinition]<transitive_form_of%200..1-%20[SlotDefinition],[SlotDefinition]<inverse%200..1-%20[SlotDefinition],[SlotDefinition]<subproperty_of%200..1-%20[SlotDefinition],[ClassDefinition]<domain_of%200..*-%20[SlotDefinition],[Definition]<owner%200..1-%20[SlotDefinition],[ArrayExpression]<array%200..1-++[SlotDefinition],[ClassDefinition]<domain%200..1-%20[SlotDefinition],[ClassDefinition]++-%20attributes%200..*>[SlotDefinition],[ClassDefinition]-%20defining_slots%200..*>[SlotDefinition],[ClassExpression]++-%20slot_conditions%200..*>[SlotDefinition],[SchemaDefinition]++-%20slots%200..*>[SlotDefinition],[ClassDefinition]++-%20slot_usage%200..*>[SlotDefinition],[ClassDefinition]-%20slots%200..*>[SlotDefinition],[PathExpression]-%20traverse%200..1>[SlotDefinition],[UniqueKey]-%20unique_key_slots%201..*>[SlotDefinition],[SlotDefinition]uses%20-.->[SlotExpression],[Definition]^-[SlotDefinition],[SchemaDefinition],[PatternExpression],[PathExpression],[LocalName],[Extension],[Example],[EnumExpression],[Element],[Definition],[ClassExpression],[ClassDefinition],[ArrayExpression],[AnonymousSlotExpression],[AnonymousClassExpression],[Annotation],[AltDescription],[UnitOfMeasure],[Anything])](https://yuml.me/diagram/nofunky;dir:TB/class/[UniqueKey],[SubsetDefinition],[StructuredAlias],[SlotExpression],[SlotDefinition]<apply_to%200..*-%20[SlotDefinition&#124;singular_name:string%20%3F;slot_uri:uriorcurie%20%3F;multivalued:boolean%20%3F;inherited:boolean%20%3F;readonly:string%20%3F;ifabsent:string%20%3F;list_elements_unique:boolean%20%3F;list_elements_ordered:boolean%20%3F;shared:boolean%20%3F;key:boolean%20%3F;identifier:boolean%20%3F;designates_type:boolean%20%3F;alias:string%20%3F;symmetric:boolean%20%3F;reflexive:boolean%20%3F;locally_reflexive:boolean%20%3F;irreflexive:boolean%20%3F;asymmetric:boolean%20%3F;transitive:boolean%20%3F;is_class_field:boolean%20%3F;role:string%20%3F;is_usage_slot:boolean%20%3F;usage_slot_name:string%20%3F;relational_role:relational_role_enum%20%3F;is_grouping_slot:boolean%20%3F;children_are_mutually_disjoint:boolean%20%3F;required:boolean%20%3F;recommended:boolean%20%3F;inlined:boolean%20%3F;inlined_as_list:boolean%20%3F;pattern:string%20%3F;implicit_prefix:string%20%3F;value_presence:presence_enum%20%3F;equals_string:string%20%3F;equals_string_in:string%20*;equals_number:integer%20%3F;equals_expression:string%20%3F;exact_cardinality:integer%20%3F;minimum_cardinality:integer%20%3F;maximum_cardinality:integer%20%3F;abstract(i):boolean%20%3F;mixin(i):boolean%20%3F;values_from(i):uriorcurie%20*;string_serialization(i):string%20%3F;name(i):string;id_prefixes(i):ncname%20*;id_prefixes_are_closed(i):boolean%20%3F;definition_uri(i):uriorcurie%20%3F;conforms_to(i):string%20%3F;implements(i):uriorcurie%20*;instantiates(i):uriorcurie%20*;description(i):string%20%3F;title(i):string%20%3F;deprecated(i):string%20%3F;todos(i):string%20*;notes(i):string%20*;comments(i):string%20*;from_schema(i):uri%20%3F;imported_from(i):string%20%3F;source(i):uriorcurie%20%3F;in_language(i):string%20%3F;see_also(i):uriorcurie%20*;deprecated_element_has_exact_replacement(i):uriorcurie%20%3F;deprecated_element_has_possible_replacement(i):uriorcurie%20%3F;aliases(i):string%20*;mappings(i):uriorcurie%20*;exact_mappings(i):uriorcurie%20*;close_mappings(i):uriorcurie%20*;related_mappings(i):uriorcurie%20*;narrow_mappings(i):uriorcurie%20*;broad_mappings(i):uriorcurie%20*;created_by(i):uriorcurie%20%3F;contributors(i):uriorcurie%20*;created_on(i):datetime%20%3F;last_updated_on(i):datetime%20%3F;modified_by(i):uriorcurie%20%3F;status(i):uriorcurie%20%3F;rank(i):integer%20%3F;categories(i):uriorcurie%20*;keywords(i):string%20*],[SlotDefinition]<mixins%200..*-%20[SlotDefinition],[SlotDefinition]<is_a%200..1-%20[SlotDefinition],[SlotDefinition]<union_of%200..*-%20[SlotDefinition],[SlotDefinition]<disjoint_with%200..*-%20[SlotDefinition],[PathExpression]<path_rule%200..1-++[SlotDefinition],[SlotDefinition]<slot_group%200..1-%20[SlotDefinition],[SlotDefinition]<reflexive_transitive_form_of%200..1-%20[SlotDefinition],[SlotDefinition]<transitive_form_of%200..1-%20[SlotDefinition],[SlotDefinition]<inverse%200..1-%20[SlotDefinition],[SlotDefinition]<subproperty_of%200..1-%20[SlotDefinition],[ClassDefinition]<domain_of%200..*-%20[SlotDefinition],[Definition]<owner%200..1-%20[SlotDefinition],[ArrayExpression]<array%200..1-++[SlotDefinition],[ClassDefinition]<domain%200..1-%20[SlotDefinition],[ClassDefinition]++-%20attributes%200..*>[SlotDefinition],[ClassDefinition]-%20defining_slots%200..*>[SlotDefinition],[ClassExpression]++-%20slot_conditions%200..*>[SlotDefinition],[SchemaDefinition]++-%20slots%200..*>[SlotDefinition],[ClassDefinition]++-%20slot_usage%200..*>[SlotDefinition],[ClassDefinition]-%20slots%200..*>[SlotDefinition],[PathExpression]-%20traverse%200..1>[SlotDefinition],[UniqueKey]-%20unique_key_slots%201..*>[SlotDefinition],[SlotDefinition]uses%20-.->[SlotExpression],[Definition]^-[SlotDefinition],[SchemaDefinition],[PatternExpression],[PathExpression],[LocalName],[Extension],[Example],[EnumExpression],[Element],[Definition],[ClassExpression],[ClassDefinition],[ArrayExpression],[AnonymousSlotExpression],[AnonymousClassExpression],[Annotation],[AltDescription],[UnitOfMeasure],[Anything])

## Parents

 *  is_a: [Definition](Definition.md) - abstract base class for core metaclasses

## Uses Mixin

 *  mixin: [SlotExpression](SlotExpression.md) - an expression that constrains the range of values a slot can take

## Referenced by Class

 *  **[ClassDefinition](ClassDefinition.md)** *[attributes](attributes.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[defining_slots](defining_slots.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[inverse](inverse.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **None** *[reflexive_transitive_form_of](reflexive_transitive_form_of.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassExpression](ClassExpression.md)** *[slot_conditions](slot_conditions.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞apply_to](slot_definition_apply_to.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞disjoint_with](slot_definition_disjoint_with.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞is_a](slot_definition_is_a.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞mixins](slot_definition_mixins.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_definition➞union_of](slot_definition_union_of.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[schema_definition➞slots](slot_definitions.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[slot_group](slot_group.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[slot_usage](slot_usage.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[ClassDefinition](ClassDefinition.md)** *[slots](slots.md)*  <sub>0..\*</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[SlotDefinition](SlotDefinition.md)** *[subproperty_of](subproperty_of.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **None** *[transitive_form_of](transitive_form_of.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **None** *[traverse](traverse.md)*  <sub>0..1</sub>  **[SlotDefinition](SlotDefinition.md)**
 *  **[UniqueKey](UniqueKey.md)** *[unique_key_slots](unique_key_slots.md)*  <sub>1..\*</sub>  **[SlotDefinition](SlotDefinition.md)**

## Attributes


### Own

 * [singular_name](singular_name.md)  <sub>0..1</sub>
     * Description: a name that is used in the singular form
     * Range: [String](types/String.md)
     * in subsets: (BasicSubset)
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
     * in subsets: (SpecificationSubset)
 * [slot_uri](slot_uri.md)  <sub>0..1</sub>
     * Description: URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [multivalued](multivalued.md)  <sub>0..1</sub>
     * Description: true means that slot can have more than one value and should be represented using a list or collection structure.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,ObjectOrientedProfile)
 * [array](array.md)  <sub>0..1</sub>
     * Description: coerces the value of the slot into an array and defines the dimensions of that array
     * Range: [ArrayExpression](ArrayExpression.md)
 * [inherited](inherited.md)  <sub>0..1</sub>
     * Description: true means that the *value* of a slot is inherited by subclasses
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [readonly](readonly.md)  <sub>0..1</sub>
     * Description: If present, slot is read only.  Text explains why
     * Range: [String](types/String.md)
 * [ifabsent](ifabsent.md)  <sub>0..1</sub>
     * Description: function that provides a default value for the slot.  Possible values for this slot are defined in linkml.utils.ifabsent_functions.default_library:
  * [Tt]rue -- boolean True
  * [Ff]alse -- boolean False
  * bnode -- blank node identifier
  * class_curie -- CURIE for the containing class
  * class_uri -- URI for the containing class
  * default_ns -- schema default namespace
  * default_range -- schema default range
  * int(value) -- integer value
  * slot_uri -- URI for the slot
  * slot_curie -- CURIE for the slot
  * string(value) -- string value
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)
 * [list_elements_unique](list_elements_unique.md)  <sub>0..1</sub>
     * Description: If True, then there must be no duplicates in the elements of a multivalued slot
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [list_elements_ordered](list_elements_ordered.md)  <sub>0..1</sub>
     * Description: If True, then the order of elements of a multivalued slot is guaranteed to be preserved. If False, the order may still be preserved but this is not guaranteed
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [shared](shared.md)  <sub>0..1</sub>
     * Description: If True, then the relationship between the slot domain and range is many to one or many to many
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [key](key.md)  <sub>0..1</sub>
     * Description: True means that the key slot(s) uniquely identify the elements within a single container
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset,RelationalModelProfile)
 * [identifier](identifier.md)  <sub>0..1</sub>
     * Description: True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,RelationalModelProfile)
 * [designates_type](designates_type.md)  <sub>0..1</sub>
     * Description: True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [alias](alias.md)  <sub>0..1</sub>
     * Description: the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)
 * [owner](owner.md)  <sub>0..1</sub>
     * Description: the "owner" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot
     * Range: [Definition](Definition.md)
 * [domain_of](domain_of.md)  <sub>0..\*</sub>
     * Description: the class(es) that reference the slot in a "slots" or "slot_usage" context
     * Range: [ClassDefinition](ClassDefinition.md)
 * [subproperty_of](subproperty_of.md)  <sub>0..1</sub>
     * Description: Ontology property which this slot is a subproperty of.  Note: setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.
     * Range: [SlotDefinition](SlotDefinition.md)
     * Example: RO:HOM0000001 this is the RO term for "in homology relationship with", and used as a value of subproperty of this means that any ontological child (related to RO:HOM0000001 via an is_a relationship), is a valid value for the slot that declares this with the subproperty_of tag.  This differs from the 'values_from' meta model component in that 'values_from' requires the id of a value set (said another way, if an entire ontology had a curie/identifier that was the identifier for the entire ontology, then that identifier would be used in 'values_from.')
 * [symmetric](symmetric.md)  <sub>0..1</sub>
     * Description: If s is symmetric, and i.s=v, then v.s=i
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [reflexive](reflexive.md)  <sub>0..1</sub>
     * Description: If s is reflexive, then i.s=i for all instances i
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [locally_reflexive](locally_reflexive.md)  <sub>0..1</sub>
     * Description: If s is locally_reflexive, then i.s=i for all instances i where s is a class slot for the type of i
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [irreflexive](irreflexive.md)  <sub>0..1</sub>
     * Description: If s is irreflexive, then there exists no i such i.s=i
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [asymmetric](asymmetric.md)  <sub>0..1</sub>
     * Description: If s is antisymmetric, and i.s=v where i is different from v, v.s cannot have value i
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [transitive](transitive.md)  <sub>0..1</sub>
     * Description: If s is transitive, and i.s=z, and s.s=j, then i.s=j
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset)
 * [inverse](inverse.md)  <sub>0..1</sub>
     * Description: indicates that any instance of d s r implies that there is also an instance of r s' d
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset)
 * [is_class_field](is_class_field.md)  <sub>0..1</sub>
     * Description: indicates that for any instance, i, the domain of this slot will include an assertion of i s range
     * Range: [Boolean](types/Boolean.md)
 * [transitive_form_of](transitive_form_of.md)  <sub>0..1</sub>
     * Description: If s transitive_form_of d, then (1) s holds whenever d holds (2) s is transitive (3) d holds whenever s holds and there are no intermediates, and s is not reflexive
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset)
 * [reflexive_transitive_form_of](reflexive_transitive_form_of.md)  <sub>0..1</sub>
     * Description: transitive_form_of including the reflexive case
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset)
 * [role](role.md)  <sub>0..1</sub>
     * Description: a textual descriptor that indicates the role played by the slot range
     * Range: [String](types/String.md)
 * [is_usage_slot](is_usage_slot.md)  <sub>0..1</sub>
     * Description: True means that this slot was defined in a slot_usage situation
     * Range: [Boolean](types/Boolean.md)
 * [usage_slot_name](usage_slot_name.md)  <sub>0..1</sub>
     * Description: The name of the slot referenced in the slot_usage
     * Range: [String](types/String.md)
 * [relational_role](relational_role.md)  <sub>0..1</sub>
     * Description: the role a slot on a relationship class plays, for example, the subject, object or predicate roles
     * Range: [relational_role_enum](relational_role_enum.md)
 * [slot_group](slot_group.md)  <sub>0..1</sub>
     * Description: allows for grouping of related slots into a grouping slot that serves the role of a group
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [is_grouping_slot](is_grouping_slot.md)  <sub>0..1</sub>
     * Description: true if this slot is a grouping slot
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset)
 * [path_rule](path_rule.md)  <sub>0..1</sub>
     * Description: a rule for inferring a slot assignment based on evaluating a path through a sequence of slot assignments
     * Range: [PathExpression](PathExpression.md)
 * [slot_definition➞disjoint_with](slot_definition_disjoint_with.md)  <sub>0..\*</sub>
     * Description: Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset)
 * [children_are_mutually_disjoint](children_are_mutually_disjoint.md)  <sub>0..1</sub>
     * Description: If true then all direct is_a children are mutually disjoint and share no instances in common
     * Range: [Boolean](types/Boolean.md)
 * [slot_definition➞union_of](slot_definition_union_of.md)  <sub>0..\*</sub>
     * Description: indicates that the domain element consists exactly of the members of the element in the range.
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset,OwlProfile)
 * [slot_definition➞is_a](slot_definition_is_a.md)  <sub>0..1</sub>
     * Description: A primary parent slot from which inheritable metaslots are propagated
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [slot_definition➞mixins](slot_definition_mixins.md)  <sub>0..\*</sub>
     * Description: A collection of secondary parent mixin slots from which inheritable metaslots are propagated
     * Range: [SlotDefinition](SlotDefinition.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile,OwlProfile)
 * [slot_definition➞apply_to](slot_definition_apply_to.md)  <sub>0..\*</sub>
     * Description: Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.
     * Range: [SlotDefinition](SlotDefinition.md)

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
 * [abstract](abstract.md)  <sub>0..1</sub>
     * Description: Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile)
 * [mixin](mixin.md)  <sub>0..1</sub>
     * Description: Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset,ObjectOrientedProfile)
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

### Mixed in from slot_expression:

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
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile)

### Mixed in from slot_expression:

 * [range_expression](range_expression.md)  <sub>0..1</sub>
     * Description: A range that is described as a boolean expression combining existing ranges
     * Range: [AnonymousClassExpression](AnonymousClassExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [enum_range](enum_range.md)  <sub>0..1</sub>
     * Description: An inlined enumeration
     * Range: [EnumExpression](EnumExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [required](required.md)  <sub>0..1</sub>
     * Description: true means that the slot must be present in instances of the class definition
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,MinimalSubset,BasicSubset,RelationalModelProfile,ObjectOrientedProfile)

### Mixed in from slot_expression:

 * [recommended](recommended.md)  <sub>0..1</sub>
     * Description: true means that the slot should be present in instances of the class definition, but this is not required
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from slot_expression:

 * [inlined](inlined.md)  <sub>0..1</sub>
     * Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from slot_expression:

 * [inlined_as_list](inlined_as_list.md)  <sub>0..1</sub>
     * Description: True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.
     * Range: [Boolean](types/Boolean.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from slot_expression:

 * [minimum_value](minimum_value.md)  <sub>0..1</sub>
     * Description: For ordinal ranges, the value must be equal to or higher than this
     * Range: [Anything](Anything.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from slot_expression:

 * [maximum_value](maximum_value.md)  <sub>0..1</sub>
     * Description: For ordinal ranges, the value must be equal to or lower than this
     * Range: [Anything](Anything.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from slot_expression:

 * [pattern](pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to this regular expression expressed in the string
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset,BasicSubset)

### Mixed in from slot_expression:

 * [structured_pattern](structured_pattern.md)  <sub>0..1</sub>
     * Description: the string value of the slot must conform to the regular expression in the pattern expression
     * Range: [PatternExpression](PatternExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [unit](unit.md)  <sub>0..1</sub>
     * Description: an encoding of a unit
     * Range: [UnitOfMeasure](UnitOfMeasure.md)

### Mixed in from slot_expression:

 * [implicit_prefix](implicit_prefix.md)  <sub>0..1</sub>
     * Description: Causes the slot value to be interpreted as a uriorcurie after prefixing with this string
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [value_presence](value_presence.md)  <sub>0..1</sub>
     * Description: if true then a value must be present (for lists there must be at least one value). If false then a value must be absent (for lists, must be empty)
     * Range: [presence_enum](presence_enum.md)

### Mixed in from slot_expression:

 * [equals_string](equals_string.md)  <sub>0..1</sub>
     * Description: the slot must have range string and the value of the slot must equal the specified value
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [equals_string_in](equals_string_in.md)  <sub>0..\*</sub>
     * Description: the slot must have range string and the value of the slot must equal one of the specified values
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [equals_number](equals_number.md)  <sub>0..1</sub>
     * Description: the slot must have range of a number and the value of the slot must equal the specified value
     * Range: [Integer](types/Integer.md)

### Mixed in from slot_expression:

 * [equals_expression](equals_expression.md)  <sub>0..1</sub>
     * Description: the value of the slot must equal the value of the evaluated expression
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [exact_cardinality](exact_cardinality.md)  <sub>0..1</sub>
     * Description: the exact number of entries for a multivalued slot
     * Range: [Integer](types/Integer.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [minimum_cardinality](minimum_cardinality.md)  <sub>0..1</sub>
     * Description: the minimum number of entries for a multivalued slot
     * Range: [Integer](types/Integer.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [maximum_cardinality](maximum_cardinality.md)  <sub>0..1</sub>
     * Description: the maximum number of entries for a multivalued slot
     * Range: [Integer](types/Integer.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [has_member](has_member.md)  <sub>0..1</sub>
     * Description: the value of the slot is multivalued with at least one member satisfying the condition
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [all_members](all_members.md)  <sub>0..1</sub>
     * Description: the value of the slot is multivalued with all members satisfying the condition
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [slot_expression➞none_of](slot_expression_none_of.md)  <sub>0..\*</sub>
     * Description: holds if none of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [slot_expression➞exactly_one_of](slot_expression_exactly_one_of.md)  <sub>0..\*</sub>
     * Description: holds if only one of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [slot_expression➞any_of](slot_expression_any_of.md)  <sub>0..\*</sub>
     * Description: holds if at least one of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)

### Mixed in from slot_expression:

 * [slot_expression➞all_of](slot_expression_all_of.md)  <sub>0..\*</sub>
     * Description: holds if all of the expressions hold
     * Range: [AnonymousSlotExpression](AnonymousSlotExpression.md)
     * in subsets: (SpecificationSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | slot |
|  | | field |
|  | | property |
|  | | attribute |
|  | | column |
|  | | variable |
| **In Subsets:** | | SpecificationSubset |
|  | | MinimalSubset |
|  | | BasicSubset |
|  | | OwlProfile |
| **Close Mappings:** | | rdf:Property |
|  | | qb:ComponentProperty |

