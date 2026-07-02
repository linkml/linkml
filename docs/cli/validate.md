{#linkml-validate-cli}
# `linkml validate`

Validate data against a LinkML schema, or validate a schema itself against the metamodel.

## Usage

**Validate data against a schema:**

```bash
linkml validate -s schema.yaml data.yaml
```

**Validate a schema against the metamodel** (no `-s` flag):

```bash
linkml validate schema.yaml
```

When `-s`/`--schema` is omitted, positional arguments are treated as schema
files and validated against the LinkML metamodel — verifying required fields,
correct types, valid URIs, and NCName constraints.

**Validate and fix data:**

```bash
linkml validate -s schema.yaml --fix data.yaml
```

With `--fix`, data is normalized before validation: types are coerced
(e.g. `"5"` → `5`), collection forms are restructured, and the corrected
data is output. Any issues that couldn't be fixed are reported.

For schema quality checks (naming conventions, recommended fields, canonical
prefixes), use [`linkml lint`](./lint.md) instead.

## Related Tools

- **`linkml lint`** — validates the schema against the metamodel *and* checks
  quality rules (naming conventions, recommended fields, etc.).

## Deprecated

- **`linkml-normalize`** — deprecated in favor of `linkml validate --fix`.
  The `linkml-normalize` CLI performed the same normalization and validation
  but as a standalone entry point in `linkml-runtime`.

## Reference

```{eval-rst}
.. click:: linkml.validator.cli:cli
    :prog: linkml validate
    :nested: full
```
