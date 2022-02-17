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
* [linkml/sparqlfun](https://github.com/linkml/sparqlfun), for templated SPARQL queries

## How do I install the LinkML tools?

See the [installation guide](intro/install).

## What tools are available for authoring schemas?

Currently the main way to author a schema is to edit schema YAML files
in a text editor or IDE (Integrated Development Environment).

We recommend using an IDE that has support for YAML format

## Is there a tool to manage schemas as spreadsheets?

Yes! See:

 * [linkml/schemasheets](https://github.com/linkml/schemasheets)

## How do I browse a schema?

For small schemas with limited inheritance, it should be possible to mentally picture the structure just by examining the source YAML. For larger schemas, with deep inheritance, it can help to have some kind of hierarchical browsing tool.

There are a few strategies:

* Use [gen-markdown](https://linkml.io/linkml/generators/markdown) to make markdown that can be viewed using mkdocs
* Use [gen-owl](https://linkml.io/linkml/generators/owl) to make an OWL ontology, which can be browsed:
    * Using an ontology editing tool like Protege
    * By publishing the ontology with an ontology repository and using a web ontology browser
    * By running the Ontology Lookup Service docker image and browsing using a web browser

## How can I check my schema is valid?

You can use any of the generator tools distributed as part of linkml to check for errors in your schema

## Are there tools to create a schema from JSON-Schema/SHACL/SQL DDL/...?

Currently the core linkml framework can
[generate](https://linkml.io/linkml/generators/) schemas in other
frameworks from a linkml schema. The generators are part of the core framework.

We have *experimental* importers as part of the
[linkml-model-enrichment](https://github.com/linkml/linkml-model-enrichment)
project, which can generate a schema from:

* An OWL ontology
* JSON-Schema

Others may be added in future

However, there importers are not part of the core, may be incomplete,
and may not be as well supported, and not as well documented. You may
still find them useful to kick-start a schema, but you should not rely
on them in a production environment.

## Are there tools to infer a schema from data?

The [linkml-model-enrichment](https://github.com/linkml/linkml-model-enrichment) framework can seed a schema from:

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

While this should work fine, the approach has some disadvantages. In particular you get no IDE support and there is no guard against making mistakes in key names or structure until you come to run the code.

A better approach for Python developers is to use the Python object model that is generated from the metamodel.

```
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition

s = SchemaDefinition(id= my_schema_id,
                     classes= [ ... ])
```

You can also use the SchemaView classes, see the developers guide section on [manipulating schemas](https://linkml.io/linkml/developers/manipulating-schemas.html)

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

## Are there guides for developing LinkML compliant tools?

See the [tool developer guide](https://linkml.io/linkml/developers/tool-developer-guide)

## Can I use my schema to do reasoning over my data?

There are a number of strategies for performing deductive inference:

* Convert your [schema to OWL](https://linkml.io/linkml/generators/owl) and your [data to RDF](https://linkml.io/linkml/data/rdf) and use an OWL reasoner
* Use the (experimental) [linkml-datalog](https://github.com/linkml/linkml-datalog) framework


