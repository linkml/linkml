GraphQL
========

`GraphQL <https://graphql.org/>`_ is a language for describing the
structure of data to be returned in an API.

.. note:: This generator will only create GraphQL definitions, it will
          not create runtime bindings.

Example Output
--------------

`personinfo.graphql <https://github.com/linkml/linkml/blob/main/examples/PersonSchema/personinfo/graphql/personinfo.graphql>`_

Overview
--------

Graphql can be generated from a LinkML schema.

To run:

.. code:: bash

   gen-graphql personinfo.yaml > personinfo.graphql


Inheritance
^^^^^^^^^^^

::

    type Person implements HasAliases
      {
        id: String!
        name: String
        description: String
        image: String
        primaryEmail: String
        birthDate: String
        ageInYears: Integer
        gender: GenderType
        currentAddress: Address
        hasEmploymentHistory: [EmploymentEvent]
        hasFamilialRelationships: [FamilialRelationship]
        hasMedicalHistory: [MedicalEvent]
        aliases: [String]
      }


Docs
----

Command Line
^^^^^^^^^^^^

.. click:: linkml.generators.graphqlgen:cli
    :prog: gen-graphql
    :nested: full

Code
^^^^

.. currentmodule:: linkml.generators.graphqlgen

.. autoclass:: GraphqlGenerator
    :members: serialize
