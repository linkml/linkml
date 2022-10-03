
# meta


**metamodel version:** 1.7.0

**version:** 2.0.0


The metamodel for schemas defined using the Linked Data Modeling Language framework.

For more information on LinkML, see [linkml.io](https://linkml.io)

Core metaclasses:

* [SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)
* [ClassDefinition](https://w3id.org/linkml/ClassDefinition)
* [SlotDefinition](https://w3id.org/linkml/SlotDefinition)

Every LinkML model instantiates SchemaDefinition, all classes in
the model instantiate ClassDefinition, and so on

Note that the LinkML metamodel instantiates itself.

For a non-normative introduction to LinkML schemas, see the tutorial
and schema guide on [linkml.io/linkml].

For canonical reference documentation on any metamodel construct,
refer to the official URI for each construct, e.g.
[https://w3id.org/linkml/is_a](https://w3id.org/linkml/is_a)


### Classes

 * [Element](Element.md) - a named element in the model
     * definition
         * class_definition
         * slot_definition
     * enum_definition
     * schema_definition
     * subset_definition
     * type_definition
 * [Example](Example.md) - usage example and description

### Mixins


### Slots

 * [examples](examples.md) - example usages of an element

### Enums

 * [alias_predicate_enum](alias_predicate_enum.md)
 * [presence_enum](presence_enum.md) - enumeration of conditions by which a slot value should be set
 * [pv_formula_options](pv_formula_options.md) - The formula used to generate the set of permissible values from the code_set values
 * [relational_role_enum](relational_role_enum.md) - enumeration of roles a slot on a relationship class can play

### Subsets

 * [Basic](Basic.md) - An extension of minimal that is a basic subset that can be implemented by a broad variety of tools
 * [Minimal](Minimal.md) - Minimal set of slots for defining a model
 * [ObjectOriented](ObjectOriented.md) - The set of constructs that have an equivalent in a minimal object oriented metamodel
 * [Owl](Owl.md) - Set of slots that appear in the OWL representation of a model
 * [RelationalModel](RelationalModel.md) - The set of constructs that have an equivalent in the classic relational mode as defined by Codd

### Types


#### Built in

 * **Bool**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [String](types/String.md)  (**str**)  - A character string
