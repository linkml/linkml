SchemaView
----------

The SchemaView class in the linkml-runtime provides a method for
dynamically introspecting and manipulating schemas.

See `SchemaView notebooks <https://github.com/linkml/linkml/tree/main/packages/linkml_runtime/notebooks>`_

.. currentmodule:: linkml_runtime.utils.schemaview

.. autoclass:: SchemaView
    :members:
    :inherited-members:
    :exclude-members: permissible_value_children

Enum Materialization Resolvers
------------------------------

SchemaView materializes intensional enum expressions into derived
``permissible_values`` during ``materialize_derived_schema``.

For dynamic query fields that require external services or custom logic
(``reachable_from``, ``matches``, ``code_set``/``pv_formula``), configure
callbacks using ``configure_enum_materialization_resolvers``.

Each resolver can return either:

- a mapping keyed by permissible value text, with values as
    ``PermissibleValue`` objects or dicts compatible with ``PermissibleValue``
- an iterable of value identifiers/texts

This allows toolchains to inject ontology/code-system expansion logic while
keeping SchemaView materialization deterministic and testable.
