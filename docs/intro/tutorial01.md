# Part 1: Creating your first LinkML schema

We assume that you already have LinkML [installed](install)

For the purposes of this tutorial, the simplest setup is to use a virtual environment, and then install linkml:

<!-- NO_EXECUTE -->
```bash
mkdir linkml-tutorial
cd linkml-tutorial
python3 -m venv venv
source venv/bin/activate
pip install linkml
```

You can check the install worked:

```bash
linkml-convert --help
```

As always, you can consult the [FAQ](../faq/index) if you have issues.

## Your first schema

Our first schema consists of a single *class* `Person`, with a number of *slots*:

First create a file

personinfo.yaml:

```{literalinclude} ../../examples/tutorial/tutorial01/personinfo.yaml
:language: yaml
```

(note that all files are available in the [examples/tutorial](https://github.com/linkml/linkml/tree/main/examples/tutorial) folder of this repository)

## Converting to JSON-Schema

Now run the following command on the file you just created:

```bash
gen-json-schema personinfo.yaml
```

Outputs:

```{literalinclude} ../../examples/tutorial/tutorial01/personinfo.json
:language: yaml
```

Don't worry if you don't know much about JSON-Schema. This is just an illustration that LinkML can be used in combination with a number of frameworks.

## Creating and validating data

Let's create an example data file. The file will contain an *instance* of the class we defined in our `personinfo.yaml` schema:

data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial01/data.yaml
:language: yaml
```

Note the values of all these fields are strings, even age; we will later return
to this example and show how we could model this more naturally as a number.

Validate:

```bash
linkml-validate -s personinfo.yaml data.yaml
```

You should see a message indicating there were no validation issues found. Success!

To see an example of data not validating:

bad-data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial01/bad-data.yaml
:language: yaml
```

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml bad-data.yaml
```

This should report an error to the effect that `made_up_field` is not allowed.

## Working with JSON

One of the advantages of LinkML is the same datamodel can be used for multiple expressions of the same data, for example:

* YAML/JSON
* TSVs/spreadsheets
* RDF
* Relational Databases

There are various complexities involved in going between these, but YAML and JSON are basically interchangeable with LinkML

data.json:

```{literalinclude} ../../examples/tutorial/tutorial01/data.json
:language: json
```

This will validate in the same way as the equivalent YAML file:

```bash
linkml-validate -s personinfo.yaml data.json
```

## Converting to RDF

You can use the linkml convert tool to convert your data to other formats, including RDF:

```bash
linkml-convert -s personinfo.yaml data.yaml -t ttl
```

This will produce RDF/turtle output as follows

<!-- MATCHES data.ttl -->

```{literalinclude} ../../examples/tutorial/tutorial01/data.ttl
:language: turtle
```

To write the RDF/turtle output directly to a file use

```bash
linkml-convert -s personinfo.yaml data.yaml -o data.ttl
```

If you are not familiar with RDF that's OK! RDF is just one of the possible ways of working with LinkML.

If you are familiar with RDF, the first thing you will likely notice
is that we are not reusing standard URIs for our properties and
classes. Don't worry! We will get to this later.

## Exercises

 1. Extend the example schema to include fields for `occupation` and `employed_by`
 2. Create a test data instance to indicate Clark Kent has an occupation of reporter and is employed by the Daily Planet
 3. Validate the data

## Next: Collections of data

Our toy example so far has a single person instance. Next we'll see how to exchange lists of records.
