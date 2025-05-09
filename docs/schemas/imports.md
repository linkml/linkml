# Imports

LinkML encourages modular schema development. You can split you schema into modules, and even reuse other peoples
modules on the web

A schema can have a list of [imports](https://w3id.org/linkml/imports) associated with it. These are specified
as CURIEs or local imports.

## Importing external schemas

Most schemas will have at least an imports to the linkml types schema, which defines core types:

```yaml
prefixes:
  linkml: https://w3id.org/linkml/
  ...: ...

imports:
  - linkml:types
```

The `prefixes` declaration (see [URIs and
mappings](uris-and-mappings.md)) registers the linkml prefix. The
import is expanded to `https://w3id.org/linkml/types`, and an implicit
file type suffix is added, yielding [https://w3id.org/linkml/types.yaml](https://w3id.org/linkml/types.yaml)

## Local imports

You can also specify relative paths, e.g

```yaml
imports:
  - core
  - ../enums/my-enums
```

The `.yaml` suffix is implicitly added, and here the list elements represent a relative path on the file system.

If you include relative paths and make a release of your schema be
sure that the imported modules are accessible and follow the same
paths

## Making merged files for distribution

Sometimes it can be convenient to *merge imports* prior to
distribution. This makes it easier for programs that want to make use
of a linkml schema, as they only have to work with one file, rather
than implementing the full import mechanism. It can also help
eliminate network dependencies.

All [generators](/generators/index) have a `--mergeimports` import that
will merge the imports closure. i.e. all imported definitions will be
recursively copied into the main file.

One particularly useful generator is the [linkml
generator](../generators/linkml). This can be used to make a single
combined file for distribution (in either JSON or YAML)
