# Part 4: Working with RDF

Previously we saw how to do basic validation of data using JSON-Schema.

This section demonstrates how to work with LinkML in conjunction with
[Linked Data/ RDF](https://www.w3.org/standards/semanticweb/data). If this is not of interest you can skip to the next
section. However, even if this is the case you may wish to revisit
this section. LinkML is intended to make it easy to get the benefits
of Linked Data, while staying simple and working within a stack many
developers are familiar with.

And even if you aren't using RDF yourself, declaring URIs for your
schema elements can help make your data FAIR, and in particular can
serve as hooks to interoperate data!

## Example schema

Let's start with the schema we developed in the previous section, with some minor modifications:

personinfo.yaml:

```{literalinclude} ../../examples/tutorial/tutorial04/personinfo.yaml
:language: yaml
```

We extended the previous schema in a few ways:

 - we included a *prefix declaration* for the ORCID IDs in our data records
 - we included an import of standard semantic web prefixes from `semweb_context`

We will use this schema with a collection of data records

data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial04/data.yaml
:language: yaml
```

We can use the linkml conversion library to translate this to RDF (Turtle syntax default)

```bash
linkml-convert -s personinfo.yaml -t rdf data.yaml
```

Outputs:

```turtle
@prefix ORCID: <https://orcid.org/> .
@prefix personinfo: <https://w3id.org/linkml/examples/personinfo/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ORCID:1234 a personinfo:Person ;
    personinfo:age 33 ;
    personinfo:full_name "Clark Kent" ;
    personinfo:phone "555-555-5555" .

ORCID:4567 a personinfo:Person ;
    personinfo:age 34 ;
    personinfo:full_name "Lois Lane" .

[] a personinfo:Container ;
    personinfo:persons ORCID:1234,
        ORCID:4567 .
```

Note that each person is now represented by an ORCID URI. This is a
start, but note we are still using classes and properties in our own namespace - there are existing vocabularies such as
[schema.org](http://schema.org) we could be reusing here.

## Adding URIs to our schema

Let's enhance our schema, using two schema slots:

 - class_uri: to declare a URI/IRI for a class
 - slot_uri: the same thing for a slot

In both cases, we provide the value as a CURIE, and include a *prefixes* map that maps CURIEs to URIs.

personinfo-semantic.yaml:

```{literalinclude} ../../examples/tutorial/tutorial04/personinfo-semantic.yaml
:language: yaml
```

Now let's try converting the same YAML/JSON using the enhanced schema

```bash
linkml-convert -s personinfo-semantic.yaml -t rdf data.yaml
```

Outputs:

```turtle
@prefix ORCID: <https://orcid.org/> .
@prefix personinfo: <https://w3id.org/linkml/examples/personinfo/> .
@prefix schema1: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ORCID:1234 a schema1:Person ;
    schema1:name "Clark Kent" ;
    schema1:telephone "555-555-5555" ;
    personinfo:age 33 .

ORCID:4567 a schema1:Person ;
    schema1:name "Lois Lane" ;
    personinfo:age 34 .

[] a personinfo:Container ;
    personinfo:persons ORCID:1234,
        ORCID:4567 .

```

Note that the prefixes are hidden but the effect is to reuse URIs such as [schema:telephone](http://schema.org/telephone)

This can be visualized using [rdf-grapher](https://www.ldf.fi/service/rdf-grapher) as:

![rdf-visualization](https://www.ldf.fi/service/rdf-grapher?rdf=%40prefix+ns1%3A+%3Chttp%3A%2F%2Fschema.org%2F%3E+.%0D%0A%40prefix+ns2%3A+%3Chttps%3A%2F%2Fw3id.org%2Flinkml%2Fexamples%2Fpersoninfo%2F%3E+.%0D%0A%40prefix+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E+.%0D%0A%0D%0A%3Chttps%3A%2F%2Forcid.org%2F1234%3E+a+ns1%3APerson+%3B%0D%0A++++ns1%3Aname+%22Clark+Kent%22+%3B%0D%0A++++ns1%3Atelephone+%22555-555-5555%22+%3B%0D%0A++++ns2%3Aage+33+.%0D%0A%0D%0A%3Chttps%3A%2F%2Forcid.org%2F4567%3E+a+ns1%3APerson+%3B%0D%0A++++ns1%3Aname+%22Lois+Lane%22+%3B%0D%0A++++ns2%3Aage+34+.%0D%0A%0D%0A%5B%5D+a+ns2%3AContainer+%3B%0D%0A++++ns2%3Apersons+%3Chttps%3A%2F%2Forcid.org%2F1234%3E%2C%0D%0A++++++++%3Chttps%3A%2F%2Forcid.org%2F4567%3E+.%0D%0A&from=ttl&to=png)

## JSON-LD contexts

You can also generate JSON-LD context files that can be used to add semantics to JSON documents:

```bash
gen-jsonld-context --no-metadata personinfo-semantic.yaml
```

Outputs:

```json
{
   "@context": {
      "xsd": "http://www.w3.org/2001/XMLSchema#",
      "ORCID": "https://orcid.org/",
      "linkml": "https://w3id.org/linkml/",
      "personinfo": "https://w3id.org/linkml/examples/personinfo/",
      "schema": "http://schema.org/",
      "@vocab": "https://w3id.org/linkml/examples/personinfo/",
      "persons": {
         "@type": "schema:Person",
         "@id": "persons"
      },
      "age": {
         "@type": "xsd:integer",
         "@id": "age"
      },
      "aliases": {
         "@id": "aliases"
      },
      "full_name": {
         "@id": "schema:name"
      },
      "id": "@id",
      "phone": {
         "@id": "schema:telephone"
      },
      "Container": {
         "@id": "Container"
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
# metamodel_version: 1.7.0
BASE <https://w3id.org/linkml/examples/personinfo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX linkml: <https://w3id.org/linkml/>
PREFIX schema1: <http://schema.org/>


linkml:String xsd:string

linkml:Integer xsd:integer

linkml:Boolean xsd:boolean

linkml:Float xsd:float

linkml:Double xsd:double

linkml:Decimal xsd:decimal

linkml:Time xsd:time

linkml:Date xsd:date

linkml:Datetime xsd:dateTime

linkml:DateOrDatetime linkml:DateOrDatetime

linkml:Uriorcurie IRI

linkml:Curie xsd:string

linkml:Uri IRI

linkml:Ncname xsd:string

linkml:Objectidentifier IRI

linkml:Nodeidentifier NONLITERAL

linkml:Jsonpointer xsd:string

linkml:Jsonpath xsd:string

linkml:Sparqlpath xsd:string

<Container> CLOSED {
    (  $<Container_tes> <persons> @<Person> * ;
       rdf:type [ <Container> ] ?
    )
}

<Person> CLOSED {
    (  $<Person_tes> (  schema1:name @linkml:String ;
          <aliases> @linkml:String * ;
          schema1:telephone @linkml:String ? ;
          <age> @linkml:Integer ?
       ) ;
       rdf:type [ schema1:Person ]
    )
}
```


```bash
gen-shacl --no-metadata personinfo-semantic.yaml > personinfo.shacl.ttl
```

Outputs:

<!-- compare_rdf -->
<!-- NOTE: the order of properties is non-deterministic so we cannot compare string directly>
```turtle
@prefix personinfo: <https://w3id.org/linkml/examples/personinfo/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix schema1: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

personinfo:Container a sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property [ sh:class schema1:Person ;
            sh:nodeKind sh:IRI ;
            sh:order 0 ;
            sh:path personinfo:persons ] ;
    sh:targetClass personinfo:Container .

schema1:Person a sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property [ sh:maxCount 1 ;
            sh:maxInclusive 200 ;
            sh:minInclusive 0 ;
            sh:order 4 ;
            sh:path personinfo:age ],
        [ sh:description "name of the person" ;
            sh:maxCount 1 ;
            sh:minCount 1 ;
            sh:order 1 ;
            sh:path schema1:name ],
        [ sh:maxCount 1 ;
            sh:order 0 ;
            sh:path personinfo:id ],
        [ sh:description "other names for the person" ;
            sh:order 2 ;
            sh:path personinfo:aliases ],
        [ sh:maxCount 1 ;
            sh:order 3 ;
            sh:path schema1:telephone ;
            sh:pattern "^[\\d\\(\\)\\-]+$" ] ;
    sh:targetClass schema1:Person .
```

<!-- TODO: SPARQL -->


## More Info

* [Working with RDF Data](../data/rdf)
* FAQ:
    - {ref}`LinkML vs shape languages <faq/why-linkml:why should i use linkml over shex/shacl?>`
* Generators:
   - [JSON-LD Context](../generators/jsonld-context)
   - [ShEx](../generators/shex)
   - [SHACL](../generators/shacl)
* RDF libraries and tools
   - [rdflib](https://github.com/RDFLib/rdflib) (Python)
   - [Apache Jena](https://jena.apache.org/)
   - [pyshex](https://github.com/hsolbrig/PyShEx)
   - [pyshacl](https://github.com/RDFLib/pySHACL)
