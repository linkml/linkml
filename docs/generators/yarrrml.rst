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

CSV / TSV sources
-----------------

Besides JSON, CSV and TSV are supported. The key differences:

- No iterator is required for CSV/TSV (each row is a candidate).
- ``sources`` must be expressed as a **list of lists** for compatibility with engines like Morph-KGC:

  .. code-block:: yaml

     mappings:
       Person:
         sources:
           - ['people.csv~csv']   # note the inner list
         s: ex:$(id)
         po:
           - p: rdf:type
             o: ex:Person
           - p: ex:name
             o: $(name)

- Values come directly from columns via ``$(column_name)``.
- For object slots (non-inlined references), IRIs are emitted:

  .. code-block:: yaml

     - p: ex:employer
       o:
         value: $(employer)
         type: iri

- TSV works the same way (``~csv``). Most engines auto-detect tab separators. Explicit CSVW options (delimiters, quoting, etc.) are out of scope for the generator and can be edited manually if needed.

Source inference
----------------

If a file path is passed without a formulation suffix, the generator infers it automatically:

- ``*.json`` → ``~jsonpath``
- ``*.csv`` / ``*.tsv`` → ``~csv``

Examples:

.. code:: bash

   # JSON (iterator required)
   linkml generate yarrrml schema.yaml > mappings.yml
   linkml generate yarrrml schema.yaml --source data.json~jsonpath
   linkml generate yarrrml schema.yaml --source data.json~jsonpath --iterator-template "$.{Class}[*]"

   # CSV / TSV (no iterator)
   linkml generate yarrrml schema.yaml --source people.csv
   linkml generate yarrrml schema.yaml --source people.tsv~csv

   # CLI alias (short form)
   gen-yarrrml schema.yaml --source data.csv~csv > mappings.yml

Overview
--------

- One mapping per LinkML class
- Prefixes come from the schema
- Subject from identifier slot (else key; else safe fallback)
- ``po`` for all class attributes (slot aliases respected)
- Emits ``rdf:type`` as CURIEs (e.g., ``ex:Person``)
- JSON default: ``sources: [[data.json~jsonpath, $.items[*]]]``
- CSV/TSV: ``sources: [[path~csv]]`` (no iterator), values via ``$(column)``

Command Line
------------

.. code:: bash

   linkml generate yarrrml path/to/schema.yaml > mappings.yml
   # CSV instead of JSON:
   linkml generate yarrrml path/to/schema.yaml --source data.csv~csv
   # class-based JSON arrays:
   linkml generate yarrrml path/to/schema.yaml --iterator-template "$.{Class}[*]"
   # or short alias:
   gen-yarrrml path/to/schema.yaml --source data.csv~csv > mappings.yml

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
- Classes without an identifier are **assigned a fallback subject**: ``ex:<Class>/$(subject_id)``
- Object slots: ``inlined: false`` → IRI; ``inlined: true`` → included as separate mapping
- Iterators are not inferred from JSON Schema
- No per-slot JSONPath/CSV expressions or transforms yet
- CSV/TSV delimiter or CSVW configs must be edited manually if needed
