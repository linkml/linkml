:tocdepth: 3

.. _panderagen:

Pandera
=======

Overview
--------

`Pandera <https://pandera.readthedocs.io/en/stable/index.html#>`__ is an open-source framework
for data validation on dataframe-like objects.
`PolaRS <https://docs.pola.rs/>`__ is a fast dataframe library.

The Pandera Generator produces Pandera models using the class-based API
using the PolaRS integration.

The implementation of the generator is incomplete. Because Pandera is a dataframe library,
the first priority is implementing models of literal data types and checks for flat tables as shown below.
`tests/test\_generators/test\_panderagen.py` also has an example using supported LinkML features.

Currently supported features are:

- literal slot ranges: string, integer, float, boolean, date, datetime
- enums
- constraints: required, pattern, minimum_value, maximum_value, multivalued

Future priorities that are currently not supported include:

- inheritance
- inline / nested struct columns
- array columns
- modeling unnested class ranges (references to separate dataframes)

Example
^^^^^^^

Given a definition of a synthetic flat table:

.. code-block:: yaml

  PanderaSyntheticTable:
    description: A flat table with a reasonably complete assortment of datatypes.
    attributes:
      identifier_column:
        description: identifier
        identifier: True
        range: integer
        required: True
      bool_column:
        description: test boolean column
        range: boolean
        required: True
      integer_column:
        description: test integer column with min/max values
        range: integer
        required: True
        minimum_value: 0
        maximum_value: 999
      float_column:
        description: test float column
        range: float
        required: True
      string_column:
        description: test string column
        range: string
        required: True
      date_column:
        description: test date column
        range: date
        required: True
      datetime_column:
        description: test datetime column
        range: datetime
        required: True
      enum_column:
        description: test enum column
        range: SyntheticEnum
        required: True
      ontology_enum_column:
        description: test enum column with ontology values
        range: SyntheticEnumOnt
        required: True
      multivalued_column:
        description: one-to-many form
        range: integer
        required: True
        multivalued: True
        inlined_as_list: True


(some details omitted for brevity, including header information)

The generate python looks like this:

.. code-block:: python

    class PanderaSyntheticTable(pla.DataFrameModel, _LinkmlPanderaValidator):
        """A flat table with a reasonably complete assortment of datatypes."""


        identifier_column: int= pla.Field()
        """identifier"""

        bool_column: bool= pla.Field()
        """test boolean column"""

        integer_column: int= pla.Field(ge=0, le=999, )
        """test integer column with min/max values"""

        float_column: float= pla.Field()
        """test float column"""

        string_column: str= pla.Field()
        """test string column"""

        date_column: Date= pla.Field()
        """test date column"""

        datetime_column: DateTime= pla.Field()
        """test datetime column"""

        enum_column: Enum= pla.Field(dtype_kwargs={"categories":('ANIMAL','VEGETABLE','MINERAL',)})
        """test enum column"""

        ontology_enum_column: Enum= pla.Field(dtype_kwargs={"categories":('fiction','non fiction',)})
        """test enum column with ontology values"""

        multivalued_column: List[int]= pla.Field()
        """one-to-many form"""


Command Line
------------

.. currentmodule:: linkml.generators.panderagen

.. click:: linkml.generators.panderagen:cli
    :prog: gen-pandera
    :nested: short

Generator
---------


.. autoclass:: PanderaGenerator
    :members:


Templates
---------

The panderagen module uses a templating system that allows generating different target APIs.
The only template currently provided is the default `panderagen_class_based` template.

The :class:`.PanderaGenerator` then serves as a translation layer between
the source models from :mod:`linkml_runtime` and the target models under
:mod:`.panderagen` , making clear what is needed to generate
schema code as well as what parts of the linkml metamodel are supported.


Additional Notes
----------------

When possible the Pandera Generator implements LinkML constraints directly as Pandera checks.
Support for additional checks using Pandera custom checks is planned for the future.

The Python code is currently generated in a single file output to the console.

Usage Example
-------------

Generate the class from tutorial 01 using the `gen-pandera` command

.. code-block:: bash

    gen-pandera examples/tutorial/tutorial01/personinfo.yaml > personinfo_pandera.py

Run an example program to create a one row dataframe and validate it.
No exceptions are raised because the data matches the model.

.. code-block:: python

    from personinfo_pandera import Person
    import polars as pl

    dataframe = pl.DataFrame(
      [
          {
          "id": "ORCID:1234",
          "full_name": "Clark Kent",
          "age": "32",
          "phone": "555-555-5555"
          }
      ]
    )
    Person.validate(dataframe)
