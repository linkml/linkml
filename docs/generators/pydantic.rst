Pydantic
======

Example Output
--------------

`personinfo_pydantic.py <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo_pydantic.py>`_

Overview
--------

The Pydantic Generator produces Pydantic flavored python dataclasses from a linkml model,
with optional support for user-supplied jinja2 templates to generate alternate classes.


Example
^^^^^^^

Given a definition of a Person class:

.. code-block:: yaml

     
    Person:
      is_a: NamedThing
      description: >-
        A person (alive, dead, undead, or fictional).
      class_uri: schema:Person
      mixins:
        - HasAliases
      slots:
        - primary_email
        - birth_date
        - age_in_years
        - gender
        - current_address
        - has_employment_history
        - has_familial_relationships
        - has_medical_history

(some details omitted for brevity, including slot definitions and
parent classes)

The generate python looks like this:

.. code-block:: python

             
    class Person(NamedThing):
        """
        A person (alive, dead, undead, or fictional).
        """
        primary_email: Optional[str] = Field(None)
        birth_date: Optional[str] = Field(None)
        age_in_years: Optional[int] = Field(None, ge=0, le=999)
        gender: Optional[GenderType] = Field(None)
        current_address: Optional[Address] = Field(None, description="""The address at which a person currently lives""")
        has_employment_history: Optional[List[EmploymentEvent]] = Field(None)
        has_familial_relationships: Optional[List[FamilialRelationship]] = Field(None)
        has_medical_history: Optional[List[MedicalEvent]] = Field(None)
        aliases: Optional[List[str]] = Field(None)
        id: Optional[str] = Field(None)
        name: Optional[str] = Field(None)
        description: Optional[str] = Field(None)
        image: Optional[str] = Field(None)


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
