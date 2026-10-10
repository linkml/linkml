ProtoBuf
========

Example Output
--------------

`personinfo.proto <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/protobuf/personinfo.proto>`_

Overview
--------

`Protocol Buffers <https://protobuf.dev/>`__ is Google's language-neutral
format for serializing structured data. ``gen-proto`` writes a ``proto3``
schema from a LinkML schema. The output compiles with ``protoc``.

To run:

.. code:: bash

   gen-proto personinfo.yaml > personinfo.proto

How a schema maps to proto3
---------------------------

Every class becomes a ``message``, including mixins and abstract classes, so
that every type a field names is declared. proto3 has no inheritance, so each
message lists the slots it inherits as well as its own. The ``package`` name
comes from the schema ``name``.

Field names are ``snake_case``. A slot with a ``rank`` keeps it as its field
number. The other slots are numbered from 1 in schema order, skipping the
numbers taken by ranks and the reserved range 19000 to 19999. When no slot of
a class has a rank, the identifier slot takes field number 1. A rank that
proto3 cannot use as a field number, or that another slot of the same class
already uses, is dropped with a warning, and the slot is numbered
automatically. Fields are written in field-number order.

LinkML types map to proto3 scalars: ``integer`` to ``int32``, ``boolean`` to
``bool``, ``float`` to ``float``, ``double`` to ``double``, and every other
type, including dates, URIs and decimals, to ``string``. A multivalued slot
becomes a ``repeated`` field. A slot with no single range, such as one declared
with ``any_of``, becomes a ``string`` field.

A slot whose range is a class carries the nested message when the slot is
inlined. Otherwise it carries a reference: the identifier of the object. The
field then has the identifier's scalar type, usually ``string``, and a
``// reference to`` comment names the class. A class without an identifier is
always inlined.

Each enum becomes an ``enum`` whose first value is ``<NAME>_UNSPECIFIED = 0``.
The permissible values follow from 1, each prefixed with the enum name so that
values of different enums never clash.

Descriptions become ``//`` comments. An identifier slot carries
``// identifier`` and a required slot ``// required``, since proto3 has no
``required`` keyword.

Inheritance
^^^^^^^^^^^

In the personinfo schema, ``Person`` inherits ``id``, ``name``, ``description``
and ``depicted_by`` from ``NamedThing``, and ``aliases`` from a mixin:

.. code-block:: yaml

  NamedThing:
    slots:
      - id
      - name
      - description
      - depicted_by

  HasAliases:
    mixin: true
    attributes:
      aliases:
        multivalued: true

  Person:
    is_a: NamedThing
    mixins:
      - HasAliases
    slots:
      - primary_email
      - birth_date
      - age_in_years
      - gender
      - current_address
      - telephone

The example leaves some slots out for brevity.

``gen-proto`` writes the following messages. The identifier leads each one.
The reference to ``Address`` stays a nested message because the slot is
inlined. ``Person`` lists ``aliases``, which it inherits from the mixin:

.. code-block:: proto

  // A generic grouping for any identifiable entity
  message NamedThing {
    // identifier
    // required
    string id = 1;
    // required
    string name = 2;
    string description = 3;
    string depicted_by = 4;
  }

  // A person (alive, dead, undead, or fictional).
  message Person {
    // identifier
    // required
    string id = 1;
    // required
    string name = 2;
    string description = 3;
    string depicted_by = 4;
    string primary_email = 5;
    string birth_date = 6;
    int32 age = 7;
    GenderType gender = 8;
    // The address at which a person currently lives
    Address current_address = 9;
    string telephone = 10;
    repeated EmploymentEvent has_employment_history = 11;
    repeated FamilialRelationship has_familial_relationships = 12;
    repeated InterPersonalRelationship has_interpersonal_relationships = 13;
    repeated MedicalEvent has_medical_history = 14;
    repeated string aliases = 15;
    repeated NewsEvent has_news_events = 16;
  }

.. _protobuf-configuration-file:

Configuration File
------------------

``gen-proto`` accepts a ``--config-file``/``-C`` YAML file. The file has the
format that ``gen-project`` reads with its own ``--config-file`` (see
:doc:`project-generator`), and ``gen-java`` (see :doc:`java`) and
``gen-golang`` (see :doc:`golang`) read the same format. One project-wide
``config.yaml`` can therefore serve ``gen-project`` and a standalone
``gen-proto`` run. The settings for ``gen-proto`` live under
``generator_args.proto``:

.. code-block:: yaml

    # config.yaml
    generator_args:
      proto:
        importmap: importmap.json
        mergeimports: true
      java:
        package: org.example.model

.. code:: bash

   gen-proto -C config.yaml personinfo.yaml > personinfo.proto

``gen-proto`` reads only ``generator_args.proto``. It ignores the sections of
other generators, so a full project ``config.yaml`` can be passed unchanged. A
file without a ``proto`` section changes nothing.

Any option of the command can be set in the section. Each key is the option's
name with underscores in place of dashes, such as ``importmap`` for
``--importmap``. A key that is
not an option of ``gen-proto`` is reported as a warning and ignored.
``--log_level``, ``--verbose`` and ``--stacktrace`` act as soon as the command
line is read, so they are taken from the command line only.

Each option takes its value in this order of precedence:

1. The option given on the command line.
2. The value under ``generator_args.proto`` in the file given with ``--config-file``.
3. The option's default.

``gen-proto`` never reads a ``config.yaml`` on its own. The file is used only
when it is named with ``--config-file``.

Docs
----

Command Line
^^^^^^^^^^^^

.. click:: linkml.generators.protogen:cli
    :prog: gen-proto
    :nested: full

Code
^^^^

.. currentmodule:: linkml.generators.protogen

.. autoclass:: ProtoGenerator
    :members: serialize
