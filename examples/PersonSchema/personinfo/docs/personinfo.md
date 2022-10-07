
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
 * [NamedThing](NamedThing.md) - A generic grouping for any identifiable entity
     * [Concept](Concept.md)
         * [DiagnosisConcept](DiagnosisConcept.md)
         * [ProcedureConcept](ProcedureConcept.md)
     * [Organization](Organization.md) - An organization such as a company or university
     * [Person](Person.md) - A person (alive, dead, undead, or fictional).
 * [Place](Place.md)
 * [Relationship](Relationship.md)
     * [FamilialRelationship](FamilialRelationship.md)

### Mixins

 * [HasAliases](HasAliases.md) - A mixin applied to any class that can have aliases/alternateNames
 * [WithLocation](WithLocation.md)

### Slots

 * [age_in_years](age_in_years.md)
 * [birth_date](birth_date.md)
 * [city](city.md)
 * [current_address](current_address.md) - The address at which a person currently lives
 * [description](description.md)
 * [diagnosis](diagnosis.md)
 * [duration](duration.md)
 * [employed_at](employed_at.md)
 * [ended_at_time](ended_at_time.md)
 * [founding_date](founding_date.md)
 * [founding_location](founding_location.md)
 * [gender](gender.md)
 * [➞aliases](hasAliases__aliases.md)
 * [has_employment_history](has_employment_history.md)
 * [has_familial_relationships](has_familial_relationships.md)
 * [has_medical_history](has_medical_history.md)
 * [id](id.md)
 * [image](image.md)
 * [in_location](in_location.md)
 * [is_current](is_current.md)
 * [mission_statement](mission_statement.md)
 * [name](name.md)
 * [organizations](organizations.md)
 * [persons](persons.md)
 * [postal_code](postal_code.md)
 * [primary_email](primary_email.md)
     * [Person➞primary_email](Person_primary_email.md)
 * [procedure](procedure.md)
 * [related to](related_to.md)
     * [FamilialRelationship➞related to](FamilialRelationship_related_to.md)
 * [related_to](related_to.md)
 * [started_at_time](started_at_time.md)
 * [street](street.md)
 * [type](type.md)
     * [FamilialRelationship➞type](FamilialRelationship_type.md)

### Enums

 * [DiagnosisType](DiagnosisType.md)
 * [FamilialRelationshipType](FamilialRelationshipType.md)
 * [GenderType](GenderType.md)

### Subsets

 * [BasicSubset](BasicSubset.md) - A subset of the schema that handles basic information

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
 * [DateOrDatetime](types/DateOrDatetime.md)  (**str**)  - Either a date or a datetime
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
