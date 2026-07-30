BigQuery DDL
============

Overview
--------

The BigQuery DDL generator produces native `Google BigQuery <https://cloud.google.com/bigquery>`_
``CREATE TABLE`` statements from a LinkML schema. It extends the SQL DDL generator with
BigQuery-specific types (``ARRAY<T>``, ``STRUCT<...>``, ``TIMESTAMP``) and supports
BigQuery table options such as time/range partitioning, clustering, and table descriptions
via LinkML annotations.

.. note::

   This generator requires the ``sqlalchemy-bigquery`` optional dependency.
   Install it with: ``pip install 'linkml[bigquery]'``

Example Output
--------------

Given a schema with a ``Person`` class, the generator produces DDL like:

.. code-block:: sql

   CREATE TABLE `Person` (
     id STRING NOT NULL,
     name STRING,
     age INT64,
     aliases ARRAY<STRING>
   );

BigQuery Annotations
--------------------

You can control BigQuery-specific table options via slot/class annotations:

- ``bigquery_type`` — override the column type (e.g. ``TIMESTAMP``)
- ``bigquery_partition_by`` — field name to use for time/range partitioning
- ``bigquery_partition_type`` — ``DAY``, ``HOUR``, ``MONTH``, ``YEAR``, or ``RANGE``
- ``bigquery_cluster_by`` — comma-separated field names for clustering
- ``bigquery_description`` — table-level description string

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.bigquerygen

.. click:: linkml.generators.bigquerygen:cli
    :prog: gen-bigquery
    :nested: short

Code
^^^^

.. autoclass:: BigQueryGenerator
    :members: serialize, generate_ddl
