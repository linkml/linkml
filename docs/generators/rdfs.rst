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

Maintained in ohi LinkML
------------------------

.. important::

   The generator itself is **not implemented in this repository**. This is a wrapper
   around the RDFS generator in `ohi LinkML
   <https://linkml.ohi.dev/>`_.

   Please report any bug reports or feature requests at
   https://github.com/NeverBlink-OSS/ohi/issues

   You can also try the generator without installing anything in the
   `in-browser playground <https://linkml.ohi.dev/playground/?target=rdfs>`_.

When reporting bugs, please include the versions of both linkml and ohi LinkML.
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

The full mapping is described in the `ohi LinkML documentation
<https://linkml.ohi.dev/docs/generators/rdfs/>`_.

Limitations
-----------

The schema has to be a path to a local file. ohi LinkML reads it and resolves its imports
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

.. currentmodule:: linkml.generators.common.ohi

.. autoclass:: OhiBackedGenerator
    :members: ohi_schema, generatorversion, close
    :no-index:
