SQL Validation
==============

Overview
--------

The SQL Validation generator creates SQL queries that identify data entries violating LinkML schema constraints.
When executed against a database, the query returns a table listing all constraint violations with standardized columns:

- **table_name**: The class/table name where the violation occurred
- **column_name**: The slot/column name that violated the constraint
- **constraint_type**: Type of constraint violated (required, range, pattern, enum, identifier, key, unique_key)
- **record_id**: ID of the violating record
- **invalid_value**: The value that violates the constraint

For example, if a Person record has an age of 200 that exceeds the maximum allowed value, running the generated
validation query would return:

.. list-table::
   :header-rows: 1

   * - table_name
     - column_name
     - constraint_type
     - record_id
     - invalid_value
   * - Person
     - age
     - range
     - P001
     - 200

Example Output
--------------

A generated sql query for the `personinfo.yml` schema with `sqlite` syntax.

`personinfo.sql <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/sqlvalidation/personinfo.sql>`_

Overview
--------





Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.sqlvalidationgen

.. click:: linkml.generators.sqlvalidationgen:cli
    :prog: gen-sqlvalidation
    :nested: short

Code
^^^^


.. autoclass:: SQLValidationGenerator
    :members: serialize
