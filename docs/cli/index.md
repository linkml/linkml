# CLI

The CLI interface to LinkML is currently divided into two styles:
- One combined cli underneath [`linkml`](./linkml.md)
  - [`linkml config`](./config.md) 
  - [`linkml generate`](./generate.md) 
  - [`linkml lint`](./lint.md)
  - [`linkml validate`](./validate.md)
- Many independent entrypoints for each generator or tool, see [Entrypoints](./entrypoints.md)

```{toctree}
---
maxdepth: 1
---
linkml
config
generate
lint
validate
entrypoints
```