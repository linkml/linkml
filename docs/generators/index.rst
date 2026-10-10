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
   openapi


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
   yarrrml

Documentation Generation
------------------------

These generators will translate LinkML models into documentation,
including UML class diagrams and markdown websites that can be easily
published on static hosting sites.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   docgen
   erdiagram
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
   golang
   typescript
   rust

Database
--------

Generators specific to database frameworks, including SQL and graph databases.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sqltable
   sqlalchemy
   sqlvalidation
   bigquery
   typedb

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

Generating part of a schema
---------------------------

The generator commands that share the common options, which is all of
them except ``gen-project``, ``gen-pandera`` and ``gen-dbml``, accept
``--subset NAME``, where ``NAME`` is a subset that the schema declares
under ``subsets`` and that elements join through ``in_subset``. The
generator then works from a copy of the schema pruned to the subset's
members and what they need: the ancestors and mixins of each kept
class, the slots of each kept class, and every class, enum and type
that those slots refer to, followed until nothing that is kept refers
to anything dropped. When the subset names slots as well as classes, a
kept class keeps only the slots that are members for it (a
``slot_usage`` can make a slot a member for one class only) and its
identifier, and a slot that stays declared on an ancestor is inherited
as usual. Imported schemas are merged into the copy, apart from the
LinkML metamodel's own such as ``linkml:types``, so an imported model
contributes only the elements that the subset reaches, and those keep
their URIs. The metamodel marks its own core as ``MinimalSubset``:

.. code-block:: bash

   gen-json-schema --subset MinimalSubset meta.yaml
   gen-doc --subset MinimalSubset -d docs meta.yaml

An unknown name is an error that lists the declared subsets. One subset
is taken per run, so a slice that spans several needs a subset of its
own. ``gen-markdown-datadict`` reads the schema file again for its
diagrams, so it does not support ``--subset``. See
:doc:`../schemas/subsets` for declaring subsets.

Feature Dashboard
-----------------

See which metamodel features each generator supports at a glance.

.. toctree::
   :maxdepth: 1

   dashboard

Common
------

Classes and utilities used by all generators

.. toctree::
   :maxdepth: 3
   :caption: Common:

   common/index
