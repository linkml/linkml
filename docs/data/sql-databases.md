# Working with data in SQL Databases

**NOTE**: Currently SQL Database support is incomplete

See [part 9 of the tutorial](../intro/tutorial09) for an introduction.

## Storing and retrieving data in SQLite3

See [Using SQL DBs](../developers/using-sql-dbs) in the Developers Guide
    
## Mapping from a LinkML model to SQL Schemas

The [SQL Table Generator](../generators/sqltable) can be used to generate SQL DDL (`CREATE TABLE` statements) from a schema.

There are many *possible* ways of mapping a LinkML schema to SQL DDL.
The existing generator makes a specific set of decisions, in future it may be possible to customize this more to your needs.

* Classes are mapped to a Tables
* Class slots are mapped to Columns
     - identifier slots are translated to Primary Keys
     - required slots are translated to mandatory fields
* When handling [inheritance](../schemas/inheritance):
    - Tables are generated for both superclasses and child classes
    - Slots are "rolled down" to child classes
* A slot `s` that has a range of a class `c`:
    - is transformed to a slot `s_{key}`
    - this is a foreign key to `{key}` in `c`, where `{key}` is the primary key
* The standard relational model does not allow for direct analogs of multivalued fields
    - A multivalued slot is modeled as a separate table with a *backreference* to the holder table
    - If the range of a multivalued slot `c.s` is a Type (literal):
          - this generates a table `c_s` with a backref `c_{key}`
          - the table also include a single-valued `s`
    - If the range of a multivalued slot `c.s` is a Class `r`:
          - if `s` is inlined, a backref to `c` is inserted into the table for `r`
          - if `s` is not inlined, a new *join table* `c_s` is created

Mapping is done via SQL Alchemy, which takes care of difference in SQL *dialects*.

## Creation of an Object-Relation Mapping layer

The [SQLAlchemy Generator](../generators/sqlalchemy) will generate a Python ORM.

Currently there is no support for ORM generation in other languages.

Given that ORM layers need to tuned to specific use cases, you may wish to provide your own mapping.
For Java you can do this by tuning the Jinja2 templates that are generated, see [Java Generation](../generators/java)
