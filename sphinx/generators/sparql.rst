SPARQL
======


Overview
--------

This generator allows you to generate a bank of sparql queries from a schema

To run:

.. code:: bash

   gen-sparql -d sparql personinfo.yaml 


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
