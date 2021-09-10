# FAQ: Why LinkML

## Why should I use LinkML at all?

All data follows some kind of schema or data model, whether it is explicitly articulated, or implicit / in the background. In our experience it is always beneficial to explicitly articulate that schema. This holds true for a range of situations, including:

 * you have simple tabular data in TSVs or a spreadsheet
 * you have a highly interlinked relational model
 * you are working with JSON documents in a document store like MongoDB
 * you have a knowledge graph in Neo4J
 * you are working with linked data in RDF

LinkML is designed to be flexible enough to cover all these use cases, allowing for lighweight semantic data dictionaries for tabular data, through rich interlinked schemas for knowledge graphs and triplestores

## My data is a simple spreadsheet/TSV, why should I use LinkML?

If your data is a simple CSV then using a framework like LinkML may seem daunting. It may be tempting to include a simple README alongside your TSV describing the column headers. While this is certainly better than not having any data description at all, consider some of the drawbacks:

 * the README isn't a computer-digestible representation of your data
 * you do not have a mechanism for validating the TSV
 * you lack a computable way of mapping your column headers to a standard data dictionary, vocabulary

LinkML provides an easy way of making your data computable. You can start with a very simple schema, with a single class, and one slot per column in your TSV; for example, for a dataset where the rows represent people:

```yaml
classes:
  Person:
    attributes:
      id:
      name:
      email:
      age:
      occupation:
      ...
```

this is already useful as it states which column headers are expected in your data.

you can later expand that to provide constraints on the values each column:

```yaml
classes:
  Person:
    attributes:
      id:
        identifier: true ## this ensures the id field is unique
      name:
      email:
        pattern: "\\S+@[\\S\\.]+\\S+"   ## regular expression
      age:
        range: integer
        minimum_value: 0
        maximum_value: 999
      occupation_class:
        range: job_code   ## enumeration
    unique_keys:
      - description: email is unique
        unique_key_slots:
          - email
enums:
  job_code:
    scientific:
    technical:
    service:
```

You can also provide textual descriptions and additional metadata on the columns that may be useful for human users

```yaml
classes:
  Person:
    attributes:
      id:
        description: unique identifier
      name:
        description: the full name of the person
      email:
        description: the persons email address
      age:
        description: the age of the person in years
      occupation_class:
        description: the kind of job the person has
      ...
```

If you like, you can provide both linked data IRIs to your schema elements, or mappings to existing systems, for example:

```yaml
prefixes:
  schema: http://schema.org/
  foaf: http://xmlns.com/foaf/0.1/
classes:
  Person:
    attributes:
      id:
        slot_uri: schema:identifier
      name:
        slot_uri: schema:name
      email:
        slot_uri: schema:email
        exact_mappings:
          - foaf:email
```

This has a number of advantages:

 - you make the intended meaning of your columns more transparent and explicit
 - your TSVs can be automatically translated to JSON-LD and RDF via the LinkML framework
 - it faciliates automated and semi-automated mapping between your data and other representations

There are a number of proposed frameworks for providing lightweight data dictionaries for your TSVs/spreadsheets:

 - frictionless table schemas
 - csvy
 - csv on the web

One advantage of LinkML is that it is not *only* for TSVs


## Why should I use LinkML over JSON-Schema?

JSON-Schema is a fantastic framework for validating JSON documents. If your primary use case is validating JSON documents then by all means keep using it!

However, if any of the following apply to you, you may want to consider LinkML - and remember, you can always compile your LinkML schema down to JSON-Schema!

 * You want to make use inheritance/polymorphism
 * you want a language with a simple core based around familiar concepts of classes and fields (slots)
 * you want to make your data more FAIR (Findable Accessible Interoperable Reusable), for example, by annotating schema elements with IRIs
 * you want to use JSON-LD but don't want to coordinate separate JSON-Schema and JSON-LD context documents - LinkML is an all-in-one-solution!
 * you want a more advanced ontology-aware enumerations
 * you want your datamodel to be used in other frameworks than JSON - e.g. TSVs, SQL databases, Triplestores, graph databases

When making your decision, you should weigh factors such as the fact that things that can be expressed in one framework may not be expressible in the other.

## Why should I use LinkML over ShEx/SHACL?

ShEx and SHACL are both excellent "shape" languages for providing
closed-world constraints on top of RDF/triples. If your universe
consists entirely of RDF then you may want to consider adopting one of
these as your primary means of expressing your data!

However, if any of the following apply to you, you may want to
consider LinkML - and remember, you can always compile your LinkML
schema to ShEx, with the ability to do this for SHACL coming soon!

 * you want your datamodel to work for non-RDF representations such as JSON, YAML, and relational databases
 * your user based and developer base is not entirely semantic web / linked data enthusiasts
 * your emphasis is more on data modeling rather than validation

Full disclosure: LinkML lead developer Harold Solbrig is also one of the authors of the ShEx specification.

## Why should I use LinkML over SQL DDL?

TODO

## Why should I use LinkML over UML?

TODO

## Why should I use LinkML over OWL?

LinkML is in a very different class of languages from OWL. LinkML is a
schema language, with features in common with JSON-Schema, XML Schema,
UML, SQL DDL, shape languages such as ShEx/SHACL.

In our experience OWL is best for "open model" direct representations
of domain knowledge, and should not be used as a schema
language. However, we appreciate this is nuanced, and we welcome any
questions or discussions via our GitHub issue tracker.

If you do have a schema expressed in OWL, you can use the linkml
toolkit to infer/bootstrap a LinkML schema from it. But note this is a
heuristic procedure, and will not give you sensible results from a
large "terminological" ontology.

It *is* possible to use LinkML to help you structure an OWL ontology
by using LinkML as a metaclass authoring system. See
[ChemSchema](https://cmungall.github.io/chem-schema/ontology.html) for
an example, and see also the
[linkml-owl](https://github.com/linkml/linkml-owl) framework.



