# FAQ: General

## Why does this project exist?

LinkML originally grew out of the needs of the Biolink Model project,
which needed a flexible schema representation for biological knowledge
graphs that was independent of particular database systems
(relational, triplestore, graph database) and serialization format
(TSV, JSON, RDF, RDFStar).

Recognizing similar needs elsewhere, Harold Solbrig took the original
Biolink metamodel and generalized it to create the BiolinkML framework. This was later named LinkML.

## Is LinkML stable?

The features of the core LinkML model are stable, you can use this to
describe your datamodel without fear of breaking changes.

The language is being continually extended to meet the needs of a
growing community.

Similarly, the LinkML toolchain is also growing.

Mappings between LinkML and other formalisms such as JSON-Schema and
ShEx may be currently incomplete, and these are continually being
improved, with plans to create new generators (e.g. for SHACL, and XSD)

## How is LinkML licensed?

All aspects of LinkML, from the core language itself to the toolchain
are in the public domain through a CC-0 waiver.

## Who uses LinkML?

A subset of groups using LinkML can be found via the 
[linkml-registry](https://linkml.io/linkml-registry/registry/)

## Is LinkML only for Python developers?

Definitely not! While the core framework is written in Python, and
there is strong support for Python developers in the form of
generation of Python dataclasses from a model, uses are not restricted
to Python developers.

For example, some users of LinkML compile their schema down to
JSON-Schema and then use JSON-Schema toolchains in their language of choice.

And note that there is increasing support for generating object models
in other languages, with java generators under active development!

## How do I cite LinkML?

A paper is in progress, for now, cite the GitHub repo

