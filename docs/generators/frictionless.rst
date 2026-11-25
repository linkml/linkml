Frictionless
============

Overview
--------

The Frictionless generator writes a `Frictionless Data Package <https://datapackage.org/>`_ for
tabular data, for example in the CSV format. Each class becomes a table, described by its own `Table Schema
<https://datapackage.org/standard/table-schema/>`_, and references between classes become foreign
keys between the tables. Tools such as `frictionless-py <https://framework.frictionlessdata.io/>`_
can then check CSV files against the package.

.. code-block:: bash

   gen-frictionless personinfo.yaml > datapackage.json
   gen-frictionless personinfo.yaml -d personinfo-package
   linkml generate frictionless --pruning-mode tree_root personinfo.yaml

By default, the package is printed as one JSON document, with the Table Schema of each table in
it. ``--output`` (``-o``) writes the same document to a file. ``--output-directory`` (``-d``)
writes ``datapackage.json`` to that directory, plus one ``schemas/<table>.json`` per table, which
``datapackage.json`` refers to. Files with the same name are replaced.

The package expects the data of each table in ``data/<table>.csv``, next to ``datapackage.json``.
The CSV files themselves are not generated.

Maintained in ohi LinkML
------------------------

.. important::

   The generator itself is **not implemented in this repository**. This is a wrapper
   around the Frictionless generator in `ohi LinkML
   <https://linkml.ohi.dev/>`_.

   Please report any bug reports or feature requests at
   https://github.com/NeverBlink-OSS/ohi/issues

   You can also try the generator without installing anything in the
   `in-browser playground <https://linkml.ohi.dev/playground/?target=frictionless>`_.

When reporting bugs, please include the versions of both linkml and ohi LinkML.
You can find them by running ``gen-frictionless --version``.

What gets generated
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - LinkML
     - Frictionless
   * - Schema
     - Data package
   * - Class that is not abstract
     - Table: a resource in ``datapackage.json``, with its Table Schema. With
       ``--skip-classes-without-identifier``, only the classes with an identifier
   * - Slot with a type or enum range
     - Field of each table that uses it
   * - ``identifier``
     - ``primaryKey``
   * - Slot referring to another class
     - Field holding the other row's identifier, with a ``foreignKeys`` entry for the other table
   * - Slot with an inlined class range
     - ``object`` field, or ``array`` field when inlined as a list
   * - ``multivalued`` slot
     - ``array`` field, without a foreign key
   * - Enum
     - ``enum`` constraint with the permissible values
   * - ``required``, ``pattern``, ``minimum_value``, ``maximum_value``
     - ``required``, ``pattern``, ``minimum`` and ``maximum`` constraints
   * - ``description``, ``title``
     - ``description``, ``title``

The full mapping is described in the `ohi LinkML documentation
<https://linkml.ohi.dev/docs/generators/frictionless/>`_.

Choosing the tables
^^^^^^^^^^^^^^^^^^^

By default, every class that is not abstract gets a table, including the ones from imported
schemas. ``--pruning-mode schema`` keeps only the classes reachable from the classes of the root
schema, and ``--pruning-mode tree_root`` only those reachable from the tree root class (or the
class given by ``--tree-root``). ``--skip-classes-without-identifier`` also skips the classes
with no identifier, whose tables have no primary key, so no other table can refer to them. The
tree root always gets a table.

Limitations
-----------

The schema has to be a path to a local file. ohi LinkML reads it and resolves its imports
from disk itself, so a URL or an already-parsed ``SchemaDefinition`` is refused.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.frictionlessgen

.. click:: linkml.generators.frictionlessgen:cli
    :prog: gen-frictionless
    :nested: short

Code
^^^^

.. autoclass:: FrictionlessGenerator
    :members: serialize, as_dict, as_files, write

.. currentmodule:: linkml.generators.common.ohi

.. autoclass:: OhiBackedGenerator
    :members: ohi_schema, generatorversion, close
    :no-index:
