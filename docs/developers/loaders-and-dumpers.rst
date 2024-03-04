.. _data_conversions:

Data Conversion: Loaders and Dumpers
====================================

The linkml-runtime loaders and dumpers framework provide a way to
convert different forms of data that conform to a LinkML Schema.

*Dumpers* dump an in-memory python object to a serialization format

*Loaders* load a file or string that is in a supported format, translating into
in-memory python objects.

All loaders take a target_class parameter that is the python class we
want to reconstitute. Some loaders and dumpers also take a SchemaView
as an argument.

The formats supported are:

- JSON
- YAML
- RDF (e.g. Turtle)
- TSV/CSV


                   

JSON Conversion
---------------

JSON serialization closely follows the in-memory python serialization

.. currentmodule:: linkml_runtime.dumpers

.. autoclass:: JSONDumper

.. currentmodule:: linkml_runtime.loaders

.. autoclass:: JSONLoader
    :members: loads, load, load_any, loads_any

YAML Conversion
---------------

YAML serialization is essentially the same as JSON

.. currentmodule:: linkml_runtime.dumpers
                   
.. autoclass:: YAMLDumper
    :members: dumps, dump

.. currentmodule:: linkml_runtime.loaders

.. autoclass:: YAMLLoader
    :members: loads, load, load_any, loads_any
              

RDF Conversion
--------------



.. currentmodule:: linkml_runtime.dumpers
                   
.. autoclass:: RDFLibDumper
    :members: dumps, dump

.. currentmodule:: linkml_runtime.loaders

.. autoclass:: RDFLibLoader
    :members: loads, load, load_any, loads_any
              

              
CSV Conversion
---------------

.. currentmodule:: linkml_runtime.dumpers
                   
.. autoclass:: CSVDumper
    :members: dumps, dump

.. currentmodule:: linkml_runtime.loaders

.. autoclass:: CSVLoader
    :members: loads, load, load_any, loads_any
