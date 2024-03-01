# FAQ: General

## Why does this project exist?

LinkML originally grew out of the needs of the [Biolink-Model](https://w3id.org/biolink/) project,
which needed a flexible schema representation for biological knowledge
graphs that was independent of particular database systems
(relational, triplestore, graph database) and serialization format
(TSV, JSON, RDF, RDFStar).

Recognizing similar needs elsewhere, [Harold Solbrig](https://github.com/hsolbrig) took the original
Biolink metamodel and generalized it to create the original BiolinkML framework.
This was later named LinkML.

## Is LinkML stable?

The features of the core LinkML model are stable, you can use this to
describe your data model without fear of breaking changes.

The language is being continually extended to meet the needs of a
growing community. New language features are always added to be
backwards compatible with existing schemas.

Similarly, the LinkML toolchain is also growing. The core toolchain
is in Python, but efforts are underway to build tooling in Java, Typescript,
and Go. Some language features may be unsupported in some toolchains.

## How is LinkML licensed?

All aspects of LinkML, from the core language itself to the toolchain
are in the public domain through a CC-0 waiver.

## Who uses LinkML?

A subset of groups using LinkML can be found via the
[linkml-registry](https://linkml.io/linkml-registry/registry/).
However, we do not have the resources to track all uses,
and the registry only scratches the surface of current usage.

LinkML is used in a number of major database resource projects. Many
of these are centered around genomics and managing complex biological
or environmental data, but the framework is completely domain neutral.

Users include:

* The National Microbiome Data Collaborative
* The Center for Cancer Data Harmonization
* The Alliance of Genome Resources
* The Biomedical Data Translator project
* The iSamples project
* The NIH INCLUDE project

See [Examples of use](https://linkml.io/linkml/examples.html) for more
info on current uses.

## Is LinkML only for Python developers?

Definitely not! While the core framework is written in Python, and
there is strong support for Python developers in the form of
[generation of Python dataclasses](/generators/python) from a model, uses are not restricted
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
here in the [OBO Foundry](https://obofoundry.org) community, where
many non-technical curators autonomously manage their ontologies in
GitHub.

We aim to make this whole process easier for curators, data modelers,
and inexperienced developers. See the [getting help](getting-help)
section for info on how to get assistance.

## Is LinkML just for metadata?

LinkML doesn't draw any hard and fast distinction between data and
metadata, recognizing that "metadata" is often defined in relative
terms.

Our position is nicely summarized by [this
paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5819722) on the
Immune Epitope Database (IEDB):

_Several of the FAIR principles make a distinction between data and metadata. This distinction makes immediate sense for knowledge repositories that store raw data in a standardized format, such as sequence reads in FASTQ format in the Sequence Read Archive (SRA) or Flow Cytometry Standard files in FlowRepository. Such ‘data’ must be accompanied with ‘metadata’ on how the data were generated. For example, in the case of an SRA deposition, information on what sample was being sequenced would be considered ‘metadata’, and specific sequence reads would be considered ‘data’. However, in the case of the information stored in the IEDB, there is no separation between data and metadata. Arguably, the IEDB stores only metadata, and the raw data can be found in the original journal article, typically in the form of figures or tables that follow no specific convention._

Full reference:

Vita R, et al. **FAIR principles and the IEDB: short-term improvements and a long-term vision of OBO-foundry mediated machine-actionable interoperability**. _Database (Oxford)_. 2018 Jan 1;2018:bax105. doi: [10.1093/database/bax105](https://doi.org/10.1093/database/bax105). PMID: 29688354; [PMC5819722](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5819722)

## Is LinkML suitable for high volume datasets?

The current main serialization formats for LinkML are JSON, YAML, RDF,
as relational databases. These may not be the most appropriate
serializations for high volume data such as brain imaging data, high
throughput instrumentation readouts, satellite data, etc.

If your use case falls into this scenario, one option is to separate
"data" and "metadata" (but see the previous question) and use LinkML
for the descriptive aspects.

You may also be interested in using metadata-aware high-volume
frameworks such as [HDMF](https://hdmf.readthedocs.io/) or [NetCDF](https://www.unidata.ucar.edu/software/netcdf/).

The LinkML N-Dimensional Array (NDArr) working group, consisting of
developers from LinkML and HDMF teams are currently actively working
towards a solution that enables LinkML to be used in conjunction with
serializations such as HDF5 and Zarr.

## How do I cite LinkML?

A paper is in progress, for now, cite the GitHub repo
