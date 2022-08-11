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

LinkML-Convert
--------------

The ``linkml-convert`` script can be used to convert data from one form
to another, following a schema

This makes use of loaders and dumpers in the linkml-runtime

.. code:: bash

   Usage: linkml-convert [OPTIONS] INPUT

     Converts instance data to and from different LinkML Runtime serialization
     formats.

     The instance data must conform to a LinkML model, and either a path to a
     python module must be passed, or a path to a schema.

     The converter works by first using a linkml-runtime *loader* to instantiate
     in-memory model objects, then a *dumper* is used to serialize. A validation
     step is optionally performed in between

     When converting to or from RDF, a path to a schema must be provided.

     For more information, see https://linkml.io/linkml/data/index.html

   Options:
     -m, --module TEXT               Path to python datamodel module
     -o, --output TEXT               Path to output file
     -f, --input-format [yaml|json|rdf|ttl|json-ld|csv|tsv]
                                     Input format. Inferred from input suffix if
                                     not specified
     -t, --output-format [yaml|json|rdf|ttl|json-ld|csv|tsv]
                                     Output format. Inferred from output suffix
                                     if not specified
     -C, --target-class TEXT         name of class in datamodel that the root
                                     node instantiates
     --target-class-from-path / --no-target-class-from-path
                                     Infer the target class from the filename,
                                     should be ClassName-<other-
                                     chars>.{yaml,json,...}  [default: no-target-
                                     class-from-path]
     -S, --index-slot TEXT           top level slot. Required for CSV
                                     dumping/loading
     -s, --schema TEXT               Path to schema specified as LinkML yaml
     -P, --prefix TEXT               Prefixmap base=URI pairs
     --validate / --no-validate      Validate against the schema  [default:
                                     validate]
     --infer / --no-infer            Infer missing slot values  [default: no-
                                     infer]
     -c, --context TEXT              path to JSON-LD context file
     --help                          Show this message and exit.
   Usage: linkml-convert [OPTIONS] INPUT

     Converts instance data to and from different LinkML Runtime serialization
     formats.

     The instance data must conform to a LinkML model, and either a path to a
     python module must be passed, or a path to a schema.

     The converter works by first using a linkml-runtime *loader* to instantiate
     in-memory model objects, then a *dumper* is used to serialize. A validation
     step is optionally performed in between

     When converting to or from RDF, a path to a schema must be provided.

     For more information, see https://linkml.io/linkml/data/index.html

   Options:
     -m, --module TEXT               Path to python datamodel module
     -o, --output TEXT               Path to output file
     -f, --input-format [yaml|json|rdf|ttl|json-ld|csv|tsv]
                                     Input format. Inferred from input suffix if
                                     not specified
     -t, --output-format [yaml|json|rdf|ttl|json-ld|csv|tsv]
                                     Output format. Inferred from output suffix
                                     if not specified
     -C, --target-class TEXT         name of class in datamodel that the root
                                     node instantiates
     --target-class-from-path / --no-target-class-from-path
                                     Infer the target class from the filename,
                                     should be ClassName-<other-
                                     chars>.{yaml,json,...}  [default: no-target-
                                     class-from-path]
     -S, --index-slot TEXT           top level slot. Required for CSV
                                     dumping/loading
     -s, --schema TEXT               Path to schema specified as LinkML yaml
     -P, --prefix TEXT               Prefixmap base=URI pairs
     --validate / --no-validate      Validate against the schema  [default:
                                     validate]
     --infer / --no-infer            Infer missing slot values  [default: no-
                                     infer]
     -c, --context TEXT              path to JSON-LD context file
     --help                          Show this message and exit.

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

.. code:: json

   {
     ...
     "employed_at": {
       ...
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

See `RDF <rdf.md>`__ for more details

Loading from and dumping to CSVs
--------------------------------

See `CSVs <csvs.md>`__ for more details

Inferring missing values
------------------------

The ``--infer`` flag can be provided to perform missing value inference

See `advanced schemas <../schemas/advanced.md>`__ for more information
on inference

Programmatic usage
------------------

See `developer docs <../code>`__ for documentation of the relevant
python classes

Command Line
-------

.. click:: linkml.utils.converter:cli
    :prog: linkml-convert
    :nested: full