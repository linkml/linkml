# FAQ: Python

this section of the FAQ is for questions about writing Python code that uses the LinkML framework.

## Why would I use LinkML in my Python code?

You can use LinkML without writing a line of Python code, but if you
are coding in Python there are a number of advantages to using parts
of the LinkML toolchain.

The primary advantage is to get the benefit of a Python object model
derived from your schema. Not only will this model gives you lots of
benefits such as avoiding boilerplate and IDE support, you also get
lots of "freebies" for things like loading/dumping to formats like YAML/JSON/RDF.

See:

- [python generator](https://linkml.io/linkml/generators/python.html)
- [working with python](https://linkml.io/linkml/data/python.html)

## Where do I find out more?

- [working with python](https://linkml.io/linkml/data/python.html)
- [developers guide](https://linkml.io/linkml/developers/index.html)

## Which packages do I need to install?

If you want to generate Python dataclasses, then you need the full [linkml](https://github.com/linkml/linkml) package.

However, your code doesn't need this at *runtime*. Once you have generated your project files your only dependency will be on the more lightweight [linkml-runtime](https://github.com/linkml/linkml-runtime) package.

*Note* you don't need to install [linkml-model](https://github.com/linkml/linkml-model), the metamodel is included as part of the runtime

## How do I get started?

We recommend going through the tutorial, and in particular, [Part 5: Using Python](https://linkml.io/linkml/intro/tutorial05.html)

## What is a loader or a dumper?

- loaders allow data to be loaded *into* python objects from supported formats
- dumpers allow data to be loaded *from* python objects into supported formats

Example dumper code:

```python
from linkml_runtime.dumpers import json_dumper
from personinfo import Person

p1 = Person(id='ORCID:9876', full_name='Lex Luthor', aliases=["Bad Guy"])
yaml_dumper.dump(p1, to_file='my-data.yaml')
```

Then to do the reverse:

```
p1 = yaml_loader('my-data.yaml', target_class=Person)
```

In contrast to dumpers, loaders need to know the class they are loading into, as
there is insufficient information in the json/yaml

Each loader and dumper supports a pair of methods:

- `load` and `loads` for loaders, for filehandles and strings respectively
- `dump` and `dumps` for loaders, for filehandles and strings respectively

This is following the convention of other python packages, such as the widely used json package

Note: dumpers shouldn't be confused with *generators* - dumpers are for exporting *data* that conforms to a LinkML schema, and generators are for converting an actual LinkML schema to another framework (e.g. json-schema)

## What formats are supported?

The core formats for LinkML data are:

* json (see json_dumper and json_loader)
* yaml (see yaml_dumper and yaml_loader)
* rdf (see rdflib_dumper and rdflib_loader)

csv is also partially supported, but this only works for certain "shapes" of data due to the fact nesting is not possible in CSVs.

Data can also be exported to and imported from SQL databases, but this is not part of the loader/dumper framework

## Why do I get a "not JSON serializable" message?

This is probably because you are using the `dump` method from the `json` package, which expects dictionaries, not objects.

you should use `json_dumper` instead.

## What is the difference between gen-python and gen-pydantic and gen-sqla?

Python has a number of different options for defining an object model:

- dataclasses (part of the standard library)
- Pydantic
- Attrs

Additional, SQL Alchemy has its own way of defining an object model
together with mappings to SQL tables and columns (in fact it actually has *two*
ways, declarative and imperative).

Additionally, there are ways to bridge between these frameworks.
For example, Pydantic has [docs on bridging to dataclasses](https://pydantic-docs.helpmanual.io/usage/dataclasses/).

All this can be a bit daunting for a novice developer - which to choose?

LinkML tries to be unopinionated on this matter, and aims to enable developers
to choose the framework they like.

Currently we provide:

- [gen-python](https://linkml.io/linkml/generators/python.html) - generates dataclasses
- [gen-pydantic](https://linkml.io/linkml/generators/pydantic.html) - generates pydantic models
- [gen-sql](https://linkml.io/linkml/generators/sqlalchemy.html) - generates SQL Alchemy models (declarative-style)

Historically, dataclasses has been the de-facto default in LinkML,
and this remains the most well-tested route. However, we see an increasing
interest in Pydantic, especially as this works well with the popular FastAPI framework.

If you are looking for an ORM, then gen-sqla is the best route.

Consult the above documentation for detailed documentation on each method. Some key differences:

- Root classes:
    - in Pydantic, everything is a BaseModel
    - for dataclasses, everything inherits from YAMLRoot in linkml-runtime
- Coercion and validation
    - The Pydantic framework provides a lot of runtime validation for free
    - The generated dataclasses follow Postel's principle, and performs coercion to repair some data
- Compatibility with other frameworks
    - Pydantic works well with FastAPI

## Can I convert between SQL Alchemy models and dataclasses/pydantic

Yes, [SQLStore](https://linkml.io/linkml/developers/sqlstore.html) can perform interconversion

See [SQL-Examples notebook](https://github.com/linkml/linkml/blob/main/notebooks/SQL-examples.ipynb)
for example code
