ProtoBuf
========

Example Output
--------------

`personinfo.schema.proto <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/protobuf/personinfo.proto>`_

Overview
--------

`Protocol Buffers <https://developers.google.com/protocol-buffers/>`__
is a protocol for seriaizing data developed by Google.

Protobuf can be generated from a LinkML schema.

To run:

.. code:: bash

   gen-proto personinfo.yaml > personinfo.proto


Inheritance
^^^^^^^^^^^

Because Protobuf does not support inheritance hierarchy, slots are
"rolled down" from parent.

For example, in the personinfo schema, slots such as `id` and `name`
are inherited from NamedThing, and `aliases` are inherited from a mixin:

.. code-block:: yaml

  NamedThing:
    slots:
      - id
      - name

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
      - birth_date
      - age_in_years
      - gender


(some parts truncated for brevity)

This would generate the following Protobuf:

.. code-block:: proto

    // A generic grouping for any identifiable entity
    message NamedThing
     {
      id String = 1
      optional name String = 2
      optional description String = 3
      optional image String = 4
     }

    // A person (alive, dead, undead, or fictional).
    message Person
     {
      id String = 1
      optional name String = 2
      optional description String = 3
      optional image String = 4
      optional primaryEmail String = 5
      optional birthDate String = 6
      optional ageInYears Integer = 7
      optional gender GenderType = 8
      optional currentAddress Address = 9
      repeated hasEmploymentHistory EmploymentEvent = 10
      repeated hasFamilialRelationships FamilialRelationship = 11
      repeated hasMedicalHistory MedicalEvent = 12
      repeated aliases String = 13
     }



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
