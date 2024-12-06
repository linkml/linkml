# Part 10: Working with SQL databases

LinkML allows you to work with SQL/Relational databases in a number of different ways.

* SQL Schemas (DDL) can be generated directly from LinkML schemas
* Optional Object Relational Mapping (ORM) layers can be generated
    - Currently only Python / SQL Alchemy ORM layers are supported
* SQL Backends can be used directly to store and retrieve data
    - No coding required
    - Currently only SQLite is supported

## Converting LinkML Schemas to DDL

### Example Schema

We will use the example from the previous tutorial (examples/tutorial07/personinfo.yaml)
```

### Generating SQL CREATE TABLE statements

Use the [gen-sqltables](/generators/sqltable) command to make a SQL schema:

```bash
gen-sqltables personinfo.yaml
```

Outputs:

```sql
CREATE TABLE "Container" (
        id INTEGER NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE "Person" (
        id TEXT NOT NULL,
        full_name TEXT NOT NULL,
        phone TEXT,
        age INTEGER,
        "Container_id" INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY("Container_id") REFERENCES "Container" (id)
);
CREATE TABLE "Person_aliases" (
        "Person_id" TEXT,
        aliases TEXT,
        PRIMARY KEY ("Person_id", aliases),
        FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
```

## Using a SQL database as a backend for data

You can store any data that has a LinkML schema in a database using the `linkml-sqldb` command, and the `dump` subcommand:

```bash
linkml-sqldb dump -s personinfo.yaml --db persons.db data.yaml
```

This will create a SQLite database `persons.db` (you don't have to worry about creating the schema, this is handled automatically)

Data can be retrieved from the database via slite3, e. g. the following command

```bash
sqlite3 persons.db "SELECT * FROM Person"
```

will result in:
```bash
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
