Using SQL Databases
-------------------

`SQL Alchemy <https://docs.sqlalchemy.org/>`_ is a SQL framework for
python. It has a core layer, and an ORM layer.

See:

- :doc:`/generators/sqlalchemy` for generating SQL Alchemy code
- :doc:`/generators/sqlddl` for generating SQL DDL

The SQLStore class provides a convenient wrapper around these
generators for working with SQL Data

SQLStore
^^^^^^^^


.. currentmodule:: linkml.utils.sqlutils
                   
.. autoclass:: SQLStore
    :members:                
    :inherited-members:

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.utils.sqlutils

.. click:: linkml.utils.sqlutils
    :prog: linkml-sqldb
    :nested: short
       
