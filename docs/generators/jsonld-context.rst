JSON-LD Contexts
================

.. note ::
    When run with ``--emit-frame``, the generator writes a ``.frame.jsonld`` with ``@embed`` directives
    derived from slot ``inlined`` settings (``@always`` / ``@never``).

    Example::

        gen-jsonld-context schema.yaml --output schema.context.jsonld --emit-frame

    This produces two files:

    * ``schema.context.jsonld`` – the JSON-LD context
    * ``schema.frame.jsonld`` – the JSON-LD frame (only if @embed rules are present)

    Alternatively, you can embed the context directly into the frame and produce a single file::

        gen-jsonld-context schema.yaml --output schema.jsonld --embed-context-in-frame

    This produces one file:

    * ``schema.frame.jsonld`` – the JSON-LD frame with the full ``@context`` embedded

    ``--emit-frame`` and ``--embed-context-in-frame`` require ``--output``.

.. warning ::

    The JSON-LD context generator does not yet include ``@type``
    directives except at the top level.

Overview
--------

`JSON-LD context <https://www.w3.org/TR/json-ld/#the-context>`__
provides mapping from JSON to RDF.

.. code:: bash

   gen-jsonld-context personinfo.yaml > personinfo.context.jsonld

You can control the output via
`prefixes <https://linkml.io/linkml-model/latest/docs/prefixes/>`__
declarations and
`default_curi_maps <https://linkml.io/linkml-model/latest/docs/default_curi_maps/>`__.

Any JSON that conforms to the derived JSON Schema (see above) can be
converted to RDF using this context.

CURIE usage
^^^^^^^^^^^

By default, JSON-LD context keys use the generator's normal slot-name alias. With
``--use-curies``, non-identifier slots use their CURIEs (for example, ``demo_id`` with
``slot_uri: demo:id`` becomes ``demo:id``). Identifier slots marked ``identifier: true``
are an exception: their slot-name key (``id`` in the example) maps to ``@id`` and is
never replaced by a CURIE, even if the slot declares a ``slot_uri``. Class context keys
are CURIE-keyed as well.

The CURIE mode is opt-in. CURIEs are resolved with ``SchemaView.get_curie`` using the
schema's prefixes and default prefix.

Example (``ex`` is the schema's ``default_prefix``):

.. code-block:: yaml

    prefixes:
      ex: https://example.org/
      demo: https://example.org/demo/
    default_prefix: ex

    classes:
      Entity:
        slots:
          - id
          - demo_id

    slots:
      id:
        range: string
        required: true
        identifier: true
      demo_id:
        range: string
        slot_uri: demo:id

With ``gen-jsonld-context --use-curies``, ``id`` remains the context key and maps to
``@id``; ``demo_id`` is keyed as ``demo:id``.

Treatment of OBO prefixes
-------------------------

All OBO ontologies use prefixes that end in underscores (for example
``http://purl.obolibrary.org/obo/PATO_``). Note that the JSON-LD 1.1
spec doesn't allow trailing underscores on simple "flat" prefix maps,
i.e this is not correct:

.. code:: json

   "@context": {
       "PATO": "http://purl.obolibrary.org/obo/PATO_",
        }

It must be represented as:

.. code:: json

   "@context": {
       "PATO": {
            "@id": "http://purl.obolibrary.org/obo/PATO_",
             "@prefix": true
        }

However, the former can still be convenient, so this can be done with
a flag:

.. code:: bash

   gen-jsonld-context --flatprefixes personinfo.yaml > personinfo.context.jsonld

However, this is not recommended and newer applications should switch
to gen-prefix-map:

.. code:: bash

   gen-prefix-map --flatprefixes personinfo.yaml > personinfo.prefixmap.json


Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.jsonldcontextgen

.. click:: linkml.generators.jsonldcontextgen:cli
    :prog: gen-jsonld-context
    :nested: short

Code
^^^^


.. autoclass:: ContextGenerator
    :members: serialize
