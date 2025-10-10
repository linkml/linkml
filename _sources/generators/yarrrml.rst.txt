.. _generators/yarrrml:

YARRRML
=======

`YARRRML <https://rml.io/yarrrml/>`_ is a YAML-friendly syntax for RML mappings.

.. note::
   Minimal generator. JSON-first. Good starting point for hand-tuning.

Example Output
--------------

Given a simple schema:

.. code-block:: yaml

   classes:
     Person:
       attributes:
         id: {identifier: true}
         name: {}

The generator produces YARRRML like:

.. code-block:: yaml

   mappings:
     Person:
       sources:
         - - data.json~jsonpath
           - $.items[*]
       s: ex:$(id)
       po:
         - p: rdf:type
           o: ex:Person
         - p: ex:name
           o: $(name)

Overview
--------

- one mapping per LinkML class
- prefixes come from the schema
- subject from identifier slot (else key; else safe fallback)
- ``po`` for class-induced slots (slot aliases respected)
- emits ``rdf:type`` as a CURIE (e.g., ``ex:Person``)
- JSON by default: ``sources: [[data.json~jsonpath, $.items[*]]]``

Command Line
------------

.. code:: bash

   linkml generate yarrrml path/to/schema.yaml > mappings.yml
   # CSV instead of JSON:
   linkml generate yarrrml path/to/schema.yaml --source data.csv~csv
   # class-based arrays:
   linkml generate yarrrml path/to/schema.yaml --iterator-template "$.{Class}[*]"

Docs
----

CLI
^^^

.. click:: linkml.generators.yarrrmlgen:cli
    :prog: gen-yarrrml
    :nested: short

Code
^^^^

.. currentmodule:: linkml.generators.yarrrmlgen

.. autoclass:: YarrrmlGenerator
    :members: serialize

Limitations
-----------

- JSON-first by default
- One source per mapping
- Classes without an identifier are skipped
- Object slots: ``inlined: false`` → IRI; ``inlined: true`` → not materialized
- Iterators not derived from JSON Schema
- No per-slot JSONPath overrides
- CSV supported via --source
