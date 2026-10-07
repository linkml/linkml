C++
===

Overview
--------

The C++ Generator produces a C++17 header from a LinkML model: ``struct`` definitions
for classes with public inheritance, ``enum class`` definitions for enums with
``to_string``/``from_string`` helpers, ``std::optional<T>`` for optional fields and
``std::vector<T>`` for multivalued ones, all wrapped in a namespace and guarded by
``#pragma once``. Custom Jinja2 templates can be supplied via ``--template-dir`` to
override any of the built-in templates.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.cppgen

.. click:: linkml.generators.cppgen:cli
    :prog: gen-cpp-header
    :nested: short

Code
^^^^


.. autoclass:: CppGenerator
    :members: serialize

Namespace Configuration
-----------------------

The generated C++ ``namespace`` is driven by the following precedence:

1. ``--namespace`` command-line option, or ``namespace=...`` when using
   ``CppGenerator`` programmatically
2. ``generator_args.cpp.namespace`` set via ``--config-file``/``-C`` (see below)
3. Fallback: derived from the schema name -- lowercased, with any character outside
   ``[a-z0-9_]`` replaced by an underscore (e.g. a schema named ``My-Schema`` yields
   ``namespace my_schema``)

A namespace may be nested with ``::`` (``game::ontology``), which the header opens as
a C++17 nested namespace definition. Each part must be a C++ identifier that is not a
keyword and not reserved to the implementation (one containing ``__``, or starting
with ``_`` and an uppercase letter).

The derived fallback is always a legal namespace: runs of underscores are collapsed,
a name that collides with a C++ keyword is suffixed with an underscore (``template``
produces ``namespace template_``), and one that is still unusable -- for example, a
schema name starting with a digit -- falls back to ``example``. A ``--namespace`` or
config-file value, by contrast, is never rewritten: an invalid one (``my-schema``,
``a::class``) is reported as an error rather than silently corrected.

Configuration File
------------------

As an alternative to ``--namespace``, ``gen-cpp-header`` accepts a
``--config-file``/``-C`` YAML file -- the **same format** used by ``gen-project``'s own
``--config-file`` (see :doc:`project-generator`) and by ``gen-java`` (see :doc:`java`),
so a single project-wide ``config.yaml`` can be shared between them. ``namespace``
lives under ``generator_args.cpp``:

.. code-block:: yaml

    # config.yaml
    generator_args:
      cpp:
        namespace: game::ontology

``gen-cpp-header`` reads only the ``generator_args.cpp`` section of this file, so a
full multi-generator project ``config.yaml`` can be passed as-is. Any
``gen-cpp-header`` option can be set there, keyed by its name with dashes as
underscores; command-line options take precedence, and a key that is not an option is
reported as a warning and ignored.
