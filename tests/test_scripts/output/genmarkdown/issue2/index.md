
# meta


**metamodel version:** 1.7.0

**version:** 2.0.0


The metamodel for schemas defined using the Linked Data Modeling Language framework.

For more information on LinkML:

* [linkml.io](https://linkml.io) main website
* [specification](https://w3id.org/linkml/docs/specification/)

LinkML is self-describing. Every LinkML schema consists of elements
that instantiate classes in this metamodel.

Core metaclasses:

* [SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)
* [ClassDefinition](https://w3id.org/linkml/ClassDefinition)
* [SlotDefinition](https://w3id.org/linkml/SlotDefinition)
* [TypeDefinition](https://w3id.org/linkml/TypeDefinition)

There are many subsets of *profiles* of the metamodel, for different purposes:

* [MinimalSubset](https://w3id.org/linkml/MinimalSubset)
* [BasicSubset](https://w3id.org/linkml/BasicSubset)
* [BasicSubset](https://w3id.org/linkml/BasicSubset)

For canonical reference documentation on any metamodel construct,
refer to the official URI for each construct, e.g.
[https://w3id.org/linkml/is_a](https://w3id.org/linkml/is_a)


### Classes

 * [Anything](Anything.md)
 * [Element](Element.md) - A named element in the model
     * definition
         * class_definition
         * enum_definition
         * slot_definition
     * schema_definition
     * subset_definition
     * type_definition
 * [Example](Example.md) - usage example and description

### Mixins


### Slots

 * [examples](examples.md) - example usages of an element

### Enums

 * [alias_predicate_enum](alias_predicate_enum.md) - permissible values for the relationship between an element and an alias
 * [presence_enum](presence_enum.md) - enumeration of conditions by which a slot value should be set
 * [pv_formula_options](pv_formula_options.md) - The formula used to generate the set of permissible values from the code_set values
 * [relational_role_enum](relational_role_enum.md) - enumeration of roles a slot on a relationship class can play

### Subsets

 * [BasicSubset](BasicSubset.md) - An extension of MinimalSubset that avoids advanced constructs and can be implemented by a broad variety of tools.
 * [MinimalSubset](MinimalSubset.md) - The absolute minimal set of elements necessary for defining any schema.
 * [ObjectOrientedProfile](ObjectOrientedProfile.md) - A profile that includes all the metamodel elements whose semantics can be expressed using a minimal
 * [OwlProfile](OwlProfile.md) - A profile that includes all the metamodel elements whose semantics can be expressed in OWL
 * [RelationalModelProfile](RelationalModelProfile.md) - A profile that includes all the metamodel elements whose semantics can be expressed using the classic Relational Model.
 * [SpecificationSubset](SpecificationSubset.md) - A subset that includes all the metamodel elements that form part of the normative LinkML specification.

### Types


#### Built in

 * **Bool**
 * **Curie**
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
