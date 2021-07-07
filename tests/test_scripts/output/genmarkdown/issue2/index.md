
# meta schema


A metamodel for defining linked open data schemas


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

 * [pv_formula_options](pv_formula_options.md) - The formula used to generate the set of permissible values from the code_set values

### Subsets

 * [Owl](Owl.md) - Set of slots that appear in the OWL representation of a model

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
