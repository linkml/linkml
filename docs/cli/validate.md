{#linkml-validate-cli}
# `linkml validate`

Validate data against a LinkML schema, or validate a schema itself against the metamodel.

## Usage

**Validate data against a schema:**

```bash
linkml validate -s schema.yaml data.yaml
```

**Validate a schema against the metamodel** (no data files):

```bash
linkml validate -s schema.yaml
```

When no data sources are provided, `linkml validate` checks the schema itself
against the LinkML metamodel — verifying required fields, correct types, valid
URIs, and NCName constraints.

For schema quality checks (naming conventions, recommended fields, canonical
prefixes), use [`linkml lint`](./lint.md) instead.

## Related Tools

- **`linkml lint`** — validates the schema against the metamodel *and* checks
  quality rules (naming conventions, recommended fields, etc.).
- **`linkml-normalize`** — coerces and restructures data to conform to a
  schema (type coercion, collection form normalization), outputting the
  corrected data. Use `linkml-normalize -s schema.yaml data.yaml` to normalize
  data, or `linkml-normalize --metamodel schema.yaml` to normalize a schema
  against the metamodel.

## Reference

```{eval-rst}
.. click:: linkml.validator.cli:cli
    :prog: linkml validate
    :nested: full
```
