SPARQL
======

This generator allows you to generate a bank of sparql queries from a
schema. These queries can then be used for validation.

Note this approach is redundant with more complete RDF shape based
strategies -- however, it can be convenient to generate individual
SPARQL queries as these can be applied on an ad-hoc basis.

Overview
--------

To run:

.. code:: bash

   gen-sparql -d /path/to/sparql-queries/ personinfo.yaml

.. seealso:: :doc:`Data Validation </data/validating-data>` for  other
             validation strategies.

.. seealso:: `linkml-sparql
             <https://github.com/linkml/linkml-sparql>`_ for an alpha
             version of a SPARQL based ORM

For example, when running over the personinfo schema, one of the
queries "CHECK_permitted_Person.rq" checks to see that only
specifically permitted properties are used when the domain is Person.

.. code-block:: sparql

    SELECT ?g ?s ?p WHERE {
     GRAPH ?g {
      ?s rdf:type schema:Person ;
         ?p ?o .
      FILTER ( ?p NOT IN (
       schema:email,
       schema:birthDate,
       personinfo:age_in_years,
       schema:gender,
       personinfo:current_address,
       personinfo:has_employment_history,
       personinfo:has_familial_relationships,
       personinfo:has_medical_history,
       personinfo:aliases,
       schema:identifier,
       schema:name,
       schema:description,
       schema:image,
       rdf:type ))
     }

    }


Schemas that import other schemas
---------------------------------

By default, ``gen-sparql`` writes queries for the classes of the schema it is
given and of every schema that schema imports. With ``--no-mergeimports``, it
writes queries only for the classes of the schema it is given:

.. code:: bash

   gen-sparql --no-mergeimports -d /path/to/sparql-queries/ personinfo.yaml

The imports are still read. A class is checked against the slots it inherits
from an imported class, and a range that names an imported class also accepts
that class's descendants. Each query declares the prefixes of the imported
schemas too, so it runs on its own.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.sparqlgen

.. click:: linkml.generators.sparqlgen:cli
    :prog: gen-sparql
    :nested: short

Code
^^^^


.. autoclass:: SparqlGenerator
    :members: serialize
