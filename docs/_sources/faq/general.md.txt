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

LinkML is used in a number of major database resource projects. Many
of these are centered around genomics and managing complex biological
or environmental data, but the framework is completely domain neutral.

Users include:

* The National Microbiome Data Collaborative
* The Center for Cancer Data Harmonization
* The Alliance of Genome Resources
* The Biomedical Data Translator project
* The iSamples project

See [Examples of use](https://linkml.io/linkml/examples.html) for more
info on current uses.

## Is LinkML only for Python developers?

Definitely not! While the core framework is written in Python, and
there is strong support for Python developers in the form of
[generation of Python dataclasses](../generators/) from a model, uses are not restricted
to Python developers.

For example, some users of LinkML compile their schema down to
JSON-Schema and then use JSON-Schema toolchains in their language of choice.

And note that there is increasing support for generating object models
in other languages, with java generators under active development!

## Do I need to be a developer to use LinkML?

You don't need to be a developer to use LinkML. You can create schemas
without writing any code.

For now it helps to have some basic familiarity with core data
modeling concepts, and the basics of object-oriented design. In future
we will add additional training material for non-modelers giving a
gentle introduction to these topics.

LinkML schemas are maintained as YAML files, so it helps to have some
basic understanding of YAML syntax. Many developers will use IDEs for
editing YAML, which helps avoid a lot of common pitfalls. You may want
the advice of a local friendly developer on what a good YAML editing
environment is for your workflow.

[schemasheets](https://github.com/linkml/schemasheets) is a tool that
allows schemas to be edited as google sheets or excel files. Currently
it still takes a little bit of technical expertise to get up and
running though.

We recommend managing all of your schema products using GitHub. If you
have not used GitHub or version control systems before, this may be a
little daunting. You may need some assistance from someone technical
to get you set up with a workflow here. There is a lot of expertise
here in the OBO Foundry community, where many non-technical curators
autonomously manage their ontologies in GitHub.

We aim to make this whole process easier for curators, data modelers,
and inexperienced developers. See the [getting help](getting-help)
section for info on how to get assistance.


## How do I cite LinkML?

A paper is in progress, for now, cite the GitHub repo

