# Part 10: Working with SQL databases

LinkML allows you to work with SQL/Relational databases in a number of different ways.

* SQL Schemas (DDL) can be generated directly from LinkML schemas
* Optional Object Relational Mapping (ORM) layers can be generated
    - Currently only Python / SQL Alchemy ORM layesr are supported
* SQL Backends can be used directly to store and retrieve data
    - No coding required
    - Currently only SQLite is supported

## Converting LinkML Schemas to DDL

### Example Schema

We will use the example from the previous tutorial:

```bash
cp ../tutorial09/personinfo.yaml .
```

### Generating SQL CREATE TABLE statements

Use the `gen-sqlddl` command to make a SQL schema:

```bash
gen-sqlddl personinfo.yaml
```

Outputs:

```sql
CREATE TABLE "Address" (
        street TEXT, 
        city TEXT, 
        postal_code TEXT, 
        PRIMARY KEY (street, city, postal_code)
);

CREATE TABLE "Concept" (
        id TEXT NOT NULL, 
        name TEXT, 
        description TEXT, 
        image TEXT, 
        PRIMARY KEY (id)
);

CREATE TABLE "Container" (
        persons TEXT, 
        organizations TEXT, 
        PRIMARY KEY (persons, organizations)
);

CREATE TABLE "DiagnosisConcept" (
        id TEXT NOT NULL, 
        name TEXT, 
        description TEXT, 
        image TEXT, 
        PRIMARY KEY (id)
);

CREATE TABLE "Event" (
        started_at_time DATE, 
        ended_at_time DATE, 
        duration FLOAT, 
        is_current BOOLEAN, 
        PRIMARY KEY (started_at_time, ended_at_time, duration, is_current)
);

CREATE TABLE "NamedThing" (
        id TEXT NOT NULL, 
        name TEXT, 
        description TEXT, 
        image TEXT, 
        PRIMARY KEY (id)
);

CREATE TABLE "Person" (
        id TEXT NOT NULL, 
        name TEXT, 
        description TEXT, 
        image TEXT, 
        primary_email TEXT, 
        birth_date TEXT, 
        age_in_years INTEGER, 
        gender VARCHAR(17), 
        current_address TEXT, 
        PRIMARY KEY (id)
);

CREATE TABLE "Place" (
        id TEXT NOT NULL, 
        name TEXT, 
        PRIMARY KEY (id)
);

CREATE TABLE "ProcedureConcept" (
        id TEXT NOT NULL, 
        name TEXT, 
        description TEXT, 
        image TEXT, 
        PRIMARY KEY (id)
);

CREATE TABLE "Relationship" (
        started_at_time DATE, 
        ended_at_time DATE, 
        related_to TEXT, 
        type TEXT, 
        PRIMARY KEY (started_at_time, ended_at_time, related_to, type)
);

CREATE TABLE "FamilialRelationship" (
        started_at_time DATE, 
        ended_at_time DATE, 
        related_to TEXT NOT NULL, 
        type VARCHAR(10) NOT NULL, 
        "Person_id" TEXT, 
        PRIMARY KEY (started_at_time, ended_at_time, related_to, type, "Person_id"), 
        FOREIGN KEY(related_to) REFERENCES "Person" (id), 
        FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "MedicalEvent" (
        started_at_time DATE, 
        ended_at_time DATE, 
        duration FLOAT, 
        is_current BOOLEAN, 
        in_location TEXT, 
        diagnosis TEXT, 
        procedure TEXT, 
        "Person_id" TEXT, 
        PRIMARY KEY (started_at_time, ended_at_time, duration, is_current, in_location, diagnosis, procedure, "Person_id"), 
        FOREIGN KEY(in_location) REFERENCES "Place" (id), 
        FOREIGN KEY(diagnosis) REFERENCES "DiagnosisConcept" (id), 
        FOREIGN KEY(procedure) REFERENCES "ProcedureConcept" (id), 
        FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "Organization" (
        id TEXT NOT NULL, 
        name TEXT, 
        description TEXT, 
        image TEXT, 
        mission_statement TEXT, 
        founding_date TEXT, 
        founding_location TEXT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(founding_location) REFERENCES "Place" (id)
);

CREATE TABLE "Person_aliases" (
        backref_id TEXT, 
        aliases TEXT, 
        PRIMARY KEY (backref_id, aliases), 
        FOREIGN KEY(backref_id) REFERENCES "Person" (id)
);

CREATE TABLE "Place_aliases" (
        backref_id TEXT, 
        aliases TEXT, 
        PRIMARY KEY (backref_id, aliases), 
        FOREIGN KEY(backref_id) REFERENCES "Place" (id)
);

CREATE TABLE "EmploymentEvent" (
        started_at_time DATE, 
        ended_at_time DATE, 
        duration FLOAT, 
        is_current BOOLEAN, 
        employed_at TEXT, 
        "Person_id" TEXT, 
        PRIMARY KEY (started_at_time, ended_at_time, duration, is_current, employed_at, "Person_id"), 
        FOREIGN KEY(employed_at) REFERENCES "Organization" (id), 
        FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "Organization_aliases" (
        backref_id TEXT, 
        aliases TEXT, 
        PRIMARY KEY (backref_id, aliases), 
        FOREIGN KEY(backref_id) REFERENCES "Organization" (id)
);
```

## Using a SQL database as a backend for data

You can store any data that has a LinkML schema in a database using the `linkml-sqldb` command, and the `dump` subcommand:

```bash
linkml-sqldb dump -s personinfo.yaml --db persons.db data.yaml
```

This will create a SQLite database `persons.db` (you don't have to worry about creating the schema, this is handled automatically)

```bash
sqlite3 tests/test_data/output/personinfo.db "SELECT * FROM Person AS p JOIN MedicalEvent AS m ON (p.id=m.Person_id)"
||||X:P1|person1|||1||1|X:Loc1|||||X:P1|ONT:D001|ONT:T001
||||X:P2|person2|||1||2||||||X:P2|ONT:D002|ONT:T002
```

Data can be retrieved from the database using the `load` subcommand:

```bash
linkml-sqldb dump -s personinfo.yaml --db persons.db data.yaml -o data_out.yaml
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
you are using a RDBMS you may find them useful.

Currently the only ORM directly supported in SQL Alchemy

### SQL Alchemy (advanced)

[SQL Alchemy](https://docs.sqlalchemy.org/) is a SQL framework for python. It has a core layer, and an ORM later.

You can generate SQL Alchemy classes using:

```bash
gen-sqla personinfo.yaml
```

See the SQLDDL generator docs for more details.

