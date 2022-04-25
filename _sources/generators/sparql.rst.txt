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
