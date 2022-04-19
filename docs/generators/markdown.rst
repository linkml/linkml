Markdown
========

Overview
--------

Markdown is a simple format for authoring documentation. Static site
generation frameworks such as mkdocs use markdown to simply the
creation of websites.

Using LinkML you can go from a schema to a complete searchable website hosted on
GitHub in minutes thanks to the markdown generator

See for example:

* `LinkML (Meta)Model <https://linkml.io/linkml-model/docs/>`_
* `NMDC Schema <https://microbiomedata.github.io/nmdc-schema/>`_
* `CRDC-H Schema <https://cancerdhc.github.io/ccdhmodel/>`_

To run:

.. code:: bash

   gen-json-schema -d docs personinfo.yaml 



Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.markdowngen

.. click:: linkml.generators.markdowngen:cli
    :prog: gen-markdown
    :nested: short

Code
^^^^

                   
.. autoclass:: MarkdownGenerator
    :members: serialize
