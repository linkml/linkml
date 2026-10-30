SchemaView
----------

The SchemaView class in the linkml-runtime provides a method for
dynamically introspecting and manipulating schemas.

See `SchemaView notebooks <https://github.com/linkml/linkml/tree/main/packages/linkml_runtime/notebooks>`_

.. currentmodule:: linkml_runtime.utils.schemaview

URI expansion compatibility note
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important::

   **Public API behavior change:** :meth:`SchemaView.expand_curie` now raises
   :class:`ValueError` when an input cannot be expanded through registered
   prefixes or declared ``default_curi_maps`` and is not a syntactically valid
   absolute URI. Previously, such inputs were returned unchanged. This affects
   callers passing bare names such as ``Person`` or relative references such as
   ``./Person``.

Registered prefixes and context maps are resolved before URI passthrough. If a
``fallback`` SchemaView is supplied, its bindings are tried only after those of
the primary view, so it cannot override a prefix resolved by the primary view.

An unresolved input that is a syntactically valid absolute URI is returned
unchanged. An authority component is not required: values such as
``urn:isbn:0451450523`` and ``mailto:a@b.org`` are accepted, as are URIs using
custom schemes. There is no scheme allowlist.

URI syntax alone cannot distinguish an absolute URI from an intended CURIE.
For example, ``UNREG:C`` is accepted as an absolute URI if no prefix binding
resolves it; an unregistered prefix does not, by itself, cause an error.
Callers are responsible for supplying the intended identifier and registering
the appropriate namespace when a value is intended as a CURIE.

**Migration:** Code relying on unchanged bare names or relative references
should supply an absolute URI or a CURIE with a registered prefix instead.
To obtain a URI for a schema element name, use :meth:`SchemaView.get_uri` with
``expand=True`` rather than passing the bare name to ``expand_curie``. Callers
accepting invalid input should handle :class:`ValueError`.

API reference
~~~~~~~~~~~~~

.. autoclass:: SchemaView
    :members:
    :inherited-members:
    :exclude-members: permissible_value_children
