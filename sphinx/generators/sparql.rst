SPARQL
======


Overview
--------

This generator allows you to generate a bank of sparql queries from a schema

To run:

.. code:: bash

   gen-sparql -d sparql personinfo.yaml 

.. seealso:: `Data Validation <../data/validating-data>`_ for  other
             validation strategies

.. seealso:: `linkml-sparql
             <https://github.com/linkml/linkml-sparql>`_ for alpha
             version of a SPARQL based ORM


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
