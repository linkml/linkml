.. linkml documentation master file, created by
   sphinx-quickstart on Sun Sep  5 18:12:49 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LinkML Documentation
====================

Everything you need to know about `LinkML <https://linkml.io>`_, the
Linked Data Modeling Language.

LinkML is a flexible modeling language that allows you to author
schemas in YAML that describe the structure of your data. LinkML
provides a framework for working with and validating data in a variety
of formats (JSON, RDF, TSV) provides generators for compiling LinkML
schemas to other frameworks.


Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro/overview
   intro/install
   intro/tutorial
   schemas/index
   data/index
   generators/index
   examples
   ecosystem
   specifications/linkml-spec.md
   faq/index
   
Metamodel Reference
-------------------

The LinkML metamodel is itself described in LinkML. This model is
hosted in the `linkml-model <https://github.com/linkml/linkml-model>`_
repository. Each element of the model has a URI of the form
``https://w3id.org/linkml/<ELEMENT>``, shortened to the CURIE ``linkml:<ELEMENT>``

The key schema elements are:

- `linkml:SchemaDefinition <https://w3id.org/linkml/SchemaDefinition>`_
  
    - `linkml:ClassDefinition <https://w3id.org/linkml/ClassDefinition>`_
    - `linkml:SlotDefinition <https://w3id.org/linkml/SlotDefinition>`_
    - `linkml:TypeDefinition <https://w3id.org/linkml/TypeDefinition>`_
    - `linkml:EnumDefinition <https://w3id.org/linkml/EnumDefinition>`_

Developers
----------------

If you are a developer looking to either contribute to the framework,
or make use of any linkml package programmatically, this section is
for you

.. toctree::
   :maxdepth: 2
   :caption: Developers guide:

   developers/index
   code



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
