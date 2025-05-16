# FAQ: Modeling

## How do I get started defining a data model?

The [tutorial](https://linkml.io/linkml/intro/tutorial) walks you through some basic data models.

After that the section on [schemas](https://linkml.io/linkml/schemas/) guides you through some of the core features of the modeling framework.

## What is the difference between is_a and mixins?

LinkML allows any class to have:

 - zero or one *is_a* parents, declared using the [is_a](https://w3id.org/linkml/is_a) slot
 - any number of *mixin* parents, declared using the [mixins](https://w3id.org/linkml/mixins) slot

Semantically these are the same - all inheritable slots are inherited through is_a and mixins.

Classes *should* have a single inheritance backbone, with `is_a`
representing the "main" parent. Generally the mixin and is_a
hierarchies should be stratified.

See these wikipedia pages for more information.

 - [mixins](https://en.wikipedia.org/wiki/Mixin)
 - [traits](https://en.wikipedia.org/wiki/Trait_(computer_programming))

## Didn't you know composition is favored over inheritance these days?

For background, see the Wikipedia article on [composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)

We have certainly seen cases where inheritance is abused in programming languages, especially when it comes to behavioral classes.

However, in our experience inheritance is still very useful when used for data classes. We trust the users of LinkML to create and design schemas carefully.  But you can avoid it altogether if you like, and use composition entirely!

## When should I use attributes vs slots?

The [attributes](https://w3id.org/linkml/attributes) metamodel slot is really just a convenient shorthand for being able to declare slots "inline".

LinkML treats slots as first class entities. They are defined in their own section of a schema, and can be reused by any number of classes (and refined, using slot_usage). This can be very powerful for reuse.

However, this can also be slightly inconvenient for simple schemas, especially those where we have classes with slots that are completely "owned" by that class. The attribute slot can be used to avoid having to specify the slot separately

## What are induced slots?

Because the same slot can be reused in different classes (with each class potentially refining semantics using [slot_usage](https://w3id.org/linkml/slot_usage)),
it can be useful to give a new "name" for the implicit class-specific version of that slot.

For example, if you have a slot `name`, and this is used in classes `Person` and `Organization`, and these are refined for each class (for example, "Organization" may refine the name slot to follow a particular regular expression). In some generators such as the markdown generator, you will see "induced" slots such as `Organization_name`.

The extent to which these are made visible is currently the subject of some discussion, see GitHub for details.

Induced slots can be *materialized* as attributes using the [linkml generator](../generators/linkml)

See:

- [derived models](../schemas/derived-models)

## Why would I need to define my own types?

Types are scalar values such as integers or strings. They are also known as "literals" in RDF.

Strictly speaking it is not necessary to define your own types, you can just use the builtin types (string, integer, etc).

However, defining your own types can be good practice, as it can make
your intent clearer. For example, if you have a slot `description` you
may want to specify the range as your own type `NarrativeText` that
maps to string behind the scenes. But this provides additional cues,
e.g. that the value of this field is intended to be human-readable
text.

An example of a type section might be:

```yaml
types:
  CountType:
    uri: xsd:integer
    base: int
    minimum_value: 0
    description: An integer that specifies cardinality
  SymbolType:
    uri: xsd:string
    base: str
    pattern: "^\\w+$"
    description: A symbol is a string used as a shorthand identifier that is restricted to a subset of characters
```

Some applications may choose to interpret this in particular ways. E.g. you may want to define all narrative text fields as being amenable to spellchecking, or machine learning natural language processing, or special kinds of indexing in ElasticSearch/Solr

## Why would I want to use enums over strings?

Enums provide a more controlled vocabulary than strings. You can validate categorical fields using enums, whereas with basic strings you don't have a built in way of validating if a string is valid.

Enums also give you hooks into ontologies and vocabularies.

More on enums:

<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vQyQsRIBjSxhaDie5ASDAOTfJO9JqFjYmdoBHgCVVKMHzKo0AyL04lGNqWdgbCnyV8a-syk1U81tRXg/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>

## How do I constrain the value of a slot based on an entry in a different slot?

You may want to make the entries in one slot contingent on a different slot. If, for example, you are developing a schema for a toy store that sells wooden horses and frogs. The horses are available in red and green, but the frogs are available in blue and pink.

You can use a [rules block](https://linkml.io/linkml/schemas/advanced.html#rules) to constrain the permissible values for a particular slot dependent on the entry in another slot. 

```yaml
classes:
  Toys:
    attributes:
      species:
        range: SpeciesRng
      colour:
    rules:
      - preconditions:
          slot_conditions:
            species:
              equals_string: horse
        postconditions:
          slot_conditions:
            colour:
              any_of:
                - range: RedGreen
      - preconditions:
          slot_conditions:
            species:
              equals_string: frog
        postconditions:
          slot_conditions:
            colour:
              any_of:
                - range: BluePink

enums:
  SpeciesRng:
    permissible_values: 
      horse:
      frog:
  BluePink:
    permissible_values:
      blue:
      pink:
  RedGreen:
    permissible_values:
      red:
      green:
```

## How do I constrain the value of a slot using an ontology or vocabulary?

There are a variety of ways of tackling this in LinkML.

The fundamental question is whether you want to either:

1. define a fixed set of terms in the schema in advance
2. specify the set of terms via a query (e.g. a particular ontology branch)

See the two questions below for answers to each

### How do I constrain a slot to a fixed set of ontology terms?

You can do this using an [enum](https://w3id.org/linkml/enum).

For example, if we wanted to model a DNA sequence variant type as being a fixed set of terms from SO:

```yaml
prefixes:
  SO: http://purl.obolibrary.org/obo/SO_

classes:
  variant:
    slots:
       - ...
       - variant type
        
slots:
  variant type:
    range: variant_type_enum
  ...:

enums:
  variant_type_enum:
    permissible_values: 
      point_mutation:
          meaning: SO:1000008
      deletion:
          meaning: SO:0000159
      insertion: 
          meaning: SO:0000667
```

Note that we are mapping each permissible value to an ontology term.
Mapping to ontology/vocabulary terms is optional, but if you can do it,
we strongly recommend it. It provides *interoperation hooks* - others with different
data models may have their own enumerations, by making the meaning of each permissible
value explicit, data can be merged automatically.

### How do I constrain a slot to a branch of an ontology or a whole ontology?

LinkML basic enums allow you to restrict a value to a fixed set of terms. This works well, if

1. the vocabulary is known in advance
2. it is a relatively small number of terms

However, this does not work so well if you want to constrain something
to a very large vocabulary - for example, any job code from an
occupation ontology, any body part from an anatomical ontology.


In this case, you can use *dynamic enums*:

```yaml
slots:
  cell_type:
    range: CellTypeEnum

enums:
  CellTypeEnum:
    reachable_from:
      source_ontology: obo:cl
      source_nodes:
        - CL:0000000
      include_self: false
      relationship_types:
        - rdfs:subClassOf
```

This restricts to any subclass (transitive, non-self) of the term [cell](http://purl.obolibrary.org/obo/CL_0000000) in the cell ontology.


An alternative pattern is to use a regular expression:

```yaml
types:
  CellTypeId:
    typeof: uriorcurie
    pattern: '^CL:\d+$'

slots:
  cell_type:
    range: CellTypeId

```

However, this has a number of limitations

You can also model ontology terms directly, e.g

```yaml
default_prefix: my_schema

classes:
  variant:
    slots:
       - variant type
  ontology term:
     slots:
        - name
        - id
        - ontology namespace
        - synonyms
        - secondary ids


slots:
  variant type:
    range: ontology term
  name:
  id:
     type: uriorcurie
  ontology namespace:
  synonyms:
  secondary ids:

```

declare id_prefixes for a class that constrain the kinds of identifiers used to describe the class

```yaml
default_prefix: my_schema

classes:
  variant:
    slots:
       - variant type
  sequence ontology term:
     slots:
        - name
        - id
        - ontology namespace
        - synonyms
        - secondary ids
     id_prefixes:
        - SO


slots:
  variant type:
    range: sequence ontology term
  name:
  id:
    identifier: true
    type: uriorcurie
  ontology namespace:
  synonyms:
  secondary ids:

```

See [dynamic enums](https://linkml.io/linkml/schemas/enums.html#dynamic-enums) for more details.

### Can I use LinkML to develop ontologies?

LinkML is intended as a schema modeling framework, rather than an ontology modeling framework.
Schemas are intended for modeling and constraining the structure of *data*, whereas ontologies
and ontology modeling frameworks like OWL are for modeling and constraining models of the *world*.

LinkML is intended to be *combined* with OWLs and other controlled vocabularies, using terms from
these resources as mappings in enumerations.

However, the distinction here is frequently blurred, and there are many examples of schemas that
have been modeled using OWL - e.g. BioPAX, FOAF.

LinkML allows any schema to be translated to OWL using the `gen-owl <https://linkml.io/linkml/generators/owl>`_ 
generator. There are a number of reasons to do this:

- take advantage of ontology exploration and browsing tools such as BioPortal and Protege
- use OWL reasoning over schemas and data (with the caveat that OWL uses *Open World* reasoning)

You can also use `Schema Automator <https://linkml.io/schema-automator>`_ to do the reverse translation.

It doesn't make sense to develop a large terminological-style ontology such as an OBO
ontology as LinkML classes, since LinkML is intended for data modeling.

One option is to use the `linkml-owl <https://linkml.io/linkml-owl>`_ framework to generate OWL
classes from LinkML *data*

### Are CURIEs used in schema definitions checked for expandability and resolution?  

No, not at this time.  However, linkml_runtime does have methods to help you expand the CURIEs in your data
using the prefixes in your model (see: linkml_runtime.utils.namespaces.py) into URIs.  In addition, the
`curies` [python package](https://github.com/cthoyt/curies/) which provides a standalone CURIE expansion service. 
There are many ways to check if a URI is resolvable.  One open source python package to do this 
is: [LinkChecker](https://pypi.org/project/LinkChecker/).
 
### Are CURIEs used in data that validates against a given LinkML schema checked for expandability and resolution?

No, not at this time.  However, linkml_runtime does have methods to help you expand the CURIEs in your data
using the prefixes in your model (see: linkml_runtime.utils.namespaces.py) into URIs.  Specifying a regular expression
to constrain the CURIEs in your data to a particular pattern is also possible.  
See the [regular expression](https://w3id.org/linkml/regular_expression) metaslot.  However, validating a CURIE
that matches the regular expression, but is invalid in some other way (e.g. is an obsolete ontology term) is not 
currently supported.

### Is it possible for us to import only a subset of an existing LinkML model?

Not yet, but we are working on a tool to this, please check out 
[linkml-transformer](https://github.com/linkml/linkml-transformer) for more details.

### Can I combine dynamic enums using boolean expressions

Yes, this is possible.

See [enum](../schemas/enums) documentation

## Can I use regular expressions to constrain values?

Yes, regular expressions can be used either on slots, or on types.

This is done using the [pattern](https://w3id.org/linkml/) metaslot

## Can I reuse regular expression patterns?

Yes, you can do this via the [structured_pattern](https://w3id.org/linkml/structured_pattern) metaslot

First you declare the patterns to be reused in the top level of your schema:

```yaml
settings:
  float: "\\d+[\\.\\d+]"
  unit: "\\S+"
  email: "\\S+@\\S+{\\.\\w}+"
```

You can then use this inside a structured pattern:

```
  height:
    range: string
    structured_pattern:
      syntax: "{float} {unit.length}"
      interpolated: true
      partial_match: false
```

## How do I do the equivalent of JSON-Schema composition?

See: [Schema Composition](https://json-schema.org/understanding-json-schema/reference/combining.html) in JSON-Schema docs

LinkML provides the following analogous concepts:

* [any_of](https://w3id.org/linkml/any_of)
* [exactly_one_of](https://w3id.org/linkml/exactly_one_of)
* [all_of](https://w3id.org/linkml/all_of)
* [none_of](https://w3id.org/linkml/none_of)

In some cases, the use of schema composition can be avoided by using simple inheritance patterns.

Note that these constructs may not be supported by all generators. See [advanced features](https://linkml.io/linkml/schemas/advanced) for current documentation.

## Why are my class names translated to CamelCase?

LinkML allows you to use any convention you like when authoring
schemas. However, when translating to other formalisms such as
JSON-Schema, RDF, Python then those naming conventions are applied.

For example, if you define a class:

```yaml
default_prefix: my_schema

classes:
  my class:
    attributes:
      my slot:
```

Then this will translate as follows:

 * Python, JSON-Schema
   * MyClass
   * my_slot
 * RDF/OWL URIs
   * my_schema:MyClass
   * my_schema:my_slot

Note in the RDF/OWL representation, separate `rdfs:label` triples will be generated retaining the original human-friendly name.

This has the advantage of keeping human-friendly nomenclature in the appropriate places without specifying redundant computer names and human names

However, the automatic translation can be confusing, so some schemas opt to follow standard naming conventions in the schema:

```yaml
default_prefix: my_schema

classes:
  MyClass:
    attributes:
      my_slot:
```

you have the option of specifying human-friendly *titles* for each element:

```yaml
default_prefix: my_schema

classes:
  MyClass:
    title: my class
    attributes:
      my_slot:
        title: my slot
```

Note that one current limitation of the LinkML generator framework is
that it does not protect you from using keywords that are reserved in
certain formalisms.

For example, if you define a slot `in`, then this conflicts with the
Python keyword, and the generated python code will raise errors. For now the recommendation is to avoid these as they arise.

In future, the LinkML framework will

 * warn if a reserved term is used
 * provide a mechanism for transparent mapping between a schema element and a "safe" version of the element

## When two data classes are linked by a slot in one class definition, how is the reciprocal association expressed in LinkML?

Relationships between classes can be defined in a few ways:
- via slots that dictate the link via domain and range constraints.
- via objects that capture the two objects and the relationship between those concepts.

via slots that dictate the link via domain and range constraints

```yaml
default_prefix: my_schema

classes:
  allele:
    slots:
       - allele of
  gene:
     
slots:
  allele of: 
     type: uriorcurie
     domain: allele
     range: gene
```

via objects that capture the two objects and the relationship between those concepts

```yaml
default_prefix: my_schema

classes:
  allele:
  gene:
  allele gene relation:
     slots:
        - subject
        - object
        - predicate
      
slots:
  predicate: 
     range: predicate_enum
  subject:
     range: allele
  object:
     range: gene

enums:
  predicate_enum:
    permissible_values:
      allele_of:
```

You can further annotate your schema with information that two of
your classes represent *entities* and one represents a *relationship*:


```yaml
default_prefix: my_schema

classes:
  allele:
  gene:
  allele gene relation:
     represents_relationship: true
     slots:
        - subject
        - object
        - predicate
      
slots:
  predicate: 
     range: predicate_enum
     relational_role: PREDICATE
  subject:
     range: allele
     relational_role: SUBJECT
  object:
     range: gene
     relational_role: OBJECT

enums:
  predicate_enum:
    permissible_values:
      allele_of:
```

Applications can make use of this metadata - e.g for compact
property graph representations, ER-style visualizations of the schema,
auto-inferring convenient shortcut slots.

## How do I avoid name clashes when importing a schema?

Currently the assumption of existing LinkML tools is that all element
names are unique, both within an individual schema *and across imports*.

This means if you want to import a schema `personinfo`, and
`personinfo` includes a class `Person`, or another imported schema or your own schema has a
class `Person`, there will be an element clash, and you will need to
either remove the import, change the imported schema, or change your
own schema.

Historically this has not been a major issue, as imports are typically
used sparingly, and the assumption is that the imported schema is
orthogonal to the importing one. In many cases the apparent issue is
resolved simply by not using an import and instead reusing `class_uri`s.

However, we recognize the unique element restriction can be limiting, and we are currently
exploring mechanisms that provide more flexibility in reuse, including:

- the use of [structured_imports](https://w3id.org/linkml/structured_imports) to *selectively* import elements from a schema
- alternatives to imports and inheritance, such as using [implements](https://w3id.org/linkml/implements)
- using [linkml-transformer](https://github.com/linkml/linkml-transformer) to *transform* upstream schemas rather than import them

## What is the prefixes section at the start of a schema?

The prefixes section can be used to provide CURIE abbreviations for entities. Under the hood,
all elements in a LinkML schema are identified by a URI, but we typically expose these
as CURIEs.

For example `linkml:SchemaDefinition` is a CURIE that expands to `https://w3id.org/linkml/SchemaDefinition`.

The prefixes section allows you to define a set of prefixes that can be used throughout the schema,
for example:

```yaml
prefixes:
  linkml: https://w3id.org/linkml/
  biolink: https://w3id.org/biolink/
  schema: http://schema.org/
```

## Is there a standard registry of prefixes?

LinkML is closely aligned with the
[bioregistry](https://bioregistry.io/), a community-driven, curated, hierarchical collection of prefix namespaces
for use in data resources. Bioregistry is used commonly in the life sciences, but it is not restricted to
this domain.

We recommend using prefixes that align with bioregistry.

See also
**Unifying the identification of biomedical entities with the Bioregistry** (2022),
[doi:10.1038/s41597-022-01807-3](https://doi.org/10.1038/s41597-022-01807-3)

## What are id_prefixes used for?

The LinkML meta modeling element, [id_prefixes](https://w3id.org/linkml/id_prefixes) can be applied to any Class. This is used to specify which prefixes should be used on the identifiers for that class.

The id_prefixes are listed in decreasing priority order, with the "preferred" prefix listed first.

Downstream software components can use this field to constrain data entry to a particular kind of identifier.

To see examples, Biolink uses id_prefixes extensively. For example, the [MolecularEntity](https://biolink.github.io/biolink-model/docs/MolecularEntity) class shows that identifiers for this class can be drawn from PubChem, CHEBI, DrugBank, etc.

For more, see [URIs and Mappings](https://linkml.io/linkml/schemas/uris-and-mappings.html)

## How to use the `alias` metamodel construct?

The [alias](https://linkml.io/linkml-model/latest/docs/alias/) construct from the metamodel is an element that can be asserted on slot definitions in the schema. If *alias* is asserted on a slot and the slot is asserted on a class then, we would need to use the alias name to refer to the slot in the instance file (CSV/TSV, YAML, JSON, etc.).

For example:

Snippet of schema file:

```yaml
classes:
  Sample:
    slots:
      - id
      - altitude
slots:
  altitude_in_meters:
    alias: alt_in_m
    unit:
      ucum_code: m
```

Instance file (as YAML):

```yaml
- id: EX-123
  alt_in_m: 5
```

## When is it important to have mappings?

Any element in a LinkML schema can have any number of *mappings* associated with it

Mappings are useful in a variety of ways including: 

- they make your data and your schema more FAIR (Findable, Accessible, Reusable, and Interoperable)
- when people use data that conforms to your model, and integrated with data that conforms to another model, they can use mappings between models to help automate data harmonization.  
- mappings can provide links to other documentation sources for your model, allowing expertise to be shared between projects and not duplicated
- mappings allow advanced users to reason over your model.

Mappings can be established for exact equivalences, close, related, narrow and broad equivalences
For more detail on the kinds of mappings (and their mappings to SKOS), see [linkml:mappings](https://w3id.org/linkml/mappings)

Mappings are an entire optional feature, you can create a schema without any mappings. However, we encourage their use, and we
encourage adding them *prospectively* as you build your data model, rather than doing this *retrospectively*. Thinking about mappings
will help you think about how your modeling relates to the modeling done by others as part of other databases or standards.

## How do I represent relationships in LinkML?

For some use cases, objects described using LinkML can stand in
isolation, and do not need to be related. For example, for a simple
database of material samples (biosamples, geosamples, etc), each
sample may be considered a standalone entity described with an
identifier and various properties.

However, more often then not, your objects need to be
inter-related. Here there are a number of modeling questions that you
will need to answer:

- can my objects be related in different ways, or is there a uniform relationship type
- do I need to store information/metadata about the relationship itself?
- are the related objects somehow "external", or are they within my dataset -- and if so, should this be enforced

Depending on the answer, LinkML has different modeling constructs to help you, including:

- [range](https://w3id.org/linkml/range) constraints, which can refer to classes
- the ability to assign a slot as an [identifier](https://w3id.org/linkml/identifier), allowing other objects to link to it
- [inlining](../schemas/inlining), which determines how relationships are serialized in formats like JSON

Other more advanced constructs are also possible to allow you to treat relationships as first-class entities.

## Can LinkML handle punning?

### Punning in OWL
In OWL, punning refers to the practice of using the same entity name in different roles—sometimes as a class and sometimes as an individual. This flexibility allows an entity to be treated as both a class (concept) and an individual (instance), depending on the context in which it is used. However, this can lead to ambiguities if not handled carefully.

### Punning in LinkML
In LinkML, there is no explicit support for punning. However, we can simulate this behavior by using the same name for both classes and slots, with the understanding that this might introduce ambiguity. Below is an example where we "pun" the name of a class and a slot, replicating a common OWL punning scenario where the entity serves both as a class and a property.

### Example Scenario: "Author" as a Class and Property
Let’s imagine a scenario where we define an "Author" both as a class (representing a person or entity who writes books) and as a property (representing the relationship between a book and its author).

#### In OWL
This could look like:

```turtle
:Author rdf:type owl:Class .
:author rdf:type owl:ObjectProperty ;
    rdfs:label "author" ;
    rdfs:range :Author ;
    skos:inScheme <https://example.org/schema> .
```
Here, `:Author` is a class representing authors, and `:author` is an object property linking books to authors.


#### In LinkML
We don't directly support this kind of punning. However, we can simulate it by reusing the name "author" for both the class and the slot. Below are two approaches to achieving this:

* Approach 1: Using `uriorcurie` for Class Reference
```yaml
classes:
  Author:
    slots:
      - id
      - name
  Book:
    slots:
      - author  # Reference to the "Author" class
slots:
  author:
    range: uriorcurie  # This points to the URI of the "Author" class
  id:
    identifier: true
  name:
```
In this example, the `author` slot in the `Book` class refers to an identifier of the `Author` class. The `range: uriorcurie` indicates that this slot is expected to hold an identifier (CURIE) for an author.

* Approach 2: Using Direct Class Reference
```yaml
classes:
  Author:
    slots:
      - id
      - name
  Book:
    slots:
      - author  # Use "author" slot in the Book class
slots:
  author:
    range: Author  # Direct reference to the Author class
  id:
    identifier: true
  name:
```
In this example, we reference the `Author` class directly in the range of the `author` slot for the `Book` class. While this introduces potential ambiguity (because `author` is both a slot and a class name), it works if we're careful with the context in which it's used.

### Potential Pitfalls
While this mimics punning, there are some caveats to keep in mind:

#### Ambiguity
If a class and a slot share the same name, it can lead to confusion. In the above example, the term "author" could be interpreted either as a class or as a property, depending on context.

#### Best Practices Warning
Many LinkML generators will issue warnings when you have overlapping class and slot names, as it’s generally considered a bad practice. For instance:

```kotlin
WARNING:linkml.utils.generator:Overlapping slot and class names: author
```
#### Serialization
Despite the potential issues with overlapping names, the LinkML-to-OWL serialization will correctly generate an object property and a class with the same name:
```turtle
test:author a owl:ObjectProperty ;
    rdfs:label "author" ;
    rdfs:range test:author ;
    skos:inScheme <https://w3id.org/test/test-model> .

test:author a owl:Class ;
    rdfs:label "author" ;
```
This serialization may work fine in OWL, but the model could be harder to read or reason about, especially when debugging or collaborating across teams.

### Final Considerations

* Clarity and Readability: If punning is crucial for your model, it’s important to document your reasoning and ensure all stakeholders understand the use of shared names. In LinkML, using different names for classes and slots, even if slightly different (e.g., `AuthorClass` and `AuthorSlot`), might help to avoid confusion.

* Tools and Validation: Be mindful of validation warnings that arise from naming overlaps. If you must use the same name, you may want to ensure that the generators or tools you use can handle this without generating errors or ambiguous interpretations.
