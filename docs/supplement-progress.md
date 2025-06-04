---
orphan: true
---

# Maturing the LinkML framework to catalyze data interoperability
**Supplement RM1HG010860 - 03S1**
**PI: Christopher J. Mungall, LBNL**

## Progress for 2022-06-01 - 2023-05-31 (as of 2023-03-31)

### Aim 1. Enhance LinkML software engineering
We have made many improvements to features and functionality of the core framework, and made it easier for external developers to contribute.
Auxiliary tools in the LinkML organization (https://github.com/linkml)
that have been updated significantly in the past year include linkml_runtime (https://github.com/linkml/linkml-runtime)
with 82 merged pull requests, linkml_model (https://github.com/linkml/linkml-model) with 61 merged pull requests,
and schemasheets (https://github.com/linkml/schemasheets) with 23 merged pull requests.
Several new repositories were created in the LinkML organization including: linkml_transformer (https://github.com/linkml/linkml-transformer)
for subsetting and transforming models as they evolve, prefixmaps (https://github.com/linkml/prefixmaps)
for creating CURIE expansions, and linkml-renderer (https://github.com/linkml/linkml-renderer) for generating visualizations of LinkML compliant data.

### Aim 2. Expand the community of LinkML developers and adopters
We led a successful LinkML workshop at ICBO 2022: International Conference on Biomedical Ontology on 2022-09-25 (https://icbo-conference.github.io/icbo2022/workshops-and-tutorials/#linkml-workshoptutorial).

We have been running monthly LinkML Community Meetings since Dec 2022, drawing ~15-25 participants per month, including members of the community who are outside of our core team.
At these meetings we host tutorials on new features and have presentations from our community members about their LinkML usage.

We also interact with our community on our Slack channel and via a mailing list.
We have an active bug tracker (https://github.com/linkml/linkml/issues) with issues reported and fixed by both community members and the team,
and Q&A on StackOverflow: https://stackoverflow.com/questions/tagged/linkml.

As of 2023-03-27, the LinkML team has closed over 296 pull requests and 312 tickets in the main LinkML repository (https://github.com/linkml/linkml),
with 34 active contributors, 22 of which are community members.

A slide deck introducing LinkML is available at https://zenodo.org/record/7778641#.ZCesgezMKkh

### Aim 3. Demonstrate semantic interoperability
We started work on a shared data model provisionally called CMDR, and are working on a transformation tool to map to individual data models.
We are working on a tool that ingests and integrates using language models via the GTP-3 API.
