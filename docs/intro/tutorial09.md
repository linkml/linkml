# Part 9: Working with SQL databases

LinkML allows you to work with SQL/Relational databases in a number of different ways.

* SQL Schemas (DDL) can be generated directly from LinkML schemas
* Optional Object Relational Mapping (ORM) layers can be generated
    - Currently only Python / SQL Alchemy ORM layers are supported
* SQL Backends can be used directly to store and retrieve data
    - No coding required
    - Currently only SQLite is supported

## Converting LinkML Schemas to DDL

### Example Schema

We will use the example from the previous tutorial (examples/tutorial/tutorial07/personinfo.yaml).

personinfo.yaml:

```{literalinclude} ../../examples/tutorial/tutorial07/personinfo.yaml
:language: yaml
```

data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial07/data.yaml
:language: yaml
```

### Generating SQL CREATE TABLE statements

Use the [gen-sqltables](/generators/sqltable) command to make a SQL schema:

```bash
gen-sqltables personinfo.yaml
```

Outputs:

<!-- no_compare -->
<!-- SQL output order (e.g. CREATE INDEX) is non-deterministic across platforms -->
```{literalinclude} ../../examples/tutorial/tutorial09/personinfo.sql
:language: sql
```

## Using a SQL database as a backend for data

You can store any data that has a LinkML schema in a database using the `linkml-sqldb` command, and the `dump` subcommand:

```bash
linkml-sqldb dump -s personinfo.yaml --db persons.db data.yaml
```

This will create a SQLite database `persons.db` (you don't have to worry about creating the schema, this is handled automatically)

Data can be retrieved from the database using the `load` subcommand:

```bash
linkml-sqldb load -s personinfo.yaml --db persons.db -o data_out.yaml
```

This will export the data from the database back into YAML format.

Alternatively, data can be queried directly from the database via sqlite3, e. g. the following command

<!-- NO_EXECUTE -->
```bash
sqlite3 persons.db "SELECT * FROM Person"
```

or alternatively using the sqlite3 module from Python (if you don't have sqlite3 installed)

```bash
python -m sqlite3 persons.db "SELECT * FROM Person"
```

The coummand will result in:
```text
ORCID:1234|Clark Kent|555-555-5555|33|1
ORCID:4567|Lois Lane||34|1
```

Currently the `sqldb` command doesn't allow complex querying. For that you need to either write SQL as above, or use code as in an ORM layer.

## Object Relational Mapping (ORMs)

Object Relational Mapping (ORM) layers provide a bridge between an
Object-Oriented (OO) representation of database and a Relational
Database. Examples of ORMs are:

* Hibernate (Java)
* SQL Alchemy (Python)
* ActiveRecord (Ruby)

The LinkML metamodel has aspects of OO modeling, so ORMs can be useful
here. Note that ORMs can be divisive among developers, with some
believe ORMs to be add unnecessary complexity, and others finding them
indispensable. Use of ORMs is completely optional with LinkML, but if
you are using a relational database management system (RDBMS) you may find them useful.

Currently the only ORM directly supported is SQL Alchemy.

### SQL Alchemy (advanced)

[SQL Alchemy](https://docs.sqlalchemy.org/) is a SQL framework for python. It has a core layer, and an ORM layer.

You can generate SQL Alchemy classes using:

```bash
gen-sqla personinfo.yaml
```

See the SQLTables generator docs for more details.
