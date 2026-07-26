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

1. ``--package`` command-line option (``--package-name`` is a deprecated alias)
2. ``generator_args.golang.package`` set via an explicit ``--config-file``/``-C`` (see below)
3. ``generator_args.golang.package`` set via a ``config.yaml`` auto-detected in the
   current working directory (only checked when ``--config-file`` is not given)
4. Fallback: derived from the schema name -- lowercased, truncated at the first
   underscore, with any character outside ``[a-z0-9_]`` stripped (e.g. a schema
   named ``kitchen_sink`` yields ``package kitchen``)

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

If ``--config-file`` is not given, ``gen-golang`` looks for a ``config.yaml`` in the
current working directory (the conventional top-level directory of a project) and
uses its ``generator_args.golang.package`` value automatically, if present.

Deprecation note
----------------

The ``--package-name`` option still works but is deprecated in favour of
``--package``, which is the canonical option name across package-scoped generators
(matching ``gen-java``). Using ``--package-name`` emits a deprecation warning.
