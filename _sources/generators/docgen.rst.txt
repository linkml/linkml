Documentation
=============

Overview
--------

Being able to automatically generate technical documentation pages for your LinkML schema is an 
important feature of the LinkML framework. The linkml library is bundled with a generator (invoked 
using the ``gen-doc`` command) which can be used to automatically create individual Markdown 
pages for each of the elements (classes, slots, enumerations, etc.) in your schema.

The documentation pages are an important resource for consumers of the schema because it provides a 
user-friendly way for users to explore and understand your schema.

If you use the official `LinkML cookicutter <https://github.com/linkml/linkml-project-cookiecutter/tree/main>`_ 
to create your schema, it will add a static site generator framework to your environment. There 
are many static site generator frameworks available, but the one recommended by LinkML is `MkDocs <https://www.mkdocs.org/>`_. 
MkDocs can be used to convert Markdown files/pages into HTML pages. The reason we recommend converting to 
HTML is so that the pages can be deployed to a static site hosting service like `GitHub Pages <https://pages.github.com/>`_. Again, 
if you have used the cookicutter to create your schema, you will find a Makefile in your project folder 
with shortcuts (Makefile targets) to help you build and deploy your documentation easily.

Another important detail about the information contained in the technical documentation pages is the fact 
that it also has automatically generated `Mermaid class diagrams <https://mermaid.js.org/syntax/classDiagram.html>`_ 
embedded on the class documentation pages. These diagrams summarize the relationships between various classes 
and slots in your schema.

Optionally linkml also allows you to exercise more granular control on the layout and content rendered on your documentation pages. 
This customization is facilitated by the modification of the `base jinja2 templates <https://github.com/linkml/linkml/tree/main/linkml/generators/docgen>`_ 
that are used to control the layout and content of the documentation pages. There are jinja2 templates for each of the elements 
in your schema, and you can modify whichever you need to based on your requirements.

.. image:: ../images/documentation_generation_schematic.png

*Figure.: schematic diagram explaining the working mechanism of the ``gen-doc`` module*

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.docgen

.. click:: linkml.generators.docgen:cli
    :prog: gen-doc
    :nested: short

Code
^^^^

.. autoclass:: DocGenerator
    :members: serialize