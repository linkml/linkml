TerminusDB
==========

Overview
--------

`TerminusDB <https://terminusdb.com/>`_ is an open-source knowledge
graph database that provides reliable, private & efficient revision
control & collaboration.

LinkML schemas can be compiled down to terminusdb WOQL schemas

To run:

.. code:: bash

   gen-terminusdb personinfo.yaml 



Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.terminusdbgen

.. click:: linkml.generators.terminusdbgen:cli
    :prog: gen-terminusdb
    :nested: short

Code
^^^^

                   
.. autoclass:: TerminusdbGenerator
    :members: serialize
