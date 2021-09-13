Project Generator
=================

Overview
--------

The ProjectGenerator is a wrapper for all other generators, and will
generate a complete project folder, with subfolders for jsonschema,
python, etc

.. seealso:: `linkml-model-template <https://github.com/linkml/linkml-model-template>`_

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.projectgen

.. click:: linkml.generators.projectgen:cli
    :prog: gen-project
    :nested: short

Code
^^^^

                   
.. autoclass:: ProjectGenerator
    :members: serialize

