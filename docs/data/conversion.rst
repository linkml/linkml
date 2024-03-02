Converting between different representations
============================================

LinkML allows you to specify schemas for data in a variety of forms:

-  JSON / YAML
-  Python object models
-  SQL databases
-  Spreadsheets and tabular data
-  RDF/Linked Data
-  Property Graphs

The process of loading from one of these formats into an internal
representation is called *loading*. The opposite process, going from an
internal representation into an external format is called *dumping*

The “native” form for LinkML can be considered JSON/YAML.

See
`PersonSchema/data <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/data>`__
for example toy data files

Specification:

- `Part 6 <https://linkml.io/linkml-model/docs/specification/06mapping/>`_ of the LinkML specification provides a more formal treatment

LinkML-Convert
--------------

The ``linkml-convert`` script can be used to convert data from one form
to another, following a schema

This makes use of loaders and dumpers in the linkml-runtime.

See below for command line docs

Loading from and dumping to JSON
--------------------------------

You can use the linkml-convert script to load or dump from JSON into
another representation.

Dumping to JSON can be lossy; if your objects contain typing information
that cannot be inferred from range constraints.

For example, if you have a schema:

.. code:: yaml

   classes:
     Person:
       attributes:
         employed_at:
           range: Organization
     Organization:
       ...
     NonProfit:
       is_a: Organization
       ...
     Corportation:
       is_a: Organization
       ...

and a person object:

.. code-block:: json

   {
     "employed_at": {
       "...": "..."
     }
   }

Then there is insufficient information to determine whether the internal
representation of the organization the person is employed at should be
instantiated as a NonProfit or a Corporation.

LinkML allows a slot to be set with
`designates_type <https://w3id.org/linkml/designates_type>`__, the value
of which is a name of a class from the schema. However, the loaders
currently do not yet make use of this when loading from JSON into the
internal representation.

Loading from and dumping to YAML
--------------------------------

The native YAML representation for LinkML is essentially identical to
JSON.

In future there may be support for a *direct* translation to YAML that
utilizes YAML tags to encode typing information.

Loading from and dumping to RDF
-------------------------------

Loading and dumping works in a similar fashion for RDF. One difference
is that the schema must be present as this contains crucial information
for being able to map classes and slots to URIs.

See :doc:`RDF <rdf>` for more details

Loading from and dumping to CSVs
--------------------------------

See :doc:`CSVs <./csvs>` for more details

Inferring missing values
------------------------

The ``--infer`` flag can be provided to perform missing value inference

See :doc:`advanced schemas </schemas/advanced>` for more information
on inference

Programmatic usage
------------------

See :doc:`developer docs </developers/index>` for documentation of the relevant
python classes

Command Line
------------

.. currentmodule:: linkml.utils.converter

.. click:: linkml.utils.converter:cli
    :prog: linkml-convert
    :nested: full
