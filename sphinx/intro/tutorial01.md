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

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
  
classes:
  Person:
    attributes:
      id:
      full_name:
      aliases:
      phone:
      age:
```

(note that all files are available in the [examples/tutorial](https://github.com/linkml/linkml/tree/main/examples/tutorial) folder of this repository)

## Converting to JSON-Schema

Now run the following command on the file you just created:

```bash
gen-json-schema personinfo.yaml 
```

Outputs:
```json
{
   "$defs": {
      "Person": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "age": {
               "type": "string"
            },
            "aliases": {
               "type": "string"
            },
            "full_name": {
               "type": "string"
            },
            "id": {
               "type": "string"
            },
            "phone": {
               "type": "string"
            }
         },
         "required": [],
         "title": "Person",
         "type": "object"
      }
   },
   "$id": "https://w3id.org/linkml/examples/personinfo",
   "$schema": "http://json-schema.org/draft-07/schema#",
   "additionalProperties": true,
   "properties": {},
   "title": "personinfo",
   "type": "object"
}
```

Don't worry if you don't know much about JSON-Schema. This is just an illustration that LinkML can be used in combination with a number of frameworks.

## Creating and validating data

Let's create an example data file. The file will contain an *instance* of the class we defined in our `personinfo.yaml` schema:

data.yaml:

```yaml
id: ORCID:1234
full_name: Clark Kent
age: 32
phone: 555-555-5555

```

Validate:

```bash
linkml-validate -s personinfo.yaml data.yaml 
```

You should see no errors. This means your data is valid. Success!

To see an example of data not validating:

bad-data.yaml:

```yaml
id: ORCID:1234
full_name: Clark Kent
age: 32
phone: 555-555-5555
made_up_field: hello
```

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml bad-data.yaml
```

This should report an error to the effect that `made_up_field` is not known.

## Working with JSON

One of the advantages of LinkML is the same datamodel can be used for multiple expressions of the same data, for example:

 * YAML/JSON
 * TSVs/spreadsheets
 * RDF
 * Relational Databases

There are various complexities involved in going between these, but YAML and JSON are basically interchangeable with LinkML

data.json:

```json
{
 "id": "ORCID:1234",
 "full_name": "Clark Kent",
 "age": 32,
 "phone": "555-555-5555"
}
```

This will validate in the same way as the equivalent YAML file:

```bash
linkml-validate -s personinfo.yaml data.json
```


## Converting to RDF

You can use the linkml convert tool to convert your data to other formats, including RDF:

```bash
linkml-convert -s personinfo.yaml data.yaml -o data.ttl
```

(Note the converter uses the suffix to determine that RDF/turtle is required, but you can be explicit by setting `-t`)

This will produce an RDF/turtle file as follows

<!-- MATCHES data.ttl -->
```turtle
@prefix ns1: <https://w3id.org/linkml/examples/personinfo/> .

[] a ns1:dict ;
    ns1:age "32" ;
    ns1:full_name "Clark Kent" ;
    ns1:id "ORCID:1234" ;
    ns1:phone "555-555-5555" .
```    

If you are not familiar with RDF that's OK! RDF is just one of the possible ways of working with LinkML.

## Exercises

 1. Extend the example schema to include fields for `occupation` and `employed_by`
 2. Create a test data instance to indicate Clark Kent has an occupation of reporter and is employed by the Daily Planet
 3. Validate the data

## Collections of data

Our toy example so far has a single person instance. Next we'll see how to exchange lists of records.