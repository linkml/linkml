SQL Validation
==============

Example Output
--------------

A generated sql query for the `personinfo.yml` schema with `sqlite` syntax.

`personinfo.sql <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/sqlvalidation/personinfo.sql>`_

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


General Functionality
^^^^^^^^^^^^^^^^^^^^^

For every constraint from the LinkML schema, one query is created. Each of those queries consists of a ``SELECT`` with one or multiple ``WHERE`` conditions.
All queries are concatenated using ``UNION ALL``. Overall, the generated query looks like this:

.. code-block:: sql

  SELECT <error information>
  WHERE <constraint 1>
  UNION ALL
  SELECT <error information>
  WHERE <constraint 2>
  UNION ALL
  ...

To learn more about constraints in LinkML, check out :doc:`Adding constraints and rules <./../schemas/constraints>`.

For simplicity, each example below shows only the query for the constraint being described. The full
output for a schema also includes the ``required`` and uniqueness checks implied by every ``identifier`` slot.

Constraint: Required
^^^^^^^^^^^^^^^^^^^^

For slots marked as ``required: true``, the generated query looks for ``NULL`` values. A schema like this

.. code-block:: yaml

  classes:
    NamedThing:
      attributes:
        id:
          identifier: true
        name:
          required: true

will generate the following constraint:

.. code-block:: sql

  SELECT
      'NamedThing' AS table_name,
      'name' AS column_name,
      'required' AS constraint_type,
      id AS record_id,
      NULL AS invalid_value
  FROM "NamedThing"
  WHERE "NamedThing".name IS NULL

Constraint: Minimum/Maximum Value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For slots with ``minimum_value`` or ``maximum_value``, the generated query identifies out-of-range numeric values. A schema like this

.. code-block:: yaml

  classes:
    Person:
      attributes:
        id:
          identifier: true
        age:
          range: integer
          minimum_value: 0
          maximum_value: 999

will generate the following constraint:

.. code-block:: sql

  SELECT
      'Person' AS table_name,
      'age' AS column_name,
      'range' AS constraint_type,
      id AS record_id,
      age AS invalid_value
  FROM "Person"
  WHERE "Person".age < 0 OR "Person".age > 999

Constraint: Range (Enum)
^^^^^^^^^^^^^^^^^^^^^^^^

For the ``range`` keyword pointing to an enum, the generated query flags values outside the set of permissible values. A schema like this

.. code-block:: yaml

  enums:
    OrganizationType:
      permissible_values:
        non profit:
        for profit:
  classes:
    Organization:
      attributes:
        id:
          identifier: true
        categories:
          range: OrganizationType

will generate the following constraint:

.. code-block:: sql

  SELECT
      'Organization' AS table_name,
      'categories' AS column_name,
      'enum' AS constraint_type,
      id AS record_id,
      categories AS invalid_value
  FROM "Organization"
  WHERE "Organization".categories NOT IN ('non profit', 'for profit')

Constraint: Pattern
^^^^^^^^^^^^^^^^^^^

For slots with a ``pattern`` (regular expression), the generated query returns values that do not match the pattern. The SQL syntax is dialect-specific: PostgreSQL uses the ``~`` operator, while SQLite uses a ``REGEXP`` function (requires an extension). A schema like this

.. code-block:: yaml

  classes:
    Person:
      attributes:
        id:
          identifier: true
        primary_email:
          pattern: "^\\S+@[\\S+\\.]+\\S+"

will generate the following constraint (SQLite dialect):

.. code-block:: sql

  SELECT
      'Person' AS table_name,
      'primary_email' AS column_name,
      'pattern' AS constraint_type,
      id AS record_id,
      primary_email AS invalid_value
  FROM "Person"
  WHERE "Person".primary_email NOT REGEXP '^\S+@[\S+\.]+\S+'


Constraint: Identifier / Key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For slots marked as ``identifier: true`` or ``key: true``, the generated query detects duplicate values using a subquery. A schema like this

.. code-block:: yaml

  classes:
    Person:
      attributes:
        id:
          identifier: true

will generate the following constraint:

.. code-block:: sql

  SELECT
      'Person' AS table_name,
      'id' AS column_name,
      'identifier' AS constraint_type,
      id AS record_id,
      id AS invalid_value
  FROM "Person"
  WHERE "Person".id IN (
      SELECT id
      FROM "Person"
      GROUP BY id
      HAVING count(*) > 1
  )

All records sharing a duplicate value are returned, not just one of them.

Constraint: Unique Keys
^^^^^^^^^^^^^^^^^^^^^^^

For classes with ``unique_keys`` (multi-column uniqueness constraints), the generated query detects duplicate combinations of values across the specified columns. The combined value is returned as a pipe-separated string. A schema like this

.. code-block:: yaml

  classes:
    Person:
      attributes:
        id:
          identifier: true
        name:
        primary_email:
      unique_keys:
        name_and_email:
          unique_key_slots:
            - name
            - primary_email

would generate the following constraint:

.. code-block:: sql

  SELECT
      'Person' AS table_name,
      'name_and_email' AS column_name,
      'unique_key' AS constraint_type,
      id AS record_id,
      (CAST(name AS TEXT) || '|') || CAST(primary_email AS TEXT) AS invalid_value
  FROM "Person"
  WHERE ("Person".name, "Person".primary_email) IN (
      SELECT name, primary_email
      FROM "Person"
      GROUP BY name, primary_email
      HAVING count(*) > 1
  )


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
