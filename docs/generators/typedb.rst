TypeDB / TypeQL
===============

Overview
--------

`TypeDB <https://typedb.com/>`_ is a polymorphic database that uses its own query language,
`TypeQL <https://typedb.com/docs/core-concepts/typeql/>`_. The TypeDB generator converts a LinkML
schema into a TypeQL 3.x ``define`` block that can be loaded directly into a TypeDB server to
define the schema for your database.

The generated schema requires **TypeDB 3.12 or later**.

Each LinkML **class** becomes a TypeDB **entity** type, or a **relation** type if it represents a
relationship; ``is_a`` becomes ``sub``, and mixins are inlined into the classes that use them.
Scalar slots become **attribute** types attached via ``owns``, and slot ``is_a`` hierarchies
become attribute subtypes. Slots whose range is another class become **relation** types with
``relates``/``plays`` declarations on the participating classes. Cardinality and value
constraints become TypeQL annotations, and ``slot_usage`` can narrow both constraints and
class ranges per class.

Classes and Slots
^^^^^^^^^^^^^^^^^

A class becomes an ``entity`` type. Its scalar slots become attributes it ``owns``, and each
class-ranged slot becomes a binary relation named after the slot. The relation's *owning* role
is named after the slot and played by the declaring class; its *played* role is named after the
range class.

A class becomes a ``relation`` type instead if ``represents_relationship: true`` is its nearest
setting in the ``is_a`` chain, or, when no class in the chain sets it, if
``SchemaView.is_relationship()`` detects it (``rdf:Statement`` / ``owl:Axiom``). Its
class-ranged slots become ``relates`` roles, so it can relate any number of participants, and
its scalar slots become ``owns``.

If a slot is not declared by any class but has a ``domain`` class, the domain class owns it
(if it is scalar-ranged) or plays its owning role (if it is class-ranged).

A ``description`` on a class or slot becomes ``@doc("...")`` on the type it produces.

Hierarchies
^^^^^^^^^^^

``is_a`` becomes ``sub`` for both classes and slots.

A slot without its own ``range`` inherits its parent's. Scalar slots become attribute subtypes.
Class-ranged slots become sub-relations that specialize the parent's owning role, and a class that
plays a slot's owning role also plays those of every slot below it.

A class with ``abstract: true`` gets the TypeDB ``@abstract`` annotation, unless a supertype is
concrete: TypeDB forbids that (``[SVL14]``), so ``@abstract`` is dropped with a warning comment.

Range Narrowing
^^^^^^^^^^^^^^^

A ``slot_usage`` that narrows a class-ranged slot emits a specialized role
``<range>_<parent-role>``, declared ``as`` the parent role, so queries on the parent role still
match. On a relationship class the role is declared on the class itself:

.. code-block:: text

   relation association @abstract, relates subject, relates object;
   relation gene_to_disease_association sub association,
       relates gene_subject as subject,
       relates disease_object as object;

On an ordinary class the generator emits a sub-relation of the slot's relation instead:

.. code-block:: text

   relation enabled_by_molecular_activity sub enabled_by,
       relates gene_or_gene_product_physical_entity as physical_entity @card(1);

Mixins
^^^^^^

Mixins are not emitted as TypeDB types. A mixin's slots are inlined as ``owns`` / ``plays``
declarations on each class that uses it.

A mixin-ranged slot is played by the concrete classes that include it, and a mixin
``domain`` resolves the same way.

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
   * - ``xsd:float``, ``xsd:double``
     - ``double``
     -
   * - ``xsd:decimal``
     - ``decimal``
     -
   * - ``xsd:boolean``
     - ``boolean``
     -
   * - ``xsd:dateTime``, ``xsd:time``
     - ``datetime``
     -
   * - ``xsd:date``
     - ``date``
     -
   * - ``xsd:duration``
     - ``duration``
     -
   * - Enum range
     - ``string``
     - Permitted values enforced via a ``@values(...)`` annotation
   * - Unknown / unresolved
     - ``string``
     - Fallback

Cardinality Annotations
^^^^^^^^^^^^^^^^^^^^^^^

- ``identifier: true`` → ``@key`` (unique, mandatory)
- ``required: true`` and not multivalued → ``@card(1)``
- ``multivalued: true`` → ``@card(0..)``
- ``minimum_cardinality`` / ``maximum_cardinality`` / ``exact_cardinality`` → ``@card(min..max)``,
  taking precedence over the flags above

For scalar slots these go on ``owns``. For class-ranged slots they go on the declaring class's
``plays`` of the owning role, since each value is its own relation; both roles of the relation
are ``@card(1)``. A ``required`` class-ranged slot therefore makes its owner commit together
with at least one relation.

Constraints
^^^^^^^^^^^

- ``minimum_value`` / ``maximum_value`` → ``@range(min..max)``
- ``pattern`` → ``@regex("...")``

``@range`` and ``@regex`` go on ``owns``, so a ``slot_usage`` override affects only that class.
The same applies to a ``slot_usage`` that narrows a slot's range to an enum: its ``@values`` go on
that class's ``owns``.

Naming
^^^^^^

Names are kept as written, except that whitespace becomes underscores
(``gene to disease association`` → ``gene_to_disease_association``). If two class names map to
the same label, generation fails with an error naming both.

Reserved Keywords
^^^^^^^^^^^^^^^^^

TypeDB has a set of `reserved keywords <https://typedb.com/docs/typeql-reference/keywords/>`_
(``entity``, ``relation``, ``match``, ``insert``, etc.). Any class or slot name that collides
with a reserved keyword is automatically renamed with a ``_attr`` or ``_rel`` suffix.

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

- An abstract class with any concrete ancestor is emitted as concrete, since TypeDB does not
  allow an abstract type under a concrete one.
- A scalar slot whose value type differs from its ``is_a`` parent's is emitted as a separate
  attribute rather than a subtype, since a TypeDB attribute subtype has its parent's value type.

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
