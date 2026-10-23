TypeDB / TypeQL
===============

Overview
--------

`TypeDB <https://typedb.com/>`_ is a polymorphic database that uses its own query language,
`TypeQL <https://typedb.com/docs/typeql/overview>`_. The TypeDB generator converts a LinkML
schema into a TypeQL 3.x ``define`` block that can be loaded directly into a TypeDB server to
define the schema for your database.

Each LinkML **class** becomes a TypeDB **entity** type. Scalar slots become **attribute** types
and are attached to entity types via ``owns`` declarations. Slots whose range is another class
become **relation** types with corresponding ``plays`` declarations on the participating entities.

Type Mapping
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - LinkML type (URI)
     - TypeDB value type
     - Notes
   * - ``xsd:string``, ``xsd:anyURI``, ``xsd:CURIE``, ``xsd:NCName``, ``xsd:language``
     - ``string``
     -
   * - ``xsd:integer``, ``xsd:int``, ``xsd:long``, ``xsd:short``
     - ``integer``
     -
   * - ``xsd:float``, ``xsd:double``, ``xsd:decimal``
     - ``double``
     -
   * - ``xsd:boolean``
     - ``boolean``
     -
   * - ``xsd:dateTime``, ``xsd:date``, ``xsd:time``
     - ``datetime``
     -
   * - ``xsd:duration``
     - ``string``
     - TypeDB 3.x has no native duration type
   * - Enum range
     - ``string``
     - Permitted values listed in an inline comment
   * - Unknown / unresolved
     - ``string``
     - Fallback; a warning comment is emitted

Cardinality Annotations
^^^^^^^^^^^^^^^^^^^^^^^

- ``identifier: true`` → ``@key`` (unique, mandatory)
- ``required: true`` and not multivalued → ``@card(1..1)``
- ``multivalued: true`` → ``@card(0..)``

Abstract Classes
^^^^^^^^^^^^^^^^

A class with ``abstract: true`` gets the TypeDB ``@abstract`` annotation on its entity
declaration.

Reserved Keywords
^^^^^^^^^^^^^^^^^

TypeDB has a set of reserved keywords (``entity``, ``relation``, ``role``, ``match``,
``insert``, etc.). Any class or slot name that collides with a reserved keyword is
automatically renamed with a ``-attr`` or ``-rel`` suffix and a warning comment is
added to the output.

Usage
-----

.. code-block:: bash

   gen-typedb my_schema.yaml

To write to a file:

.. code-block:: bash

   gen-typedb my_schema.yaml > schema.tql

Dependencies
------------

The generator itself only produces text and has no runtime dependency on the TypeDB
driver. To run the integration tests (which connect to a live TypeDB 3.x server) you
need the optional ``typedb`` extras group:

.. code-block:: bash

   uv sync --group typedb

Limitations
-----------

- Enum permissible values are not enforced by TypeDB; they are recorded as comments only.
- ``xsd:duration`` has no native TypeDB equivalent and is stored as ``string``.
- Multiple inheritance (``mixins``) is partially supported — each mixin's slots are
  inlined as ``owns`` / ``plays`` declarations on the inheriting entity.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.typedbgen

.. click:: linkml.generators.typedbgen:cli
    :prog: gen-typedb
    :nested: short

Code
^^^^

.. autoclass:: TypeDBGenerator
    :members: serialize
