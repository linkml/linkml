C++
===

Overview
--------

The C++ Generator produces a C++17 header from a LinkML model. Classes become ``struct``
definitions with public inheritance, and enums become ``enum class`` definitions with
``to_string`` and ``from_string`` helpers. Optional fields use ``std::optional<T>``, and
multivalued ones use ``std::vector<T>``. The whole header sits in a namespace and is
guarded by ``#pragma once``. To override any of the built-in templates, supply custom
Jinja2 templates with ``--template-dir``.

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

These sources set the generated C++ ``namespace``, in order of precedence:

1. The ``--namespace`` command-line option, or ``namespace=...`` when you use
   ``CppGenerator`` from Python code.
2. ``generator_args.cpp.namespace``, set through ``--config-file`` or ``-C`` (see
   below).
3. Otherwise, a name derived from the schema name. It is lowercased, and each character
   outside ``[a-z0-9_]`` becomes an underscore. For example, a schema named
   ``My-Schema`` gives ``namespace my_schema``.

A namespace may be nested with ``::``, as in ``game::ontology``. The header opens it as
a C++17 nested namespace definition. Each part must be a C++ identifier that is neither
a keyword nor reserved to the implementation. A reserved identifier contains ``__``, or
starts with ``_`` and an uppercase letter.

The derived fallback is always a legal namespace. A run of underscores collapses to one,
and a name that collides with a C++ keyword gets a trailing underscore: ``template``
gives ``namespace template_``. A name that is still unusable, such as a schema name that
starts with a digit, falls back to ``example``. By contrast, a ``--namespace`` or
config-file value is never rewritten. An invalid one, such as ``my-schema`` or
``a::class``, is reported as an error rather than silently corrected.

Configuration File
------------------

As an alternative to ``--namespace``, ``gen-cpp-header`` accepts a YAML file through
``--config-file`` or ``-C``. The file has the **same format** as the ``--config-file``
of ``gen-project`` (see :doc:`project-generator`) and of ``gen-java`` (see :doc:`java`),
so one project-wide ``config.yaml`` can serve them all. ``namespace`` goes under
``generator_args.cpp``:

.. code-block:: yaml

    # config.yaml
    generator_args:
      cpp:
        namespace: game::ontology

``gen-cpp-header`` reads only the ``generator_args.cpp`` section of this file, so a full
multi-generator project ``config.yaml`` can be passed as-is. Any ``gen-cpp-header``
option can be set there, under its name with each dash written as an underscore. Options
given on the command line take precedence. A key that is not an option gets a warning
and is ignored.
