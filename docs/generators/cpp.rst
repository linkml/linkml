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

Slots named after C++ keywords
------------------------------

A slot named after a C++ keyword, such as ``class`` or ``new``, cannot be a C++ field
name, so its field gets a trailing underscore:

.. code:: cpp

    std::optional<std::string> class_ = std::nullopt;

This also covers the alternative tokens, such as ``not``, and the keywords added in
C++20, so the header still compiles as C++20.

A class cannot have both a slot named after a keyword and a slot named like its field,
such as ``class`` and ``class_``. The generator reports an error for it.

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
