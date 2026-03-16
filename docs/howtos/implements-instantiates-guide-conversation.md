# Conversation Log: Implementing Issue #3281

## Task

Implement issue 3281 — create a tutorial doc to disambiguate `linkml:implements`, `linkml:instantiates`, and `linkml:is_a`+`linkml:mixin`, with a best-practices style guide.

## Steps Taken

### 1. Explored the documentation structure

Used an exploration agent to map out the docs layout:

- **Primary docs directory:** `docs/`
- **Build tool:** Sphinx with Furo theme
- **Source formats:** `.md` (Markdown) and `.rst` (ReStructuredText)
- **Main sections:** `intro/`, `schemas/`, `data/`, `generators/`, `howtos/`, `faq/`, `cli/`, `developers/`, etc.

### 2. Reviewed existing documentation

Read the following files to understand current coverage and style:

- `docs/schemas/inheritance.md` — covers `is_a` and `mixins`
- `docs/schemas/annotations.md` — covers `instantiates` for annotation validation
- `docs/howtos/multidimensional-arrays.md` — covers `implements` for array templates
- `docs/faq/modeling.md` — brief mention of `implements` as alternative to imports
- `docs/howtos/index.rst` — toctree for how-to guides
- `docs/schemas/index.rst` — toctree for schema docs

### 3. Created the new guide

Wrote `docs/howtos/implements-instantiates-guide.md` with the following sections:

- **Quick Reference** — comparison table of all four mechanisms
- **`is_a` and `mixins` — Classical Inheritance** — when to use genuine type hierarchies
- **`implements` — Structural Conformance** — interface/contract pattern, including slot-level semantic property binding
- **`instantiates` — Metamodel Extension** — metaclass-level annotation governance
- **Putting It All Together** — full geochem profile example from the issue text
- **Decision Flowchart** — step-by-step guide for choosing the right mechanism
- **Schema Profiles** — discussion of linkml-microschema-profile and issue #3282
- **Common Pitfalls** — four common mistakes and how to avoid them
- **Summary** — quick-reference table mapping questions to mechanisms

### 4. Added the linkml-term-validator reference

Per user request, added a subsection under `implements` covering slot-level `implements` for semantic properties (e.g. `rdfs:label`), with a link to:
https://linkml.io/linkml-term-validator/binding-validation/#1-using-implements-recommended

### 5. Added cross-references from existing docs

- `docs/schemas/annotations.md` — added a "See also" link to the new guide at the end
- `docs/schemas/inheritance.md` — added a "See also" link after the mixins section

### 6. Registered in the toctree

Added `implements-instantiates-guide` to `docs/howtos/index.rst`.

### 7. Verified the build

Installed missing Sphinx dependencies (`sphinxcontrib-mermaid`, `sphinxcontrib-programoutput`, `furo`, `matplotlib`, etc.) and ran `sphinx-build`. The build succeeded with no errors from the new doc (only pre-existing warnings from `sphinx-click`).

## Files Changed

| File | Change |
|------|--------|
| `docs/howtos/implements-instantiates-guide.md` | **New** — the main tutorial/guide |
| `docs/howtos/index.rst` | Added new guide to toctree |
| `docs/schemas/annotations.md` | Added cross-reference to new guide |
| `docs/schemas/inheritance.md` | Added cross-reference to new guide |
