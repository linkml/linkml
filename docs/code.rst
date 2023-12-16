Code
====



MetaModel
---------

See `Datamodel docs <https://linkml.io/linkml-model/docs/>`_ for full documentation

.. currentmodule:: linkml_runtime.linkml_model.meta
.. autoclass:: SchemaDefinition
    :members:
.. autoclass:: ClassDefinition
    :members:
.. autoclass:: SlotDefinition
    :members:


Generators
----------

Code for various generators for schema definitions

.. currentmodule:: linkml.generators.jsonschemagen

.. autoclass:: JsonSchemaGenerator
    :members: serialize, json_schema_types

.. currentmodule:: linkml.generators.yamlgen

.. autoclass:: YAMLGenerator
    :members: serialize

Loaders and Dumpers
-------------------

.. currentmodule:: linkml_runtime.dumpers.json_dumper

.. autoclass:: JSONDumper
    :members: dumps, dump

.. currentmodule:: linkml_runtime.loaders

.. autoclass:: JSONLoader
    :members: loads

Schema Utils
------------

.. currentmodule:: linkml_runtime.utils.schemaview

.. autoclass:: SchemaView
    :members: schemaview


Utils
-----

Utilities

.. currentmodule:: linkml.generators.utils

.. automodule:: datautils
    :members:

.. automodule:: validation
    :members:


Validator
---------

.. automodule:: linkml.validator
    :members:

Loaders
^^^^^^^

.. automodule:: linkml.validator.loaders
    :members:
    :exclude-members: iter_instances

Plugins
^^^^^^^

.. automodule:: linkml.validator.plugins
    :members:
    :exclude-members: process, pre_process, post_process
