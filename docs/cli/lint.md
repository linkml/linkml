{#linkml-lint-cli}
# `linkml lint`

Validate a LinkML schema against the metamodel and check it against
configurable quality rules.

## Usage

```bash
linkml lint schema.yaml
```

`linkml lint` runs two levels of checking:

1. **Metamodel validation** — verifies the schema conforms to the LinkML
   metamodel (required fields, valid types, URI format, NCName constraints).
   This always runs and cannot be disabled.

2. **Quality rules** — checks best practices like naming conventions,
   recommended fields, canonical prefixes, and tree root classes. These are
   configurable via a `.linkmllint.yaml` configuration file.

If you only need to check whether a schema is structurally valid (without
quality rules), use [`linkml validate -s schema.yaml`](./validate.md) instead.

## Reference

```{eval-rst}
.. click:: linkml.cli.main:linkml_lint
    :prog: linkml lint
    :nested: short
```
