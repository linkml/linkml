# Symposium 2026 Abstracts

Abstracts are listed in the same order as the [schedule](symposium-2026-schedule.md).

```{contents} Jump to an Abstract
:local:
:depth: 2
:backlinks: none
:class: this-will-duplicate-information-and-it-is-still-useful-here
```

## Session 1: Schemas & domain modelling

### Running LinkML in Production at the Human Tumor Atlas Network

- **Presenter:** Aditi Gopalan
- **Affiliation:** Sage Bionetworks
- **Project:** [github.com/ncihtan/htan2-data-model](https://github.com/ncihtan/htan2-data-model)

The Human Tumor Atlas Network (HTAN) is a National Cancer Institute-funded program developing multimodal atlases of human cancers. For HTAN Phase 2, we rebuilt the data model in LinkML, creating twelve modules that cover clinical, biospecimen, sequencing, single-cell, imaging, spatial omics, and mass spectrometry imaging data. These modules are organized as an inheritance chain, starting from a shared core file class and extending to specific assay classes. This talk will focus on the schema tooling. We convert each LinkML class into a flat Draft-07 JSON Schema, which Synapse uses for project metadata validation. Large vocabularies, such as ICD-O-3, are generated from upstream ontology releases at build time rather than maintained manually. Each build generates reports on added and obsolete terms. Schema pull requests undergo multi-agent LLM review to check inheritance and test coverage against repository rules. We will share our successes, challenges, and key lessons learned.

### LinkML everything: How are we turning hundreds of ontologies to LinkML

- **Presenter:** Kacper Grzymkowski
- **Affiliation:** NeverBlink
- **Project:** [github.com/NeverBlink-OSS/ohi](https://github.com/NeverBlink-OSS/ohi)

While more ontology languages have appeared recently, most existing ontologies are still only available in OWL. Conversions to LinkML have so far been mostly done by hand or on a case-by-case basis. Our earlier work on SAREF-LinkML showed that ontologies can be converted with good results, but left open the question whether the approach can be scaled.

This question became practical with ohi.dev, a package manager for ontologies, which needs hundreds of ontologies, in many formats. To solve it, we developed OWL tooling for ohi LinkML, and applied it to a large corpus of ontologies.

The talk will focus on conversion fidelity: which constructs are preserved, and which are lost. We then analyse the main sources of failure: limits in LinkML expressivity, and quality problems in the source ontologies. For each, we describe the strategies we used to recover as much information as possible.

The results give an empirical picture of how well OWL and LinkML map onto each other in practice, and point to concrete improvements for both the conversion tools and ontology publishing practices.

### Aligning OKN Graphs with LinkML Representations

- **Presenter:** Mahir Morshed
- **Affiliation:** Renaissance Computing Institute
- **Project:** [github.com/frink-okn/schema-gen](https://github.com/frink-okn/schema-gen)

This session discusses representing ontologies and detailed relationship statistics of RDF graphs in the Open Knowledge Network (okn.us, formerly the Proto-OKN) in the LinkML schema format. Although this representation primarily assists in identifying opportunities for entity and predicate alignment across those graphs, the session also goes over automatic graph documentation based on entity metadata, linking schemas made for fundamental RDF ontologies for dependency tracking, and ultimately assisting external tools to optimize SPARQL query construction by reducing exploratory effort. The session will also cover some challenges in coercing arbitrary RDF to use the LinkML metamodel, including OWL restrictions, multi-class domains and ranges, and redundancy due to inferred triples, as well as customizations to LinkML runtime processing scripts that try to handle some of these.

### DCAT-AP+ & ChemDCAT-AP: Building domain-specific subprofiles of DCAT-AP with LinkML

- **Presenter:** Philip Strömert
- **Affiliation:** TIB & NFDI4Chem
- **Project:** [nfdi-de.github.io/dcat-ap-plus/latest](https://nfdi-de.github.io/dcat-ap-plus/latest/)

DCAT-AP+ is a LinkML-based extension of the DCAT Application Profile 3.0 that adds a provenance layer for describing how a dataset was generated and what it is about, using the Starting Point Terms of PROV-O, the QUDT ontology, and Dublin Core Terms.

DCAT-AP+ is domain-agnostic. It provides a generic set of classes and properties that any domain can import and specialize into its own DCAT-AP conformant application profile. ChemDCAT-AP is the first such domain profile, built for chemistry and catalysis research data.

### Common practices for interoperable LinkML schemas in the bioimaging community

- **Presenter:** Damien Goutte-Gattat
- **Affiliation:** German BioImaging e.V.
- **Project:** [github.com/gouttegd/linkml-guidelines](https://github.com/gouttegd/linkml-guidelines)

Several projects in the bioimaging community have adopted or are on the verge of adopting LinkML as the schema definition language of choice to formally describe imaging (meta)data. For example, the QUAREP-LiMi Consortium is migrating its model for image acquisition metadata from XML Schema to LinkML; the Imaging-PHD project will use LinkML to define its Persistent Hardware Descriptors; and LinkML is under consideration to define at least parts of the Next Generation File Format (OME-NGFF, aka “OME-Zarr”).

This broadening adoption creates a need to ensure that independently developed LinkML schemas are interoperable. To that effect, we are establishing a set of guidelines and recommendations for schema authors, that we propose as a complement to LinkML’s own documentation. The guidelines aim to promote schemas that are easily reusable, composable, and extensible while preserving backward, and ideally forward, compatibility.

## Session 2: Public-sector, library, geo & cross-domain schemas

### Making the “Common” in CDEs More Common Using LinkML and Microschemas

- **Presenter:** Anne Thessen
- **Affiliation:** University of North Carolina Chapel Hill
- **Projects:** [github.com/linkml/linkml-microschema-profile](https://github.com/linkml/linkml-microschema-profile), [github.com/linkml/clinical-microschemas](https://github.com/linkml/clinical-microschemas), [github.com/linkml/bdc-variable-library](https://github.com/linkml/bdc-variable-library)

A Common Data Element (CDE) is a standardized representation of a measurement or survey question and its permissible answers. CDEs were designed to facilitate interoperability across biomedical studies, but do not yet meet this computability need. Working with CDEs is largely manual, constrained by partially overlapping CDEs and metadata that are implied rather than explicit, limiting interoperability at scale. To address this, we developed a generalizable LinkML microschema that defines an observation as a key-value pair. From this, we created clinical microschemas for numerical measurements, disease status, procedure status, and drug exposures, specifying required metadata, units, and plausible value ranges. We are applying these microschemas to the NHLBI BioData Catalyst ® (BDC) to test their efficacy for cross-study data integration. We will also create environmental microschemas to test cross-domain interoperability, linking clinical and geospatial data. We aim to show that a computationally actionable CDE can support data validation and integration across disciplines at scale.

### LinkML Common Data Element Microschemas to Support Reuse of Myositis Clinical Research Data

- **Presenter:** Matthew Diller
- **Affiliation:** National Library of Medicine
- **Project:** [github.com/NIH-NLM/myositis_cdes](https://github.com/NIH-NLM/myositis_cdes)

The National Institutes of Health (NIH) Strategic Plan for Data Science promotes the use of common data elements (CDE) to enhance research data interoperability and reuse in adherence with FAIR principles. CDEs are standardized pairs of questions and allowed responses that are intended to be reused in multiple studies. Recently, US Congress appropriated funding for the development of CDEs for chronic autoimmune diseases to help accelerate clinical research in this area. However, NIH CDEs specific to the instruments and assessments used for myositis research have not yet been developed. To address this need, we are working with the International Myositis Assessment and Clinical Studies (IMACS) Group to develop CDEs for the myositis research community. To enhance the interoperability and reusability of these CDEs, we used LinkML to develop data representation design patterns (i.e., bundles) that we mapped to ontologies and OMOP. In total, we developed 852 CDEs in LinkML that are being deposited for reuse in REDCap electronic data capture forms and the NIH CDE Repository.

### Generating the Human Reference Atlas KG

- **Presenter:** Bruce W. Herr II
- **Affiliation:** Indiana University
- **Project:** [humanatlas.io](https://humanatlas.io)

The Human Reference Atlas (HRA) for the healthy, adult body is being developed by a team of international, interdisciplinary experts across 25+ consortia. It provides standard terminologies and data structures for describing specimens, biological structures, and spatial positions of experimental datasets and ontology-linked reference anatomical structures (ASs), cell types (CTs), and biomarkers (Bs). The presentation explains how the HRA Knowledge Graph is constructed including its extensible architecture, LinkML usage, automated normalization, enrichment, and publishing pipeline, Linked Open Data deployment, and access through SPARQL, REST APIs, and interactive applications.

### Heritage/Data Custodian

- **Presenter:** Simon Kemper
- **Affiliation:** National Archives of the Netherlands, TextPast
- **Project:** [github.com/netwerk-digitaal-erfgoed/heritage_custodian](https://github.com/netwerk-digitaal-erfgoed/heritage_custodian)

The heritage custodian (bronhouder in Dutch) model was developed by us for the Netwerk Digitaal Erfgoed (NDE) last year to capture the properties of organisations and groups managing collections. The model conveys the work involved in looking after collections, including acquisition, accessioning, preservation, enrichment and access. It also expresses the ever-changing shape of heritage organisations, their teams and their infrastructure. Inspired by the work on enterprise engineering by late Jan Dietz, we are currently exploring the extension of this model into a general data custodian model that can also be applied outside the field of heritage.

The model is expressed through LinkML to allow conversions from our data lakehouse to property-, multi- and hypergraphs. The schemata are altered through automated updates of infrastructural and organisational data as well as manual edits through dashboards. Changes to the schemata alter how data flows through the databases connected to the application.

### SOMA: An Open Framework for Linking Outcomes, Measurements, Assays, and Evidence Across Biological Scales

- **Presenter:** Sierra Moxon
- **Affiliation:** Lawrence Berkeley National Laboratory
- **Project:** [github.com/EHS-Data-Standards](https://github.com/EHS-Data-Standards)

Developing analyses for environmental applications requires integrating evidence across biological scales, from molecular perturbations and cellular responses to animal observations, clinical measurements, and adverse health outcomes. Although existing resources capture portions of this information, linking outcomes, measurements, assays, and supporting evidence in a consistent, computable manner remains challenging.

To address this need, we developed the Schema for Outcomes, Measurements & Assays (SOMA), a flexible framework for representing relationships among biological outcomes, measurements, assays, and evidence. By incorporating multiple community standards, SOMA facilitates interoperability across platforms and datasets through an open, computable representation. The resulting framework supports the reuse of alternative and emerging methods across domains while preserving the contextual information needed to compare results.

## Session 3: Tools, generators & workflows I

### Term Harvester

- **Presenter:** Damion Dooley
- **Affiliation:** Simon Fraser University
- **Project:** [github.com/ClimateSmartAgCollab/term-harvester](https://github.com/ClimateSmartAgCollab/term-harvester/)

Data specifications need to draw upon established or defacto-standards for measurement and metadata variable content, including picklists. Many diverse sources of controlled vocabulary may be referenced, ranging from ontologies to SKOS vocabularies like AGROVOC, terminology portals like BioPortal or EMBL-EBI Ontology Lookup Service, and even web pages like STATSCAN or pdf documents from USDA. Organizing and keeping up-to-date controlled vocabulary from all these sources is quite a challenge. The term_harvester.py script and its growing library of document or API fetch-and-parse scripts enable retrieval of known-good vocabulary according to a configuration file for use by a particular project or more broadly, by an agency.

Term library management mainly involves priming a configuration file for each desired term source, downloading or refreshing the source's document files, processing each into its LinkML YAML representation, and assembling them into a single schema.yaml file. Features include versioning, term translations, term/branch include & minus, and AI parsing of free-text.

### LinkML Explorer: A highly interactive visualization tool for understanding schemas

- **Presenter:** Sigfried Gold
- **Project:** [github.com/Sigfried/dynamic-model-var-docs](https://github.com/Sigfried/dynamic-model-var-docs)

Understanding containment hierarchies and part-whole relationships between classes is essential for complex schemas, but it becomes difficult as they grow. Users need to see how classes fit together and determine what belongs to what. However, a standard class-ranged slot in LinkML does not inherently specify whether its domain class contains its range class or is contained by it.

LinkML Explorer shows these relationships (<https://sigfried.github.io/dynamic-model-var-docs?tour=ownership>) based on has-part/part-of specifications in the schema or rules in a separate configuration file.

The application allows users to selectively render classes in a left-to-right ownership diagram. Each class is presented as a node displaying its slots, with directed edges tracking the precise relationship from the source slot to the target class. This interactive visualization offers significant advantages over static documentation by improving navigation efficiency (eliminating page-to-page clicking), thoroughness, and cognitive legibility.

### Standardizing Prefixes, CURIEs, and URIs in LinkML Schemas with the Bioregistry/Semantic Farm

- **Presenter:** Charles Tapley Hoyt
- **Affiliation:** RWTH Aachen University
- **Project:** [github.com/biopragmatics/bioregistry](https://github.com/biopragmatics/bioregistry/)

LinkML schemas have a first-class notion of a prefix map, which connects CURIE prefixes to URI prefix expansions. The Bioregistry (and its domain-agnostic counterpart, the Semantic Farm) provides an actionable standard for CURIE prefixes and URI prefixes. This presentation introduces a new workflow for validating the prefix map in a given LinkML schema and suggesting improvements to bolster the schema's semantic interoperability. It's available through the Bioregistry Python package and CLI (bioregistry validate linkml).

For further reading, see <https://cthoyt.com/2026/01/06/bioregistry-linkml-validation.html>

### Tesserops: computable collaboration infrastructure

- **Presenter:** Julie McMurry
- **Affiliation:** University of North Carolina Chapel Hill
- **Project:** [github.com/collabri-community/core](https://github.com/collabri-community/core)

Collabri Core (<https://collabri-community.github.io/>) is a LinkML vocabulary for contract-scoped statements of work and the budgets that fund them. It defines a shared work hierarchy (task team → task → subtask → typed deliverables), structured evaluation (objectives, metrics, acceptance criteria), payment and cost bases, and a first-class change layer so amendments are addressable and versioned—not buried in prose. The goal is one unambiguous exchange model that sponsors, primes, and performers can validate and reuse across tools.

Tesserops is a purpose-built operations platform for sponsored research collaborations. It puts Collabri Core into day-to-day practice: shared SOWs, progress tracking, billing and claims, membership and training, and related coordination workflows for multi-org programs (e.g. RAPID, CLAD). Core stays the portable contract language; Tesserops is the living system of record and workflow surface that executes against it.

### Native semantic storage: TypeDB as a LinkML store

- **Presenter:** Alex Walker
- **Affiliation:** TypeDB
- **Project:** [github.com/typedb/typedb](https://github.com/typedb/typedb)

LinkML and TypeDB were built independently but ended up making many of the same design choices. LinkML's classes, slots and hierarchies align closely with the inheritable entities, attributes, and multi-role relations of TypeDB.

We present the end-to-end toolchain connecting the two ecosystems: compiling LinkML schemas to TypeQL; a TypeDB backend adapter in linkml-store; and reverse schema generation to export TypeDB databases into LinkML. We demonstrate concrete mapping patterns on the kinds of complex association models that come up time and time again in scientific datasets. We share thoughts on practical divergences like mixins, and show how the integration provides LinkML with an expressive runtime database while also giving TypeDB a standardised schema ecosystem. And at the end, we'll discuss possible next steps for the project.

### LinkML and Apache Ossie (incubating): two approaches to semantic modeling

- **Presenter:** Piotr Sowiński
- **Affiliation:** NeverBlink
- **Project:** [linkml.ohi.dev](https://linkml.ohi.dev/)

Apache Ossie (incubating), formerly OSI, is a new open initiative, creating specifications for exchanging semantic metadata between analytical and AI systems. Ossie is supported by many leading companies in data, AI, and finance. Ossie’s ontology layer describes business concepts, with mappings to BI metrics. LinkML, as a general-purpose modelling language addresses an overlapping problem. As both communities grow, it is worth asking how closely the two languages align and how to make them interoperable.

We will first give a short introduction to Ossie, followed by a comparison with LinkML, identifying constructs that map directly, and those that do not.

To put this into practice, we built converters in both directions, in ohi LinkML. They are currently being upstreamed both in LinkML and Ossie. With them, we evaluate round-trip conversion fidelity on a large corpus of LinkML schemas.

We will close with a discussion of where the two communities could align, including metamodel features, handling non-standard extensions, and common tooling.

## Session 4: LinkML × AI / agentic

### litschema: Turn a folder of PDFs into a dataset you can defend

- **Presenter:** Cory Levinson
- **Affiliation:** UC Davis
- **Project:** [github.com/clevinson/litschema](https://github.com/clevinson/litschema)

Evidence synthesis, from systematic reviews to meta-analyses, depends on data extracted by hand from hundreds of papers, a slow step that limits how often syntheses get done and updated. AI agents can now do this extraction in minutes, but there's a gap in auditability: their output is only useful if a researcher can check each value against its source and defend it to others. Litschema is a tool for that trusted extraction layer. Researchers define what to extract as a LinkML schema, written themselves or co-designed with an agent from a sample of their papers. An agent then extracts each paper into the schema, citing for every value the exact lines of the paper it came from along with its reasoning, and a second, independent model scores how likely each value is to be correct. Researchers audit the values in a web app against the lines and paragraphs they cite, starting with the ones flagged as doubtful, and every decision is recorded in git. The result is a dataset where each value traces back to a sentence in a paper and a human who checked it.

### Machine-Actionable Datasheets for Datasets: Schema-Guided Agentic Extraction from Project Documentation

- **Presenter:** Marcin Joachimiak
- **Affiliation:** Lawrence Berkeley National Laboratory
- **Project:** [github.com/bridge2ai/data-sheets-schema](https://github.com/bridge2ai/data-sheets-schema)

Scientific dataset documentation is scattered across publications, protocols, and repositories, making context difficult to recover and reuse. We present a workflow that combines a modular LinkML schema, semantic mappings, and schema-guided agentic AI extraction to generate machine-actionable Datasheets for Datasets (D4D). The workflow integrates document preprocessing, structured generation, deterministic validation, rendering, and rubric-based evaluation. We apply it to four NIH Bridge2AI resources (AI-READI, CHORUS, CM4AI, and VOICE), assessing full and D4D-Core records in 32 evaluations across four rubrics. Mean scores ranged from 91.0–97.3% for field presence and compliance and 79.0–94.3% for semantic quality. The open schema and toolchain provide researchers, curators, and repositories with reusable resources to create, review, and exchange dataset documentation. Future D4D work will expand metadata integration, collaborative curation, and evaluation across scientific domains.

### Knowledge Trust Ladder

- **Presenter:** Noel McLoughlin
- **Affiliation:** Open Engineering / TD Bank
- **Project:** [github.com/noelmcloughlin/knowledge-trust-ladder](https://github.com/noelmcloughlin/knowledge-trust-ladder)

Knowledge Trust Ladder keeps a repository's scattered knowledge as a collection: catalogued, authenticated and explained, with the trust in every claim left visible

### Fixing category errors in single cell annotation

- **Presenter:** Sid Cox
- **Affiliation:** Broad
- **Project:** [broadinstitute.github.io/warp/docs/Pipelines/scANVI_Pipeline/README](https://broadinstitute.github.io/warp/docs/Pipelines/scANVI_Pipeline/README)

Modern single-cell reference atlases combine high-throughput transcriptomic measurements with multi-level biological taxonomies and curated ontologies. In the Allen Institute and BICAN Whole Mouse Brain consensus atlas (AIT33), 7.64 million cells across 372 donors are organised into five nested levels of detail: 9 neighbourhoods at the top, 43 classes, 414 subclasses, 1,386 supertypes, and 6,721 clusters at the leaf level, cross-referenced to the Cell Ontology (CL) and the Uberon anatomy ontology. In production pipelines such as Broad DSP's WARP scANVI workflow, semi-supervised deep generative models take raw transcript counts across 21,205 genes and assign cell-type labels at each level of this taxonomy.

When cell-type predictions are exported into downstream tables, knowledge graphs, or ontology files, data pipelines routinely commit a category error: they collapse three fundamentally different kinds of statement into a single representation.

### ohi.dev: An ontology and LinkML schema package manager, for humans and agents

- **Presenter:** Alireza Furutanpey
- **Affiliation:** NeverBlink
- **Project:** [ohi.dev](https://ohi.dev)

Ontologies are meant to be reused, but in practice reuse is difficult. They are published across many institutional websites, their locations change and websites go down, versions are unclear, and they are available in only one or two formats. As a result, both people and AI agents often create new terms instead of reusing established ones.

ohi.dev addresses this by treating ontologies as versioned packages. It provides a searchable catalog of hundreds of ontologies, with explicit versions, recorded dependencies, and files in multiple formats, including LinkML. Users can search the catalog, inspect an ontology’s metadata, download a specific version in the format they need, and record their choices in a project file that keeps ontology files consistent and reproducible.

In this talk we explain the problem ohi.dev solves and show the main ways to use it, from single searches on the command line to managing the ontologies of a whole project. We then demonstrate how AI agents can use ohi.dev as a tool, through sample workflows, and what are the benefits of this approach.

### A Shared LinkML Metadata Schema for FAIR, Machine-Actionable Scientific Data, Models, Agents, and Resources

- **Presenter:** Diana McSpadden
- **Affiliation:** Thomas Jefferson National Accelerator Facility
- **Project:** [doi.org/10.18141/3376151](https://doi.org/10.18141/3376151)

As AI, scientific machine learning, and agentic workflows become central to Department of Energy (DOE) science, machine-actionable metadata must cover not only datasets but also models, agents, software, and computing resources. This talk presents a shared LinkML-based framework and extensible “xCards” for describing these resources. Each card pairs validated structured data with human-readable context, enabling automated processing and understanding. FAIR-aligned features include discovery, access, interoperability, reuse, governance, and AI use. Controlled vocabularies, persistent identifiers, and typed relationships connect artifacts into a navigable scientific resource network. Relationships such as is derived from, is trained on, processes, and runs on support provenance, workflow composition, and grounded agent reasoning. Governance, sensitivity, licensing, and access details enable responsible reuse by humans and machines. The presentation covers the schema, standards alignment, validation tools, and integration with emerging xCard registries and discovery services.

## Session 5: Tools, generators & workflows II

### DataHarmonizer 2.0

- **Presenter:** Damion Dooley
- **Affiliation:** Simon Fraser University
- **Project:** [github.com/cidgoh/DataHarmonizer](https://github.com/cidgoh/DataHarmonizer/)

Data Harmonizer is a standardized browser-based tabular data editor and validator that can be run offline and which directly implements LinkML data specifications. This open source project, created by the Centre for Infectious Disease Genomics and One Health (CIDGOH) at Simon Fraser University, has also taken in contributions from the LinkML development team and others. The previous 1.0 version application's theory and design paper, which introduces DataHarmonizer's initial epidemiology data sharing standardization mission, is available at <https://doi.org/10.1099/mgen.0.000908>, and a <https://www.youtube.com/watch?v=rdN2_Vhwb8E> video illustrate various features such as versioning and ontology-mapped picklists that resolve traditional spreadsheet limitations.

DataHarmonizer's 2.0 vision will be demonstrated - the smooth incorporation of multiple tab and sub-tab user interface in 1-to-many relationships, such that sample/subsample/test result or other hierarchies of records can be managed. DataHarmonizer provides a way to edit the very LinkML schemas that specify such relationships!

### LinkML is Relatable

- **Presenter:** James Overton
- **Affiliation:** Knocean Inc.
- **Project:** [github.com/rltbl/relatable](https://github.com/rltbl/relatable)

Relatable is a new tool for connecting your data. Backed by a SQL database, it handles large collections of messy data while you clean them and connect them to terminologies and ontologies. We will demonstrate how you can use your LinkML schema with a Relatable project to load, validate, edit, and share your data.

### ohi LinkML: a modern tool stack for LinkML

- **Presenter:** Piotr Sowiński
- **Affiliation:** NeverBlink
- **Project:** [linkml.ohi.dev](https://linkml.ohi.dev/)

Data models often need to be reused across many platforms, processed quickly, and turned reliably into code. LinkML is a mature language for semantic modelling, but its first implementation is written in Python. This makes it hard to use in the JVM or web browsers, and too slow for interactive apps or huge schemas.

This talk presents ohi LinkML, an open-source (Apache 2.0) implementation of LinkML written in Scala. It runs on the JVM, in JavaScript, Python, C, C++ and Rust, and on the command line. It covers schema importing, derivation, validation, and code generation, and usually runs 10–100x faster than the Python implementation.

We describe the architecture of ohi LinkML and how we keep it reliable: 10,000+ tests, a model zoo of 100+ schemas, and fuzz testing. We also cover new features, such as support for multilingual schemas. To show the project’s development pace, we present a timeline of its releases and major features.

Finally, we report on real-world enterprise deployments, and outline ongoing work on further features and interoperability with LinkML-Python.

### From Spec to Study: LinkML-Map in Production with dm-bip

- **Presenter:** Corey Cox
- **Affiliation:** University of North Carolina Chapel Hill
- **Project:** [github.com/linkml/dm-bip](https://github.com/linkml/dm-bip)

LinkML-Map lets you describe, in a YAML specification, how data in one LinkML schema maps to another, and then run that mapping. dm-bip is an ingest pipeline built on it, first deployed to harmonize dbGaP studies for NHLBI BioData Catalyst. This talk covers what happened when a declarative mapping tool met large, messy, real-world cohorts, and the changes that pushed into LinkML-Map for every user. We’ll close with where both are headed: dm-bip as a general-purpose ingest pipeline, and spec writing that scales past hand-written YAML.

### From Pydantic to LinkML without changing the schema: migrating the DANDI archive metadata models

- **Presenter:** Yaroslav Halchenko
- **Affiliation:** Center for Open Neuroscience
- **Project:** [github.com/dandi/dandi-schema](https://github.com/dandi/dandi-schema/)

DANDI is the NIH BRAIN Initiative archive for neurophysiology data: over 1,200 datasets (over 2.5 PB) in NWB, Zarr, BIDS, etc. Its metadata schema, dandi-schema, describes datasets and their assets, and has been maintained as Pydantic models with custom Python validators. JSON Schema and a JSON-LD context are generated from those models. These validate submissions in the Python/command-line client and the archive backend, and drive the web metadata editor and dataset landing pages. Constraints written as Python code never reach JSON Schema, and every component is pinned to one schema version, so we maintain upgrade and downgrade migrations.

We present our ongoing move to LinkML as the source of truth. We reduce Pydantic-specific constructs, convert the models automatically with our pydantic2linkml tool plus hand-written overlays, regenerate Pydantic and JSON Schema from LinkML. The aim is a change of representation only, leaving the schema itself "effectively" untouched for the moment of transition. We will share the workflow and some gotchas we hit in our way.
