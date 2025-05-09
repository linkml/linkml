# How to run a collaborative data modeling project

This document describes how to run a collaborative data modeling project using the [LinkML](https://linkml.io) modeling language.

This guide is intended to serve as a practical how-to for running a collaborative data modeling project,
adaptable to the diverse needs of different projects.
Whether you're tackling a small, focused endeavor or a large-scale, multi-organizational initiative,
the principles and practices outlined here can be tailored to your project's unique requirements.

Our aim is to provide a straightforward, actionable set of guidelines that balance the technical aspects
of data modeling with the nuances of collaborative work.
You'll find insights on initiating and planning your project, managing contributions,
and maintaining effective communication and governance.

Remember, the success of a data modeling project hinges on a well-coordinated blend of technical
proficiency and collaborative synergy.
This guide is designed to equip you with the essentials for navigating these complexities efficiently.

This guide is a work in progress, and in the spirit of the guide itself, we welcome comments ([issue 1744](https://github.com/linkml/linkml/issues/1744))
and pull requests.

## Sources

In this guide we draw from:

- The O3 guidelines: [Open code, open data, and open infrastructure to promote the longevity of curated scientific resources](https://osf.io/vuzt3/)
- The [OBOOK](https://oboacademy.github.io/obook), and in particular [How to be an Open Science Engineer - maximising impact for a better world](https://oboacademy.github.io/obook/howto/open-science-engineer/)
- The TISLab collaboration guide (link TBD)

## Principles

### Version Control Your Schema

(adapted from [O3 guidelines](https://osf.io/vuzt3/))

Version control systems like git track changes in files and enable multiple users to collaborate. They are widely used for maintaining code,
but can (and should) also be used to maintain and manage data, metadata, ontologies, schemas, and other semantic artifacts.

Some projects may opt to manage their data alongside the schema in the same repo. This may be a good pattern
for "registry" style projects, but in other cases the data may be best managed separately in a dedicated
store or a repository like Zenodo or Figshare.

### Permissively License Your Code and Data

(adapted from [O3 guidelines](https://osf.io/vuzt3/))

Using recognizable, permissive licenses (e.g., CC0, CC BY) encourages contribution and ensures content longevity.
Non-permissive licenses or custom terms can hinder reuse and engagement.
Permissive licensing doesn't typically lead to a lack of credit for the original resource.

CC0 and CC BY are good for non-code resources; code should be licensed with a permissive software license such as Apache-2.0 (used in the [linkml repo](https://github.com/linkml/linkml/blob/main/LICENSE)), BSD-3, or MIT.

### Use Technical Workflows (Automation) and Social Workflows

(adapted from [O3 guidelines](https://osf.io/vuzt3/))

Automating quality control, generation of artifacts, releases, and deployment helps in maintaining and contributing to projects.
This includes using continuous integration for quality checks, automating the generation of data views, and packaging data and code for easy deployment.

The [LinkML Cookiecutter](https://github.com/linkml/linkml-project-cookiecutter/) provides a template for a project that
includes a number of automation features using GitHub actions.

Implementing social workflows through tools like GitHub enhances community engagement.
Transparent discussion forums, giving credit to contributors, and using issue trackers and discussion boards are crucial for maintaining a dynamic and active contributor base.

Document or reference best practices for contributing to the schema. This includes things such 
as [keeping issues and pull requests small and atomic](https://codeinthehole.com/tips/advanced-pull-request-crafting/).

### Establish Project Governance

(adapted from [O3 guidelines](https://osf.io/vuzt3/) and TisLab guide)

Clear governance defines roles, responsibilities, and behavior expectations in a project.
Establishing codes of conduct, standard operating procedures, and guidelines for administration and contribution roles is vital.
Governance should evolve over time to meet the project's needs.

You may wish to use an existing governance model or community documents as a starting point for your project:

- Bioschemas [community](https://bioschemas.org/community/) and [governance](https://github.com/Bioschemas/governance/blob/master/governance.md) docs
- [Biolink](https://biolink.github.io/biolink-model/) 
- schema.org [how we work](https://schema.org/docs/howwework.html)
- [GA4GH Constitution](https://www.ga4gh.org/constitution/)
- [Bioregistry](https://github.com/biopragmatics/bioregistry/blob/main/docs/GOVERNANCE.md)

Some things the governance model should cover:

- What are the collaborative processes for this project?
- What are the norms and shared expectations, technical and social? This can include a code of conduct.
- What is the procedure for deciding on schema changes?
- What is the credit model for schema contributors?
- What is the procedure for recording decisions? E.g. GitHub issues, [ADRs](https://adr.github.io/)
- What is the procedure for resolving conflicts?

### Attract and Engage Contributors

Detailed contribution guidelines, offering various ways to contribute, and hosting projects in neutral spaces increase contributor engagement and recruitment. Projects should be accessible and welcoming to new contributors to ensure longevity and development.

The [LinkML Cookiecutter](https://github.com/linkml/linkml-project-cookiecutter/) provides a template 
for project documents such as a `CONTRIBUTING.md` file and a `CODE_OF_CONDUCT.md` file that can be
adapted for your project.

The core schema developers should be familiar with existing best practice for contribution.
But don't assume that everyone is familiar with these practices. It's a good idea to document these
in a schema developers handbook or similar document. This could be appended to your CONTRIBUTING.md,
or it could be a separate document, or something interwoven into your deployed documentation.

Some things that the guide might cover:

- **Tutorial and documentation**
    * You can link to the LinkML tutorial, or you could have a tutorial specific to your schema
- **Style guide for documentation**
    * How should the information in the `description` field be written? US or UK spelling? Long or short? Technical or layperson?
    * We recommend setting standards for minimizing jargon and ensuring clear language
    * It is a good idea to set up GitHub actions to incorpore spell checking and other checks, e.g. codespell
- **Naming conventions for schema elements**
    * Good defaults: Use the LinkML [Linter recommended configuration](https://linkml.io/linkml/schemas/linter.html)
    * Whatever you choose, consistency and documenting deviations from conventions is important
    * Fully spell out names, except where this goes against conventions in the field
         - Very few systems have character length limits. Say `address` not `addr`
         - Conversely, for a biological schema `DNA` is well understood, no need for `DeoxyribonucleicAcid`
         - You can use `aliases` to provide alternative names where there is possibility of confusion
    * Classes should in general be noun phrases
    * Ontology-style schemas: slots should be named such that `subject slot object` is a grammatical sentence
- **Minimal information standards**
    * What is the minimal information that should be provided for each schema element?
    * LinkML allows for a variety of different metadata, but also permits very minimal metadata
    * We recommend defining minimal metadata standards or recommendations for a particular project
    * Consistency is sometimes better than boiling the ocean.
         - E.g. Adding `mappings` is less valuable if it is only applied to a subset of elements 
         - It may be better to use fewer elements but more broadly than many elements populated inconsistently
    * Some good defaults:
         - Every element **should** have a `description`
         - Every class **should**  have testable examples and counterexamples
         - Aliases should be populated if there is potential for confusing due to inconsistent terminology in the field
- **Modeling style guide**
    * LinkML allows for a wide variety of schema styles, from data dictionaries through to ontology-like models
    * Decide on the most appropriate style for your project and document it
    * Mixins allow for flexible multi-axial classification but you should be sure you really need them before using them
    * Parsimony is a good principle to follow, avoid proliferating entities
    * Document when to use inheritance vs composition
    * The choice of whether and how to reuse other data models and standards is very project specific
    * Document whether redundancy and denormalization is to be avoided (OLTP schemas) or embraced (OLAP schemas)
    * Semantic schemas: Document the policy for where prefixes are derived and how to adjudicate conflicts
         * bioregistry.io is a good choice
- **Editor workflows**
    * Document the canonical toolbox or workflow for editing the schema
    * LinkML source is in YAML (or CSVs/spreadsheets if schemasheets is incorporated), there are many ways to edit YAML
      - You may wish to encourage a canonical IDE or editor, and favor documenting processes for using it
    * Document linking and whitespace conventions
    * You may wish to encourage a canonical Git/GitHub tool and document this
        - The [OBook recommends GitHub Desktop](https://oboacademy.github.io/obook/reference/github-desktop/)
- **Communication protocols**
    * Where should general questions be asked? (e.g. GitHub issues or discussions, Slack, email, zoom, Stack Overflow, etc.)
    * We recommend setting up issue voting; see the [LinkML issue tracker](https://github.com/linkml/linkml/issues/974)
    * What are expectations in terms of pull request review time, time frame in which questions are answered?
- **Release Processes**
    * We recommend following semantic versioning (semver) for all releases
    * We recommend leveraging GitHub release processes
    * Release processes will be heavily dependent on the role the schema plays in the broader ecosystem
    * Manage change explicitly - provide data migration scripts where necessary
    * Document how releases are planned and announced

In general the guide should point to external resources where defaults are followed, broadly summarize these,
and concentrate on things that are project-specific.

## Open Science Principles

Many schemas developed in LinkML are not intended to be used in isolation, but rather as part of a larger
open ecosystem. The [OBook](https://oboacademy.github.io/obook) has a chapter [How to be an Open Science Engineer - maximising impact for a better world](https://oboacademy.github.io/obook/howto/open-science-engineer/) outlines principles and practices for effective collaboration and impact in the field of open science engineering.

Here's a summary:

### Principle of Collaboration

Emphasizes the importance of social collaborative workflows in open science. It advises on effective online communication, upvoting helpful answers on platforms like Stack Overflow and GitHub, answering questions even outside one's specific project, conducting basic research before posting queries, and continuously improving open science documentation.

### Principle of Upstream Fixing

Encourages fixing issues at the earliest possible stage in the dependency chain, maximizing the impact of changes and benefiting a wider community. It includes a case study highlighting the importance of quality control and community contributions in ontology development.

### Principle of No-ownership

Advocates for a mindset of shared ownership and collaborative development in open science projects, particularly in the context of publicly funded work like ontologies. It suggests embracing community-driven development without specific owners or decision-makers and emphasizes the importance of proactive involvement and decision-making in a decentralized environment.

The document also includes a TL;DR summary with key takeaways:

- Upvote and get involved in issue trackers.
- Always conduct a basic search before asking questions.
- Continuously improve documentation.
- Be generous with likes and gratitude.
- Promote open communication and push fixes upstream.
- See issues and pull requests through to the end.
- Encourage reviewing each other's work and reducing fear of making mistakes or having pull requests rejected.

These principles and practices are aimed at fostering a more collaborative, efficient, and impactful open science community.

## Example Governance and Community Documents

### Bioschemas governance

__Source__: Bioschemas [community](https://bioschemas.org/community/) and [governance](https://github.com/Bioschemas/governance/blob/master/governance.md) docs

The document titled "Bioschemas Governance" outlines the governance structure and guidelines for the Bioschemas community, a project aimed at improving data interoperability in life sciences. Here's a summary:

- **Overview**: Bioschemas adheres to five core principles of OpenStand: Respectful cooperation, adherence to standards development parameters, collective empowerment, availability, and voluntary adoption. Community members must follow the Code of Conduct based on FORCE11 guidelines.

- **Steering Council**: Responsible for strategic and organizational planning, oversight of community activities, and promoting Bioschemas activities. The council meets every two months and communicates regularly via email and online messaging platforms.

- **Community and Working Groups**: Day-to-day activities are conducted by the community, focusing on profile and type development and adoption. Working groups, each led by two individuals, develop markup practices for specific concepts. The Steering Council approves releases of profiles and types.

- **Role Holder Appointment and Removal Processes**: Describes the election of Steering Council members and Working Group Leads, with a 2-year term of service. Inactive role holders may be removed following a defined process.

- **Specification Development and Versioning**: Explains how specifications (profiles or types) are developed, including collaborative community engagement, version numbering, and authorship acknowledgment.

- **Profile and Type Development**: Details steps for developing profiles and types, including identifying base types, property cardinality, and use cases. Processes for proposing new profiles or types and renaming or deprecating them are also covered.

- **Changing Governance Documents**: Future changes to governance documents are to be submitted via a GitHub pull request, with public comment and Steering Council approval.

- **Sources**: Lists references used in the document, including links to governing principles and codes of conduct from other organizations like FORCE11, Jupyter, and W3C.

This document provides a comprehensive guide to the governance structure, roles, processes, and best practices within the Bioschemas community, emphasizing open collaboration, transparency, and adherence to established standards.

### schema.org

__SOURCE__: schema.org [how we work](https://schema.org/docs/howwework.html)

The document titled "How We Work - Schema.org" provides an overview of the processes and practices employed by Schema.org in developing and updating its schemas. Here's a summary:

- **Overview and Process**:
  - Schema.org updates materials through official named releases every few weeks.
  - Simple improvements and bug fixes can be fast-tracked as "Early Access Fixes".
  - A development version of the site, "webschemas.org", reflects the latest work-in-progress based on community discussions and proposals.
  - A "pending" extension at pending.webschemas.org showcases new vocabulary proposals, which may not yet reflect wider consensus.
  - Steering group reviews and approves release candidates; if no concerns are raised within 10 business days, the official site is updated.

- **Versioning and Change Control**:
  - Schema.org is developed incrementally, with several updates a year, each documented as a release.
  - Content for each release is based on public discussions and unanimous agreement of the Steering Group.
  - Two types of extension vocabulary are introduced: hosted (part of Schema.org but tagged within a subdomain) and external (published elsewhere and managed by other organizations).

- **Schema Structure**:
  - Schema.org contains term definitions (types, properties, enumerated values), machine-readable files, and a JSON-LD context file.
  - The approach to schema definitions is based on W3C RDFS with customizations.

- **Extensibility Mechanisms**:
  - Schema.org allows for extensibility through mechanisms independent of its vocabulary definitions and release planning.
  - This includes publishing Schema.org data alongside other structured data types and using PropertyValue and Role mechanisms for additional annotations.

- **Early Access Fixes and Pending Releases**:
  - Early Access Fixes allow for rapid updates between official releases.
  - The "pending schemas" extension is a staging area for work-in-progress terms, subject to change and community review.

- **Workflow FAQ**:
  - The document addresses common questions regarding public-vocabs, W3C WebSchemas group, the role of the Schema.org webmaster, and how to get involved or propose new schemas.

- **Related Links and Further Reading**:
  - The document provides links to additional resources for more in-depth understanding of Schema.org's work and processes.

This document serves as a comprehensive guide to the operational framework, versioning system, and collaborative nature of Schema.org's efforts in structuring and standardizing web data.
