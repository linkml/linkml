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
