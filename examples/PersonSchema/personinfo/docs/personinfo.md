
# personinfo


**metamodel version:** 1.7.0

**version:** None


Information about people, based on [schema.org](http://schema.org)


### Classes

 * [Address](Address.md)
 * [Container](Container.md)
 * [Event](Event.md)
     * [EmploymentEvent](EmploymentEvent.md)
     * [MedicalEvent](MedicalEvent.md)
     * [NewsEvent](NewsEvent.md)
 * [IntegerPrimaryKeyObject](IntegerPrimaryKeyObject.md)
 * [NamedThing](NamedThing.md) - A generic grouping for any identifiable entity
     * [Concept](Concept.md)
         * [DiagnosisConcept](DiagnosisConcept.md)
         * [ProcedureConcept](ProcedureConcept.md)
             * [ImagingProcedureConcept](ImagingProcedureConcept.md)
             * [OperationProcedureConcept](OperationProcedureConcept.md)
     * [Organization](Organization.md) - An organization such as a company or university
     * [Person](Person.md) - A person (alive, dead, undead, or fictional).
 * [Place](Place.md)
 * [Relationship](Relationship.md)
     * [FamilialRelationship](FamilialRelationship.md)
     * [InterPersonalRelationship](InterPersonalRelationship.md)
 * [CodeSystem](CodeSystem.md)

### Mixins

 * [HasAliases](HasAliases.md) - A mixin applied to any class that can have aliases/alternateNames
 * [HasNewsEvents](HasNewsEvents.md)
 * [WithLocation](WithLocation.md)

### Slots

 * [➞age](age_in_years.md)
     * [Person➞age](Person_age_in_years.md)
 * [birth_date](birth_date.md)
 * [categories](categories.md)
     * [Organization➞categories](Organization_categories.md)
 * [city](city.md)
 * [➞code system](concept__code_system.md)
 * [➞mappings](concept__mappings.md)
 * [current_address](current_address.md) - The address at which a person currently lives
 * [depicted_by](depicted_by.md)
 * [description](description.md)
 * [diagnosis](diagnosis.md)
 * [duration](duration.md)
 * [employed_at](employed_at.md)
 * [ended_at_time](ended_at_time.md)
 * [founding location](founding_location.md)
 * [founding_date](founding_date.md)
 * [gender](gender.md)
 * [➞aliases](hasAliases__aliases.md)
 * [➞has_news_events](hasNewsEvents__has_news_events.md)
 * [has_employment_history](has_employment_history.md)
 * [has_familial_relationships](has_familial_relationships.md)
 * [has_interpersonal_relationships](has_interpersonal_relationships.md)
 * [has_medical_history](has_medical_history.md)
 * [id](id.md)
 * [image](image.md)
 * [in_location](in_location.md)
 * [int_id](int_id.md)
 * [is_current](is_current.md)
 * [min_salary](min_salary.md)
 * [mission_statement](mission_statement.md)
 * [name](name.md)
 * [➞headline](newsEvent__headline.md)
 * [organizations](organizations.md)
 * [persons](persons.md)
 * [places](places.md)
 * [postal_code](postal_code.md)
 * [primary_email](primary_email.md)
     * [Person➞primary_email](Person_primary_email.md)
 * [procedure](procedure.md)
 * [related to](related_to.md)
     * [FamilialRelationship➞related to](FamilialRelationship_related_to.md)
     * [InterPersonalRelationship➞related to](InterPersonalRelationship_related_to.md)
 * [related_to](related_to.md)
 * [salary](salary.md)
 * [score](score.md) - A score between 0 and 5, represented as a decimal
 * [started_at_time](started_at_time.md)
 * [street](street.md)
 * [telephone](telephone.md)
     * [Person➞telephone](Person_telephone.md)
 * [type](type.md)
     * [FamilialRelationship➞type](FamilialRelationship_type.md)
     * [InterPersonalRelationship➞type](InterPersonalRelationship_type.md)

### Enums

 * [DiagnosisType](DiagnosisType.md)
 * [FamilialRelationshipType](FamilialRelationshipType.md)
 * [GenderType](GenderType.md)
 * [NonFamilialRelationshipType](NonFamilialRelationshipType.md)
 * [OrganizationType](OrganizationType.md)

### Subsets

 * [BasicSubset](BasicSubset.md) - A subset of the schema that handles basic information

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

 * [CrossReference](types/CrossReference.md)  ([Uriorcurie](types/Uriorcurie.md))  - A string URI or CURIE representation of an external identifier, modeled as a Resource in RDF
 * [ImageURL](types/ImageURL.md)  ([Uri](types/Uri.md))
 * [SalaryType](types/SalaryType.md)  ([Decimal](types/Decimal.md))
 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Curie](types/Curie.md)  (**Curie**)  - a compact URI
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [DateOrDatetime](types/DateOrDatetime.md)  (**str**)  - Either a date or a datetime
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Jsonpath](types/Jsonpath.md)  (**str**)  - A string encoding a JSON Path. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded in tree form.
 * [Jsonpointer](types/Jsonpointer.md)  (**str**)  - A string encoding a JSON Pointer. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to a valid object within the current instance document when encoded in tree form.
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [Sparqlpath](types/Sparqlpath.md)  (**str**)  - A string encoding a SPARQL Property Path. The value of the string MUST conform to SPARQL syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded as RDF.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
