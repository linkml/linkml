# FAQ: Why LinkML

## Why should I use LinkML at all?

All data follows some kind of schema or data model, whether it is explicitly articulated, or implicit / in the background. In our experience it is always beneficial to explicitly articulate that schema. This holds true for a range of situations, including:

 * you have simple tabular data in TSVs or a spreadsheet
 * you have a highly interlinked relational model
 * you are working with JSON documents in a document store like MongoDB
 * you have a knowledge graph in Neo4J
 * you are working with linked data in RDF

LinkML is designed to be flexible enough to cover all these use cases, allowing for lightweight semantic data dictionaries for tabular data, through rich interlinked schemas for knowledge graphs and triplestores

## My data is a simple spreadsheet/TSV, why should I use LinkML?

If your data is a simple spreadsheet, then using a framework like LinkML may seem daunting. It may be tempting to include a simple README alongside your TSV describing the column headers. While this is certainly better than not having any data description at all, consider some of the drawbacks:

 * the README isn't a computer-digestible representation of your data
 * you do not have a mechanism for validating the TSV
 * you lack a computable way of mapping your column headers to a standard data dictionary or vocabulary

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
      primary:
        description: email is unique
        unique_key_slots:
          - email
enums:
  job_code:
    scientific:
    technical:
    service:
```

You can also provide textual descriptions and additional metadata on the columns that may be useful for human users:

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

If you like, you can provide linked data IRIs to your schema elements or mappings to existing systems, for example:

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
 - it facilitates automated and semi-automated mapping between your data and other representations

There are a number of proposed frameworks for providing lightweight data dictionaries for your TSVs/spreadsheets:

 - frictionless table schemas
 - csvy
 - csv on the web

One advantage of LinkML is that it is not *only* for TSVs. It can read and write many popular data formats.


## Why should I use LinkML over JSON-Schema?

JSON-Schema is a fantastic framework for validating JSON documents. If your primary use case is validating JSON documents then by all means keep using it!

However, if any of the following apply to you, you may want to consider LinkML - and remember, you can always
[compile your LinkML schema down to JSON-Schema](../generators/json-schema)!

 * You want to make use of inheritance/polymorphism
 * you want a language with a simple core based around familiar concepts of classes and fields (slots)
 * you want to make your data more FAIR (Findable Accessible Interoperable Reusable), for example, by annotating schema elements with IRIs
 * you want to use JSON-LD but don't want to coordinate separate JSON-Schema and JSON-LD context documents - LinkML is an all-in-one-solution!
 * you want enums to be aligned with ontologies or standard vocabularies
 * you need to use [dynamic enumerations](https://douroucouli.wordpress.com/2022/07/15/using-ontologies-within-data-models-and-standards/)
 * you want your data model to be used in other frameworks than JSON - e.g. TSVs, SQL databases, Triple stores, graph databases

When making your decision, you should weigh factors such as the fact that things that can be expressed in one framework may not be expressible in the other.

See also FAQ entries in [modeling](modeling) which compare some similar constructs.

## Why should I use LinkML over JSON-LD?

JSON-LD is a lightweight way of exchanging RDF data as JSON files. Different groups use JSON-LD
in different ways. In some cases, JSON-LD contexts are provided as a way to map from developer-friendly
JSON files to less familiar RDF/Turtle formats. In other cases, the JSON-LD files are operated on
directly as JSON objects.

Note that JSON-LD doesn't in itself describe how data should be *structured* - e.g. which fields
are expected, what the expected range is of different fields, etc. Some groups combine a JSON-LD
specification with either JSON-Schema or with a shape language like SHACL.

One advantage of LinkML is that it provides a "one stop shop", where all aspects of your data
can be described in one place without duplication, and then have JSON-LD contexts, shapes, and
JSON schema generated for you.

For more, see [Using JSON-LD](https://linkml.io/linkml/howtos/using-jsonld.html) in the how-tos
section of this site.

## Why should I use LinkML over ShEx/SHACL?

ShEx and SHACL are both excellent "shape" languages for providing
closed-world constraints on top of RDF/triples. If your universe
consists entirely of RDF then you may want to consider adopting one of
these as your primary means of expressing your data!

However, if any of the following apply to you, you may want to
consider LinkML - and remember, you can always compile your LinkML
schema to ShEx, with a prototype SHACL generator now available.

 * you want your datamodel to work for non-RDF representations such as JSON, YAML, and relational databases
 * your user based and developer base is not entirely semantic web / linked data enthusiasts
 * your emphasis is more on data modeling rather than validation

Note: former LinkML lead developer Harold Solbrig is also one of the authors of the ShEx specification.

See also:

 * [ShEx generator](https://linkml.io/linkml/generators/shex.html)
 * [SHACL generator](https://linkml.io/linkml/generators/shacl.html)

## Why should I use LinkML over SQL DDL?

SQL Data Description Language (DDL; or simply "CREATE TABLE"
statements) is a means of describing the structure of a relational
database.

If you are using a relational database and have minimal lightweight
application code that performs direct SQL queries over data, there may
be no compelling use case for LinkML.

However, most information architectures that use a SQL database also
involve some alternative representation of the data - for example, a
JSON representation in an API, or an object representation -- or even
an RDF representation. It can be challenging to keep these different
representations in sync. There are some excellent products that
solve "one part" of this mapping problem -- e.g. an ORM (Object
Relational Mapping) tool. LinkML is intended to allow you to give a
"bigger picture" view of your model that is as independent as possible
from underlying storage or exchange technologies, and at the same time
can be compiled down.

LinkML also allows you to specify URIs and CURIE/URI mappings for each
element of your schema, which provides a declarative specification of
how your data should be mapped. For example, if you are trying to
bring together two schemas (whether via federation or via
warehousing), if both schemas annotate the same field with the same
URI then we know these can be merged.

Even if you are not interested in mapping your SQL data model to
anything else, it can still be a great idea to use LinkML as a data
definition language for your schema, especially if you have a schema
with many fields that a domain scientist or stakeholder needs to
understand.

In our opinion, SQL DDL is not a great language for data
dictionaries. There is a lack of standard ways to even add comments or
descriptions to fields, and it can be challenging to introspect
these. LinkML provides a simple easy to use way to provide rich
metadata about your fields.

Compare:

```sql
CREATE TABLE sample (
  id TEXT PRIMARY KEY,  -- unique sample id
  individual_id TEXT FOREIGN KEY(person.id),
  name TEXT,
  disease TEXT,
  src TEXT,
  collec_location TEXT FOREIGN KEY(geoloc.id),
  ...
);
```

with:

```yaml
classes:
  Sample:
    attributes:
      id:
        title: identifier
        identifier: true
        pattern: "SAMPLEDB:SAM\\d{8}"
        description: A unique identifier for the sample
      name:
        title: sample name
        description: A human-readable name for the sample
        range: NarrativeText
      disease:
        title: disease
        description: the disease with which the patient was diagnosed
        range: DiseaseEnum
      src:
        title: tissue source
        description: the anatomical location from which the tissue was sampled
        range: DiseaseEnum
        todos:
          - model this using an ontology term instead
      collec_location:
        title: collection location
        description: the geocoordinates of the site where the sampling was obtained
        notes:
          - this should NOT be the site of processing
        range: GeoLoc
```

Here we have a standard way of providing human-readable names for our
columns (via [title](https://w3id.org/linkml/title)). We have a
human-friendly textual description. Both of these could be used to
drive dynamic tooltips in an application that collects or displays data.

See also:

 * [SQL Table generator](https://linkml.io/linkml/generators/sqltable.html)

## Why should I use LinkML over UML?

UML is a powerful language for software engineer diagramming. [UML
Class Diagrams](https://en.wikipedia.org/wiki/Class_diagram) provide a
standard way to draw a class hierarchy for a program that has some
similarities to LinkML.

There are a number of reasons to use LinkML over UML:

* The UML standard is large and complex
* UML serialization in [XMI (XML Medata Interchange)](https://en.wikipedia.org/wiki/XML_Metadata_Interchange) is hard to work with
* UML is more geared towards software engineering and includes features not needed for data modeling, such as operations
* UML tools are complex and expensive (both financially and in terms of learning curves)
* In contrast, LinkML makes it easy to author schemas using nothing more than a text editor
* All the tooling for LinkML is free and open
* LinkML has the ability to compile to other frameworks
* LinkML has facilities for *semantic modeling*, not anticipated in UML

Currently there is no way to generate complete UML from a LinkML schema.

However, the yUML generator (used in [the markdown generator](https://linkml.io/linkml/generators/markdown.html)) can be used to make yUML diagrams for any class or schema.

## Why should I use LinkML over OWL?

The Web Ontology Language (OWL) is a Description Logic formalism for representing
ontological knowledge.

LinkML is in a very different class of languages from OWL. LinkML is a
*schema language*, with features in common with JSON-Schema, XML Schema,
UML, SQL DDL, shape languages such as ShEx/SHACL. OWL is a subset of first-order logic
based in set theory that is intended for open-world reasoning.

In our experience OWL is best for open world direct representations
of domain knowledge, and should not be used as a schema
language. Many LinkML contributors and users also work with large biomedical
terminological-style ontologies in OWL; these are essentially large structured
vocabularies, and are not intended for representing *data*. In the wider
semantic web world, people have historically sought to use OWL as a schema language,
with mixed results.

However, we appreciate this is nuanced, and we welcome any
questions or discussions via our [GitHub issue tracker](https://github.com/linkml/linkml/issues).

If you do have a schema expressed in OWL, you can use [schema-automator](https://github.com/linkml/schema-automator)
to infer/bootstrap a LinkML schema from it. But note that this is a
heuristic procedure, and will not give you sensible results from a
large "terminological" ontology (such as an OBO ontology); it is best used with schema-style "ontologies",
such as common semantic web vocabularies.

It *is* possible to use LinkML to help you structure an OWL ontology
by using LinkML as a metaclass authoring system. See
[CHEMROF](https://chemkg.github.io/chemrof/ontology) for
an example, and see also the
[linkml-owl](https://github.com/linkml/linkml-owl) framework.

See also:

 * [OWL generator](https://linkml.io/linkml/generators/owl.html)

## Why should I use LinkML over custom spreadsheets?

It is common in many projects for metadata elements and data dictionaries to be maintained as ad-hoc spreadsheets.

Doing this in the absence of any overarching framework can be
problematic. It is easy for mistakes to creep into these spreadsheets
unnoticed. Often the semantics are unclear, and when developers are
asked to write validators or UIs driven by these spreadsheets, the lack
of clear semantics can lead to repetitive error-prone code that is
costly to maintain.

LinkML provides a **systematic way to manage data dictionaries and metadata elements**.

Historically this has required use of YAML files to maintain a schema,
which can be off-putting to non-technical metadata curators. SchemaSheets allows the best of both worlds:

 * [SchemaSheets](https://github.com/linkml/schemasheets) -- author schemas as spreadsheets

This framework allows schemas to be maintained using Excel, google sheets, or TSVs, providing flexibility to non-technical modelers, with all the benefits of LinkML.

## Why should I use LinkML over CSV-on-the-web?

The W3C [CSV on the Web](https://www.w3.org/TR/tabular-data-primer/)
(CSVW) Working Group have developed standard ways to express metadata about
CSVs and other kinds of tabular data.

An example use of CSVW is to semantically describe the columns in a
CSV/TSV, for example a CSV about country locations and nomenclature. The following is Example 10 from the CSVW primer:

```json
{
  "@context": "http://www.w3.org/ns/csvw",
  "url": "countries.csv"
  "tableSchema": {
    "columns": [{
      "titles": "country",
      "dc:description": "The ISO two-letter code for a country, in lowercase."
    },{
      "titles": "country group",
      "dc:description": "A lowercase two-letter code for a group of countries."
    },{
      "titles": "name (en)",
      "dc:description": "The official name of the country in English."
    },{
      "titles": "name (fr)",
      "dc:description": "The official name of the country in French."
    },{
      "titles": "name (de)",
      "dc:description": "The official name of the country in German."
    },{
      "titles": "latitude",
      "dc:description": "The latitude of an indicative point in the country."
    },{
      "titles": "longitude",
      "dc:description": "The longitude of an indicative point in the country."
    }]
  }
}
```

CSVW provides a number of advantages for making data FAIR over the use
of CSVs alone, or CSVs in combination with non-machine-readable documentation files.

Most of the things that can be expressed using CSVW can also be expressed with
LinkML, and LinkML is not restricted solely to CSVs - e.g. you can
semantically describe JSON files with LinkML too.

We are currently planning on writing a generator for CSVW JSON-LD.

## Why should I use LinkML over ISO-11179?

[ISO-11179](https://en.wikipedia.org/wiki/ISO/IEC_11179) is an ISO standard for metadata and metadata registries. It
provides a rich standardized way of exchanging data dictionaries. For
example, an ISO-11179 registry can be used to register all of the
columns in a data file or tags in an XML file, and to map semantics
onto these, making integration across datasets more automatable.

Currently ISO-11179 and LinkML serve different purposes, but there are
overlaps in goals, and we are currently working on documentation
clarifying the connection.
