
# mappings schema


LinkML model for mappings


### Classes


### Mixins


### Slots

 * [deprecated element has exact replacement](deprecated_element_has_exact_replacement.md) - When an element is deprecated, it can be automatically replaced by this uri or curie
 * [deprecated element has possible replacement](deprecated_element_has_possible_replacement.md) - When an element is deprecated, it can be potentially replaced by this uri or curie
 * [mappings](mappings.md) - A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.
     * [broad mappings](broad_mappings.md) - A list of terms from different schemas or terminology systems that have broader meaning.
     * [close mappings](close_mappings.md) - A list of terms from different schemas or terminology systems that have close meaning.
     * [exact mappings](exact_mappings.md) - A list of terms from different schemas or terminology systems that have identical meaning.
     * [narrow mappings](narrow_mappings.md) - A list of terms from different schemas or terminology systems that have narrower meaning.
     * [related mappings](related_mappings.md) - A list of terms from different schemas or terminology systems that have related meaning.

### Enums


### Subsets


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

 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
