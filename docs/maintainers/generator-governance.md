# Generator and Validator Governance

## Why generator-level governance matters

LinkML supports a large and growing number of output formats, each maintained by
different contributors with varying levels of activity. Without clear ownership
and decision-making processes at the generator level, several problems arise:

- **Unreviewed changes** can break downstream consumers who depend on a specific
  output format. A change to the JSON Schema generator, for example, can silently
  invalidate validation pipelines across many projects.
- **Stalled maintenance** becomes invisible. When the sole contributor to a
  generator moves on, there is no clear path for someone else to pick up
  responsibility, and issues accumulate without triage.
- **Inconsistent quality** across generators. Some have extensive test coverage
  and active reviewers; others have little of either. Users have no way to gauge
  the maturity or reliability of a given output format.
- **Decision deadlocks** around breaking changes. Without a designated maintainer
  who understands the design intent and user base, even straightforward
  improvements can stall in review.

Establishing per-generator maintainers, documenting contributor history, and
linking to the relevant issue trackers makes it possible to route questions,
reviews, and decisions to the right people, and to identify generators that need
new maintainers or should be deprecated.

Current line attribution per generator/validator based on `git blame`, run on the 4th February 2026 (Lines reflect the current codebase, not historical contributions). These serve as _candidates_ to form generator-level governance teams, and do not constitue the final structure. The idea is to (1) define the teams collaboratively (and organically as issues arise) and (2) enshrine editorial policies in CODEOWNERS.

## Generators

### CSV Generator (`gen-csv`)

Generates CSV summaries of schema classes and slots.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 44 |
| Chris Mungall | @cmungall | 24 |
| Jonny Saunders | @sneakers-the-rat | 19 |
| Harshad Hegde | @hrshdhgd | 12 |
| David Linke | @dalito | 2 |
| Corey Cox | @amc-corey-cox | 2 |
| Deepak Unni | @deepakunni3 | 2 |
| Patrick Kalita | @pkalita-lbl | 1 |
| Sujay Patil | @sujaypatil96 | 1 |

### DBML Generator (`gen-dbml`)

Converts a LinkML schema into DBML (Database Markup Language) for database diagram tools.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Sierra Taylor Moxon | @sierra-moxon | 170 |
| Corey Cox | @amc-corey-cox | 2 |

### Doc Generator (`gen-doc`)

Generates Markdown documentation pages from a schema, with embedded Mermaid class diagrams.

**Issues and PRs**: [label:`generator-doc`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-doc%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Chris Mungall | @cmungall | 484 |
| Sujay Patil | @sujaypatil96 | 308 |
| Harshad Hegde | @hrshdhgd | 103 |
| Patrick Kalita | @pkalita-lbl | 77 |
| Vincent Kelleher | @VincentKelworthy | 59 |
| Chien-Chun Ni | @saibalmars | 55 |
| ialarmedalien | @ialarmedalien | 23 |
| David Linke | @dalito | 23 |
| Ben Dichter | @bendichter | 22 |
| Jonny Saunders | @sneakers-the-rat | 21 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 21 |
| Sierra Taylor Moxon | @sierra-moxon | 15 |
| timothy-trinidad-ps | @timothy-trinidad-ps | 14 |
| Corey Cox | @amc-corey-cox | 6 |
| Damien Goutte-Gattat | @gouttegd | 6 |
| Yaroslav Halchenko | @yarikoptic | 2 |

### Dot/Graphviz Generator (`gen-graphviz`)

Generates Graphviz dot files for schema visualization.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 71 |
| Harshad Hegde | @hrshdhgd | 50 |
| Chris Mungall | @cmungall | 19 |
| Jonny Saunders | @sneakers-the-rat | 5 |
| Patrick Kalita | @pkalita-lbl | 4 |
| David Linke | @dalito | 2 |
| Corey Cox | @amc-corey-cox | 2 |
| Sujay Patil | @sujaypatil96 | 1 |

### ER Diagram Generator (`gen-erdiagram`)

Serializes schemas as Entity-Relationship diagrams in Mermaid syntax.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Chris Mungall | @cmungall | 235 |
| Vlad Korolev | @v-lad | 234 |
| Patrick Kalita | @pkalita-lbl | 48 |
| Jonny Saunders | @sneakers-the-rat | 8 |
| Ben Dichter | @bendichter | 6 |
| Chien-Chun Ni | @saibalmars | 4 |
| Nolan Nichols | @nicholsn | 3 |
| Corey Cox | @amc-corey-cox | 2 |
| Yaroslav Halchenko | @yarikoptic | 2 |
| ialarmedalien | @ialarmedalien | 1 |

### Excel Generator (`gen-excel`)

Generates Excel workbooks with sheets per class, columns per slot, and dropdown validation for enums.

**Issues and PRs**: [label:`generator-excel`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-excel%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Sujay Patil | @sujaypatil96 | 167 |
| Nico Matentzoglu | @matentzn | 34 |
| Ben Dichter | @bendichter | 8 |
| Chris Mungall | @cmungall | 5 |
| Patrick Kalita | @pkalita-lbl | 4 |
| Jonny Saunders | @sneakers-the-rat | 2 |
| Corey Cox | @amc-corey-cox | 1 |
| David Linke | @dalito | 1 |

### Golang Generator (`gen-golang`)

Generates Go structs from a LinkML schema.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Jeffrey N. Johnson | @jeff-cohere | 188 |
| Ben Dichter | @bendichter | 5 |
| Patrick Kalita | @pkalita-lbl | 4 |
| Jonny Saunders | @sneakers-the-rat | 3 |
| Isaac To | @candleindark | 3 |
| Corey Cox | @amc-corey-cox | 2 |
| Chris Mungall | @cmungall | 1 |

### Golr Schema Generator (`gen-golr-views`)

Generates GOlr (Gene Ontology Lucene/Solr) YAML schema definitions.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 64 |
| Harshad Hegde | @hrshdhgd | 20 |
| Chris Mungall | @cmungall | 10 |
| Deepak Unni | @deepakunni3 | 6 |
| Patrick Kalita | @pkalita-lbl | 4 |
| Jonny Saunders | @sneakers-the-rat | 4 |
| Corey Cox | @amc-corey-cox | 3 |
| Sierra Taylor Moxon | @sierra-moxon | 1 |
| David Linke | @dalito | 1 |

### GraphQL Generator (`gen-graphql`)

Generates a GraphQL schema from a LinkML schema.

**Issues and PRs**: [label:`generator-graphql`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-graphql%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 64 |
| Harold Solbrig | @hsolbrig | 24 |
| Jonny Saunders | @sneakers-the-rat | 14 |
| Harshad Hegde | @hrshdhgd | 6 |
| Chris Mungall | @cmungall | 5 |
| David Linke | @dalito | 2 |
| Corey Cox | @amc-corey-cox | 2 |
| Deepak Unni | @deepakunni3 | 2 |
| Patrick Kalita | @pkalita-lbl | 1 |
| ialarmedalien | @ialarmedalien | 1 |

### Java Generator (`gen-java`)

Generates Java classes from a LinkML schema.

**Issues and PRs**: [label:`generator-java`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-java%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Damien Goutte-Gattat | @gouttegd | 86 |
| Chris Mungall | @cmungall | 51 |
| Harshad Hegde | @hrshdhgd | 46 |
| Jules Jacobsen | @julesjacobsen | 28 |
| Kevin Schaper | @kevinschaper | 17 |
| Patrick Kalita | @pkalita-lbl | 6 |
| Ben Dichter | @bendichter | 4 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 4 |
| ialarmedalien | @ialarmedalien | 2 |
| David Linke | @dalito | 2 |
| Sujay Patil | @sujaypatil96 | 2 |
| Corey Cox | @amc-corey-cox | 1 |
| Sierra Taylor Moxon | @sierra-moxon | 1 |
| Jonny Saunders | @sneakers-the-rat | 1 |

### JSON-LD Context Generator (`gen-jsonld-context`)

Generates JSON-LD context files for RDF serialization of schema-conformant data.

**Issues and PRs**: [label:`generator-jsonld`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-jsonld%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 103 |
| Volodymyr Lapkin | @kapystya | 77 |
| Harshad Hegde | @hrshdhgd | 42 |
| Jonny Saunders | @sneakers-the-rat | 40 |
| Vincent Kelleher | @VincentKelworthy | 33 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 16 |
| Chris Mungall | @cmungall | 12 |
| Corey Cox | @amc-corey-cox | 3 |
| Ben Dichter | @bendichter | 3 |
| David Linke | @dalito | 2 |
| Sierra Taylor Moxon | @sierra-moxon | 2 |
| Patrick Kalita | @pkalita-lbl | 1 |
| Dorota Jarecka | @djarecka | 1 |

### JSON-LD Generator (`gen-jsonld`)

Generates a JSON-LD representation of the schema itself.

**Issues and PRs**: [label:`generator-jsonld`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-jsonld%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 106 |
| Jonny Saunders | @sneakers-the-rat | 55 |
| Harshad Hegde | @hrshdhgd | 34 |
| Chris Mungall | @cmungall | 26 |
| Patrick Kalita | @pkalita-lbl | 23 |
| Corey Cox | @amc-corey-cox | 5 |
| ialarmedalien | @ialarmedalien | 3 |
| Sierra Taylor Moxon | @sierra-moxon | 2 |
| David Linke | @dalito | 1 |

### JSON Schema Generator (`gen-json-schema`)

Generates JSON Schema for validating data that conforms to a LinkML schema.

**Issues and PRs**: [label:`generator-jsonschema`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-jsonschema%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Patrick Kalita | @pkalita-lbl | 405 |
| Jonny Saunders | @sneakers-the-rat | 137 |
| Chris Mungall | @cmungall | 79 |
| Harshad Hegde | @hrshdhgd | 33 |
| Harold Solbrig | @hsolbrig | 26 |
| Chien-Chun Ni | @saibalmars | 24 |
| Kevin Schaper | @kevinschaper | 22 |
| Paul Millar | @paulmillar | 19 |
| Sierra Taylor Moxon | @sierra-moxon | 16 |
| Gaurav Vaidya | @gaurav | 11 |
| madanucd | @madanucd | 10 |
| Corey Cox | @amc-corey-cox | 7 |
| Hugh Emerson | @hughemerson | 5 |
| Isaac To | @candleindark | 4 |
| Ben Dichter | @bendichter | 3 |
| Leon Kuchenbecker | @lkuchenb | 2 |
| Deepak Unni | @deepakunni3 | 2 |
| Vlad Korolev | @v-lad | 2 |
| Nico Matentzoglu | @matentzn | 1 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 1 |
| Bill Duncan |  | 1 |
| David Linke | @dalito | 1 |

### LinkML Generator (`gen-linkml`)

Re-serializes a LinkML schema in normalized YAML form (useful for schema transformations).

**Issues and PRs**: [label:`generator-linkml`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-linkml%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Sujay Patil | @sujaypatil96 | 109 |
| Chris Mungall | @cmungall | 18 |
| Ben Dichter | @bendichter | 3 |
| David Linke | @dalito | 2 |
| Corey Cox | @amc-corey-cox | 2 |
| Harshad Hegde | @hrshdhgd | 1 |
| Yaroslav Halchenko | @yarikoptic | 1 |
| ialarmedalien | @ialarmedalien | 1 |
| Jonny Saunders | @sneakers-the-rat | 1 |

### Markdown Data Dictionary Generator (`gen-markdown-datadict`)

Generates a simple Markdown data dictionary table from a schema.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Vlad Korolev | @v-lad | 1598 |

### Markdown Generator (`gen-markdown`)

Generates Markdown documentation for a schema.

Deprecated, use `gen-doc`.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Jonny Saunders | @sneakers-the-rat | 343 |
| Harshad Hegde | @hrshdhgd | 192 |
| Harold Solbrig | @hsolbrig | 181 |
| Chris Mungall | @cmungall | 35 |
| Patrick Kalita | @pkalita-lbl | 28 |
| Sujay Patil | @sujaypatil96 | 25 |
| ialarmedalien | @ialarmedalien | 12 |
| Vlad Korolev | @v-lad | 8 |
| Sierra Taylor Moxon | @sierra-moxon | 8 |
| Corey Cox | @amc-corey-cox | 6 |
| joeflack4 | @joeflack4 | 3 |
| Deepak Unni | @deepakunni3 | 3 |
| Ben Dichter | @bendichter | 2 |
| David Linke | @dalito | 1 |

### Mermaid Class Diagram Generator (`gen-mermaid-class-diagram`)

Generates standalone Mermaid class diagrams from a schema.

**Issues and PRs**: [label:`generator-mermaid`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-mermaid%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Sujay Patil | @sujaypatil96 | 118 |
| Chien-Chun Ni | @saibalmars | 20 |
| Sierra Taylor Moxon | @sierra-moxon | 9 |
| David Linke | @dalito | 4 |
| Corey Cox | @amc-corey-cox | 3 |
| Jonny Saunders | @sneakers-the-rat | 2 |

### Namespace Generator (`gen-namespaces`)

Generates Python namespace definition modules for use with the LinkML runtime.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 180 |
| Harshad Hegde | @hrshdhgd | 17 |
| Chris Mungall | @cmungall | 3 |
| David Linke | @dalito | 2 |
| Corey Cox | @amc-corey-cox | 1 |
| Sierra Taylor Moxon | @sierra-moxon | 1 |
| Jonny Saunders | @sneakers-the-rat | 1 |

### OWL Generator (`gen-owl`)

Generates an OWL ontology representation of a LinkML schema.

**Issues and PRs**: [label:`generator-owl`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-owl%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Chris Mungall | @cmungall | 1169 |
| Harshad Hegde | @hrshdhgd | 74 |
| Harold Solbrig | @hsolbrig | 52 |
| Jonny Saunders | @sneakers-the-rat | 20 |
| Patrick Kalita | @pkalita-lbl | 16 |
| Ben Dichter | @bendichter | 16 |
| Isaac To | @candleindark | 12 |
| egavard | @egavard | 10 |
| Corey Cox | @amc-corey-cox | 9 |
| Sierra Taylor Moxon | @sierra-moxon | 7 |
| Deepak Unni | @deepakunni3 | 6 |
| Martin Janik | @janik-martin | 1 |
| David Linke | @dalito | 1 |

### Pandera Generator (`gen-pandera`)

Generates Pandera and Polars dataframe validation schemas from a LinkML schema.

Includes `panderagen/` and `polars_schema/` subpackages.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Tim Fliss | @timfliss | 1952 |
| Corey Cox | @amc-corey-cox | 2 |

### PlantUML Generator (`gen-plantuml`)

Generates PlantUML class diagrams from a schema.

**Issues and PRs**: [label:`generator-plantuml`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-plantuml%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 298 |
| Jim Snyder | @jsnyder-csdisco | 21 |
| Jonny Saunders | @sneakers-the-rat | 18 |
| Chien-Chun Ni | @saibalmars | 17 |
| Sierra Taylor Moxon | @sierra-moxon | 9 |
| Vladimir Alexiev | @VladimirAlexiev | 6 |
| Corey Cox | @amc-corey-cox | 4 |
| Patrick Kalita | @pkalita-lbl | 1 |
| Ben Dichter | @bendichter | 1 |

### Prefix Map Generator (`gen-prefix-map`)

Generates a prefix map (CURIE-to-URI mappings) from a schema.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 67 |
| Jonny Saunders | @sneakers-the-rat | 23 |
| Chris Mungall | @cmungall | 11 |
| Harshad Hegde | @hrshdhgd | 7 |
| Sujay Patil | @sujaypatil96 | 4 |
| Corey Cox | @amc-corey-cox | 3 |
| Patrick Kalita | @pkalita-lbl | 2 |
| David Linke | @dalito | 2 |
| Sierra Taylor Moxon | @sierra-moxon | 2 |

### Project Generator (`gen-project`)

Meta-generator that runs multiple generators at once to produce a full project output directory.

**Issues and PRs**: [label:`generator-project`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-project%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Chris Mungall | @cmungall | 109 |
| Harshad Hegde | @hrshdhgd | 65 |
| Jonny Saunders | @sneakers-the-rat | 27 |
| Vlad Korolev | @v-lad | 17 |
| Sujay Patil | @sujaypatil96 | 14 |
| Isaac To | @candleindark | 12 |
| Patrick Kalita | @pkalita-lbl | 5 |
| Mark Andrew Miller | @turbomam | 3 |
| Sierra Taylor Moxon | @sierra-moxon | 3 |
| David Linke | @dalito | 2 |
| Ben Dichter | @bendichter | 2 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 1 |

### Protobuf Generator (`gen-proto`)

Generates Protocol Buffer (protobuf) schema definitions from a LinkML schema.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 31 |
| Jonny Saunders | @sneakers-the-rat | 24 |
| Harshad Hegde | @hrshdhgd | 8 |
| Chris Mungall | @cmungall | 5 |
| Sierra Taylor Moxon | @sierra-moxon | 3 |
| Ben Dichter | @bendichter | 2 |
| David Linke | @dalito | 2 |
| Corey Cox | @amc-corey-cox | 2 |
| Deepak Unni | @deepakunni3 | 2 |

### Pydantic Generator (`gen-pydantic`)

Generates Pydantic BaseModel classes for data validation and serialization.

Includes `pydanticgen/` subpackage.

**Issues and PRs**: [label:`generator-pydantic`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-pydantic%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Jonny Saunders | @sneakers-the-rat | 1710 |
| Ryan Ly | @rly | 371 |
| Kevin Schaper | @kevinschaper | 144 |
| Chris Mungall | @cmungall | 85 |
| Vlad Korolev | @v-lad | 73 |
| Emmanuel Ferdman | @emmanuelferdman | 50 |
| Daniel Ji | @danieljbk | 49 |
| Harshad Hegde | @hrshdhgd | 43 |
| Frank Dekervel | @kervel | 34 |
| Elias Oltmanns | @EOltmanns | 28 |
| ialarmedalien | @ialarmedalien | 23 |
| Corey Cox | @amc-corey-cox | 14 |
| Chr1st0p43rR | @Chr1st0p43rR | 14 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 12 |
| Isaac To | @candleindark | 10 |
| glass-ships | @glass-ships | 9 |
| Sierra Taylor Moxon | @sierra-moxon | 9 |
| David Linke | @dalito | 6 |
| Ben Dichter | @bendichter | 6 |
| Vincent Kelleher | @VincentKelworthy | 5 |
| Patrick Kalita | @pkalita-lbl | 3 |
| Jules Jacobsen | @julesjacobsen | 2 |

### Python Generator (`gen-python`)

Generates Python dataclasses compatible with the LinkML runtime.

Includes `python/` subpackage. See also label `generator-dataclasses`.

**Issues and PRs**: [label:`generator-python`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-python%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 494 |
| Harshad Hegde | @hrshdhgd | 218 |
| Chris Mungall | @cmungall | 167 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 131 |
| ialarmedalien | @ialarmedalien | 124 |
| Vincent Kelleher | @VincentKelworthy | 102 |
| Patrick Kalita | @pkalita-lbl | 51 |
| Sierra Taylor Moxon | @sierra-moxon | 43 |
| Jonny Saunders | @sneakers-the-rat | 36 |
| Isaac To | @candleindark | 12 |
| Ben Dichter | @bendichter | 9 |
| Frank Dekervel | @kervel | 9 |
| Corey Cox | @amc-corey-cox | 8 |
| Mark Andrew Miller | @turbomam | 2 |
| Yaroslav Halchenko | @yarikoptic | 2 |
| Deepak Unni | @deepakunni3 | 1 |
| David Linke | @dalito | 1 |

### RDF Generator (`gen-rdf`)

Generates an RDF representation of the schema itself.

**Issues and PRs**: [label:`generator-rdf`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-rdf%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 41 |
| Harshad Hegde | @hrshdhgd | 21 |
| Jonny Saunders | @sneakers-the-rat | 14 |
| Volodymyr Lapkin | @kapystya | 11 |
| Chris Mungall | @cmungall | 6 |
| Patrick Kalita | @pkalita-lbl | 4 |
| David Linke | @dalito | 2 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 2 |
| Ben Dichter | @bendichter | 1 |
| Corey Cox | @amc-corey-cox | 1 |
| Sierra Taylor Moxon | @sierra-moxon | 1 |

### Rust Generator (`gen-rust`)

Generates Rust struct and enum types from a LinkML schema.

Includes `rustgen/` subpackage.

**Issues and PRs**: [label:`generator-rust`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-rust%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Frank Dekervel | @kervel | 1562 |
| Jonny Saunders | @sneakers-the-rat | 699 |
| Kevin Schaper | @kevinschaper | 159 |
| Corey Cox | @amc-corey-cox | 10 |

### SHACL Generator (`gen-shacl`)

Generates SHACL shapes for RDF data validation against a LinkML schema.

Includes `shacl/` subpackage.

**Issues and PRs**: [label:`generator-shacl`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-shacl%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Vincent Kelleher | @VincentKelworthy | 180 |
| anjastrunk | @anjastrunk | 98 |
| Kevin Schaper | @kevinschaper | 65 |
| Chris Mungall | @cmungall | 63 |
| Stephan Heunis | @jsheunis | 52 |
| Patrick Kalita | @pkalita-lbl | 30 |
| Eli Chadwick | @Eli-Chadwick | 16 |
| HendrikBorgelt | @HendrikBorgelt | 15 |
| Jonny Saunders | @sneakers-the-rat | 13 |
| Harshad Hegde | @hrshdhgd | 12 |
| robertschubert | @robertschubert | 10 |
| Corey Cox | @amc-corey-cox | 5 |
| Sierra Taylor Moxon | @sierra-moxon | 5 |
| Vincent Emonet | @vemonet | 5 |
| Nico Matentzoglu | @matentzn | 5 |
| Isaac To | @candleindark | 3 |
| Deepak Unni | @deepakunni3 | 3 |
| Ben Dichter | @bendichter | 2 |
| David Linke | @dalito | 2 |
| glass-ships | @glass-ships | 2 |
| ialarmedalien | @ialarmedalien | 1 |

### ShEx Generator (`gen-shex`)

Generates ShEx (Shape Expressions) for RDF data validation.

**Issues and PRs**: [label:`generator-shex`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-shex%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 115 |
| Harshad Hegde | @hrshdhgd | 43 |
| Kevin Schaper | @kevinschaper | 35 |
| Deepak Unni | @deepakunni3 | 21 |
| Patrick Kalita | @pkalita-lbl | 14 |
| Jonny Saunders | @sneakers-the-rat | 13 |
| Chris Mungall | @cmungall | 12 |
| Corey Cox | @amc-corey-cox | 8 |
| Sierra Taylor Moxon | @sierra-moxon | 6 |
| David Linke | @dalito | 1 |

### SPARQL Generator (`gen-sparql`)

Generates SPARQL queries for deferred validation of RDF data against a schema.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Chris Mungall | @cmungall | 175 |
| Harshad Hegde | @hrshdhgd | 19 |
| Jonny Saunders | @sneakers-the-rat | 7 |
| Corey Cox | @amc-corey-cox | 3 |
| Isaac To | @candleindark | 3 |
| David Linke | @dalito | 2 |
| Patrick Kalita | @pkalita-lbl | 1 |
| ialarmedalien | @ialarmedalien | 1 |
| Sierra Taylor Moxon | @sierra-moxon | 1 |
| Ben Dichter | @bendichter | 1 |
| Yaroslav Halchenko | @yarikoptic | 1 |

### SQLAlchemy Generator (`gen-sqla`)

Generates SQLAlchemy ORM model classes from a LinkML schema.

Includes `sqlalchemy/` subpackage.

**Issues and PRs**: [label:`generator-SQL`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-SQL%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Chris Mungall | @cmungall | 226 |
| Harshad Hegde | @hrshdhgd | 55 |
| Patrick Kalita | @pkalita-lbl | 17 |
| Sujay Patil | @sujaypatil96 | 14 |
| ialarmedalien | @ialarmedalien | 9 |
| Ben Dichter | @bendichter | 8 |
| Isaac To | @candleindark | 5 |
| Corey Cox | @amc-corey-cox | 4 |
| Sierra Taylor Moxon | @sierra-moxon | 4 |
| Jonny Saunders | @sneakers-the-rat | 3 |
| David Linke | @dalito | 2 |
| Kevin Schaper | @kevinschaper | 1 |
| glass-ships | @glass-ships | 1 |
| Jan Katins | @jankatins | 1 |
| Mark Andrew Miller | @turbomam | 1 |

### SQL Table Generator (`gen-sqltables`)

Generates SQL DDL (CREATE TABLE statements) from a LinkML schema.

**Issues and PRs**: [label:`generator-SQL`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-SQL%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| ialarmedalien | @ialarmedalien | 123 |
| Chris Mungall | @cmungall | 120 |
| VictoriaSavageNNL | @VictoriaSavageNNL | 75 |
| Harshad Hegde | @hrshdhgd | 72 |
| Jonny Saunders | @sneakers-the-rat | 28 |
| Vlad Korolev | @v-lad | 20 |
| Ben Dichter | @bendichter | 8 |
| Patrick Kalita | @pkalita-lbl | 5 |
| Corey Cox | @amc-corey-cox | 4 |
| Sujay Patil | @sujaypatil96 | 3 |
| pizzashi | @pizzashi | 2 |
| David Linke | @dalito | 2 |
| Isaac To | @candleindark | 2 |
| Noah Lorang | @noahlorang | 2 |
| Florian Kotthoff | @FlorianK13 | 1 |

### SSSOM Generator (`gen-sssom`)

Generates Simple Standard for Sharing Ontology Mappings (SSSOM) TSV files from schema mappings.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harshad Hegde | @hrshdhgd | 162 |
| Chris Mungall | @cmungall | 14 |
| Patrick Kalita | @pkalita-lbl | 10 |
| Corey Cox | @amc-corey-cox | 3 |
| Sierra Taylor Moxon | @sierra-moxon | 1 |
| Jonny Saunders | @sneakers-the-rat | 1 |
| David Linke | @dalito | 1 |

### Summary Generator (`gen-summary`)

Generates summary spreadsheets of schema statistics.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harshad Hegde | @hrshdhgd | 44 |
| Harold Solbrig | @hsolbrig | 28 |
| Jonny Saunders | @sneakers-the-rat | 9 |
| Chris Mungall | @cmungall | 5 |
| Sierra Taylor Moxon | @sierra-moxon | 2 |
| Patrick Kalita | @pkalita-lbl | 2 |
| Ben Dichter | @bendichter | 2 |
| David Linke | @dalito | 2 |
| Corey Cox | @amc-corey-cox | 2 |

### TerminusDB Generator (`gen-terminusdb`)

Experimental generator for TerminusDB graph database schemas.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Donny Winston | @dwinston | 106 |
| Jonny Saunders | @sneakers-the-rat | 15 |
| Chris Mungall | @cmungall | 11 |
| Patrick Kalita | @pkalita-lbl | 5 |
| Harshad Hegde | @hrshdhgd | 2 |
| David Linke | @dalito | 2 |
| Sierra Taylor Moxon | @sierra-moxon | 2 |
| Corey Cox | @amc-corey-cox | 1 |
| Harold Solbrig | @hsolbrig | 1 |
| ialarmedalien | @ialarmedalien | 1 |

### TypeScript Generator (`gen-typescript`)

Generates TypeScript interfaces and types from a LinkML schema.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Chris Mungall | @cmungall | 110 |
| Corey Cox | @amc-corey-cox | 79 |
| Kevin Schaper | @kevinschaper | 72 |
| glass-ships | @glass-ships | 37 |
| Harshad Hegde | @hrshdhgd | 17 |
| Patrick Kalita | @pkalita-lbl | 8 |
| Vlad Korolev | @v-lad | 6 |
| Isaac To | @candleindark | 5 |
| Jonny Saunders | @sneakers-the-rat | 3 |
| Ben Dichter | @bendichter | 2 |
| David Linke | @dalito | 1 |
| Ryan Ly | @rly | 1 |

### YAML Generator (`gen-yaml`)

Re-serializes a schema as a normalized YAML document.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 20 |
| Harshad Hegde | @hrshdhgd | 19 |
| Chris Mungall | @cmungall | 16 |
| Ben Dichter | @bendichter | 2 |
| David Linke | @dalito | 2 |
| Sierra Taylor Moxon | @sierra-moxon | 1 |
| Patrick Kalita | @pkalita-lbl | 1 |
| Corey Cox | @amc-corey-cox | 1 |
| Jonny Saunders | @sneakers-the-rat | 1 |

### YARRRML Generator

Generates YARRRML mapping rules for RDF transformation pipelines.

No CLI entry point.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Volodymyr Lapkin | @kapystya | 177 |
| Corey Cox | @amc-corey-cox | 2 |

### YUML Generator (`gen-yuml`)

Generates yUML class diagrams.

Deprecated.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Harold Solbrig | @hsolbrig | 144 |
| Harshad Hegde | @hrshdhgd | 72 |
| madanucd | @madanucd | 33 |
| Jonny Saunders | @sneakers-the-rat | 19 |
| Patrick Kalita | @pkalita-lbl | 16 |
| Jan Katins | @jankatins | 11 |
| Sierra Taylor Moxon | @sierra-moxon | 10 |
| Chris Mungall | @cmungall | 4 |
| Ben Dichter | @bendichter | 2 |
| Corey Cox | @amc-corey-cox | 2 |
| Sujay Patil | @sujaypatil96 | 1 |

## Validators

### JSON Schema Validator (`linkml-jsonschema-validate`)

Validates data instances against a LinkML schema using generated JSON Schema.

**Issues and PRs**: [label:`generator-jsonschema`](https://github.com/linkml/linkml/issues?q=label%3Agenerator-jsonschema%20state%3Aopen)

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Patrick Kalita | @pkalita-lbl | 78 |
| Chris Mungall | @cmungall | 74 |
| Harshad Hegde | @hrshdhgd | 29 |
| Jonny Saunders | @sneakers-the-rat | 17 |
| Silvano Cirujano Cuesta | @silvano-cirujano-cuesta | 15 |
| Corey Cox | @amc-corey-cox | 5 |
| Isaac To | @candleindark | 3 |
| Sierra Taylor Moxon | @sierra-moxon | 3 |
| David Linke | @dalito | 2 |
| Sujay Patil | @sujaypatil96 | 1 |

### SPARQL Validator (`linkml-sparql-validate`)

Validates RDF data against a LinkML schema using SPARQL queries.

| Contributor | GitHub | Lines |
| --- | --- | --- |
| Chris Mungall | @cmungall | 90 |
| Harshad Hegde | @hrshdhgd | 39 |
| Jonny Saunders | @sneakers-the-rat | 8 |
| Patrick Kalita | @pkalita-lbl | 5 |
| Isaac To | @candleindark | 5 |
| David Linke | @dalito | 2 |
| Corey Cox | @amc-corey-cox | 2 |

