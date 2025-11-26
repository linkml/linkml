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
the first priority is implementing models of literal and nested data types and checks for single tables as shown below.
`tests/test\_generators/test\_panderagen.py` also has an example using supported LinkML features.

Currently supported LinkML features are:

- literal slot ranges: string, integer, float, boolean, date, datetime
- enums
- constraints: required, pattern, minimum_value, maximum_value, multivalued
- inlining: nested single-valued objects, lists of literals, lists of objects
- **note:** nested dictionary collections (including 'simple' dicts) inlining is inefficient and incomplete, use inlined-as-list instead.

Future priorities that are currently not supported include:

- foreign key association to other tables
- model and slot inheritance
- aliases
- different target dataframe libraries

Example
^^^^^^^

Given a definition of a synthetic flat table with some nested/inlined columns:

.. code-block:: yaml

  PanderaSyntheticTable:
      description: A flat table with a reasonably complete assortment of datatypes.
      attributes:
        identifier_column:
          description: identifier
          identifier: true
          range: integer
          required: true
        bool_column:
          description: test boolean column
          range: boolean
          required: true
        integer_column:
          description: test integer column with min/max values
          range: integer
          required: true
          minimum_value: 0
          maximum_value: 999
        float_column:
          description: test float column
          range: float
          required: true
        string_column:
          description: test string column
          range: string
          required: true
          pattern: "^(this)|(that)|(whatever)$"
        date_column:
          description: test date column
          range: date
          required: true
        datetime_column:
          description: test datetime column
          range: datetime
          required: true
        enum_column:
          description: test enum column
          range: SyntheticEnum
          required: true
        ontology_enum_column:
          description: test enum column with ontology values
          range: SyntheticEnumOnt
          required: true
        multivalued_column:
          description: one-to-many form
          range: integer
          required: true
          multivalued: true
          inlined_as_list: true
        any_type_column:
          description: needs to have type object
          range: AnyType
          required: true
        inlined_class_column:
          description: test column with another class inlined as a struct
          range: ColumnType
          required: true
          inlined: true
          inlined_as_list: false
          multivalued: true
        inlined_as_list_column:
          description: test column with another class inlined as a list
          range: ColumnType
          required: true
          inlined: true
          inlined_as_list: true
          multivalued: true
        inlined_simple_dict_column:
          description: test column inlined using simple dict form
          range: SimpleDictType
          multivalued: true
          inlined: true
          inlined_as_list: false
          required: true


(details omitted, including header information, slots, enums and nested class definitions)

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

        any_type_column: Object = pla.Field()
        """needs to have type object"""

        inlined_class_column: Struct = pla.Field()
        """test column with another class inlined as a struct"""

        inlined_as_list_column: pl.List = pla.Field()
        """test column with another class inlined as a list"""

        inlined_simple_dict_column: Struct = pla.Field()
        """test column inlined using simple dict form"""

        @pla.check("inlined_class_column")
        def check_nested_struct_inlined_class_column(cls, data: PolarsData):
            return cls._check_collection_struct(data)

        @pla.check("inlined_as_list_column")
        def check_nested_struct_inlined_as_list_column(cls, data: PolarsData):
            return cls._check_nested_list_struct(data)

        @pla.check("inlined_simple_dict_column")
        def check_nested_struct_inlined_simple_dict_column(cls, data: PolarsData):
            return cls._check_simple_dict(data)

        _NESTED_RANGES = {
            "inlined_class_column": "ColumnType",
            "inlined_as_list_column": "ColumnType",
            "inlined_simple_dict_column": "SimpleDictType",
        }
        _INLINE_FORM = {
            "inlined_class_column": "inline_collection_dict",
            "inlined_as_list_column": "inlined_list_dict",
            "inlined_simple_dict_column": "simple_dict",
        }
        _INLINE_DETAILS = {
            "inlined_simple_dict_column": {'id': 'id', 'other': 'x'},
        }


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
Support for nested columns uses Pandera custom checks to first isolate the nested column
and then recursvely call Pandera validation.

The Python code is currently output to the console.
The generated class depends on helper methods in the LinkML library at runtime to perform nested checks.


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

Development Notes
-----------------

This generator primarily supports Pandera, which is a validator. The underlying dataframe libraries are only partially supported.
As a consequence, loading data from many of the unit tests (into a dataframe format) can be challenging when the library
does not support some of the LinkML conventions. These include 'simple' dict inlining and polymorphism from row to row.

Following nested objects (and eventually foreign-key associations) relies on using PolaRS expressions API for efficiency.
These may make greater use of the Narwhals API for more general support of additional dataframe libraries in the future.

Future Roadmap
--------------

The following major features need to be prioritized

- Foreign key associations
- Model and slot inheritance, including abstract models
- Make transformer module more general rather than performing operations only at validation time.
- Generalize support for additional dataframe libraries
  - PolaRS independent of Pandera to help loading tables prior to validation
  - Parquet/PyArrow storage formats
  - PySpark (also supported by Pandera)
  - Narwhals (general dataframe API wrapper)
- Improve modularity
  - leverage and align with existing linkml-runtime modules and tables
- Conversion mechanism (loaders) for models using inlined-as-dictionary and inlined-as-simple-dict forms to inlined-as-list.
- Top-level validator cli tool under linkml/validators
- Ability to use the generated Pandera without a runtime LinkML dependency.
- Cardinality checks over entire dataframe columns
