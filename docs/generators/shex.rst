ShEx
======

Overview
--------

`ShEx <http://shex.io/shex-semantics/index.html>`__, short for Shape
Expressions Language is a modeling language for RDF files.

.. seealso:: `ShEx Primer notebook <https://github.com/linkml/linkml/blob/main/notebooks/ShExPrimerModel.ipynb>`_

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.shexgen

.. click:: linkml.generators.shexgen:cli
    :prog: gen-shex
    :nested: short

Code
^^^^

                   
.. autoclass:: ShexGenerator
    :members: serialize
