{#build-cli}
# `linkml build`

## Configuration

```{literalinclude} example_config.toml
---
language: toml
linenos: true
---
```

Order of precedence (least to greatest, ie. later entries override previous):
- generate.global
- generate.{{ generator_name }}
- build.{{ schema_name }}.global
- build.{{ schema_name }}.{{ generator_name }}

```{eval-rst} 
.. click:: linkml.cli.build:build
    :prog: linkml build
    :nested: full
```