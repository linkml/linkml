.. _api:

API
===

.. currentmodule:: ontobio

Ontology Access
---------------

Factory
^^^^^^^

The OntologyFactory class provides a means of creating an ontology
object backed by either local files or remote services. See
:ref:`inputs` for more details.

.. currentmodule:: ontobio.ontol_factory
       
.. autoclass:: OntologyFactory
    :members:

Ontology Object Model
^^^^^^^^^^^^^^^^^^^^^
       
.. currentmodule:: ontobio.ontol

.. autoclass:: Ontology
    :members:
    :inherited-members:

.. autoclass:: Synonym
    :members:
    :inherited-members:

.. autoclass:: LogicalDefinition
    :members:        
    :inherited-members:


Assocation Access
-----------------

Factory
^^^^^^^

.. currentmodule:: ontobio.assoc_factory
       
.. autoclass:: AssociationSetFactory
    :members:

Assocation Object Model
^^^^^^^^^^^^^^^^^^^^^^^
       
.. currentmodule:: ontobio.assocmodel

.. autoclass:: AssociationSet
    :members:

**TODO** - detailed association modeling

Association File Parsers
^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: ontobio.io.gafparser

.. autoclass:: AssocParser
    :members:
    :inherited-members:


.. autoclass:: GafParser
    :members:
    :inherited-members:


.. autoclass:: GpadParser
    :members:
    :inherited-members:

.. autoclass:: HpoaParser
    :members:
    :inherited-members:

.. autoclass:: AssocParserConfig
    :members:


GOlr Queries
------------

.. currentmodule:: ontobio.golr.golr_query

.. autoclass:: GolrAssociationQuery
    :members:

.. autoclass:: GolrSearchQuery
    :members:


Lexmap
------

.. currentmodule:: ontobio.lexmap

.. autoclass:: LexicalMapEngine
    :members:
    

