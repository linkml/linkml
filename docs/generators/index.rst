.. _generators:

Generators
==========

A LinkML *generator* is code that transforms a linkml schema into a
datamodel expressed using another framework, or into some other
artefact, such as JSON-Schema, or markdown documentation.

Generators allow you to tap into the rich tooling offered in other
technical stacks. The philosophy of LinkML is to embrace and reuse
these existing frameworks, rather than serve as an alternative.

Schema Frameworks
-----------------

These generators translate from a LinkML model to commonly used web
standards for structuring data such as JSON-Schema, Protocol Buffers
(ProtoBuf), and GraphQL.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   json-schema
   protobuf
   graphql


Linked Data Standards
---------------------

`Linked Data <https://en.wikipedia.org/wiki/Linked_data>`_ is a broad
term encompassing frameworks based on RDF and URIs/IRIs. LinkML
schemas, can be translated directly into RDF, or they can be mapped to
OWL, or translated to shape languages such as ShEx and SHACL.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   jsonld-context
   jsonld
   rdf
   sparql
   shex
   shacl
   owl

Documentation Generation
------------------------

These generators will translate LinkML models into documentation,
including UML class diagrams and markdown websites that can be easily
published on static hosting sites.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   markdown
   docgen
   erdiagram
   yuml
   plantumlgen
   project-generator


Language Specific
-----------------

These will generate object models that are particular to specific
languages such as Python, Javascript, or Java.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   python
   pydantic
   java
   typescript

Database
--------

Generators specific to database frameworks. Currently only SQL databases.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sqltable
   sqlalchemy

Others
------

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   linkml
   prefixmap
   sssom
   terminusdb
   excel
   csv
   yaml
   pandera

Common
------

Classes and utilities used by all generators

.. toctree::
   :maxdepth: 3
   :caption: Common:

   common/index
