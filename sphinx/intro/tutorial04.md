# Part 4: Working with RDF

Previously we saw how to do basic validation of data using JSON-Schema.

This section demonstrates how to work with LinkML in conjunction with
Linked Data/ RDF. If this is not of interest you can skip to the next
section. However, even if this is the case you may wish to revisit
this section. LinkML is intended to make it easy to get the benefits
of Linked Data, while staying simple and working within a stack many
developers are familiar with.

And even if you aren't using RDF yourself, declaring URIs for your
schema elements can help make your data FAIR, and in particular can
serve as hooks to interoperate data!

## Example schema

Let's start with the schema we developed in the previous section:

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
        identifier: true
      full_name:
        required: true
        description:
          name of the person
      aliases:
        multivalued: true
        description:
          other names for the person
      phone:
        pattern: "^[\\d\\(\\)\\-]+$"
      age:
        range: integer
        minimum_value: 0
        maximum_value: 200
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person
```

As well as a collection of person records

data.yaml:

```yaml
persons:
  - id: ORCID:1234
    full_name: Clark Kent
    age: 33
    phone: 555-555-5555
  - id: ORCID:4567
    full_name: Lois Lane
    age: 34
```

We can use the linkml conversion library to translate this to RDF (Turtle syntax default)

```bash
linkml-convert -s personinfo.yaml -t rdf data.yaml
```

Outputs:

```ttl
@prefix ns1: <https://w3id.org/linkml/examples/personinfo/> .

<ORCID:1234> ns1:age "33" ;
    ns1:full_name "Clark Kent" ;
    ns1:phone "555-555-5555" .

<ORCID:4567> ns1:age "34" ;
    ns1:full_name "Lois Lane" .

[] a ns1:dict ;
    ns1:persons <ORCID:1234>,
        <ORCID:4567> .
```

This is a start, but it is not ideal - there are existing vocabularies such as [schema.org](http://schema.org) we could be reusing.

There are also some serious problems - there URIs for our two people are not syntactically valid. We need to provide additional information

## Adding URIs to our schema

Let's enhance our schema, using two schema slots:

 - class_uri: to declare a URI/IRI for a class
 - slot_uri: the same thing for a slot

In both cases, we provide the value as a CURIE, and include a *prefixes* map that maps CURIEs to URIs.

personinfo-semantic.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:                                  ## Note are adding 3 new ones here
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  personinfo: https://w3id.org/linkml/examples/personinfo/
  ORCID: https://orcid.org/
imports:
  - linkml:types
default_range: string
  
classes:
  Person:
    class_uri: schema:Person              ## reuse schema.org vocabulary
    attributes:
      id:
        identifier: true
      full_name:
        required: true
        description:
          name of the person
        slot_uri: schema:name             ## reuse schema.org vocabulary
      aliases:
        multivalued: true
        description:
          other names for the person
      phone:
        pattern: "^[\\d\\(\\)\\-]+$"
        slot_uri: schema:telephone       ## reuse schema.org vocabulary
      age:
        range: integer
        minimum_value: 0
        maximum_value: 200
    id_prefixes:
      - ORCID
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person
```

Now let's try converting the same YAML/JSON using the enhanced schema

```bash
linkml-convert -s personinfo-semantic.yaml -t rdf data.yaml
```

Outputs:

```ttl
@prefix ns1: <https://w3id.org/linkml/examples/personinfo/> .
@prefix ns2: <http://schema.org/> .

<https://orcid.org/1234> ns2:name "Clark Kent" ;
    ns2:telephone "555-555-5555" ;
    ns1:age "33" .

<https://orcid.org/4567> ns2:name "Lois Lane" ;
    ns1:age "34" .

[] a ns1:dict ;
    ns1:persons <https://orcid.org/1234>,
        <https://orcid.org/4567> .
```

Note that the prefixes are hidden but the effect is to reuse URIs such as [schema:telephone](http://schema.org/telephone)

## JSON-LD contexts

Behind the scenes, the linkml-convert tool is using JSON-LD contexts to convert from JSON to RDF. This is in the following parts:

 * A JSON-LD context is generated from the schema
 * the native JSON representation is enhanced with this context, to make it JSON-LD
 * A standard JSON-LD converter (in this case, rdflib) is used to convert to RDF

```bash
gen-jsonld-context --no-metadata personinfo-semantic.yaml
```

Outputs:

```json
{
   "@context": {
      "ORCID": "https://orcid.org/",
      "linkml": "https://w3id.org/linkml/",
      "personinfo": "https://w3id.org/linkml/examples/personinfo/",
      "schema": "http://schema.org/",
      "@vocab": "https://w3id.org/linkml/examples/personinfo/",
      "persons": {
         "@type": "@id"
      },
      "age": {
         "@type": "xsd:integer"
      },
      "full_name": {
         "@id": "schema:name"
      },
      "id": "@id",
      "phone": {
         "@id": "schema:telephone"
      },
      "Person": {
         "@id": "schema:Person"
      }
   }
}
```

NOTE: currently you need to declare your own type object and map this to `rdf:type` for typing information to be shown

## Using Shape Languages

In the previous section we saw how to use JSON-Schema validators. LinkML also allows the use of ShEx (future versions will allow SPARQL)


```bash
gen-shex --no-metadata personinfo-semantic.yaml
```

Outputs:

```shex
BASE <https://w3id.org/linkml/examples/personinfo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX linkml: <https://w3id.org/linkml/>
PREFIX schema: <http://schema.org/>


linkml:String xsd:string

linkml:Integer xsd:integer

linkml:Boolean xsd:boolean

linkml:Float xsd:float

linkml:Double xsd:double

linkml:Decimal xsd:decimal

linkml:Time xsd:dateTime

linkml:Date xsd:date

linkml:Datetime xsd:dateTime

linkml:Uriorcurie IRI

linkml:Uri IRI

linkml:Ncname xsd:string

linkml:Objectidentifier IRI

linkml:Nodeidentifier NONLITERAL

<Container> CLOSED {
    (  $<Container_tes> <persons> @<Person> * ;
       rdf:type [ <Container> ] ?
    )
}

<Person> CLOSED {
    (  $<Person_tes> (  schema:name @linkml:String ;
          <aliases> @linkml:String * ;
          schema:telephone @linkml:String ? ;
          <age> @linkml:Integer ?
       ) ;
       rdf:type [ schema:Person ]
    )
}
```

<!-- TODO: SPARQL -->

## RDF support is evolving

RDF support in LinkML is evolving, and future versions will have more direct support.

## More Info

* [Working with RDF Data](../data/rdf.html)
* FAQ:
    - [LinkML vs shape languages](../faq/why-linkml.html#why-should-i-use-linkml-over-shex-shacl)
* Generators:
   - [JSON-LD Context](../generators/jsonld-context)
   - [ShEx](../generators/shex)