# Imports

LinkML encourages modular schema development. You can split you schema into modules, and even reuse other peoples modules on the web

A schema can have a list of [imports](https://w3id.org/linkml/imports) associated with it. These are specified as [CURIEs](curies) or local imports.

Most schemas will have at least an imports to the linkml types schema, which defines core types:

```yaml
imports:
  - linkml:types
```

