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

| Category | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|----------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| <a href="#arrays">Arrays</a> | ✅ | ❓ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#boolean-expressions">Boolean Expressions</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#cardinality-presence">Cardinality & Presence</a> | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#core-structure">Core Structure</a> | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |
| <a href="#defaults-computed">Defaults & Computed</a> | ✅ | ✅ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ✅ | ✅ |
| <a href="#enumerations">Enumerations</a> | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#identity-keys">Identity & Keys</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |
| <a href="#inheritance-refinement">Inheritance & Refinement</a> | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#inlining-references">Inlining & References</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#metadata">Metadata</a> | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ❓ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ |
| <a href="#other">Other</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#rules-classification">Rules & Classification</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#schema-level">Schema-Level</a> | ✅ | ✅ | ✅ | ❓ | ⚠️ | ❓ | ❓ | ✅ | ✅ | ❓ | ⚠️ | ✅ |
| <a href="#slot-typing-ranges">Slot Typing & Ranges</a> | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ⚠️ |
| <a href="#value-constraints">Value Constraints</a> | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| <a href="#uncategorized">Uncategorized</a> | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |

## Coverage Scores

Percentage of tests where the generator fully implements the feature (excluding not-applicable).

| Generator | Implements | Partial | Ignores | N/A | Total | Score |
|-----------|:----------:|:-------:|:-------:|:---:|:-----:|:-----:|
| Pydantic | 29 | 33 | 1 | 0 | 63 | 46% |
| Python DC | 16 | 37 | 10 | 0 | 63 | 25% |
| JSON Schema | 38 | 23 | 2 | 0 | 63 | 60% |
| Java | 0 | 23 | 40 | 0 | 63 | 0% |
| SHACL | 19 | 24 | 20 | 0 | 63 | 30% |
| ShEx | 0 | 23 | 40 | 0 | 63 | 0% |
| OWL | 0 | 25 | 38 | 0 | 63 | 0% |
| JSON-LD Ctx | 34 | 23 | 6 | 0 | 63 | 54% |
| SQLite DDL | 12 | 39 | 12 | 0 | 63 | 19% |
| Postgres DDL | 0 | 22 | 41 | 0 | 63 | 0% |
| Pandera | 14 | 27 | 22 | 0 | 63 | 22% |
| Polars Schema | 28 | 22 | 13 | 0 | 63 | 44% |

## Details by Category

### Arrays

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| N-dimensional arrays | ✅ | ❓ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ |

### Boolean Expressions

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Cardinality in exactly_one_of | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Class any_of | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Class boolean with expressions | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |
| Slot all_of | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Slot any_of | ✅ | ⚠️ | ⚠️ | ❓ | ❓ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ❓ | ❓ |
| Slot boolean with expressions | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |
| Slot exactly_one_of | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Slot none_of | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

### Cardinality & Presence

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Identifier implies required | ✅ | ✅ | ✅ | ❓ | ❓ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |
| Membership constraints | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Min/max cardinality | ✅ | ⚠️ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |
| Required / multivalued | ⚠️ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |

### Core Structure

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Abstract classes | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |
| Attribute refinement | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ⚠️ | ✅ |
| Attributes | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |
| Class inheritance (is_a) | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |
| Mixins | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |
| Slot inheritance | ✅ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |
| Slot usage | ✅ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |

### Defaults & Computed

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| If-absent defaults | ✅ | ✅ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ✅ | ✅ |

### Enumerations

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Enum aliases | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |
| Enum hierarchy | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |
| Non-standard enum names | ⚠️ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ❓ |
| Static enums | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Typed permissible values | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |

### Identity & Keys

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Identifier | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |
| Nested keys | ⚠️ | ⚠️ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ❓ | ❓ |
| Type designator | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |
| Unique keys | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |

### Inheritance & Refinement

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Subproperty class range | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty deep hierarchy | ✅ | ❓ | ✅ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty multivalued | ✅ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty range formatting | ✅ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty slot_usage narrowing | ✅ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Subproperty value constraint | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

### Inlining & References

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Inlined as simple dict | ⚠️ | ⚠️ | ✅ | ❓ | ⚠️ | ❓ | ⚠️ | ✅ | ❓ | ❓ | ✅ | ✅ |
| Inlined objects | ✅ | ⚠️ | ✅ | ❓ | ❓ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ✅ | ✅ |
| Inlined with unique keys | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ❓ |

### Metadata

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Aliasing | ✅ | ✅ | ✅ | ❓ | ⚠️ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |
| Annotations | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |
| Common metadata | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Descriptions | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |
| Element URIs | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |

### Other

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| JSON Pointer | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

### Rules & Classification

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Classification rules | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Precondition combos | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Precondition rules | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |
| Value presence in rules | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |

### Schema-Level

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Instantiates | ✅ | ✅ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |
| Schema imports | ✅ | ✅ | ✅ | ❓ | ❓ | ❓ | ❓ | ✅ | ✅ | ❓ | ⚠️ | ✅ |

### Slot Typing & Ranges

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Any type | ✅ | ✅ | ✅ | ❓ | ❓ | ❓ | ❓ | ✅ | ❓ | ❓ | ❓ | ✅ |
| Custom types (typeof) | ⚠️ | ⚠️ | ⚠️ | ❓ | ❓ | ❓ | ⚠️ | ✅ | ⚠️ | ❓ | ❓ | ✅ |
| Date/datetime types | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ⚠️ | ❓ |
| Primitive type ranges | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ❓ | ✅ | ✅ |
| URI types | ⚠️ | ✅ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ |

### Value Constraints

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Equals string | ✅ | ❓ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ❓ | ❓ | ❓ | ❓ |
| Equals string in | ✅ | ❓ | ✅ | ❓ | ✅ | ❓ | ⚠️ | ✅ | ❓ | ❓ | ❓ | ❓ |
| ID prefix | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Min/max value | ✅ | ⚠️ | ✅ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ✅ | ✅ |
| Regex pattern | ⚠️ | ⚠️ | ⚠️ | ❓ | ✅ | ❓ | ❓ | ✅ | ⚠️ | ❓ | ⚠️ | ✅ |

### Uncategorized

| Test | Pydantic | Python DC | JSON Schema | Java | SHACL | ShEx | OWL | JSON-LD Ctx | SQLite DDL | Postgres DDL | Pandera | Polars Schema |
|------| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| range expression booleans | ⚠️ | ❓ | ✅ | ⚠️ | ❓ | ❓ | ❓ | ⚠️ | ❓ | ❓ | ❓ | ⚠️ |
| range expression nesting | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ | ⚠️ | ⚠️ | ❓ | ⚠️ |

---

*This dashboard is auto-generated from compliance test results. To update: run the compliance tests with `--with-output`, then run `uv run python scripts/generate_dashboard.py`. To add features, write a new compliance test and decorate it with `@feature_category("Category Name", "Display Name")`.*
