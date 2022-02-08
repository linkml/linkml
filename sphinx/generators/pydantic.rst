Pydantic
======

Overview
--------

The Pydantic Generator produces Pydantic flavored python dataclasses from a linkml model,
with optional support for user-supplied jinja2 templates to generate alternate classes.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.pydanticgen

.. click:: linkml.generators.pydanticgen:cli
    :prog: gen-pydantic
    :nested: short

Code
^^^^


.. autoclass:: PydanticGenerator
    :members: serialize

Additional Notes
----------------
LinkML contains two Python generators. The Pydantic dataclass generator is specifically
useful for FastAPI, but is newer and less full featured than the standard 
:doc:`Python generator <generators/python>`.


Biolink Example
---------------

Begin by downloading the Biolink Model YAML and adding a virtual environment and installing linkml.

.. code-block:: bash

    curl -OJ https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml
    python3 -m venv venv
    source venv/bin/activate
    pip install linkml

Now generate the classes using the `gen-pydantic` command

.. code-block:: bash

    gen-pydantic biolink-model.yaml > biolink-model.py
