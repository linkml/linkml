(generator-feature-dashboard)=

# Generator Feature Dashboard

This dashboard shows which LinkML metamodel features each generator supports. **The compliance test suite ([tests/linkml/test_compliance/](https://github.com/linkml/linkml/tree/main/tests/linkml/test_compliance)) is the source of truth** — every cell below is derived from actual test results.

*Regenerate with: `uv run pytest tests/linkml/test_compliance/ --with-output && uv run python scripts/generate_dashboard.py`*

## Legend

| Icon | Meaning |
|------|---------|
| ✅ | Fully supported |
| ⚠️ | Partial / incomplete / mixed |
| ❌ | Not implemented |
| ⚪ | Not applicable |
| ❓ | Not yet tested |

## Summary by Category

Each cell shows the aggregate result across all tests in that category. Scroll down for per-test details.

| Category | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|----------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| <a href="#arrays">Arrays</a> | ✅ | ❓ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#boolean-expressions">Boolean Expressions</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#cardinality-presence">Cardinality & Presence</a> | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#core-structure">Core Structure</a> | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |
| <a href="#defaults-computed">Defaults & Computed</a> | ✅ | ✅ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ✅ | ✅ | ❓ |
| <a href="#enumerations">Enumerations</a> | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#identity-keys">Identity & Keys</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |
| <a href="#inheritance-refinement">Inheritance & Refinement</a> | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#inlining-references">Inlining & References</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#metadata">Metadata</a> | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ❓ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ❓ |
| <a href="#other">Other</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#rules-classification">Rules & Classification</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#schema-level">Schema-Level</a> | ✅ | ✅ | ✅ | ❓ | ⚠️ | ❓ | ❓ | ✅ | ✅ | ❓ | ⚠️ | ✅ | ❓ |
| <a href="#slot-typing-ranges">Slot Typing & Ranges</a> | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ⚠️ | ❓ |
| <a href="#value-constraints">Value Constraints</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#uncategorized">Uncategorized</a> | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |

## Coverage Scores

Percentage of tests where the generator fully implements the feature (excluding not-applicable).

| Generator | Implements | Partial | Ignores | N/A | Total | Score |
|-----------|:----------:|:-------:|:-------:|:---:|:-----:|:-----:|
| Pydantic | 29 | 34 | 1 | 0 | 64 | 45% |
| Python DC | 16 | 38 | 10 | 0 | 64 | 25% |
| JSON Schema | 39 | 23 | 2 | 0 | 64 | 61% |
| Java | 0 | 24 | 40 | 0 | 64 | 0% |
| SHACL | 19 | 25 | 20 | 0 | 64 | 30% |
| ShEx | 0 | 24 | 40 | 0 | 64 | 0% |
| OWL | 0 | 26 | 38 | 0 | 64 | 0% |
| JSON-LD Ctx | 34 | 24 | 6 | 0 | 64 | 53% |
| SQLite DDL | 12 | 40 | 12 | 0 | 64 | 19% |
| Postgres DDL | 0 | 23 | 41 | 0 | 64 | 0% |
| Pandera | 14 | 28 | 22 | 0 | 64 | 22% |
| Polars Schema | 28 | 23 | 13 | 0 | 64 | 44% |
| sql_ddl_bigquery | 0 | 24 | 40 | 0 | 64 | 0% |

## Details by Category

### Arrays

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| N-dimensional arrays | ✅ | ❓ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

### Boolean Expressions

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Cardinality in exactly_one_of | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Class any_of | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Class boolean constraints with required | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Class boolean with expressions | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |
| Slot all_of | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Slot any_of | ✅ | ⚠️ | ⚠️ | ❓ | ❓ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ❓ | ❓ | ❓ |
| Slot boolean with expressions | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |
| Slot exactly_one_of | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Slot none_of | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

### Cardinality & Presence

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Identifier implies required | ✅ | ✅ | ✅ | ❓ | ❓ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |
| Membership constraints | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Min/max cardinality | ✅ | ⚠️ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |
| Required / multivalued | ⚠️ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |

### Core Structure

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Abstract classes | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |
| Attribute refinement | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ⚠️ | ✅ | ❓ |
| Attributes | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |
| Class inheritance (is_a) | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |
| Mixins | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |
| Slot inheritance | ✅ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |
| Slot usage | ✅ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |

### Defaults & Computed

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| If-absent defaults | ✅ | ✅ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ✅ | ✅ | ❓ |

### Enumerations

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Enum aliases | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |
| Enum hierarchy | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |
| Non-standard enum names | ⚠️ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ❓ | ❓ |
| Static enums | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Typed permissible values | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |

### Identity & Keys

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Identifier | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |
| Nested keys | ⚠️ | ⚠️ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ❓ | ❓ | ❓ |
| Type designator | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |
| Unique keys | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |

### Inheritance & Refinement

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Subproperty class range | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty deep hierarchy | ✅ | ❓ | ✅ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty multivalued | ✅ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty range formatting | ✅ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty slot_usage narrowing | ✅ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty value constraint | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

### Inlining & References

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Inlined as simple dict | ⚠️ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ |
| Inlined objects | ✅ | ⚠️ | ✅ | ❓ | ❓ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ✅ | ✅ | ❓ |
| Inlined with unique keys | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ❓ | ⚠️ |

### Metadata

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Aliasing | ✅ | ✅ | ✅ | ❓ | ⚠️ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |
| Annotations | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |
| Common metadata | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Descriptions | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |
| Element URIs | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |

### Other

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| JSON Pointer | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

### Rules & Classification

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Classification rules | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Precondition combos | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Precondition rules | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |
| Value presence in rules | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |

### Schema-Level

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Instantiates | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |
| Schema imports | ✅ | ✅ | ✅ | ❓ | ❓ | ❓ | ❓ | ✅ | ✅ | ❓ | ⚠️ | ✅ | ❓ |

### Slot Typing & Ranges

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Any type | ✅ | ✅ | ✅ | ❓ | ❓ | ❓ | ❓ | ✅ | ❓ | ❓ | ❓ | ✅ | ❓ |
| Custom types (typeof) | ⚠️ | ⚠️ | ⚠️ | ❓ | ❓ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ❓ | ✅ | ❓ |
| Date/datetime types | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ❓ | ❓ |
| Primitive type ranges | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ✅ | ✅ | ❓ |
| URI types | ⚠️ | ✅ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ |

### Value Constraints

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Equals string | ✅ | ❓ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Equals string in | ✅ | ❓ | ✅ | ❓ | ✅ | ❓ | ⚠️ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ |
| ID prefix | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Min/max value | ✅ | ⚠️ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ✅ | ✅ | ❓ |
| Regex pattern | ⚠️ | ⚠️ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ |

### Uncategorized

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema | sql_ddl_bigquery |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| range expression booleans | ⚠️ | ❓ | ✅ | ⚠️ | ❓ | ❓ | ❓ | ⚠️ | ❓ | ❓ | ❓ | ⚠️ | ⚠️ |
| range expression nesting | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |

---

*This dashboard is auto-generated from compliance test results. To update: run the compliance tests with `--with-output`, then run `uv run python scripts/generate_dashboard.py`. To add features, write a new compliance test and decorate it with `@feature_category("Category Name", "Display Name")`.*
