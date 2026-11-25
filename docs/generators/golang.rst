Go
====

Overview
--------

The Go Generator produces idiomatic Go code from a LinkML model: structs for
classes, const blocks for enums, JSON tags for serialization, and struct
embedding for inheritance. Custom Jinja2 templates can be supplied via
``--template-dir`` to override any of the built-in templates.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.golanggen

.. click:: linkml.generators.golanggen.golanggen:cli
    :prog: gen-golang
    :nested: short

Code
^^^^


.. autoclass:: GolangGenerator
    :members: serialize

JSON Tag Preservation
---------------------

By default each field's JSON tag is the snake-cased slot name
(``underscore(slot.alias or slot.name)``). Some schemas need a serialization key
that cannot be expressed as a Go identifier -- for example a JSON-LD CURIE such as
``demo:id``, which contains a colon. The generator resolves the tag with the
following precedence:

1. **Slot CURIE** -- with ``--use-curies`` (or ``use_curies=True``), each
   non-identifier slot uses its CURIE, resolved with ``SchemaView.get_curie``.
   This is the same resolution used by the JSON-LD
   Context generator and the JSON Schema generator under their ``--use-curies``
   flags, so Go JSON tags agree with their keys for non-identifier slots.
   Identifier slots retain their ordinary alias/name, matching those generators'
   identifier-key behavior. For non-identifier slots, a declared ``slot_uri`` is
   compacted to its CURIE (e.g. ``demo:id``); a slot without a
   declared URI is synthesized as ``<default_prefix>:<name>`` (e.g. ``ex:name``)
   and compacted.
2. **Automatic fallback** -- when ``--use-curies`` is not set and snake-casing
   changes the key (for example an alias containing ``-`` or whitespace), the
   original ``slot_alias`` is used. This mirrors the Pydantic generator, which
   preserves the original key via ``Field(alias=...)``.
3. **Default** -- the snake-cased slot alias (unchanged legacy behavior).

The CURIE mode is opt-in: output is unchanged when it is not enabled. Only the
JSON tag is affected -- ``go_name`` is still derived from ``camelcase(slot_alias)``,
so colons never leak into the exported Go field identifier. The negative CLI form
is ``--not-use-curies``, matching the sibling generators.

Given (``ex`` is the schema's ``default_prefix``):

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

``gen-golang --use-curies`` produces:

.. code-block:: go

    type Entity struct {
        Id     string  `json:"ex:id"`
        DemoId *string `json:"demo:id,omitempty"`
    }

Package Configuration
---------------------

The generated Go ``package`` clause is driven by the following precedence:

1. ``--package`` command-line option, or ``package=...`` when using ``GolangGenerator``
   programmatically (``--package-name``/``package_name=...`` is a deprecated alias)
2. ``generator_args.golang.package`` set via ``--config-file``/``-C`` (see below)
3. Fallback: derived from the schema name -- lowercased, truncated at the first
   underscore, with any character outside ``[a-z0-9_]`` stripped (e.g. a schema
   named ``kitchen_sink`` yields ``package kitchen``)

The derived fallback is always a legal Go package name: a name that collides with a
Go reserved word is suffixed with an underscore (similar to pythongen.py, ``type_test``
produces ``package type_``), and one that strips down to nothing -- for example, a
schema named ``_private``, -- falls back to ``example``. A ``--package`` or config-file
value, by contrast, is never rewritten: an invalid one is reported as an error rather
than silently corrected.

Configuration File
------------------

As an alternative to ``--package``, ``gen-golang`` accepts a ``--config-file``/``-C``
YAML file -- the **same format** used by ``gen-project``'s own ``--config-file``
(see :doc:`project-generator`) and by ``gen-java`` (see :doc:`java`), so a single
project-wide ``config.yaml`` can be shared between them. ``package`` lives under
``generator_args.golang``:

.. code-block:: yaml

    # config.yaml
    generator_args:
      golang:
        package: mypackage

``gen-golang`` only ever reads ``generator_args.golang.package`` out of this file --
every other key is ignored, so a full multi-generator project ``config.yaml`` can be
passed as-is without modification.

Deprecation note
----------------

The ``--package-name`` option still works but is deprecated in favour of
``--package``, which is the canonical option name across package-scoped generators
(matching ``gen-java``). Using ``--package-name`` emits a deprecation warning.

The same rename applies to the generator's constructor: ``GolangGenerator`` takes
``package``, the same field ``JavaGenerator`` takes, so the two are configured
identically in code. ``package_name=...`` remains accepted as a deprecated alias, and
reading ``.package_name`` off an instance still returns the package; both emit the
same deprecation warning.
