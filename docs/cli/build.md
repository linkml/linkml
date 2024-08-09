{#build-cli}
# `build`

## Configuration

```{literalinclude}
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