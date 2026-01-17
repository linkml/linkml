Solr
====

`Apache Solr <https://solr.apache.org/>`_ is a highly scalable, open-source enterprise search platform.

The Solr generator creates schema definitions in Solr's JSON format for schema operations.

.. note:: This generator creates a flattened schema suitable for Solr, which does not
          support class hierarchies. All fields from all classes are merged into a single
          schema definition.

Example Output
--------------

Given a LinkML schema with classes and slots:

.. code:: yaml

   id: http://example.org/organization
   name: organization

   classes:
     Employee:
       attributes:
         id:
           range: string
           identifier: true
         name:
           range: string
         age:
           range: integer
         emails:
           range: string
           multivalued: true

The Solr generator produces:

.. code:: json

   {
     "add-field": [
       {
         "name": "id",
         "type": "string"
       },
       {
         "name": "name",
         "type": "string"
       },
       {
         "name": "age",
         "type": "int"
       },
       {
         "name": "emails",
         "type": "string",
         "multiValued": true
       }
     ]
   }

This output can be used with Solr's Schema API to add fields to an existing schema.

Overview
--------

To generate a Solr schema from a LinkML schema:

.. code:: bash

   gen-solr my_schema.yaml > solr_schema.json

To generate schema for a specific class only:

.. code:: bash

   gen-solr my_schema.yaml --top-class Employee > employee_schema.json

Type Mappings
^^^^^^^^^^^^^

LinkML types are mapped to Solr field types as follows:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - LinkML Type
     - Solr Type
     - Notes
   * - string
     - string
     -
   * - integer, int
     - int
     -
   * - boolean, bool
     - boolean
     -
   * - float
     - pfloat
     - Point-based float
   * - double, decimal
     - pdouble
     - Point-based double
   * - date, xsddate, xsddatetime
     - date
     -
   * - time, xsdtime
     - time
     -
   * - Class references
     - string
     - Foreign key as string
   * - Enums
     - string
     - Enum values as strings

Features
^^^^^^^^

- **Field Deduplication**: When multiple classes have slots with the same name, only one field definition is created
- **Multivalued Support**: LinkML multivalued slots are mapped to Solr's ``multiValued`` attribute
- **Class Filtering**: Use ``--top-class`` to generate schema for a specific class and its slots only

Usage with Solr Schema API
---------------------------

The generated JSON can be posted directly to Solr's Schema API:

.. code:: bash

   # Generate schema
   gen-solr my_schema.yaml > schema.json

   # Post to Solr Schema API
   curl -X POST -H 'Content-type:application/json' \
     --data-binary @schema.json \
     http://localhost:8983/solr/my_core/schema

Docs
----

Command Line
^^^^^^^^^^^^

.. click:: linkml.generators.solrgen:cli
    :prog: gen-solr
    :nested: full

Code
^^^^

.. currentmodule:: linkml.generators.solrgen

.. autoclass:: SolrSchemaGenerator
    :members: serialize, class_schema, get_field, get_transaction
