Ossie
=====

Overview
--------

`Apache Ossie <https://github.com/apache/ossie>`_ (formerly OSI – Open Semantic Interchange) is a
vendor-neutral specification for exchanging semantic models between data analytics, AI and BI
tools. This generator targets the `Ossie ontology specification
<https://github.com/apache/ossie/blob/main/ontology/ontology.md>`_, which is used for domain models:
concepts and the relationships between them.

.. code-block:: bash

   gen-ossie personinfo.yaml
   linkml generate ossie --format json personinfo.yaml

Maintained in ohi LinkML
------------------------

.. important::

   The generator itself is **not implemented in this repository**. This is a wrapper
   around the Ossie generator in `ohi LinkML
   <https://linkml.ohi.dev/>`_.

   Please report any bug reports or feature requests at
   https://github.com/NeverBlink-OSS/ohi/issues

   You can also try the generator without installing anything in the
   `in-browser playground <https://linkml.ohi.dev/playground/>`_.

When reporting bugs, please include the versions of both linkml and ohi LinkML.
You can find them by running ``gen-ossie --version``.

What gets generated
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - LinkML
     - Ossie
   * - Class
     - ``EntityType`` concept
   * - Enum
     - ``ValueType`` concept extending ``String``, with its permissible values in ``requires``
   * - Type
     - ``ValueType`` concept extending the built-in value type for its base
   * - Slot
     - Relationship of each class that uses it
   * - ``is_a`` and ``mixins`` on a class
     - ``extends``
   * - ``identifier``, ``key`` or ``unique_keys``
     - ``identify_by``
   * - Required slot
     - ``requires``
   * - ``description``
     - ``description``

The full mapping is described in the `ohi LinkML documentation
<https://linkml.ohi.dev/docs/generators/ossie/>`_.

Limitations
-----------

The schema has to be a path to a local file. ohi LinkML reads it and resolves its imports
from disk itself, so a URL or an already-parsed ``SchemaDefinition`` is refused.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.ossiegen

.. click:: linkml.generators.ossiegen:cli
    :prog: gen-ossie
    :nested: short

Code
^^^^

.. autoclass:: OssieGenerator
    :members: serialize, as_yaml, as_json, as_dict

.. currentmodule:: linkml.generators.common.ohi

.. autoclass:: OhiBackedGenerator
    :members: ohi_schema, generatorversion, close
