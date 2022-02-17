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

   gen-json-schema --index-file docs/schema.md -d docs personinfo.yaml 

This will generate one markdown file per element, plus an index
document.

Use with mkdocs
---------------

The markdown files can be ported across many frameworks. Currently,
most projects that use linkml use `mkdocs <https://www.mkdocs.org/>`_
for site generation.

Using mkdocs you can set up a static site hosted on github in
minutes. To get started:

1. Install mkdocs
2. Create a mkdocs.yml file
3. Run gen-markdown   

After doing this, you can test the site locally:

.. code:: bash

   mkdocs serve

Once you are finished you can make it live:   
   
.. code:: bash

   mkdocs gh-deploy


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
