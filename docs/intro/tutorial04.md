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

```{literalinclude} ../../examples/tutorial/tutorial04/data.ttl
:language: turtle
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

```{literalinclude} ../../examples/tutorial/tutorial04/data-semantic.ttl
:language: turtle
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

```{literalinclude} ../../examples/tutorial/tutorial04/personinfo-semantic.context.jsonld
:language: json
```

NOTE: currently you need to declare your own type object and map this to `rdf:type` for typing information to be shown

## Using Shape Languages

In the previous section we saw how to use JSON-Schema validators. LinkML also allows the use of ShEx (future versions will allow SPARQL)


```bash
gen-shex --no-metadata personinfo-semantic.yaml
```

Outputs:

```{literalinclude} ../../examples/tutorial/tutorial04/personinfo-semantic.shex
:language: shex
```


```bash
gen-shacl --no-metadata personinfo-semantic.yaml > personinfo.shacl.ttl
```

Outputs:

<!-- compare_rdf -->
<!-- NOTE: the order of properties is non-deterministic so we cannot compare string directly>
```{literalinclude} ../../examples/tutorial/tutorial04/personinfo-semantic.shacl.ttl
:language: turtle
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
