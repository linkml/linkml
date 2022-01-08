# Working with RDF and LinkML

LinkML can be used to structure data housed as RDF triples, and to convert data between RDF and other forms.

Our philosophy is to allow reuse of semantic web and linked data tooling without forcing a commitment to the full RDF stack, which many developers find [daunting or off-putting](https://us2ts.org/2019/posts/program-session-x.html)

## Converting and validating RDF

Both `linkml-convert` and `linkml-validate` (see previous section) will work with RDF data. Any RDF serialization format that is supported by RDFLib can be used.

## JSON-LD

JSON-LD contexts can be generated from any LinkML schema. These are
compatible with the JSON objects that conform to the same schema. This
allows model developers to control both the shape of the JSON and how
it maps to RDF in a single model rather than having these be
disconnected.

When this JSON-LD context is combined with JSON it generates valid RDF

Note there are some features missing from JSON-LD generation:

 * `@type` information is not generated at all levels
 * `@embed` is not generated for JSON-LD framing, limiting the ability to translate from RDF to JSON

These should be addressed in future LinkML releases

## ShEx and SHACL

A ShEx or SHACL shapefile can be generated from any LinkML schema

 * [ShEx generator](https://linkml.io/linkml/generators/shex.html)
 * [SHACL generator](https://linkml.io/linkml/generators/shacl.html)

## OWL

OWL can be generated from an LinkML schema. Note that OWL has open
world-semantics which makes it less suitable for data structure
validation. However, generation of OWL can be useful for leveraging OWL tooling.
