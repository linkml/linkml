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


Mixins
^^^^^^

A class that cannot be instantiated on its own, because it is ``abstract`` or a
``mixin``, becomes an interface, and a class mixing it in implements it. An
interface may implement an interface, so a mixin keeps that role when it is
itself mixed into another one, and a class declares the interfaces that the
interfaces it implements declare in turn::

    interface Base
      {
        a: String
      }

    interface Nested implements Base
      {
        b: String
        a: String
      }

    type Consumer implements Nested & Base
      {
        c: String
        b: String
        a: String
      }


Types
^^^^^

A type imported from ``linkml:types`` maps onto one of GraphQL's built-in
scalars. A type the schema brings itself has no built-in to map onto and is
declared as a custom scalar, so that the document defines every type it names::

    types:
      city code:
        typeof: string

becomes::

    type Place
      {
        code: CityCode
      }

    scalar CityCode

Only a type that a field actually names is declared. A type whose name lands on
that of a class or of an enumeration is left undeclared, with a warning: GraphQL
carries every type of a schema in one namespace, in which a name is unique,
while LinkML holds its types, classes and enumerations apart.


Enumerations
^^^^^^^^^^^^

An enumeration listing ``permissible_values`` becomes a GraphQL enum. A GraphQL
enum defines one or more values, so an enumeration that draws its values from an
ontology through ``reachable_from`` cannot be one: its values are not known at
generation time. It is declared as a custom scalar instead, with a warning, so
that the fields naming it stay defined.


Classes without a slot
^^^^^^^^^^^^^^^^^^^^^^

GraphQL has no empty type: an object type and an interface each define at least
one field. A class resolving to no slot therefore carries a single
``_placeholder`` field. A class implementing an interface in that position
carries it as well, because it repeats the fields of the interfaces it
implements::

    interface Annotation
      {
        _placeholder: Boolean
      }


Known gaps
^^^^^^^^^^

The generated document describes types only: it names no root operation type,
which a schema has to provide, so it is not servable on its own.

A name that is not alphanumeric throughout is encoded with ``__``, a prefix
GraphQL reserves for introspection: an enum value starting with a digit is
prefixed with it, and any other character is replaced by its Unicode name
wrapped in it, as in ``__PLUS_SIGN__``.

A class narrowing the range of an inherited slot keeps the narrowed type, which
an interface it implements may disagree with.

``implements`` is derived from ``mixins`` alone, never from ``is_a``, so an
abstract class that is never mixed into another becomes an interface that no
object type implements. A class listed in another class's ``mixins`` without
being declared ``abstract`` or ``mixin`` stays an object type, which the class
mixing it in may then not implement.


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
