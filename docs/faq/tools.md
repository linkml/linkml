# FAQ: Tools

## What tools do I need for LinkML?

Formally, LinkML is a specification for modeling data, and is independent of any set of tools.

However, for practical purposes, you will find the core python toolchain useful, whether you use this as a python library, or a command line tool.

This includes functionality like:

* [generators](https://linkml.io/linkml/generators) to convert schemas to other modeling languages
* [data converters and validators](https://linkml.io/linkml/data) for working with data that conforms to LinkML (including RDF, JSON, and TSV)

The GitHub repo is [https://github.com/linkml/linkml](https://github.com/linkml/linkml)

For installation, see [installation](https://linkml.io/linkml/intro/install.html)

There are other tools in the LinkML ecosystem that you may find useful:

* [linkml/schemasheets](https://github.com/linkml/schemasheets), for managing your schema as a spreadsheet
* [linkml/linkml-model-enrichment](https://github.com/linkml/linkml-model-enrichment), for bootstrapping and enhancing schemas
* [linkml/linkml-owl](https://github.com/linkml/linkml-owl), for generating OWL ontologies using schemas as templates

See [../ecosystem](../ecosystem) for more info on the LinkML ecosystem.

## How do I install the LinkML tools?

See the [installation guide](../intro/install).

## What tools are available for authoring schemas?

Currently the main way to author a schema is to edit schema YAML files
in a text editor or IDE (Integrated Development Environment).

We recommend using an IDE that has support for YAML format.

## Is there IDE support for editing schemas

IDEs like PyCharm and VSCode have support for schema-aware editing of YAML files.
These require a JSON-Schema input.

The LinkML meta model is converted to JSON-Schema here: [https://w3id.org/linkml/meta.schema.json](https://w3id.org/linkml/meta.schema.json) and can be incorporated into pycharm for model syntax validation.  For more details on pycharm specifically: [PyCharm docs](https://www.jetbrains.com/help/pycharm/json.html#ws_json_schema_add_custom)

See the section below on "Are there tools for editing my data?" for
suggestions (note that your schema *is* data - schemas instantiate the
schema class in the metamodel)


## Is there a tool to manage schemas as spreadsheets?

Yes! See:

 * [linkml/schemasheets](https://github.com/linkml/schemasheets)

## How do I browse a schema?

For small schemas with limited inheritance, it should be possible to mentally picture the structure just by examining the source YAML. For larger schemas, with deep inheritance, it can help to have some kind of hierarchical browsing tool.

There are a few strategies:

* Use [gen-doc](https://linkml.io/linkml/generators/markdown) to make markdown that can be viewed using mkdocs
    * note you get this "for free" if you set up your project using the LinkML cookiecutter
* Use [gen-owl](https://linkml.io/linkml/generators/owl) to make an OWL ontology, which can be browsed:
    * Using an ontology editing tool like Protege
    * By publishing the ontology with an ontology repository (e.g. BioPortal or a member of the OntoPortal alliance) and using a web ontology browser
    * By running the Ontology Lookup Service docker image and browsing using a web browser

## How can I check my schema is valid?

You can use any of the generator tools distributed as part of linkml to check for errors in your schema.

## Is there a linter for LinkML?

Yes! See the documentation for [the schema linter](https://linkml.io/linkml/schemas/linter).

The linter will attempt to ensure your schema follows best practice.

## Are there tools to create a schema from JSON-Schema/SHACL/SQL DDL/...?

Currently the core linkml framework can
[generate](https://linkml.io/linkml/generators/) schemas in other
frameworks from a linkml schema. The generators are part of the core framework.

We have *experimental* importers as part of the
[schema-automator](https://github.com/linkml/schema-automator)
project, which can generate a schema from:

* An OWL ontology
* JSON-Schema

Others may be added in future

However, there importers are not part of the core, may be incomplete,
and may not be as well supported, and not as well documented. You may
still find them useful to kick-start a schema, but you should not rely
on them in a production environment.

## Are there tools to infer a schema from data?

The [schema-automator](https://github.com/linkml/schema-automator) framework can seed a schema from:

* CSV/TSV files
* JSON data
* RDF triples

Note that a number of heuristic measures are applied, and the results
are not guaranteed to be correct. You may still find them useful to
bootstrap a new schema.

This framework also has tools to:

* Automatically annotate mappings in a schema using bioportal annotator service
* Automatically assign meaning fields in enums using bioportal and OLS annotators

Again, this is a text-mining based approach, and will yield both false positives and negatives.

## How do I programmatically create schemas?

As LinkML schemas are YAML files, you can use library that writes YAML.

For example, in Python you can write code like this:

```python
import yaml

schema = {
  "id": my_schema_url,
  classes: [
   {
    "Person": {
      "description": "any person, living or dead",
      "attributes": {
          ...
       }
    }
   }
  ]
}
print(yaml.dump(schema))
```

You can also write similar code in most languages.

While this should work fine, the approach has some disadvantages.
In particular, you get no IDE support and there is no guard against making mistakes in key names or structure until you come to run the code.

A better approach for Python developers is to use the Python object model that is generated from the metamodel.

```
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition

s = SchemaDefinition(id= my_schema_id,
                     classes= [ ... ])
```

You can also use the SchemaView classes, see the developers guide section on [manipulating schemas](https://linkml.io/linkml/developers/manipulating-schemas.html)

Another approach is to use [SchemaBuilder schemas](https://linkml.io/linkml/developers/schemabuilder.html) objects.


## How can I check my data is valid?

If you have data in RDF, JSON, or TSV then you can check for validiting using `linkml-validate`

See [validating data](https://linkml.io/linkml/data/validating-data) for more details

## Are there tools for editing my data?

the same LinkML data can be rendered as JSON or RDF, and for schemas
that have a relatively flat structure, TSVs can be used. Any editing
tool that can be used for those formats can be used for LinkML. For
example, you can turn your schema into OWL and then use Protege to
edit instance data. Or you can simply edit your data in a TSV.

For "flat" schemas such as those for collecting sample or specimen
metadata, the
[DataHarmonizer](https://github.com/cidgoh/DataHarmonizer) accepts
LinkML as a schema language.

If you are comfortable using an IDE like PyCharm, and with editing you data as JSON, then you can use your LinkML schema to provide dynamic schema validation and autocompletion while editing, see [these slides](https://docs.google.com/presentation/d/10fVBY5m89wKd8qyIvDwNHvCRnJnQx1YCXmyiVIbyNYI/edit#slide=id.p) for a guide

## Are there guides for developing LinkML compliant tools?

See the [tool developer guide](https://linkml.io/linkml/developers/tool-developer-guide)

## Can I generate a website from a LinkML schema

Yes!

See the [markdown generator](https://linkml.io/linkml/generators/markdown) for details.

If you run:

```
gen-doc -d docs personinfo.yaml
```

It will place all the markdown documents you need to run a [mkdocs](https://www.mkdocs.org/) site

## How do I include UML class diagrams?

The docgen framework uses [Mermaid](https://mermaid.js.org/) to generate class diagrams
from your schema. This is included as a default when you use the docgen framework.

## Can I include generated documentation in a Sphinx site?

The default documentation framework for LinkML is [mkdocs](https://www.mkdocs.org/).

However, you can also include generated markdown in your sphinx site. This may be desirable
if you are incorporating LinkML into a software project that uses [Sphinx](https://www.sphinx-doc.org/).

You should make sure your sphinx configuration includes:

1. The [MyST](https://myst-parser.readthedocs.io/) extension, for parsing markdown
2. The [Mermaid](https://sphinxcontrib-mermaid-demo.readthedocs.io/en/latest/) extension, for Mermaid class diagrams

Your `conf.py` should include:

```python
extensions = [
    ...
    'myst_parser',
    'sphinxcontrib.mermaid',
    ...
]
```

Consult the [sphinx configuration docs](https://www.sphinx-doc.org/en/master/usage/configuration.html) for more details.

Note that in order for mermaid to render properly, you will need to tell `gen-docs` to use
[MyST flavored Markdown](https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html)

```python
gen-doc --dialect myst ...
```

## Can I customize the Markdown generation for my schema site?

For some purposes, the generic schema documentation provided by `gen-markdown` may look too... generic.

You can customize markdown generation using your own templates. This requires a basic understanding of Jinja2 templates.

The protocol is:

1. copy the jinja templates from [docgen](https://github.com/linkml/linkml/tree/main/linkml/generators/docgen) to your own repo in a folder `templates`
2. customize these templates
3. run `gen-docs --template-directory templates -d docs my_schema.yaml`
4. run `mkdocs serve` to test locally
5. iterate until they look how you want, then deploy (e.g. `mkdocs gh-deploy`)

An example repo that uses highly customized templates: [GSC MIxS](https://genomicsstandardsconsortium.github.io/mixs)

Note that one disadvantage of using custom templates is that you will not automatically get improvements
made back in the core templates - you will need to manually sync. We are working on ways to make the
Jinja2 templates more compositional so that this is less of an issue.

## Can I use LinkML in conjunction with SQL Databases?

Yes, and in fact providing semantics and expressivity to relational databases is a core LinkML use case.

With LinkML you can:

- [Generate a relational database schema](https://linkml.io/linkml/generators/sqltable.html) from a LinkML schema
- Reverse engineer a LinkML schema [from a Relational Database schema](https://linkml.io/schema-automator/packages/importers.html#importing-from-sql)
- Create [ORM helper code](https://linkml.io/linkml/generators/sqlalchemy.html)

See the [SQL tutorial](https://linkml.io/linkml/intro/tutorial09.html) for more details.

## Can I use LinkML in conjunction with MongoDB?

LinkML is compatible with MongoDB, in that both can use JSON as a common
exchange format.

We don't yet have any helper code for working with MongoDB, but you should be
able to take any LinkML objects, [serialize as JSON](https://linkml.io/linkml/data/index.html),
and store in the database, as well as the reverse.

## Can I use LinkML in conjunction with Triplestores?

RDF is a natural way of serializing and working with data in LinkML, see
[working with RDF](https://linkml.io/linkml/data/rdf.html).

There are some additional helper packages for working with RDF stored in triplestores:

- [sparqlfun](https://github.com/linkml/sparqlfun) allows you to define SPARQL templates in LinkML
- [linkml-sparql](https://github.com/linkml/linkml-sparql) is an experimental ORM for SPARQL

## Can I use LinkML in conjunction with Neo4J or graph databases?

You definitely can, although we don't yet have any bindings for Neo4J or other graph databases.

Note however, that most of the examples and documentation on this site
is geared towards either JSON tree-oriented data shapes, or RDF
triples. Graph databases typically follow a property-graph (PG).

If you are using PGs, we recommend following the design patterns in
the [BioLink Model](https://biolink.github.io/biolink-model/), which
itself follows commonly established Entity-Relationship (ER)
patterns. Here you would have one set of classes corresponding to
nodes, and another set of classes corresponding to edges. The slots on
edge classes can be decorated with
[relational_role](https://w3id.org/linkml/relational_role) descriptors.


## Can I use my schema to do reasoning over my data?

There are a number of strategies for performing deductive inference:

* Convert your [schema to OWL](https://linkml.io/linkml/generators/owl) and your [data to RDF](https://linkml.io/linkml/data/rdf) and use an OWL reasoner
* Use the (experimental) [linkml-datalog](https://github.com/linkml/linkml-datalog) framework

## What does _if_missing mean in my JSON output?

If you pass a LinkML object directly to `json.dump` you will see internal hidden fields, these start with underscore: e.g. `_if_missing`.

We recommend instead using `json_dumper.dump` in the linkml-runtime package, which will give the *canonical* JSON representation of a LinkML object.

See:

 - [working with data - python](https://linkml.io/linkml/data/python.html)
 - [loaders and dumpers, code docs](https://linkml.io/linkml/developers/loaders-and-dumpers.html)

## What does _csv.Error: field larger than field limit (131072) mean?

The Python CSV module has a built-in default limit on the size of the data
that can fit into any one column value. This is usually enough for most purposes,
but there may be scenarios where you have a CSV with large data values, e.g

- storing DNA sequence data
- storing image data in base64 or similar

In these cases you should pass in `--csv-field-size-limit NUMBER`

E.g.

```bash
linkml-sqldb --csv-field-size-limit 250000 dump  -s my-schema.yaml my-data.tsv -D my.db
```
