# Derived models

## Asserted vs Derived Models/Schemas

LinkML distinguishes between the *asserted* data model and the *derived* data model

For example, if a class inherits a slot from a parent class, the schema author does not
need to redundantly assert this, as this can be inferred.

Examples of things that can be derived:

- new slot definitions by composing:
    - slot_usage
    - information from parent/ancestor slots
    - information from parent/ancestor classes
- deriving patterns from structured patterns

## Materializing a derived model

Use [gen-linkml](../generators/linkml) to create a derived schema saved as YAML

This can be useful for feeding to basic tools that do not need to implement logic for inheritance

Pattern-aware generators derive regular expressions from `structured_pattern`
automatically. Explicit pattern materialization options are deprecated.

## Programmatically inferring models

- Python developers can use SchemaView, see [developers guide](../developers/manipulating-schemas).
  `resolve_pattern()` resolves a particular slot or type definition, while
  `induced_slot()` and `induced_type()` include pattern inheritance as part of the
  effective definition.
- Javascript developers can use the javascript equivalent in [linkml-runtime.js](https://github.com/linkml/linkml-runtime.js)

## Specification

- [LinkML metamodel source](https://github.com/linkml/linkml-model/tree/main/linkml_model/model/schema) (see derived schema rules)
