RDFS
====

Overview
--------

`RDF Schema <https://www.w3.org/TR/rdf-schema/>`_ is the W3C's small vocabulary for describing
RDF vocabularies: classes, properties, and the ``domain``, ``range`` and ``subClassOf``
relations between them.

.. code-block:: bash

   gen-rdfs personinfo.yaml
   linkml generate rdfs --format nt personinfo.yaml

Maintained in LinkML-Scala
--------------------------

.. important::

   The generator itself is **not implemented in this repository**. This is a wrapper
   around the RDFS generator in `LinkML-Scala
   <https://github.com/NeverBlink-OSS/linkml-scala>`_.

   Please report any bug reports or feature requests at
   https://github.com/NeverBlink-OSS/linkml-scala

   You can also try the generator without installing anything in the
   `in-browser playground <https://linkml.neverblink.eu/playground/>`_.

When reporting bugs, please include the versions of both linkml and LinkML-Scala.
You can find them by running ``gen-rdfs --version``.

What gets generated
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - LinkML
     - RDFS
   * - Class
     - ``rdfs:Class``, under its ``class_uri`` if it has one
   * - Enum
     - ``rdfs:Class``
   * - Permissible value
     - An individual typed by the enum's class, under its ``meaning`` if it has one
   * - Slot
     - ``rdf:Property``, under its ``slot_uri`` if it has one
   * - ``is_a`` and ``mixins`` on a class
     - ``rdfs:subClassOf``
   * - ``is_a`` on a slot
     - ``rdfs:subPropertyOf``
   * - Slot ``range``
     - ``rdfs:range``, as an XSD datatype for types and a class URI otherwise
   * - ``title``
     - ``rdfs:label``
   * - ``description``
     - ``rdfs:comment``
   * - ``see_also``
     - ``rdfs:seeAlso``

Limitations
-----------

The schema has to be a path to a local file. LinkML-Scala reads it and resolves its imports
from disk itself, so a URL or an already-parsed ``SchemaDefinition`` is refused.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.rdfsgen

.. click:: linkml.generators.rdfsgen:cli
    :prog: gen-rdfs
    :nested: short

Code
^^^^

.. autoclass:: RdfsGenerator
    :members: serialize, as_turtle, as_ntriples, as_graph

.. currentmodule:: linkml.generators.common.scala

.. autoclass:: ScalaBackedGenerator
    :members: scala_schema, generatorversion, close
